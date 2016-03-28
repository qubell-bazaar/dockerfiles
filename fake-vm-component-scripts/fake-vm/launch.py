#!/usr/bin/env python3

import yaml
import sys
import uuid

import fvm

arguments = yaml.safe_load(sys.stdin)

instances = []

def fix_config_keys(source):
    for k, v in source:
        yield (k, v) if '.' not in k else (k.split('.')[1], v)

for (instance_id, params) in arguments.get('launch-instances', {}).items():
    model = {}

    vmid = fvm.generate_id()  # generate a fresh id

    # merge default configuration
    model.update(fix_config_keys(arguments.get('configuration', {}).items()))

    # merge instance configuration
    model.update(fix_config_keys(params.get('configuration', {}).items()))

    instances.append((fvm.FakeVm(vmid, model), instance_id))

for (vm, instance_id) in instances:
    fvm.save_fake_vm(vm)

result = {
    'instances': {
        vm.vmid: {
            'instanceId': instance_id,  # pass instance for correlation
            'status': {
                'flags': {'active': True, 'converging': False, 'failed': False}
            }
        } for (vm, instance_id) in instances
    }
}

yaml.safe_dump(result, sys.stdout)

