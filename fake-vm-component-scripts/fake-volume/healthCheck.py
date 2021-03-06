#!/usr/bin/env python3

import sys
import yaml

import fvol

arguments = yaml.safe_load(sys.stdin)

vol_ids = list(arguments.get('instances', {}).keys())

vol_infos = {}
for volid in vol_ids:
    vol = fvol.load(volid)
    if vol:
        status = {
            'flags': {
                'active': True,
                'converging': False,
                'failed': bool(vol.failure)
            }
        }
        if vol.failure:
            status['message'] = vol.failure

        interfaces = {
            'info': {
                'signals': {
                    'volume-id': volid,
                    'color': vol.color
                }
            }
        }

        vol_infos[volid] = {
            'status': status,
            'interfaces': interfaces
        }
    else:
        # a volume is absent, set its status to destroyed
        vol_infos[volid] = {
            'status': {
                'flags': {
                    'active': False,
                    'converging': False,
                    'failed': False
                }
            }
        }

result = {
    'instances': vol_infos
}
yaml.safe_dump(result, sys.stdout)
