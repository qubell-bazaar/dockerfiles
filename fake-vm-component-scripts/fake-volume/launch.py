#!/usr/bin/env python3

import yaml
import sys

import fvol

arguments = yaml.safe_load(sys.stdin)

instances = []

for (instance_id, params) in arguments.get('launch-instances', {}).items():
    # merge factory and instance configurations
    joined_config = dict(arguments.get('configuration', {}), **params.get('configuration', {}))
    color = joined_config.get('configuration.color')

    if not color:
        print("No color is specified for volume {}".format(instance_id), file=sys.stderr)
        sys.exit(1)

    instances.append((fvol.FakeVolume(None, None, color), instance_id))

for (vol, instance_id) in instances:
    fvol.save(vol)

result = {
    'instances': {
        vol.volid: {
            'instanceId': instance_id,  # pass instance for correlation
            'status': {
                'flags': {'active': True, 'converging': False, 'failed': False}
            }
        } for (vol, instance_id) in instances
    }
}

yaml.safe_dump(result, sys.stdout)

