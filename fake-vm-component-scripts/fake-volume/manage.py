#!/usr/bin/env python3

import click
import yaml
import sys

import fvol

# manage.py list [ --with-names ]
# manage.py show <ID>
# manage.py create --color <CUSTOM COLOR>
#                  [ --id <CUSTOM ID> ]
#                  [ --name <CUSTOM NAME> ]
#                  [ --failure <CUSTOM FAILURE MESSAGE> ]
# manage.py modify <ID> [ --name <NEW NAME> ]
#                       [ --color <NEW COLOR> ]
#                       [ --failure <NEW FAILURE MESSAGE> | --no-failure ]
# manage.py delete <ID>

@click.group()
def cli():
    pass

@cli.command()
@click.option('--with-names', is_flag=True)
def list(with_names):
    vols = fvol.load_all()
    if with_names:
        for vol in vols:
            print("{} ({}, {})".format(vol.volid, vol.name, vol.color))
    else:
        for vol in vols:
            print("{} ({})".format(vol.volid, vol.color))

@cli.command()
@click.argument('id')
def show(id):
    vol = fvol.load(id)

    if not vol:
        print('Fake Volume {} does not exist'.format(id), file=sys.stderr)
        sys.exit(1)

    model = {
        'id': vol.volid,
        'color': vol.color,
    }
    if vol.name:
        model['name'] = vol.name
    if vol.failure:
        model['failure'] = vol.failure

    yaml.safe_dump(model, sys.stdout, default_flow_style=False)

@cli.command()
@click.option('--id', type=str)
@click.option('--name', type=str)
@click.option('--color', type=str, required=True)
@click.option('--failure', type=str)
def create(id, name, color, failure):
    if id and fvol.exists(id):
        print('Fake Volume {} already exists'.format(id), file=sys.stderr)
        sys.exit(1)

    vol = fvol.FakeVolume(id, name, color, failure)
    fvol.save(vol)
    
    print('Successfully created a new Fake Volume {}'.format(vol.volid))

@cli.command()
@click.argument('id')
@click.option('--name', type=str)
@click.option('--color', type=str)
@click.option('--failure', type=str)
@click.option('--no-failure', is_flag=True)
def modify(id, name, color, failure, no_failure):
    vol = fvol.load(id)

    if not vol:
        print('Fake Volume {} does not exist'.format(id), file=sys.stderr)
        sys.exit(1)

    if name: vol.name = name
    if color: vol.color = color
    if failure: vol.failure = failure
    if no_failure: vol.failure = None

    fvol.save(vol)

    print('Fake Volume {} has been successfully updated'.format(id))

@cli.command()
@click.argument('id')
def delete(id):
    if not fvol.exists(id):
        print('Fake Volume {} does not exist'.format(id), file=sys.stderr)
        sys.exit(1)

    fvol.delete(id)

    print('Fake Volume {} has been successfully deleted'.format(id))

if __name__=="__main__":
    cli()
