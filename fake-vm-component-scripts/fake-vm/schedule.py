#!/usr/bin/env python3

import sys
import yaml
import time
import datetime

import fvm

arguments = yaml.safe_load(sys.stdin)
instances = arguments.get('instances', {})
ids = list(instances.keys())

for vmid in ids:
    if not fvm.exists(vmid):
        print("Fake VM {} does not exist".format(vmid), file=sys.stderr)
        sys.exit(1)

vm_infos = {}
for vmid in ids:
    vm = fvm.load(vmid)

    commands = instances.get(vmid, {}).get('commands', {})
    updates = {}
    for (command_id, command_data) in commands.items():
        schedule_args = command_data.get('control', {}).get('schedule', {})
        delay = schedule_args.get('delay', 1);
        task = schedule_args.get('task')
        if task:
            scheduled_instant = datetime.datetime.utcnow() + datetime.timedelta(seconds=delay)
            vm.model['tasks'] = vm.model.get('tasks', []) + [{
                'timestamp': scheduled_instant.timestamp(),
                'task': task
            }]
            fvm.save(vm)
            updates['commands.' + command_id] = [ {} ]
        else:
            updates['commands.' + command_id] = [
                { 'failure': 'Task argument not specified' }
            ]
    vm_infos[vmid] = {
        '$pushAll': updates
    }

result = {
    'instances': vm_infos
}
yaml.safe_dump(result, sys.stdout)
