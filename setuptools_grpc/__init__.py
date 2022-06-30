"""Setuptools grpc."""

__version__ = '0.2'


def install(dist):
    build = dist.get_command_obj("build")
    build.sub_commands = [("build_grpc", None)] + build.sub_commands
