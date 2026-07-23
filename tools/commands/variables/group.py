"""Command file for the Variables command"""
import click

from finopspp.commands import utils

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
    click.echo(f'Creating new {name}.fppvars.ini file under profile {profile}')
