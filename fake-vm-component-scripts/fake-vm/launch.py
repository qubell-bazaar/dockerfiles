#!/usr/bin/env python3

import yaml
import sys

import fvm

arguments = yaml.safe_load(sys.stdin)

instances = []

for (instance_id, params) in arguments.get('launch-instances', {}).items():
    # merge factory and instance configurations
    joined_config = dict(arguments.get('configuration', {}), **params.get('configuration', {}))
    login = joined_config.get('configuration.login')

    model = {}
    if login: model['login'] = login

    instances.append((fvm.FakeVm(None, model), instance_id))

for (vm, instance_id) in instances:
    fvm.save(vm)

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

