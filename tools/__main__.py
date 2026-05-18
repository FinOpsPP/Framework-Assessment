"""primary code for the finopspp CLI"""
import click

from finopspp.commands import utils
from finopspp.commands.version import group as version_group
from finopspp.commands.generate import group as generate_group
from finopspp.commands.specifications import group as specifications_group

@click.group(cls=utils.ClickGroup)
def cli():
    """FinOps++ administration tool"""

cli.add_command(version_group.version)
cli.add_command(generate_group.generate)
cli.add_command(specifications_group.specifications)

# include for those running script directly
# as a python module.
if __name__ == "__main__":
    cli()
