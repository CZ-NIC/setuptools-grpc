import shutil
from pathlib import Path

import pytest
from build import ProjectBuilder
from setuptools import Distribution
from wheel_inspect import inspect_wheel

from setuptools_grpc import has_grpc, inject_build


@pytest.fixture
def project_no_config(tmp_path):
    shutil.copytree(Path(__file__).parent / "project_no_config", tmp_path, dirs_exist_ok=True)
    builder = ProjectBuilder(tmp_path)
    yield builder.build("wheel", output_directory=tmp_path)


@pytest.fixture
def project_no_protos(tmp_path):
    shutil.copytree(Path(__file__).parent / "project_no_protos", tmp_path, dirs_exist_ok=True)
    builder = ProjectBuilder(tmp_path)
    yield builder.build("wheel", output_directory=tmp_path)


@pytest.fixture
def project_protos(tmp_path):
    shutil.copytree(Path(__file__).parent / "project_protos", tmp_path, dirs_exist_ok=True)
    builder = ProjectBuilder(tmp_path)
    yield builder.build("wheel", output_directory=tmp_path)


def test_no_config(project_no_config):
    output = inspect_wheel(project_no_config)
    assert output["derived"]["modules"] == ["example"]


def test_no_protos(project_no_protos):
    output = inspect_wheel(project_no_protos)
    assert output["derived"]["modules"] == ["example"]


def test_protos(project_protos):
    output = inspect_wheel(project_protos)
    assert output["derived"]["modules"] == ["example", "example.service_pb2"]


def test_inject_build():
    dist = Distribution()
    build_cls = dist.get_command_class("build")
    sub_commands = list(build_cls.sub_commands)
    inject_build(dist)
    assert build_cls.sub_commands == [("build_grpc", has_grpc)] + sub_commands
