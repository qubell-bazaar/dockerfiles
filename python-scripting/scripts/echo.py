#!/usr/bin/env python3

import sys, yaml

data = yaml.safe_load(sys.stdin)
yaml.dump(data, sys.stdout)
