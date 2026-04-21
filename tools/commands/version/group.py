"""Command file for the Version command"""
import platform
import sys
from importlib.metadata import metadata as meta

import click

@click.command()
def version():
    """Version and runtime information about the finopspp tool"""
    tool_version = meta('finopspp').get('Version', '0.0.0')
    click.echo(f'Version: {tool_version}')
    python_version = sys.version.split(' ', maxsplit=1).pop(0)
    click.echo(f'Python Version: {python_version}')
    click.echo(f'System: {platform.system()} ({platform.release()})')
