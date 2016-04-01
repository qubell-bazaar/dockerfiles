#!/usr/bin/env python3

import sys
import yaml

import fvm

vms = fvm.load_all()

def get_model(vm):
    if vm.name:
        return {
            'name': vm.name,
            'interfaces': {
                'info': {
                    'signals': {
                        'vm-id': vm.vmid
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
