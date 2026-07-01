Check explorer
---------------

**dns_explorer** is toolset for checking DNS.

Developed in `python <https://www.python.org/>`_ code.

The README is used to introduce the tool and provide instructions on
how to install the tool, any machine dependencies it may have and any
other information that should be provided before the tool is installed.

|dns_explorer python checker| |dns_explorer python package| |github issues| |documentation status| |github contributors|

.. |dns_explorer python checker| image:: https://github.com/vroncevic/dns_explorer/actions/workflows/dns_explorer_python_checker.yml/badge.svg
   :target: https://github.com/vroncevic/dns_explorer/actions/workflows/dns_explorer_python_checker.yml

.. |dns_explorer python package| image:: https://github.com/vroncevic/dns_explorer/actions/workflows/dns_explorer_package_checker.yml/badge.svg
   :target: https://github.com/vroncevic/dns_explorer/actions/workflows/dns_explorer_package.yml

.. |github issues| image:: https://img.shields.io/github/issues/vroncevic/dns_explorer.svg
   :target: https://github.com/vroncevic/dns_explorer/issues

.. |github contributors| image:: https://img.shields.io/github/contributors/vroncevic/dns_explorer.svg
   :target: https://github.com/vroncevic/dns_explorer/graphs/contributors

.. |documentation status| image:: https://readthedocs.org/projects/dns_explorer/badge/?version=latest
   :target: https://dns-explorer.readthedocs.io/en/latest/?badge=latest

.. toctree::
   :maxdepth: 4
   :caption: Contents

   self
   modules

Installation
-------------

|dns_explorer python3 build|

.. |dns_explorer python3 build| image:: https://github.com/vroncevic/dns_explorer/actions/workflows/dns_explorer_python3_build.yml/badge.svg
   :target: https://github.com/vroncevic/dns_explorer/actions/workflows/dns_explorer_python3_build.yml

Navigate to release `page`_ download and extract release archive.

.. _page: https://github.com/vroncevic/dns_explorer/releases

To install **dns_explorer** type the following

.. code-block:: bash

    tar xvzf dns_explorer-x.y.z.tar.gz
    cd dns_explorer-x.y.z/
    # python3
    wget https://bootstrap.pypa.io/get-pip.py
    python3 get-pip.py 
    python3 -m pip install --upgrade setuptools
    python3 -m pip install --upgrade pip
    python3 -m pip install --upgrade build
    pip3 install -r requirements.txt
    python3 -m build --no-isolation --wheel
    pip3 install ./dist/dns_explorer-*-py3-none-any.whl
    rm -f get-pip.py
    chmod 755 /usr/local/lib/python3.10/dist-packages/usr/local/bin/dns_explorer_run.py
    ln -s /usr/local/lib/python3.10/dist-packages/usr/local/bin/dns_explorer_run.py /usr/local/bin/dns_explorer_run.py

You can use Docker to create image/container, or You can use pip to install

.. code-block:: bash

    # pyton3
    pip3 install dns_explorer

Dependencies
-------------

**dns_explorer** requires next modules and libraries

* `ats-utilities - Python App/Tool/Script Utilities <https://pypi.org/project/ats-utilities/>`_
* `dnspython - DNS toolkit for Python <https://pypi.org/project/dnspython/>`_

Tool structure
---------------

**dns_explorer** is based on OOP.

Tool structure

.. code-block:: bash

    dns_explorer/
         ├── application/
         │   ├── __init__.py
         │   └── service.py
         ├── dns_explorer_bundle.py
         ├── domain/
         │   ├── __init__.py
         │   ├── models.py
         │   └── ports/
         │       ├── idns_resolver.py
         │       ├── __init__.py
         │       └── iservice.py
         ├── engine.py
         ├── infrastructure/
         │   ├── cli.py
         │   ├── cli_bundle.py
         │   ├── config/
         │   │   ├── dns_explorer.cfg
         │   │   └── dns_explorer.logo
         │   ├── dns_resolver.py
         │   ├── explore_command.py
         │   ├── icli.py
         │   ├── icli_command.py
         │   ├── __init__.py
         │   ├── records_command.py
         │   ├── resolve_command.py
         │   └── reverse_command.py
         └── __init__.py

     6 directories, 22 files

Usage
------

Install package

.. code-block:: bash

    pip3 install armpicom

Prepare main entry point by downloading `main.py` or create your own.

.. code-block:: bash

    wget -O main.py https://raw.githubusercontent.com/vroncevic/armpicom/main/main.py

Running tool for DNS exploring

.. code-block:: bash

    # Use case 1: Standard domain scan (no cluster variations, non-verbose)
    echo "=== Running Use Case 1: Standard scan for google.com ==="
    python3 main.py explore --domain google.com

    # Use case 2: Scan with cluster variations (size 1)
    echo "=== Running Use Case 2: Scan for google.com with cluster size 1 ==="
    python3 main.py explore --domain google.com --cluster 1

    # Use case 3: Scan with cluster size 2 and verbose logging enabled
    echo "=== Running Use Case 3: Verbose scan for google.com with cluster size 2 ==="
    python3 main.py explore --domain google.com --cluster 2 --verbose True

    # Use case 4: Query domain DNS records (A, AAAA, MX, NS, TXT, SOA)
    echo "=== Running Use Case 4: DNS Records query for google.com ==="
    python3 main.py records --domain google.com

    # Use case 5: Resolve forward IP and reverse hostnames for a single domain name
    echo "=== Running Use Case 5: Resolve single domain google.com ==="
    python3 main.py resolve --domain google.com --verbose True

    # Use case 6: Query reverse DNS hostnames for an IP address
    echo "=== Running Use Case 6: Query reverse DNS for IP 8.8.8.8 ==="
    python3 main.py reverse --ip 8.8.8.8


Copyright and licence
-----------------------

|license: gpl v3| |license: apache 2.0|

.. |license: gpl v3| image:: https://img.shields.io/badge/license-gplv3-blue.svg
   :target: https://www.gnu.org/licenses/gpl-3.0

.. |license: apache 2.0| image:: https://img.shields.io/badge/license-apache%202.0-blue.svg
   :target: https://opensource.org/licenses/apache-2.0

Copyright (C) 2024 - 2026 by `vroncevic.github.io/dns_explorer <https://vroncevic.github.io/dns_explorer>`_

**dns_explorer** is free software; you can redistribute it and/or modify
it under the same terms as Python itself, either Python version 3.x or,
at your option, any later version of Python 3 you may have available.

Lets help and support PSF.

|python software foundation|

.. |python software foundation| image:: https://raw.githubusercontent.com/vroncevic/dns_explorer/dev/docs/psf-logo-alpha.png
   :target: https://www.python.org/psf/

|donate|

.. |donate| image:: https://www.paypalobjects.com/en_us/i/btn/btn_donatecc_lg.gif
   :target: https://www.python.org/psf/donations/

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
