#!/usr/bin/env python3

import yaml
import sys

import fvm

arguments = yaml.safe_load(sys.stdin)

vms = []

for (vmid, params) in arguments.get('instances', {}).items():
    vm = fvm.load(vmid)
    if not vm:
        print("Fake VM {} does not exist".format(vmid), file=sys.stderr)
        sys.exit(1)

    # merge factory and instance configurations
    joined_config = dict(arguments.get('configuration', {}), **params.get('configuration', {}))
    login = joined_config.get('configuration.login')

    if login:
        vm.model['login'] = login
    elif 'login' in vm.model:
        del vm.model['login']

    vms.append(vm)

for vm in vms:
    fvm.save(vm)

def gen_interfaces(vm):
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
    
    return interfaces

result = {
    'instances': {
        vm.vmid: {
            # TODO: this should actually be done with $set, but it is not available now
            'interfaces': gen_interfaces(vm)
        } for vm in vms
    }
}

yaml.safe_dump(result, sys.stdout)

