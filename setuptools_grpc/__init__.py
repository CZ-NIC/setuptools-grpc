"""Setuptools grpc."""

from setuptools import Command, Distribution

__version__ = "1.0.0"


def has_grpc(build: Command) -> bool:
    """Check whether project has any protobuf files."""
    build_grpc = build.get_finalized_command("build_grpc")
    return bool(build_grpc.proto_files + build_grpc.grpc_files)


def inject_build(dist: Distribution) -> None:
    """Inject `build_grpc` command as first subcommand of `build`."""
    build = dist.get_command_class("build")
    build.sub_commands.insert(0, ("build_grpc", has_grpc))
