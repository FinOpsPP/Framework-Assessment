"""primary code for the finopspp CLI"""
import click

from finopspp.commands import utils
from finopspp.commands.info import group as info_group
from finopspp.commands.generate import group as generate_group
from finopspp.commands.specifications import group as specifications_group
from finopspp.commands.inventory import group as inventory_group
from finopspp.commands.variables import group as variables_group

@click.group(cls=utils.ClickGroup)
def cli():
    """FinOps++ administration tool"""

cli.add_command(info_group.info)
cli.add_command(generate_group.generate)
cli.add_command(specifications_group.specifications)
cli.add_command(inventory_group.inventory)
cli.add_command(variables_group.variables)

# include for those running script directly
# as a python module.
if __name__ == "__main__":
    cli()
