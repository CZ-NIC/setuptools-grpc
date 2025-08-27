from pathlib import Path
from unittest.mock import call, patch

import grpc_tools
import pytest
from setuptools import Distribution
from testfixtures import TempDirectory

from setuptools_grpc.build_grpc import build_grpc


@pytest.fixture
def tmpdir():
    tmp = TempDirectory()
    tmp.makedir("src")
    tmp.makedir("src/services")
    tmp.makedir("dest")
    tmp.write("src/module1.proto", b"")
    tmp.write("src/module2.proto", b"")
    tmp.write("src/services/service_grpc.proto", b"")
    yield tmp
    tmp.cleanup()


def test_finalize_options_empty():
    cmd = build_grpc(Distribution())
    cmd.initialize_options()
    cmd.finalize_options()
    assert cmd.proto_files == []
    assert cmd.grpc_files == []


def test_finalize_options_not_empty(tmpdir):
    cmd = build_grpc(Distribution())
    cmd.initialize_options()
    cmd.proto_files = "**/*.proto"
    cmd.grpc_files = "**/*_grpc.proto"
    cmd.proto_path = tmpdir.path + "/src"
    cmd.output_path = tmpdir.path + "/dest"
    cmd.finalize_options()

    assert cmd.proto_files == ["module1.proto", "module2.proto", "services/service_grpc.proto"]
    assert cmd.grpc_files == ["services/service_grpc.proto"]


def test_finalize_options_trailing_slashes(tmpdir):
    cmd = build_grpc(Distribution())
    cmd.initialize_options()
    cmd.proto_files = "**/*.proto"
    cmd.grpc_files = "**/*_grpc.proto"
    cmd.proto_path = tmpdir.path + "/src/"
    cmd.output_path = tmpdir.path + "/dest/"
    cmd.finalize_options()

    assert cmd.proto_files == ["module1.proto", "module2.proto", "services/service_grpc.proto"]
    assert cmd.grpc_files == ["services/service_grpc.proto"]


def test_run(tmpdir):
    with patch("setuptools_grpc.build_grpc.protoc_main", autospec=True) as mock:
        cmd = build_grpc(Distribution())
        cmd.initialize_options()
        cmd.proto_files = "**/*.proto"
        cmd.grpc_files = "**/*_grpc.proto"
        cmd.proto_path = tmpdir.path + "/src"
        cmd.output_path = tmpdir.path + "/dest"
        cmd.finalize_options()

        mock.return_value = False
        cmd.run()

        assert mock.mock_calls == [
            call(
                [
                    "__main__",
                    "-I" + str(Path(grpc_tools.__file__).parent / "_proto"),
                    "-I" + tmpdir.path + "/src",
                    "--python_out",
                    tmpdir.path + "/dest",
                    "--pyi_out",
                    tmpdir.path + "/dest",
                    tmpdir.path + "/src/module1.proto",
                    tmpdir.path + "/src/module2.proto",
                    tmpdir.path + "/src/services/service_grpc.proto",
                ]
            ),
            call(
                [
                    "__main__",
                    "-I" + str(Path(grpc_tools.__file__).parent / "_proto"),
                    "-I" + tmpdir.path + "/src",
                    "--grpc_python_out",
                    tmpdir.path + "/dest",
                    tmpdir.path + "/src/services/service_grpc.proto",
                ]
            ),
        ]
