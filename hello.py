#!/usr/bin/env python3

from decouple import config
from icecream import ic
# from <local.py_module> import *
from pathlib import Path


# env
cwd = Path.cwd()
home = Path.home()
env = Path('.env')

# verbose icecream
ic.configureOutput(includeContext=True)


