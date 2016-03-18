#!/usr/bin/env python3

import sys
import yaml
import fvm

vms = fvm.load_fake_vms()

def get_model(vm):
    if vm.name:
        return {
            'name': vm.name,
            'interfaces': {
                'info': {
                    'signals': {
                        'vmid': vm.vmid
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
