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
  Paths are relative to ``proto_path``.
  ``**`` can be used to match any files and zero or more directories.
  Default value is empty list.

* ``grpc_files``: Newline separated list of glob patterns matching grpc service files to be compiled.
  Paths are relative to ``proto_path``.
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
You can read more about it in `setuptools docs <https://setuptools.pypa.io/en/latest/build_meta.html>`__.

.. code-block:: toml

   # file: pyproject.toml
   [build-system]
   requires = ["setuptools", "setuptools-grpc"]
   build-backend = "setuptools.build_meta"

Next, you need to configure ``setuptools_grpc`` itself.
This can be done in ``setup.py``, but we recommend declarative config in ``setup.cfg``.
Depending on your project structure, you may not need some of the options below.
You'll always need to specify at least ``proto_files`` or ``grpc_files``,
otherwise ``setuptools_grpc`` won't do anything.

.. code-block:: ini

   # file: setup.cfg
   [build_grpc]
   proto_files = **/*.proto
   grpc_files = **/*_grpc.proto
   proto_path = ./src
   output_path = ./out

It's also recommended to add generated files to your ``MANIFEST.in``. Otherwise they might be missing from the built wheel. See `setuptools docs <https://setuptools.pypa.io/en/latest/userguide/miscellaneous.html#controlling-files-in-the-distribution>`__ for more details about how files are included in the distribution.

.. code-block::

   # file: MANIFEST.in
   graft out

------------------------------
Restricting build dependencies
------------------------------

Generated gRPC Python modules have a restriction:
You should ideally run the code with the same version of ``protobuf`` that was used to build the package.
To complicate matters even further, ``grpcio-tools`` bundles its own version of ``protobuf`` and although
it does depend on ``protobuf`` package, it doesn't actually use it to generate the Python modules.

There's a possible solution: Don't generate the gRPC Python modules until you know which version of
``protobuf`` will be used to run it.
If you have a separate package for gRPC API, you can publish the ``sdist``, but not the wheel.
Wheel will be built when you install the ``sdist`` and you can specify the ``grpcio-tools`` version used to build it.
To this end, ``setuptools-grpc`` offers ``setuptools_grpc.build_backend``.
When you use this build backend, env variable ``SETUPTOOLS_GRPC_BUILD_DEPS`` will be considered and all
of the specified dependencies will be used as additional build dependencies.
You can specify multiple dependency restrictions separated by whitespace (don't use any whitespaces otherwise!).

.. code-block:: toml

   # file: pyproject.toml
   [build-system]
   requires = ["setuptools-grpc"]
   build-backend = "setuptools_grpc.build_backend"

.. code-block:: sh

   SETUPTOOLS_GRPC_BUILD_DEPS="grpcio-tools==1.74.0" pip install "my-grpc-api-package" "protobuf==4.31.1"

If you ensure that the specified ``protobuf`` version matches the version bundled in ``grpcio-tools``,
you'll run the code with the exaclty same ``protobuf`` version that was used to build it.
