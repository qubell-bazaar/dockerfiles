#!/usr/local/bin/python

import sys, yaml, subprocess

stdin = yaml.safe_load(sys.stdin)
script = stdin['script']
arguments = stdin['arguments']

process = subprocess.Popen([script], stdin=subprocess.PIPE, stdout=subprocess.PIPE, universal_newlines=True)
yaml.dump(arguments, process.stdin)
process.stdin.close()

output = yaml.safe_load(process.stdout)
stdout = { "results": output }
yaml.dump(stdout, sys.stdout)
