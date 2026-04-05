"""Command file for all Specification group commands"""
import datetime
import json
import os
import sys
from collections import namedtuple
from importlib.resources import files

import click
import semver
import yaml
from pydantic import TypeAdapter, ValidationError
from rich.console import Console
from rich.syntax import Syntax

from finopspp.models import definitions, defaults
from finopspp.commands import utils


# if MANPAGER is set to something odd, it will break the pager
# user by rich.console. So remove this if it is found and take
# what ever the system default is to try and help. If the pager
# is still broken at this point, the user might need to make
# changes.
# largely from https://github.com/Textualize/rich/issues/1688#issuecomment-997479763
os.environ.pop('MANPAGER', None)

@click.group(cls=utils.ClickGroup)
def specifications():
    """Informational command on Specifications"""


@specifications.command()
@click.option(
    '--specification-type',
    type=click.Choice(list(utils.SpecSubspecMap.keys())),
    default='profiles',
    help='Which specification type to use. Defaults to "profiles"'
)
@click.argument('id_', metavar='<spec ID>', type=click.IntRange(1, 999))
def new(id_, specification_type):
    """Create a new specification for a new ID

    It is required that the ID be new itself for a given specification.
    The command will fail otherwise.
    """
    spec_id = str(id_)
    file = '0'*(3-len(spec_id)) + spec_id
    path = files(
        f'finopspp.specifications.{specification_type}'
    ).joinpath(f'{file}.yaml')
    click.echo(f'Attempting to create "{path}" for specification-type={specification_type}:')

    if os.path.exists(path):
        click.secho(f'Specification "{path}" already exists. Existing', err=True, fg='red')
        sys.exit(1)

    data = None
    match specification_type:
        case 'actions':
            data = json.loads(defaults.Action.model_dump_json())
        case 'capabilities':
            data = json.loads(defaults.Capability.model_dump_json())
        case 'domains':
            data = json.loads(defaults.Domain.model_dump_json())
        case 'profiles':
            data = json.loads(defaults.Profile.model_dump_json())

    data['Specification']['ID'] = id_
    with open(path, 'w', encoding='utf-8') as file:
        yaml.dump(
            data,
            file,
            default_flow_style=False,
            sort_keys=False,
            indent=2
        )

    click.secho(f'Specification "{path}" successfully created', fg='green')


@specifications.command(name='list')
@click.option(
    '--show-action-status',
    is_flag=True,
    help='Show status of action'
)
@click.option(
    '--status-by',
    default=None,
    type=click.Choice([enum.value for enum in definitions.StatusEnum] + [None]),
    help='Filter by status. Defaults to "None"'
)
@click.option(
    '--profile',
    default='FinOps++',
    type=click.Choice(list(utils.profiles().keys())),
    help='Which assessment profile to list. Defaults to "FinOps++"'
)
def list_specs(show_action_status, status_by, profile):
    """List all Specifications by fully qualified ID per profile
    
    Fully qualified ID is of the format Domain.Capability-Action"""
    with open(utils.ProfilesMap[profile], 'r', encoding='utf-8') as yaml_file:
        spec = yaml.safe_load(
            yaml_file
        ).get('Specification')
        domains = spec.get('Domains')
        profile_id = spec.get('ID')

    domain_files = files('finopspp.specifications.domains')
    capability_files = files('finopspp.specifications.capabilities')
    action_files = files('finopspp.specifications.actions')
    click.echo(f'Fully qualified IDs for {profile}. Profile ID: {profile_id}')
    for domain in domains:
        domain_id = domain.get('ID')
        if not domain_id:
            continue

        domain_id = str(domain_id)
        file = '0'*(3-len(domain_id)) + domain_id
        with open(domain_files.joinpath(f'{file}.yaml'), 'r', encoding='utf-8') as yaml_file:
            capabilities = yaml.safe_load(
                yaml_file
            ).get('Specification').get('Capabilities')

        for capability in capabilities:
            capability_id = capability.get('ID')
            if not capability_id:
                continue

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

                action_status = raw_action['Metadata']['Status']
                if status_by and status_by != action_status:
                    continue

                action_id = raw_action['Specification'].get('Slug') or action_id
                unique_id = f'{domain_id}.{capability_id}.{action_id}'
                if show_action_status:
                    unique_id += f': (Action {action_status})'
                click.echo(unique_id)


@specifications.command()
@click.option(
    '--metadata',
    is_flag=True,
    help='Show the Metadata for a Specifications'
)
@click.option(
    '--specification-type',
    type=click.Choice(list(utils.SpecSubspecMap.keys())),
    default='profiles',
    help='Which specification type to show. Defaults to "profiles"'
)
@click.argument('id_', metavar='<spec ID>', type=click.IntRange(1, 999))
def show(id_, metadata, specification_type):
    """Show information on a given specification by ID by type
    
    Information is shown in a Pager, if one is available
    """
    data_type = 'Specification'
    if metadata:
        data_type = 'Metadata'

    spec_id = str(id_)
    file = '0'*(3-len(spec_id)) + spec_id
    path = files(
        f'finopspp.specifications.{specification_type}'
    ).joinpath(f'{file}.yaml')

    if not os.path.exists(path):
        click.secho(f'Specification "{path}" does not exists. Existing', err=True, fg='red')
        sys.exit(1)

    specification_data = None
    with open(path, 'r', encoding='utf-8') as file:
        specification_data = yaml.safe_load(file)

    console = Console()
    syntax = Syntax(
        yaml.dump(
            specification_data[data_type],
            default_flow_style=False,
            sort_keys=False,
            indent=2
        ),
        'yaml'
    )
    with console.pager(styles=True):
        console.print(syntax)


@specifications.command()
@click.option(
    '--specification-type',
    type=click.Choice(list(utils.SpecSubspecMap.keys())),
    default='profiles',
    help='Which schema specification type to show. Defaults to "profiles"'
)
def schema(specification_type):
    """Give schema (in YAML format) for a given specification type
    
    The schema is based on the pydantic version of the JSON and OpenAPI
    Schemas. For more info on this type of schema specification, please view:
    https://docs.pydantic.dev/latest/concepts/json_schema/

    Schemas are shown in a Pager, if one is available.
    """
    spec_schema = None
    match specification_type:
        case 'actions':
            spec_schema = TypeAdapter(definitions.Action).json_schema(mode='serialization')
        case 'capabilities':
            spec_schema = TypeAdapter(definitions.Capability).json_schema(mode='serialization')
        case 'domains':
            spec_schema = TypeAdapter(definitions.Domain).json_schema(mode='serialization')
        case 'profiles':
            spec_schema = TypeAdapter(definitions.Profile).json_schema(mode='serialization')

    console = Console()
    syntax = Syntax(
        yaml.dump(
            spec_schema,
            default_flow_style=False,
            sort_keys=False,
            indent=2
        ),
        'yaml'
    )
    with console.pager(styles=True):
        console.print(syntax)


class AllOrIntRangeParamType(click.ParamType):
    """Class to deal with selection valid specification IDs"""
    name = 'All or ID'

    def get_metavar(self, param, ctx):
        return f'{param.name.upper()} [all|1-999]'

    def convert(self, value, param, ctx):
        try:
            if value == 'all':
                return value

            return str(click.IntRange(1, 999).convert(value, param, ctx))
        except click.BadParameter:
            self.fail(f"'{value}' must be \"all\" or an int between 1-999")

@specifications.command()
@click.option(
    '--specification-type',
    type=click.Choice(list(utils.SpecSubspecMap.keys())),
    default='profiles',
    help='Which specification type to show. Defaults to "profiles"'
)
@click.argument('selection', type=AllOrIntRangeParamType())
def validate(selection, specification_type):
    """Validate all or a specific specification ID, for a given specification type."""
    model = None
    match specification_type:
        case 'actions':
            model = definitions.Action
        case 'capabilities':
            model = definitions.Capability
        case 'domains':
            model = definitions.Domain
        case 'profiles':
            model = definitions.Profile

    specs_files = files(f'finopspp.specifications.{specification_type}')
    if selection == 'all':
        specs = specs_files.iterdir()
    else:
        # we need a light-weight object here to enable spec.name
        # to be a valid attribute blow to match was is yielded
        # by specs_files.iterdir above. So using a named tuple
        file = '0'*(3-len(selection)) + selection
        Spec = namedtuple('Spec', ['name'])
        specs = [Spec(name=f'{file}.yaml')]

    failed = False
    for spec in specs:
        number, _ = os.path.splitext(spec.name)
        # skip over example 0 specs
        if not int(number):
            continue

        path = specs_files.joinpath(spec.name)
        click.echo(f'Validating "{path}" for specification-type={specification_type}:')
        with open(path, 'r', encoding='utf-8') as yaml_file:
            specification_data = yaml.safe_load(yaml_file)

        try:
            model.model_validate(specification_data, extra='forbid')
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


@specifications.command()
@click.option(
    '--specification-type',
    type=click.Choice(list(utils.SpecSubspecMap.keys())),
    default='profiles',
    help='Which specification type to show. Defaults to "profiles"'
)
@click.option(
    '--major',
    is_flag=True,
    default=False,
    help='Specifies that the update should increase the major version. By default the minor version increases'
)
@click.option(
    '--force',
    is_flag=True,
    default=False,
    help='For an update even when changes to specifications are not detected'
)
@click.argument('selection', type=AllOrIntRangeParamType())
def update(selection, specification_type, major, force):
    """Mass update the Specification format per type based on model
    
    By default, all updates are treated as minor updates if the "--major" flag
    is not specified.
    
    Updates are skipped if no changes are detected for a specification, unless
    the "--force" flag is passed. When updating "all" specifications for a given
    specification type, each specification is subject to this check individually,
    but the flag only needs to be passed in once to disable the check for all
    specifications.
    """
    model = None
    match specification_type:
        case 'actions':
            model = definitions.Action
        case 'capabilities':
            model = definitions.Capability
        case 'domains':
            model = definitions.Domain
        case 'profiles':
            model = definitions.Profile

    specs_files = files(f'finopspp.specifications.{specification_type}')
    if selection == 'all':
        specs = specs_files.iterdir()
    else:
        file = '0'*(3-len(selection)) + selection
        Spec = namedtuple('Spec', ['name'])
        specs = [Spec(name=f'{file}.yaml')]

    failed = False
    for spec in specs:
        number, _ = os.path.splitext(spec.name)
        # skip over example 0 specs
        if not int(number):
            continue

        path = specs_files.joinpath(spec.name)
        click.echo(f'Updating "{path}" for specification-type={specification_type}:')

        # load up previous data first
        with open(path, 'r', encoding='utf-8') as yaml_file:
            specification_data = yaml.safe_load(yaml_file)

        passthrough_data = None
        try:
            # pass data through the model to force the data
            # to update to whatever changes have happened in the model
            passthrough_data = json.loads(
                model(**specification_data).model_dump_json()
            )

            # if force is not set, check if new passthrough_data is actually
            # different from the original specification data, if it is not, then
            # just skip any update
            if not force and passthrough_data == specification_data:
                click.secho(
                    f'Update for "{path}" skipped. Update determined to be unnecessary',
                    fg='yellow'
                )
                continue

            # update version
            spec_version = semver.Version.parse(passthrough_data['Metadata']['Version'])
            if major:
                spec_version = spec_version.bump_major()
            else:
                spec_version = spec_version.bump_minor()
            passthrough_data['Metadata']['Version'] = str(spec_version)

            # update date
            passthrough_data['Metadata']['Modified'] = str(datetime.date.today())

            # write out modified data back to spec file
            with open(path, 'w', encoding='utf-8') as yaml_file:
                yaml.dump(
                    passthrough_data,
                    yaml_file,
                    default_flow_style=False,
                    sort_keys=False,
                    indent=2
                )
        except Exception as error: # pylint: disable=broad-exception-caught
            failed = True
            click.secho(
                f'Update for "{path}" failed with --\n', fg='yellow'
            )
            click.secho(str(error) + '\n', err=True, fg='red')
        else:
            click.secho(
                f'Update for "{path}" succeeded', fg='green'
            )

    if failed:
        sys.exit(1)


@specifications.command()
def approvals():
    """Command to help do mass approvals for each component type"""
    # start with profiles
    specs = files('finopspp.specifications.profiles').iterdir()
    for spec in specs:
        number, _ = os.path.splitext(spec.name)
        # skip over example 0 specs
        if not int(number):
            continue
