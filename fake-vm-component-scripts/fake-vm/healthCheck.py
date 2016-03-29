#!/usr/bin/env python3

import sys
import yaml
import fvm

arguments = yaml.safe_load(sys.stdin)

ids = list(arguments.get('instances', {}).keys())

vm_infos = {}
for vmid in ids:
    vm = fvm.load_fake_vm(vmid)
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
                    'vmid': vmid,
                    'color': vm.color,
                }
            }
        }

        if 'address' in vm.model:
            interfaces['info']['signals']['address'] = vm.model['address']

        if 'login' in vm.model:
            interfaces['info']['signals']['login'] = vm.model['login']

        components = {}
        if 'links' in vm.model:
            for color, linked_fvms in vm.model['links'].items():
                # color will map to group name in the tree
                components[color] = {'children': {}}
                for linked_id in linked_fvms:
                    components[color]['children'] = {
                        linked_id: {  # linked_id will map to component name in the tree
                            'reference': {
                                'type': "{}-vms".format(color),
                                'id': linked_id
                            }
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
