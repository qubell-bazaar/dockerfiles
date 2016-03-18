#!/usr/bin/env python3

import sys
import yaml
import fvm

arguments = yaml.safe_load(sys.stdin)

vm_ids = list(arguments.get('instances', {}).keys())

for vmid in vm_ids:
    if not fvm.fake_vm_exists(vmid):
        print("Fake VM {} does not exist".format(vmid), file=sys.stderr)
        sys.exit(1)

for vmid in vm_ids:
    fvm.destroy_fake_vm(vmid)

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

