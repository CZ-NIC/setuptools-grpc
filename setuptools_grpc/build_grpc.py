"""Plugin for setuptools providing python gRPC modules build."""

import os
from distutils import log
from glob import glob
from pathlib import Path

import pkg_resources
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
        self.proto_files = []
        self.grpc_files = []
        self.proto_path = "."
        self.output_path = "."

    def finalize_options(self):
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
        includes = (self.proto_path, pkg_resources.resource_filename("grpc_tools", "_proto"))
        args = ["__main__"]
        args.extend("-I%s" % x for x in includes)

        # Generate protobuf modules
        log.info("building protos")
        for proto_file in self.proto_files:
            log.info("generating %s → %s", proto_file, py_module_name(proto_file))
        if protoc_main(
            args
            + ["--python_out", self.output_path, "--pyi_out", self.output_path]
            + [os.path.join(self.proto_path, proto_file) for proto_file in self.proto_files]
        ):
            raise RuntimeError("grpc_build failed")

        # Generate grpc modules
        log.info("building grpc")
        for grpc_file in self.grpc_files:
            log.info("generating %s → %s", grpc_file, grpc_py_module_name(grpc_file))
        if protoc_main(
            args
            + ["--grpc_python_out", self.output_path]
            + [os.path.join(self.proto_path, grpc_file) for grpc_file in self.grpc_files]
        ):
            raise RuntimeError("grpc_build failed")
