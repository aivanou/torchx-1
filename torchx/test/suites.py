#!/usr/bin/env python3
# Copyright (c) Facebook, Inc. and its affiliates.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

import os
import random
import unittest
from itertools import chain


def _circleci_parallelism(suite: unittest.TestSuite) -> unittest.TestSuite:
    """Allow for parallelism in CircleCI for speedier tests.."""
    if int(os.environ.get("CIRCLE_NODE_TOTAL", 0)) <= 1:
        # either not running on circleci, or we're not using parallelism.
        return suite
    # tests are automatically sorted by discover, so we will get the same ordering
    # on all hosts.
    total = int(os.environ["CIRCLE_NODE_TOTAL"])
    index = int(os.environ["CIRCLE_NODE_INDEX"])

    # right now each test is corresponds to a /file/. Certain files are slower than
    # others, so we want to flatten it
    # pyre-fixme[16]: `TestCase` has no attribute `_tests`.
    tests = [testfile._tests for testfile in suite._tests]
    tests = list(chain.from_iterable(tests))
    random.Random(42).shuffle(tests)
    tests = [t for i, t in enumerate(tests) if i % total == index]
    return unittest.TestSuite(tests)


def unittests() -> unittest.TestSuite:
    """
    Short tests.

    Runs on CircleCI on every commit. Returns everything in the tests root directory.
    """
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover(".", pattern="*_test.py", top_level_dir=".")
    test_suite = _circleci_parallelism(test_suite)
    return test_suite


if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(unittests())
