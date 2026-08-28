"""Command file for the Variables command"""
import os
import sys
import tomllib
from importlib.resources import files

import click
import yaml
from jinja2 import Environment, PackageLoader
from pydantic import ValidationError

from finopspp.models.variables import Variables
from finopspp.models.specs import StatusEnum
from finopspp.commands import utils
from finopspp.commands.generate import helpers as generate_helpers

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
    """Create a new variables file for a profile
    
    NOTE: The name you pass in can have space by surrounding 
    your name in quotes. But if you use space, they will be
    ignored in the file name itself.

    NOTE: This will include components of any status type that
    are specified. Even if a downstream assessment does not use
    a specific status.
    """
    path = files(
        'finopspp.specifications.variables'
    ).joinpath(f'{name.replace(" ", "")}.fppvars.toml')
    click.echo(f'Attempting to create "{path}" for profile={profile}:')

    if os.path.exists(path) and not force:
        click.secho(f'Variables file for "{path}" already exists. Existing', err=True, fg='red')
        sys.exit(1)

    with open(utils.ProfilesMap[profile], 'r', encoding='utf-8') as yaml_file:
        prof = yaml.safe_load(yaml_file)
        prof['actions'] = []


    domain_files = files('finopspp.specifications.domains')
    capability_files = files('finopspp.specifications.capabilities')
    action_files = files('finopspp.specifications.actions')

    allowed_statuses = [
        StatusEnum.accepted.value,
        StatusEnum.proposed.value,
        StatusEnum.deprecated.value
    ]

    for domain in prof.get('Specification').get('Domains'):
        _, spec = generate_helpers.domain_collector(
            profile,
            domain,
            domain_files,
            allowed_statuses
        )
        if not spec:
            continue

        domain_id = spec.get('ID', spec.get('Title'))
        if not domain_id:
            continue

        domain_drops = spec['domain_drops']
        for capability in spec.get('Capabilities'):
            _, spec = generate_helpers.capability_collector(
                profile,
                capability,
                capability_files,
                domain_drops,
                allowed_statuses
            )
            if not spec:
                continue

            capability_id = spec.get('ID', spec.get('Title'))
            if not capability_id:
                continue

            capability_drops = spec['capability_drops']
            for action in spec.get('Actions'):
                _, spec = generate_helpers.action_collector(
                    profile,
                    action,
                    action_files,
                    capability_drops,
                    allowed_statuses
                )
                if not spec:
                    continue

                action_id = spec.get('ID')
                if not action_id:
                    continue

                action_weight = spec['Weight']
                action_id = spec.get('Slug') or action_id
                unique_id = f'{domain_id}.{capability_id}.{action_id}'.replace(' ', '')

                prof['actions'].append({
                    'fqid': unique_id,
                    'weight': action_weight
                })

    # pull in template and specification files for given specification type
    env = Environment(loader=Templates, keep_trailing_newline=True)
    template = env.get_template('fppvars.toml.j2')

    output = template.render(
        name=name,
        profile=prof
    )

    # finally, write README.md for the schemas
    # from the rendered output
    with open(path, 'w', encoding='utf-8') as outfile:
        outfile.write(output)

    click.secho(f'Attempt to create "{path}" succeeded', fg='green')


@variables.command(name='list')
def list_variables():
    """List all registered variables files

    List is in the form of Name-Profile (minus spaces) for each
    saved variable files TOML file under finopspp.specifications.variables
    """
    click.echo('Variable IDs:')
    spec_files = files('finopspp.specifications.variables')
    for file in spec_files.iterdir():
        # only include toml files
        if not file.name.endswith('.toml'):
            continue

        path = spec_files.joinpath(file.name)
        with open(path, 'rb') as toml_file:
            var_file = tomllib.load(toml_file)
            name = var_file.get('basic').get('name').replace(' ', '')
            title = var_file.get('profile').get('title').replace(' ', '')

        click.echo(f'{name}-{title}')


@variables.command()
def validate():
    """Validate all variable files"""
    model = Variables
    specs_files = files('finopspp.specifications.variables')

    failed = False
    for spec in specs_files.iterdir():
        path = specs_files.joinpath(spec.name)
        click.echo(f'Validating "{path}":')
        with open(path, 'rb') as toml_file:
            specification_data = tomllib.load(toml_file)

        try:
            model.model_validate(specification_data)
        except ValidationError as val_error:
            failed = True
            click.secho(
                f'Validation for "{path}" failed with --\n', fg='yellow'
            )
            click.secho(str(val_error) + '\n', err=True, fg='red')
        else:
            click.secho(
                f'Validation for "{path}" passed', fg='green'
            )

    if failed:
        sys.exit(1)
