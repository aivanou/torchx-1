# Copyright (c) Facebook, Inc. and its affiliates.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

"""
These components are meant to be used as convenience methods when constructing
other components. Many methods in the base component library are factory methods
for ``Role``, ``Container``, and ``Resources`` that are hooked up to
TorchX's configurable extension points.
"""
from typing import Any, Dict, List, Optional

from torchx.specs.api import NULL_RESOURCE, Container, Resource, RetryPolicy, Role
from torchx.util.entrypoints import load

from .roles import create_torch_dist_role  # noqa: F401 F403


def named_resource(name: str) -> Resource:
    # TODO <PLACEHOLDER> read instance types and resource mappings from entrypoints
    return NULL_RESOURCE


def torch_dist_role(
    name: str,
    container: Container,
    entrypoint: str,
    script_args: Optional[List[str]] = None,
    script_envs: Optional[Dict[str, str]] = None,
    num_replicas: int = 1,
    max_retries: int = 0,
    retry_policy: RetryPolicy = RetryPolicy.APPLICATION,
    **launch_kwargs: Any,
) -> Role:
    """
    A ``Role`` for which the user provided ``entrypoint`` is executed with the
        torchelastic agent (in the container). Note that the torchelastic agent
        invokes multiple copies of ``entrypoint``.

    The method will try to search factory method that is registerred via entrypoints.
    If no group or role found, the default ``torchx.components.base.role.create_torch_dist_role``
    will be used.

    For more information see ``torchx.components.base.roles``
    """
    dist_role_factory = load(
        "torchx.base",
        "dist_role",
        default=create_torch_dist_role,
    )

    return dist_role_factory(
        name,
        container,
        entrypoint,
        script_args,
        script_envs,
        num_replicas,
        max_retries,
        retry_policy,
        **launch_kwargs,
    )
