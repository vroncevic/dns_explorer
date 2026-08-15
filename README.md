# DNS explorer

<img align="right" src="https://raw.githubusercontent.com/vroncevic/dns_explorer/dev/docs/dns_explorer_logo.png" width="25%">

**dns_explorer** is toolset for checking DNS.

Developed in **[python](https://www.python.org/)** code.

The README is used to introduce the modules and provide instructions on
how to install the modules, any machine dependencies it may have and any
other information that should be provided before the modules are installed.

[![dns_explorer python checker](https://github.com/vroncevic/dns_explorer/actions/workflows/dns_explorer_python_checker.yml/badge.svg)](https://github.com/vroncevic/dns_explorer/actions/workflows/dns_explorer_python_checker.yml) [![dns_explorer package checker](https://github.com/vroncevic/dns_explorer/actions/workflows/dns_explorer_package_checker.yml/badge.svg)](https://github.com/vroncevic/dns_explorer/actions/workflows/dns_explorer_package.yml) [![GitHub issues open](https://img.shields.io/github/issues/vroncevic/dns_explorer.svg)](https://github.com/vroncevic/dns_explorer/issues) [![GitHub contributors](https://img.shields.io/github/contributors/vroncevic/dns_explorer.svg)](https://github.com/vroncevic/dns_explorer/graphs/contributors)

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**

- [🚀 Installation](#-installation)
    - [Install using pip](#install-using-pip)
    - [Install using build](#install-using-build)
    - [Install using py setup](#install-using-py-setup)
    - [Install using docker](#install-using-docker)
- [📦 Dependencies](#-dependencies)
- [📁 Tool structure](#-tool-structure)
- [📊 Code coverage](#-code-coverage)
- [🛠 Usage](#-usage)
- [📚 Docs](#-docs)
- [👥 Contributing](#-contributing)
- [📄 Copyright and licence](#-copyright-and-licence)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

### 🚀 Installation
Used next development environment

![debian linux os](https://raw.githubusercontent.com/vroncevic/dns_explorer/dev/docs/debtux.png)

[![dns_explorer python3 build](https://github.com/vroncevic/dns_explorer/actions/workflows/dns_explorer_python3_build.yml/badge.svg)](https://github.com/vroncevic/dns_explorer/actions/workflows/dns_explorer_python3_build.yml)

Currently there are three ways to install package
* Install process based on using pip mechanism
* Install process based on build mechanism
* Install process based on setup.py mechanism
* Install process based on docker mechanism

##### Install using pip

**dns_explorer** is located at **[pypi.org](https://pypi.org/project/dns_explorer/)**.

You can install by using pip

```bash
# python3
pip3 install dns_explorer
```

##### Install using build

Navigate to release **[page](https://github.com/vroncevic/dns_explorer/releases/)** download and extract release archive.

To install **dns_explorer** type the following

```bash
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
```

##### Install using py setup

Navigate to **[release page](https://github.com/vroncevic/dns_explorer/releases)** download and extract release archive.

To install **dns_explorer** locate and run setup.py with arguments

```bash
tar xvzf dns_explorer-x.y.z.tar.gz
cd dns_explorer-x.y.z
# python3
pip3 install -r requirements.txt
python3 setup.py install_lib
python3 setup.py install_egg_info
```

##### Install using docker

You can use Dockerfile to create image/container.

### 📦 Dependencies
**dns_explorer** requires next modules and libraries

* [ats-utilities - Python App/Tool/Script Utilities](https://pypi.org/project/ats-utilities/)
* [dnspython - DNS toolkit for Python](https://pypi.org/project/dnspython/)

### 📁 Tool structure
**dns_explorer** is based on OOP.

Tool structure

<details>
<summary><b>Click to expand framework structure</b></summary>

```bash
    dns_explorer/
         ├── core/
         │   ├── __init__.py
         │   ├── model/
         │   │   ├── __init__.py
         │   │   └── models.py
         │   └── service/
         │       ├── engine.py
         │       ├── idns_resolver.py
         │       ├── __init__.py
         │       └── iservice.py
         ├── engine.py
         ├── infrastructure/
         │   ├── cli/
         │   │   ├── engine.py
         │   │   ├── icli.py
         │   │   ├── __init__.py
         │   │   └── setup/
         │   │       ├── bundle.py
         │   │       ├── dep_validator.py
         │   │       ├── dependencies.py
         │   │       ├── factory.py
         │   │       ├── __init__.py
         │   │       ├── keys.py
         │   │       ├── opt_validator.py
         │   │       ├── options.py
         │   │       ├── registry.py
         │   │       └── validator.py
         │   ├── command/
         │   │   ├── command.py
         │   │   ├── explore_command_definition.py
         │   │   ├── explore_command_executor.py
         │   │   ├── icommand_definition.py
         │   │   ├── icommand_executor.py
         │   │   ├── __init__.py
         │   │   ├── records_command_definition.py
         │   │   ├── records_command_executor.py
         │   │   ├── resolve_command_definition.py
         │   │   ├── resolve_command_executor.py
         │   │   ├── reverse_command_definition.py
         │   │   └── reverse_command_executor.py
         │   ├── config/
         │   │   ├── dns_explorer.cfg
         │   │   └── dns_explorer.logo
         │   ├── dns_resolver.py
         │   └── __init__.py
         ├── __init__.py
         ├── py.typed
         └── setup/
             ├── bundle.py
             ├── dep_validator.py
             ├── dependencies.py
             ├── factory.py
             ├── __init__.py
             ├── keys.py
             ├── opt_validator.py
             ├── options.py
             ├── registry.py
             └── validator.py

     10 directories, 49 files
```
</details>

### 📊 Code coverage
<details>
<summary><b>Click to expand code coverage</b></summary>

| Name | Stmts | Miss | Cover |
|------|-------|------|-------|
| `dns_explorer/__init__.py` | 8 | 0 | 100%|
| `dns_explorer/core/__init__.py` | 9 | 0 | 100%|
| `dns_explorer/core/model/__init__.py` | 9 | 0 | 100%|
| `dns_explorer/core/model/models.py` | 19 | 0 | 100%|
| `dns_explorer/core/service/__init__.py` | 9 | 0 | 100%|
| `dns_explorer/core/service/engine.py` | 68 | 12 | 82%|
| `dns_explorer/core/service/idns_resolver.py` | 17 | 0 | 100%|
| `dns_explorer/core/service/iservice.py` | 18 | 0 | 100%|
| `dns_explorer/engine.py` | 57 | 0 | 100%|
| `dns_explorer/infrastructure/__init__.py` | 8 | 0 | 100%|
| `dns_explorer/infrastructure/cli/__init__.py` | 9 | 0 | 100%|
| `dns_explorer/infrastructure/cli/engine.py` | 43 | 0 | 100%|
| `dns_explorer/infrastructure/cli/icli.py` | 15 | 0 | 100%|
| `dns_explorer/infrastructure/cli/setup/__init__.py` | 9 | 0 | 100%|
| `dns_explorer/infrastructure/cli/setup/bundle.py` | 22 | 0 | 100%|
| `dns_explorer/infrastructure/cli/setup/dep_validator.py` | 36 | 0 | 100%|
| `dns_explorer/infrastructure/cli/setup/dependencies.py` | 18 | 0 | 100%|
| `dns_explorer/infrastructure/cli/setup/factory.py` | 46 | 0 | 100%|
| `dns_explorer/infrastructure/cli/setup/keys.py` | 28 | 0 | 100%|
| `dns_explorer/infrastructure/cli/setup/opt_validator.py` | 34 | 0 | 100%|
| `dns_explorer/infrastructure/cli/setup/options.py` | 17 | 0 | 100%|
| `dns_explorer/infrastructure/cli/setup/registry.py` | 26 | 0 | 100%|
| `dns_explorer/infrastructure/cli/setup/validator.py` | 43 | 0 | 100%|
| `dns_explorer/infrastructure/command/__init__.py` | 9 | 0 | 100%|
| `dns_explorer/infrastructure/command/command.py` | 16 | 0 | 100%|
| `dns_explorer/infrastructure/command/explore_command_definition.py` | 24 | 1 | 96%|
| `dns_explorer/infrastructure/command/explore_command_executor.py` | 50 | 17 | 66%|
| `dns_explorer/infrastructure/command/icommand_definition.py` | 14 | 0 | 100%|
| `dns_explorer/infrastructure/command/icommand_executor.py` | 14 | 0 | 100%|
| `dns_explorer/infrastructure/command/records_command_definition.py` | 24 | 1 | 96%|
| `dns_explorer/infrastructure/command/records_command_executor.py` | 47 | 14 | 70%|
| `dns_explorer/infrastructure/command/resolve_command_definition.py` | 24 | 1 | 96%|
| `dns_explorer/infrastructure/command/resolve_command_executor.py` | 51 | 19 | 63%|
| `dns_explorer/infrastructure/command/reverse_command_definition.py` | 24 | 1 | 96%|
| `dns_explorer/infrastructure/command/reverse_command_executor.py` | 46 | 14 | 70%|
| `dns_explorer/infrastructure/dns_resolver.py` | 66 | 15 | 77%|
| `dns_explorer/setup/__init__.py` | 9 | 0 | 100%|
| `dns_explorer/setup/bundle.py` | 23 | 0 | 100%|
| `dns_explorer/setup/dep_validator.py` | 36 | 0 | 100%|
| `dns_explorer/setup/dependencies.py` | 19 | 0 | 100%|
| `dns_explorer/setup/factory.py` | 59 | 0 | 100%|
| `dns_explorer/setup/keys.py` | 27 | 0 | 100%|
| `dns_explorer/setup/opt_validator.py` | 34 | 0 | 100%|
| `dns_explorer/setup/options.py` | 12 | 0 | 100%|
| `dns_explorer/setup/registry.py` | 32 | 0 | 100%|
| `dns_explorer/setup/validator.py` | 48 | 0 | 100%|
| **Total** | 1276 | 95 | 93% |

</details>

### 🛠 Usage
Install package

```bash
pip3 install armpicom
```

Prepare main entry point by downloading [main.py](https://raw.githubusercontent.com/vroncevic/armpicom/main/main.py) or create your own.


```bash
wget -O main.py https://raw.githubusercontent.com/vroncevic/armpicom/main/main.py
```

Running tool for DNS exploring

```bash
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
```

### 📚 Docs
[![Documentation Status](https://readthedocs.org/projects/dns_explorer/badge/?version=latest)](https://dns-explorer.readthedocs.io/en/latest/?badge=latest)

More documentation and info at

* [dns_explorer.readthedocs.io](https://dns-explorer.readthedocs.io)
* [www.python.org](https://www.python.org/)

### 👥 Contributing
[Contributing to dns_explorer](CONTRIBUTING.md)

### 📄 Copyright and licence
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0) [![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

Copyright (C) 2024 - 2026 by [vroncevic.github.io/dns_explorer](https://vroncevic.github.io/dns_explorer)

**dns_explorer** is free software; you can redistribute it and/or modify
it under the same terms as Python itself, either Python version 3.x or,
at your option, any later version of Python 3 you may have available.

Lets help and support PSF.

[![Python Software Foundation](https://raw.githubusercontent.com/vroncevic/dns_explorer/dev/docs/psf-logo-alpha.png)](https://www.python.org/psf/)

[![Donate](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://www.python.org/psf/donations/)
