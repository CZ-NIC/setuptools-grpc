"""Build backend of setuptools-grpc.

Use this if you want to restrict build dependencies.
Any dependencies specified in env variable SETUPTOOLS_GRPC_BUILD_DEPS
will be added to existing build dependencies.
"""

import os

from setuptools import build_meta as _orig
from setuptools.build_meta import *  # noqa: F403


def get_requires_for_build_wheel(config_settings=None):
    """Add dependencies specified in env variable."""
    return (
        _orig.get_requires_for_build_wheel(config_settings)
        + os.environ.get("SETUPTOOLS_GRPC_BUILD_DEPS", "").split()
    )
