#!/usr/bin/env python

# This imports and runs ../../xos-observer.py

import importlib
import os
import sys
from xosconfig import Config

config_file = os.path.abspath(os.path.dirname(os.path.realpath(__file)) + '/metronetwork_config.yaml')

sys.path.append("/opt/xos/synchronizers/base")
print sys.path
mod = importlib.import_module("xos-synchronizer")
mod.main()
