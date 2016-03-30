#!/usr/bin/env python3

import yaml
import sys

import fvol

arguments = yaml.safe_load(sys.stdin)

instances = []

for (instance_id, params) in arguments.get('launch-instances', {}).items():
    joined_config = dict(params.get('configuration', {}), **arguments.get('configuration', {}))
    name = joined_config.get('configuration.name')
    color = joined_config.get('configuration.color')

    if not color:
        print("No color is specified for volume {}".format(instance_id), file=sys.stderr)
        sys.exit(1)

    volid = fvol.generate_id()  # generate a fresh id

    instances.append((fvol.FakeVolume(volid, name, color), instance_id))

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

