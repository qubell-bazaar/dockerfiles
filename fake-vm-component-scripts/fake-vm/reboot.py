#!/usr/bin/env python3

import sys
import yaml
import time

arguments = yaml.safe_load(sys.stdin)
instances = arguments.get('instances', {})
ids = list(instances.keys())

vm_infos = {}
for vmid in ids:
    commands = instances.get(vmid, {}).get('commands', {})
    commandids = list(commands.keys())
    updates = {}
    for commandid in commandids:
        command = commands.get(commandid, {})
        delay = command.get('control', {}).get('reboot', {}).get('delay', 0)
        time.sleep(delay)
        updates['commands.' + commandid] = [
                { '$intermediate': True, 'message': "Rebooting" },
                { 'message': "Done" }
        ]
    vm_infos[vmid] = {
        '$pushAll': updates
    }

result = {
    'instances': vm_infos
}
yaml.safe_dump(result, sys.stdout)
