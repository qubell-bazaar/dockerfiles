#!/usr/bin/env python3

import sys
import yaml

import fvm
import fvol

from collections import defaultdict
from yaml.representer import SafeRepresenter

# to serialize defaultdicts normally
SafeRepresenter.add_representer(defaultdict, SafeRepresenter.represent_dict)

arguments = yaml.safe_load(sys.stdin)

vm_ids = list(arguments.get('instances', {}).keys())

def multidict():
    return defaultdict(multidict)

vm_infos = {}
for vmid in vm_ids:
    vm = fvm.load(vmid)
    if vm:
        status = {
            'flags': {
                'active': True,
                'converging': False,
                'failed': bool(vm.model.get('failure'))
            }
        }
        if 'failure' in vm.model:
            status['message'] = vm.model['failure']

        interfaces = {
            'info': {
                'signals': {
                    'vm-id': vmid
                }
            }
        }

        if 'address' in vm.model:
            interfaces['info']['signals']['address'] = vm.model['address']

        if 'login' in vm.model:
            interfaces['info']['signals']['login'] = vm.model['login']

        components = multidict()
        if 'volumes' in vm.model:
            for volid in vm.model['volumes']:
                vol = fvol.load(volid)
                color = vol.color if vol else 'unknown'
                components[color]['components'][volid] = {
                    'reference': {
                        'mapping': 'volumes.volume-by-id',
                        'key': volid
                    }
                }
        
        vm_infos[vmid] = {
            'status': status,
            'interfaces': interfaces,
            'components': components,
        }
    else:
        # a vm is absent, set its status to destroyed
        vm_infos[vmid] = {
            'status': {
                'flags': {
                    'active': False,
                    'converging': False,
                    'failed': False
                }
            }
        }

result = {
    'instances': vm_infos
}
yaml.safe_dump(result, sys.stdout)
