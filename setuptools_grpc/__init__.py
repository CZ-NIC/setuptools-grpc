"""Setuptools grpc."""
from .build_grpc import build_grpc

__version__ = '0.2'


def install(dist):
    dist.cmdclass.update(build_brpc=build_grpc)
    build = dist.get_command_obj("build")
    build.sub_commands = [("build_grpc", None)] + build.sub_commands
