#!/usr/bin/env python3

import sys
import yaml
import fvm

arguments = yaml.safe_load(sys.stdin)

color = (arguments or {}).get('configuration', {}).get('configuration.color')

vms = fvm.load_fake_vms()

if color:
    vms = [vm for vm in vms if vm.color == color]

def get_model(vm):
    if vm.name:
        return {
            'name': vm.name,
            'interfaces': {
                'info': {
                    'signals': {
                        'vmid': vm.vmid,
                        'color': vm.color,
                    }
                }
            }
        }
    else:
        return {}

result = {
    'instances': { vm.vmid: get_model(vm) for vm in vms }
}
yaml.safe_dump(result, sys.stdout)
