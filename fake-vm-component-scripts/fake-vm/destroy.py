#!/usr/bin/env python3

import sys
import yaml

import fvm

arguments = yaml.safe_load(sys.stdin)

vm_ids = list(arguments.get('instances', {}).keys())

errors = False
for vmid in vm_ids:
    if not fvm.exists(vmid):
        print("Fake VM {} does not exist".format(vmid), file=sys.stderr)
        errors = True

if errors:
    sys.exit(1)

for vmid in vm_ids:
    fvm.delete(vmid)

result = {
    'instances': {
        vmid: {
            'status': {
                'flags': {'active': False, 'converging': False, 'failed': False}
            }
        } for vmid in vm_ids
    }
}
yaml.safe_dump(result, sys.stdout)

