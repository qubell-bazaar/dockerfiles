#!/usr/local/bin/python

import sys, yaml

data = yaml.safe_load(sys.stdin)
yaml.dump(data, sys.stdout)
