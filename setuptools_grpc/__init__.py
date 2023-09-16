"""Setuptools grpc."""

from setuptools import Command, Distribution

__version__ = "0.5"


def has_grpc(build: Command) -> bool:
    build_grpc = build.get_finalized_command("build_grpc")
    return bool(build_grpc.proto_files + build_grpc.grpc_files)


def inject_build(dist: Distribution) -> None:
    build = dist.get_command_class("build")
    build.sub_commands.insert(0, ("build_grpc", has_grpc))
