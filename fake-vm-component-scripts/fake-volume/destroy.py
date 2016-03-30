#!/usr/bin/env python3

import sys
import yaml

import fvol

arguments = yaml.safe_load(sys.stdin)

vol_ids = list(arguments.get('instances', {}).keys())

errors = False
for volid in vol_ids:
    if not fvol.exists(volid):
        print("Fake Volume {} does not exist".format(volid), file=sys.stderr)
        errors = True

if errors:
    sys.exit(1)

for volid in vol_ids:
    fvol.delete(volid)

result = {
    'instances': {
        volid: {
            'status': {
                'flags': {'active': False, 'converging': False, 'failed': False}
            }
        } for volid in vol_ids
    }
}
yaml.safe_dump(result, sys.stdout)

