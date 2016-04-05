#!/usr/bin/env python3

import yaml
import sys

import fvol

arguments = yaml.safe_load(sys.stdin)

volumes = []

for (volid, params) in arguments.get('instances', {}).items():
    vol = fvol.load(volid)
    if not vol:
        print("Fake Volume {} does not exist".format(volid), file=sys.stderr)
        sys.exit(1)

    # merge factory and instance configurations
    joined_config = dict(arguments.get('configuration', {}), **params.get('configuration', {}))
    color = joined_config.get('configuration.color')

    if not color:
        print("No color is specified for volume {}".format(volid), file=sys.stderr)
        sys.exit(1)

    vol.color = color

    volumes.append(vol)

for vol in volumes:
    fvol.save(vol)

def gen_interfaces(vol):
    return {
        'info': {
            'signals': {
                'volume-id': volid,
                'color': vol.color
            }
        }
    }

result = {
    'instances': {
        vol.volid: {
            # TODO: this should actually be done with $set, but it is not available now
            'interfaces': gen_interfaces(vol)
        } for vol in volumes
    }
}

yaml.safe_dump(result, sys.stdout)

