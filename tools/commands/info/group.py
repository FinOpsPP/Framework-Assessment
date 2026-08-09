"""Command file for the Version command"""
import platform
import sys
from importlib.metadata import metadata as meta

import click

from finopspp.commands import utils


@click.group(cls=utils.ClickGroup)
def info():
    """Provide basic information about regarding the finopspp tool"""


@info.command()
def version():
    """Show the current version of the finopspp tool"""
    tool_version = meta('finopspp').get('Version', '0.0.0')
    click.echo(f'Version: {tool_version}')


@info.command()
def runtime():
    """Show runtime environment of the finopspp tool"""
    python_version = sys.version.split(' ', maxsplit=1).pop(0)
    click.echo(f'Python Version: {python_version}')
    click.echo(f'System: {platform.system()} ({platform.release()})')


@info.command()
@click.pass_context
def full(ctx):
    """Show all information together"""
    ctx.invoke(version)
    ctx.invoke(runtime)
