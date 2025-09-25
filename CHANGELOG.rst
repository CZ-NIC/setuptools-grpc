ChangeLog
=========

.. contents:: Releases
   :backlinks: none
   :local:

Unreleased
----------


1.0.0 (2025-09-25)
--------------------

* Inject ``build_grpc`` as ``build`` subcommand (#7).
  * This means that you should no longer modify the ``build`` command in your ``setup.py``.
  ``build_grpc`` is automatically injected as first subcommand of ``build``.
* Add build backend for customizing build dependencies (#20).
* Drop ``pkg_resources`` (#24).
* Update supported python versions: 3.9, 3.10, 3.11, 3.12 and 3.13
* Use ruff instead of flake8, isort and black.

1.0.0b2 (2025-09-04)
--------------------

* Add build backend for customizing build dependencies
* Drop ``pkg_resources``
* Update supported python versions: 3.9, 3.10, 3.11, 3.12 and 3.13

1.0.0b1 (2024-02-01)
--------------------

* Inject ``build_grpc`` as ``build`` subcommand (#7).
  * This means that you should no longer modify the ``build`` command in your ``setup.py``.
  ``build_grpc`` is automatically injected as first subcommand of ``build``.
* Use ruff instead of flake8, isort and black.

0.5 (2023-12-14)
----------------

* Support Python versions 3.8, 3.9, 3.10, 3.11 and 3.12.
* Fix tailing slash issues with proto files glob discovery (#9).
* Add basic tests (#11).
* Improve documentation.

0.4 (2023-02-08)
----------------

* Fix missing dependency constraint for grpcio-tools.

0.3 (2023-02-08)
----------------

* Add generation of .pyi files.

0.2 (2022-06-28)
----------------

* Fix grpc_files option processing.


0.1 (2022-06-28)
----------------

Initial version.
