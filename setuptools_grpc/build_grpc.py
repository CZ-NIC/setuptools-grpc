"""Plugin for setuptools providing python gRPC modules build."""

import importlib.resources
import os
from distutils import log
from glob import glob
from pathlib import Path

import grpc_tools
from grpc_tools.protoc import main as protoc_main
from setuptools import Command

from ._utils import grpc_py_module_name, listify_value, py_module_name

__all__ = ["build_grpc"]


class build_grpc(Command):
    """Custom command that builds protobuf and gRPC python modules."""

    description = "build grpc script"
    user_options = [
        ("proto-files=", None, "newline separated list of glob patterns matching protobuf files"),
        ("grpc-files=", None, "newline separated list of glob patterns matching grpc files"),
        ("proto-path=", None, "path to directory with protobuf files"),
        ("output-path=", None, "output path"),
    ]

    def initialize_options(self):
        """Initialize command options."""
        self.proto_files = []
        self.grpc_files = []
        self.proto_path = "."
        self.output_path = "."

    def finalize_options(self):
        """Finalize command options.

        Expand globs to finalize protobuf and grpc file lists.
        """
        self.ensure_dirname("proto_path")
        self.ensure_dirname("output_path")

        proto_files, grpc_files = [], []

        for fileglob in (v for v in listify_value(self.proto_files, "\n") if v):
            proto_files.extend(
                [
                    str(Path(filename).relative_to(self.proto_path))
                    for filename in glob(os.path.join(self.proto_path, fileglob), recursive=True)
                ]
            )
        self.proto_files = sorted(proto_files)

        for fileglob in (v for v in listify_value(self.grpc_files, "\n") if v):
            grpc_files.extend(
                [
                    str(Path(filename).relative_to(self.proto_path))
                    for filename in glob(os.path.join(self.proto_path, fileglob), recursive=True)
                ]
            )
        self.grpc_files = sorted(grpc_files)

    def run(self):
        """Run command.

        Call `protoc` command to compile protobuf and grpc source files to python modules.
        """
        # Include grpc_tools._proto dir
        proto_path = (importlib.resources.files(grpc_tools) / "_proto").resolve()
        # NOTE: Argument __main__ serves as sys.argv placeholder. Do not remove it!
        args = ["__main__", "-I{}".format(proto_path), "-I{}".format(self.proto_path)]

        # Generate protobuf modules
        if self.proto_files:
            log.info("building protos")
            for proto_file in self.proto_files:
                log.info("generating %s → %s", proto_file, py_module_name(proto_file))

            protoc_args = (
                args
                + ["--python_out", self.output_path, "--pyi_out", self.output_path]
                + [os.path.join(self.proto_path, proto_file) for proto_file in self.proto_files]
            )
            if protoc_main(protoc_args):
                raise RuntimeError("grpc_build failed")

        # Generate grpc modules
        if self.grpc_files:
            log.info("building grpc")
            for grpc_file in self.grpc_files:
                log.info("generating %s → %s", grpc_file, grpc_py_module_name(grpc_file))
            grpc_protoc_args = (
                args
                + ["--grpc_python_out", self.output_path]
                + [os.path.join(self.proto_path, grpc_file) for grpc_file in self.grpc_files]
            )
            if protoc_main(grpc_protoc_args):
                raise RuntimeError("grpc_build failed")
