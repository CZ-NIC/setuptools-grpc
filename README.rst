===============
setuptools-grpc
===============

Plugin for setuptools to compile protobuf and gRPC service files to python modules.

-----
Usage
-----

This package provides ``build_grpc`` command.

Run ``python setup.py build_grpc`` for available options.

-------
Options
-------

Command ``build_grpc`` provides following options:

* ``proto_files``: Newline separated list of glob patterns matching protobuf files to be compiled.
  Paths are relative to the current directory.
  ``**`` can be used to match any files and zero or more directories.
  Default value is empty list.

* ``grpc_files``: Newline separated list of glob patterns matching grpc service files to be compiled.
  Paths are relative to the current directory.
  ``**`` can be used to match any files and zero or more directories.
  Default value is empty list.

* ``proto_path``: Path to root directory with protobuf files.
  This path is passed through ``-I`` option to ``grpc_tools.protoc``.
  Default is ``.`` (current directory).

* ``output_path``: Path to root directory for generated python modules.
  This path is passed through ``--python_out`` or ``--grpc_python_out`` option to ``grpc_tools.protoc``.
  Default is ``.`` (current directory).

-------
Example
-------

.. code-block::

   # pyproject.toml
   [build-system]
   requires = ["setuptools", "setuptools-grpc"]
   build-backend = "setuptools.build_meta"

.. code-block::

   # setup.py
   from distutils.command.build import build
   from setuptools import setup

   class custom_build(build):
       sub_commands = [
           ('build_grpc', None),
       ] + build.sub_commands

   setup(cmdclass={'build': custom_build})

.. code-block::

   # setup.cfg
   [build_grpc]
   proto_files = src/**/*.proto
   grpc_files = src/**/*_grpc.proto
   proto_path = ./src
   output_path = ./out
