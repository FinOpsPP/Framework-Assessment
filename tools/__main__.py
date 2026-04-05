"""primary code for the finopspp CLI"""
import click

from finopspp.commands import (
    generate,
    specifications,
    utils,
    version
)

@click.group(cls=utils.ClickGroup)
def cli():
    """FinOps++ administration tool"""

cli.add_command(version.version)
cli.add_command(generate.generate)
cli.add_command(specifications.specifications)

# include for those running script directly
# as a python module.
if __name__ == "__main__":
    cli()
