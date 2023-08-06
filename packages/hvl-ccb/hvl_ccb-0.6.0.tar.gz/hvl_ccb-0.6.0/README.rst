====================
HVL Common Code Base
====================

.. image:: https://img.shields.io/pypi/v/hvl_ccb?logo=PyPi
   :target: https://pypi.org/project/hvl_ccb/
   :alt: PyPI version

.. image:: https://img.shields.io/pypi/pyversions/hvl_ccb?logo=Python
   :target: https://pypi.org/project/hvl_ccb/
   :alt: Supported Python versions

.. image:: https://img.shields.io/gitlab/pipeline/ethz_hvl/hvl_ccb/master?logo=gitlab
    :target: https://gitlab.com/ethz_hvl/hvl_ccb/-/tree/master
    :alt: Pipeline status

.. image:: https://img.shields.io/gitlab/coverage/ethz_hvl/hvl_ccb/master?logo=gitlab
    :target: https://gitlab.com/ethz_hvl/hvl_ccb/commits/master
    :alt: Coverage report

.. image:: https://img.shields.io/readthedocs/hvl_ccb?logo=read-the-docs
    :target: https://hvl-ccb.readthedocs.io/en/stable/
    :alt: Documentation Status

.. image:: https://img.shields.io/gitlab/pipeline/ethz_hvl/hvl_ccb/devel?label=devel&logo=gitlab
    :target: https://gitlab.com/ethz_hvl/hvl_ccb/-/tree/devel
    :alt: Development pipeline status

Python common code base to control devices high voltage research devices, in
particular, as used in Christian Franck's High Voltage Lab (HVL), D-ITET, ETH.


* Free software: GNU General Public License v3
* Copyright (c) 2019-2021 ETH Zurich, SIS ID and HVL D-ITET


Features
--------

For managing multi-device experiments instantiate the :code:`ExperimentManager`
utility class.

Devices
~~~~~~~

The devices wrappers in :code:`hvl_ccb` provide a standardised API with configuration
dataclasses, various settings and options enumerations, as well as start/stop methods.
Currently, wrappers to control the following devices are available:

+-------------------------+------------------------------------------------------------+
| Function/Type           | Devices                                                    |
+=========================+============================================================+
| Data acquisition and    | | LabJack (T4, T7, T7-PRO)                                 |
| Digital IO              |                                                            |
+-------------------------+------------------------------------------------------------+
| Experiment control      | | HVL Supercube with and without Frequency Converter       |
+-------------------------+------------------------------------------------------------+
| Gas Analyser            | | MBW 973-SF6 gas dew point mirror analyzer                |
|                         | | Pfeiffer Vacuum TPG (25x, 26x and 36x) controller for    |
|                         |   compact pressure gauges                                  |
|                         | | SST Luminox oxygen sensor                                |
+-------------------------+------------------------------------------------------------+
| I2C host                | | TiePie (HS5, WS5)                                        |
+-------------------------+------------------------------------------------------------+
| Laser                   | | CryLaS pulsed laser                                      |
|                         | | CryLaS laser attenuator                                  |
+-------------------------+------------------------------------------------------------+
| Oscilloscope            | | Rhode & Schwarz RTO 1024                                 |
|                         | | TiePie (HS5, HS6, WS5)                                   |
+-------------------------+------------------------------------------------------------+
| Power supply            | | Elektro-Automatik PSI9000                                |
|                         | | FuG Elektronik                                           |
|                         | | Heinzinger PNC                                           |
|                         | | Technix capacitor charger                                |
+-------------------------+------------------------------------------------------------+
| Stepper motor drive     | | Newport SMC100PP                                         |
|                         | | Schneider Electric ILS2T                                 |
+-------------------------+------------------------------------------------------------+
| Waveform generator      | | TiePie (HS5, WS5)                                        |
+-------------------------+------------------------------------------------------------+

Each device uses at least one standardised communication protocol wrapper.

Communication protocols
~~~~~~~~~~~~~~~~~~~~~~~

In :code:`hvl_ccb` by "communication protocol" we mean different levels of
communication standards, from the low level actual communication protocols like
serial communication to application level interfaces like VISA TCP standard. There
are also devices in :code:`hvl_ccb` that use dummy communication protocol concept;
this is because these devices build on propriety vendor libraries that communicate
with vendor devices, like in case of the TiePie devices.

The communication protocol wrappers in :code:`hvl_ccb` provide a standardised API with
configuration dataclasses, as well as open/close, and read/write/query methods.
Currently, wrappers to use the following communication protocols are available:

+------------------------+-------------------------------------------------------------+
| Communication protocol | Devices using                                               |
+========================+=============================================================+
| Modbus TCP             | | Schneider Electric ILS2T stepper motor drive              |
+------------------------+-------------------------------------------------------------+
| OPC UA                 | | HVL Supercube with and without Frequency Converter        |
+------------------------+-------------------------------------------------------------+
| Serial                 | | CryLaS pulsed laser and laser attenuator                  |
|                        | | FuG Elektronik power supply (e.g. capacitor charger HCK)  |
|                        |   using the Probus V protocol                               |
|                        | | Heinzinger PNC power supply                               |
|                        |   using Heinzinger Digital Interface I/II                   |
|                        | | SST Luminox oxygen sensor                                 |
|                        | | MBW 973-SF6 gas dew point mirror analyzer                 |
|                        | | Newport SMC100PP single axis driver for 2-phase stepper   |
|                        |   motors                                                    |
|                        | | Pfeiffer Vacuum TPG (25x, 26x and 36x) controller for     |
|                        |   compact pressure gauges                                   |
|                        | | Technix capacitor charger                                 |
+------------------------+-------------------------------------------------------------+
| Telnet                 | | Technix capacitor charger                                 |
+------------------------+-------------------------------------------------------------+
| VISA TCP               | | Elektro-Automatik PSI9000 DC power supply                 |
|                        | | Rhode & Schwarz RTO 1024 oscilloscope                     |
+------------------------+-------------------------------------------------------------+
| *propriety*            | | LabJack (T4, T7, T7-PRO) devices, which communicate via   |
|                        |   LJM Library                                               |
|                        | | TiePie (HS5, HS6, WS5) oscilloscopes, generators and I2C  |
|                        |   hosts, which communicate via LibTiePie SDK                |
+------------------------+-------------------------------------------------------------+


Documentation
-------------

Note: if you're planning to contribute to the :code:`hvl_ccb` project do read
beforehand the **Contributing** section in the HVL CCB documentation.

Do either:

* read `HVL CCB documentation at RTD`_,

or

* build and read HVL CCB documentation locally; install first documentation build
  requirements::

    $ pip install docs/requirements.txt

  and then either on Windows in Git BASH run::

    $ ./make.sh docs

  or from any other shell with GNU Make installed run::

    $ make docs

  The target index HTML (:code:`"docs/_build/html/index.html"`) should open
  automatically in your Web browser.

.. _`HVL CCB documentation at RTD`: https://readthedocs.org/projects/hvl-ccb/

Credits
-------

This package was created with Cookiecutter_ and the
`audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
