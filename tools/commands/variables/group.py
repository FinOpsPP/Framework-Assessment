"""Command file for the Variables command"""
import os
import sys
from importlib.resources import files

import click
import yaml
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
@click.option(
    '--force',
    is_flag=True,
    default=False,
    help='Force the creation of a variable file, potentially overwriting an existing one'
)
@click.argument('name', type=click.STRING)
def new(name, profile, force):
    """Create a new variables file for a profile"""
    path = files(
        'finopspp.specifications.profiles'
    ).joinpath(f'{name}.fppvars.toml')
    click.echo(f'Attempting to create "{path}" for profile={profile}:')

    if os.path.exists(path) and not force:
        click.secho(f'Variables file for "{path}" already exists. Existing', err=True, fg='red')
        sys.exit(1)

    with open(utils.ProfilesMap[profile], 'r', encoding='utf-8') as yaml_file:
        prof = yaml.safe_load(
            yaml_file
        )
        prof['actions'] = []


    domain_files = files('finopspp.specifications.domains')
    capability_files = files('finopspp.specifications.capabilities')
    action_files = files('finopspp.specifications.actions')

    domains = prof.get('Specification').get('Domains')
    for domain in domains:
        domain_id = domain.get('ID', domain.get('Title'))
        if not domain_id:
            continue

        # If a domain ID is include, look it up as a file
        # else take whatever exists on that domain should
        # a title exist
        capabilities = domain.get('Capabilities') or []
        if isinstance(domain_id, int):
            domain_id = str(domain_id)
            file = '0'*(3-len(domain_id)) + domain_id
            with open(domain_files.joinpath(f'{file}.yaml'), 'r', encoding='utf-8') as yaml_file:
                capabilities = yaml.safe_load(
                    yaml_file
                ).get('Specification').get('Capabilities')

        for capability in capabilities:
            capability_id = capability.get('ID', capability.get('Title'))
            if not capability_id:
                continue

            # If a capability ID is include, look it up as a file
            # else take whatever exists on that capability should
            # a title exist
            actions = capability.get('Actions') or []
            if isinstance(capability_id, int):
                capability_id = str(capability_id)
                file = '0'*(3-len(capability_id)) + capability_id
                with open(capability_files.joinpath(f'{file}.yaml'), 'r', encoding='utf-8') as yaml_file:
                    actions = yaml.safe_load(
                        yaml_file
                    ).get('Specification').get('Actions')

            for action in actions:
                action_id = action.get('ID')
                if not action_id:
                    continue

                action_id = str(action_id)
                file = '0'*(3-len(action_id)) + action_id
                with open(action_files.joinpath(f'{file}.yaml'), 'r', encoding='utf-8') as yaml_file:
                    raw_action = yaml.safe_load(
                        yaml_file
                    )

                action_weight = raw_action['Specification']['Weight']
                action_id = raw_action['Specification'].get('Slug') or action_id
                unique_id = f'{domain_id}.{capability_id}.{action_id}'.replace(' ', '')

                prof['actions'].append({
                    'fqid': unique_id,
                    'weight': action_weight
                })

    # pull in template and specification files for given specification type
    env = Environment(loader=Templates, keep_trailing_newline=True)
    template = env.get_template('fppvars.toml.j2')

    output = template.render(
        profile=prof
    )

    # finally, write README.md for the schemas
    # from the rendered output
    with open(path, 'w', encoding='utf-8') as outfile:
        outfile.write(output)

    click.secho(f'Attempt to create "{path}" succeeded', fg='green')
