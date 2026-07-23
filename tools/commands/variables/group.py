"""Command file for the Variables command"""
import os
import sys
from importlib.resources import files

import click
from jinja2 import Environment, PackageLoader

from finopspp.commands import utils

Templates = PackageLoader('finopspp', 'templates')

@click.group(cls=utils.ClickGroup)
def variables():
    """Do operations on FinOps++ Variable files"""


@variables.command()
@click.option(
    '--profile',
    default='FinOps++',
    type=click.Choice(list(utils.profiles().keys())),
    help='Which assessment profile to list. Takes preference over specification type'
)
@click.argument('name', type=click.STRING)
def new(name, profile):
    """Create a new variables file for a profile"""
    path = files(
        f'finopspp.specifications.profiles.{profile}'
    ).joinpath(f'{name}.fppvars.toml')
    click.echo(f'Attempting to create "{path}" for profile={profile}:')

    if os.path.exists(path):
        click.secho(f'Variables file for "{path}" already exists. Existing', err=True, fg='red')
        sys.exit(1)

    # pull in template and specification files for given specification type
    env = Environment(loader=Templates, keep_trailing_newline=True)
    template = env.get_template('fppvars.toml.j2')

    template.render()
