[![Build Status](https://dev.azure.com/l-johnston/unit_system/_apis/build/status/l-johnston.unit_system?branchName=master)](https://dev.azure.com/l-johnston/unit_system/_build/latest?definitionId=8&branchName=master) ![Code Coverage](https://img.shields.io/azure-devops/coverage/l-johnston/unit_system/8) ![Version](https://img.shields.io/pypi/v/unit-system)
# `unit_system`
The unit_system package provides a way to do physical quantity math
in Python that replicates Mathcad's unit system. The implementation
conforms to the [SI standard](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication811e2008.pdf).

## Installation
```linux
$ pip install unit_system
```  

## Usage

```python
>>> from unit_system import Quantity
>>> V = Quantity(1, "V")
>>> A = Quantity(1, "A")
>>> 1*V / (1*A)
1.0 Ω
```  

You can load predefined units like the ones in Mathcad.

```python
>>> from unit_system import *
>>> 1*mΩ * 1*A
0.001 V
```

## Documentation
https://l-johnston.github.io/unit_system/