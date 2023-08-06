# PC-Info
[![GitHub license](https://img.shields.io/badge/license-MIT-brightgreen.svg)](https://raw.githubusercontent.com/stop-bark/PC-Info/main/LICENSE)
[![PyPI version](https://badge.fury.io/py/PC-Info.svg)](https://badge.fury.io/py/PC-Info)
[![Downloads](https://pepy.tech/badge/PC-Info)](https://pepy.tech/project/PC-Info)

PC-Info is a library used for getting all kinds of information about the computer you are using this module on.

## How to install

Install it with pip `pip install pc-info`

## Examples

* [Get System Architecture](#get-system-architecture)

### Get System Architecture
```python
import pc_tools

print(pc_tools.architecture())
```
This code will return ```64``` for a 64 bit operating system, or ```32``` for a 32 bit operating system.