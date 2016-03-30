#!/usr/bin/env python3

import click
import fvm
import yaml
import sys

# manage.py list
# manage.py show <ID>
# manage.py create [ --id <CUSTOM ID> ]
#                  [ --name <CUSTOM NAME> ]
#                  [ --address <CUSTOM ADDRESS> ]
#                  [ --login <CUSTOM LOGIN> ]
#                  [ --failure <FAILURE MESSAGE> ]
#                  [ --link-volume <VOLUME ID> ]*
# manage.py modify <ID> [ --name <NEW NAME> ]
#                       [ --address <NEW ADDRESS> ]
#                       [ --login <NEW LOGIN> ]
#                       [ --failure <NEW FAILURE MESSAGE> | --no-failure ]
#                       [ --link-volume <VOLUME ID> ]*
#                       [ --unlink-volume <VOLUME ID> ]*
# manage.py delete <ID>

@click.group()
def cli():
    pass

@cli.command()
@click.option('--with-names', is_flag=True)
def list(with_names):
    if with_names:
        vms = fvm.load_all()
        for vm in vms:
            print("{} ({})".format(vm.vmid, vm.name))
    else:
        ids = fvm.load_ids()
        for id in ids:
            print(id)

@cli.command()
@click.argument('id')
def show(id):
    vm = fvm.load(id)

    if not vm:
        print('Fake VM {} does not exist'.format(id), file=sys.stderr)
        sys.exit(1)

    model = {}
    model['id'] = id
    model.update(vm.model)

    yaml.safe_dump(model, sys.stdout, default_flow_style=False)

@cli.command()
@click.option('--id', type=str)
@click.option('--name', type=str)
@click.option('--address', type=str)
@click.option('--login', type=str)
@click.option('--failure', type=str)
@click.option('--link-volume', type=str, multiple=True)
def create(id, name, address, login, failure, link_volume):
    if id and fvm.exists(id):
        print('Fake VM {} already exists'.format(id), file=sys.stderr)
        sys.exit(1)

    model = {}
    if name: model['name'] = name
    if address: model['address'] = address
    if login: model['login'] = login
    if failure: model['failure'] = failure
    if link_volume: model['volumes'] = set(link_volume)

    vm = fvm.FakeVm(id, model)
    fvm.save(vm)
    
    print('Successfully created a new Fake VM {}'.format(vm.vmid))

@cli.command()
@click.argument('id')
@click.option('--name', type=str)
@click.option('--address', type=str)
@click.option('--login', type=str)
@click.option('--failure', type=str)
@click.option('--no-failure', is_flag=True)
@click.option('--link-volume', type=str, multiple=True)
@click.option('--unlink-volume', type=str, multiple=True)
def modify(id, name, address, login, failure, no_failure, link_volume, unlink_volume):
    vm = fvm.load(id)

    if not vm:
        print('Fake VM {} does not exist'.format(id), file=sys.stderr)
        sys.exit(1)

    if name: vm.model['name'] = name
    if address: vm.model['address'] = address
    if login: vm.model['login'] = login
    if failure: vm.model['failure'] = failure
    if no_failure and 'failure' in vm.model: del vm.model['failure']

    if link_volume:
        volumes = vm.model.get('volumes', set())
        volumes.update(link_volume)
        vm.model['volumes'] = volumes

    if unlink_volume and 'volumes' in vm.model:
        for volume in unlink_volume:
            vm.model['volumes'].discard(volume)
        if not vm.model['volumes']:
            del vm.model['volumes']

    fvm.save(vm)

    print('Fake VM {} has been successfully updated'.format(id))

@cli.command()
@click.argument('id')
def delete(id):
    if not fvm.exists(id):
        print('Fake VM {} does not exist'.format(id), file=sys.stderr)
        sys.exit(1)

    fvm.delete(id)

    print('Fake VM {} has been successfully deleted'.format(id))

if __name__=="__main__":
    cli()
