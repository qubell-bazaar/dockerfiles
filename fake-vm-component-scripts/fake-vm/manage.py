#!/usr/bin/env python3

import click
import fvm
import yaml
import sys

# manage.py list
# manage.py show <ID>
# manage.py create --color <CUSTOM COLOR>
#                  [ --id <CUSTOM ID> ]
#                  [ --name <CUSTOM NAME> ]
#                  [ --address <CUSTOM ADDRESS> ]
#                  [ --login <CUSTOM LOGIN ]
#                  [ --failure <FAILURE MESSAGE> ]
#                  [ --link <color>:<id> ]*
# manage.py modify <ID> [ --name <NEW NAME> ]
#                       [ --address <NEW ADDRESS> ]
#                       [ --login <NEW LOGIN> ]
#                       [ --color <NEW COLOR> ]
#                       [ --failure <NEW FAILURE MESSAGE> | --no-failure ]
#                       [ --link <color>:<id> ]*
#                       [ --unlink <color>:<id> ]*
# manage.py delete <ID>

@click.group()
def cli():
    pass

@cli.command()
@click.option('--with-names', is_flag=True)
def list(with_names):
    vms = fvm.load_fake_vms()
    if with_names:
        for vm in vms:
            print("{} ({}), {}".format(vm.vmid, vm.name, vm.color))
    else:
        for vm in vms:
            print("{}, {}".format(vm.vmid, vm.color))

@cli.command()
@click.argument('id')
def show(id):
    vm = fvm.load_fake_vm(id)

    if not vm:
        print('Fake VM {} does not exist'.format(id), file=sys.stderr)
        sys.exit(1)

    model = {}
    model['id'] = id
    model.update(vm.model)

    yaml.safe_dump(model, sys.stdout, default_flow_style=False)

def parse_links(ctx, param, value):
    try:
        result = []
        for item in value:
            color, id = item.split(':', 2)
            result.append((color, id))
        return tuple(result)
    except ValueError:
        raise click.BadParameter('links must have "<color>:<vmid>" format')

@cli.command()
@click.option('--id', type=str)
@click.option('--name', type=str)
@click.option('--color', type=str, required=True)
@click.option('--address', type=str)
@click.option('--login', type=str)
@click.option('--failure', type=str)
@click.option('--link', multiple=True, callback=parse_links)
def create(id, name, color, address, login, failure, link):
    id = id or fvm.generate_id()

    if fvm.fake_vm_exists(id):
        print('Fake VM {} already exists'.format(id), file=sys.stderr)
        sys.exit(1)

    model = {'color': color}
    if name: model['name'] = name
    if address: model['address'] = address
    if login: model['login'] = login
    if failure: model['failure'] = failure
    if link:
        model['links'] = {}
        for (color, vmid) in link:
            color_links = model['links'].get(color, set())
            color_links.add(vmid)
            model['links'][color] = color_links

    vm = fvm.FakeVm(id, model)
    fvm.save_fake_vm(vm)
    
    print('Successfully created a new Fake VM {}'.format(id))

@cli.command()
@click.argument('id')
@click.option('--name', type=str)
@click.option('--color', type=str)
@click.option('--address', type=str)
@click.option('--login', type=str)
@click.option('--failure', type=str)
@click.option('--no-failure', is_flag=True)
@click.option('--link', multiple=True, callback=parse_links)
@click.option('--unlink', multiple=True, callback=parse_links)
def modify(id, name, color, address, login, failure, no_failure, link, unlink):
    vm = fvm.load_fake_vm(id)

    if not vm:
        print('Fake VM {} does not exist'.format(id), file=sys.stderr)
        sys.exit(1)

    if name: vm.name = name
    if color: vm.color = color
    if address: vm.model['address'] = address
    if login: vm.model['login'] = login
    if failure: vm.model['failure'] = failure
    if no_failure and 'failure' in vm.model: del vm.model['failure']
    if link or unlink:
        links = vm.model.get('links', {})
        for (color, vmid) in link:
            color_links = links.get(color, set())
            color_links.add(vmid)
            links[color] = color_links
        for (color, vmid) in unlink:
            color_links = links.get(color, set())
            color_links.discard(vmid)
            if color_links:
                links[color] = color_links
            elif color in links:
                del links[color]
        if links:
            vm.model['links'] = links
        elif 'links' in vm.model:
            del vm.model['links']

    fvm.save_fake_vm(vm)

    print('Fake VM {} has been successfully updated'.format(id))

@cli.command()
@click.argument('id')
def delete(id):
    if not fvm.fake_vm_exists(id):
        print('Fake VM {} does not exist'.format(id), file=sys.stderr)
        sys.exit(1)

    fvm.destroy_fake_vm(id)

    print('Fake VM {} has been successfully destroyed'.format(id))

if __name__=="__main__":
    cli()
