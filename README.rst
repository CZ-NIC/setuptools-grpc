===============
setuptools-grpc
===============

.. image:: https://img.shields.io/pypi/v/setuptools-grpc
   :target: https://pypi.org/project/setuptools-grpc/
   :alt: PyPI - Version

.. image:: https://img.shields.io/pypi/l/setuptools-grpc
   :target: https://pypi.org/project/setuptools-grpc/
   :alt: PyPI - License

.. image:: https://img.shields.io/pypi/pyversions/setuptools-grpc
   :target: https://pypi.org/project/setuptools-grpc/
   :alt: PyPI - Python Version

.. image:: https://img.shields.io/github/actions/workflow/status/CZ-NIC/setuptools-grpc/test.yml
   :target: https://github.com/CZ-NIC/setuptools-grpc/
   :alt: GitHub Workflow Status (with event)

Plugin for setuptools to compile protobuf and gRPC service files to python modules.

This package provides ``build_grpc`` command for `setuptools <https://pypi.org/project/setuptools/>`_.
Its purpose is to build gRPC modules during ``build`` step of ``setuptools`` packaging.

---------------
What this isn't
---------------

**This is not a command line script.**

Direct invocation of ``setup.py`` (such as ``python setup.py build_grpc``) has been deprecated
and will be removed in future version of ``setuptools``.

If you'd like to have CLI for building gRPC modules, use
`grpcio-tools <https://pypi.org/project/grpcio-tools/>`_
directly (that's what this package uses under the hood).
After installing that package, you can learn about its options
by running ``python -m grpc_tools.protoc --help``.

------------
Installation
------------

You probably shouldn't install this package directly.
Instead, you should add it to the ``build-system.requires`` in ``pyproject.toml``.
See `Configuration`_.

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

-------------
Configuration
-------------

You have to specify ``setuptools-grpc`` as part of build backend requirements.
This follows specification introduced in `PEP 518 <https://peps.python.org/pep-0518/>`_.
You can read more about it in `setuptools docs <https://setuptools.pypa.io/en/latest/build_meta.html>`_.

.. code-block:: toml

   # file: pyproject.toml
   [build-system]
   requires = ["setuptools", "setuptools-grpc"]
   build-backend = "setuptools.build_meta"

Next, you need to actually add ``build_grpc`` as subcommand of the ``build`` command.
This needs to be done in ``setup.py``, but if ``setuptools`` ever allows for declarative
config, we'll be happy to support it.

.. code-block:: python

   # file: setup.py
   from setuptools import setup
   from setuptools.command.build import build

   class custom_build(build):
       sub_commands = [
           ('build_grpc', None),
       ] + build.sub_commands

   setup(cmdclass={'build': custom_build})

Finally, you need to configure ``setuptools_grpc`` itself.
This can be done in ``setup.py``, but we recommend declarative config in ``setup.cfg``.
Depending on your project structure, you may not need some of the options below.
You'll always need to specify at least ``proto_files`` or ``grpc_files``,
otherwise ``setuptools_grpc`` won't do anything.

.. code-block:: ini

   # file: setup.cfg
   [build_grpc]
   proto_files = src/**/*.proto
   grpc_files = src/**/*_grpc.proto
   proto_path = ./src
   output_path = ./out
