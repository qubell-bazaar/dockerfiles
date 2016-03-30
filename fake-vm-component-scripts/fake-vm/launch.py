#!/usr/bin/env python3

import yaml
import sys
import uuid

import fvm

arguments = yaml.safe_load(sys.stdin)

instances = []

config_keys = {
    k: k.split('.')[1] for k in {
        'configuration.name',
        'configuration.address',
        'configuration.login',
        'configuration.failure',
    }
}

for (instance_id, params) in arguments.get('launch-instances', {}).items():
    model = {}

    # merge factory and instance configurations
    joined_config = dict(arguments.get('configuration', {}), **params.get('configuration'))
    final_config = {
        config_keys[k]: v for k, v in joined_config.items() if k in config_keys
    }

    model.update(final_config)

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

