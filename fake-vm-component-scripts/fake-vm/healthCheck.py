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
                    'vmid': vmid
                }
            }
        }

        if 'address' in vm.model:
            interfaces['info']['signals']['address'] = vm.model['address']

        if 'login' in vm.model:
            interfaces['info']['signals']['login'] = vm.model['login']
        
        vm_infos[vmid] = {
            'status': status,
            'interfaces': interfaces
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
