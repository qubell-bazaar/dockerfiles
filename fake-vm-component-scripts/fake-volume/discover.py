#!/usr/bin/env python3

import sys
import yaml

import fvol

vols = fvol.load_all()

arguments = yaml.safe_load(sys.stdin)
color = (arguments or {}).get('configuration', {}).get('configuration.color')

if color:
    vols = [vol for vol in vols if vol.color == color]

def get_model(vol):
    if vol.name:
        return {
            'name': vol.name,
            'interfaces': {
                'info': {
                    'signals': {
                        'volume-id': vol.volid,
                        'color': vol.color,
                    }
                }
            }
        }
    else:
        return {}

result = {
    'instances': { vol.volid: get_model(vol) for vol in vols }
}
yaml.safe_dump(result, sys.stdout)
