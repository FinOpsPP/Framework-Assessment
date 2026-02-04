"""primary code for the finopspp CLI"""
import json
import os
import sys
import platform
from collections import namedtuple
from importlib.resources import files
from importlib.metadata import metadata as meta

import click
import yaml
import semver
from pydantic import TypeAdapter, ValidationError

from finopspp.models import definitions, defaults
from finopspp.composers import excel, markdown

# presenters based on answers from
# https://stackoverflow.com/questions/8640959/how-can-i-control-what-scalar-form-pyyaml-uses-for-my-data
def str_presenter(dumper, data):
    # for multi-line strings
    if len(data.splitlines()) > 1:
        return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')

    # for standard strings
    return dumper.represent_scalar('tag:yaml.org,2002:str', data)

yaml.add_representer(str, str_presenter)


ProfilesMap = {}
def profiles():
    """Return all profiles. Including proposed one"""
    if ProfilesMap:
        return ProfilesMap

    profile_specs = files('finopspp.specifications.profiles')
    for file in profile_specs.iterdir():
        path = profile_specs.joinpath(file.name)
        with open(path, 'r', encoding='utf-8') as yaml_file:
            title = yaml.safe_load(yaml_file).get('Specification').get('Title')
            if not title:
                continue

            ProfilesMap[title] = path

    return ProfilesMap

SpecSubspecMap = {
    'profiles': 'domains',
    'domains': 'capabilities',
    'capabilities': 'actions',
    'actions': '' # empty string just to help with functionality below
}


@click.group()
def cli():
    """FinOps++ administration tool"""

@cli.command()
def version():
    """Version and runtime information about the finopspp tool"""
    tool_version = meta('finopspp').get('Version', '0.0.0')
    click.echo(f'Version: {tool_version}')
    python_version = sys.version.split(' ', maxsplit=1).pop(0)
    click.echo(f'Python Version: {python_version}')
    click.echo(f'System: {platform.system()} ({platform.release()})')

@cli.group()
def generate():
    """Generate files from YAML specifications"""


def sub_specification_helper(spec, spec_file):
    """Helps find and pull Specification subsection from a specification"""
    spec_id = spec.get('ID')
    # if no ID, or it is ID 0, assume the full sub-specification is given and return
    if not spec_id:
        return spec

    # else look up sub-specification file ID
    spec_id = str(spec_id)
    file = '0'*(3-len(spec_id)) + spec_id
    with open(spec_file.joinpath(f'{file}.yaml'), 'r', encoding='utf-8') as yaml_file:
        return yaml.safe_load(yaml_file).get('Specification')

def overrides_helper(spec, profile, override_type='std'):
    """Helper for receiving the overrides for a profile if they exist
    
    Also ensure that if an override exists, it conforms to the specification of an
    override
    """
    overrides = spec.get('Overrides')
    if not overrides:
        overrides = []

    # pull correct override model based on override type
    model = definitions.OverrideMap[override_type]

    validated_override = model(Profile=profile)
    for override in overrides:
        # Only validate the override for the relevant profile
        if override.get('Profile') != profile:
            continue

        try:
            validated_override = model(**override)
        except ValidationError as val_error:
            click.secho(
                f'Validation for override "{profile}" on {spec["Title"]} failed with --\n', fg='yellow'
            )
            click.secho(str(val_error) + '\n' + 'Exiting early!', err=True, fg='red')
            sys.exit(1)

        # after validating the correct override, which we take to be the first with a given
        # title or Spec ID, we break out of the loop.
        break

    return validated_override.model_dump()

@generate.command()
@click.option(
    '--profile',
    default='FinOps++',
    type=click.Choice(list(profiles().keys())),
    help='Which assessment profile to generate. Defaults to "FinOps++"',
)
def assessment(profile): # pylint: disable=too-many-branches,too-many-statements,too-many-locals
    """Generate assessment files from their specifications"""
    click.echo(f'Attempting to create assessment for profile={profile}:')

    domain_files = files('finopspp.specifications.domains')
    cap_files = files('finopspp.specifications.capabilities')
    action_files = files('finopspp.specifications.actions')
    with open(ProfilesMap[profile], 'r', encoding='utf-8') as yaml_file:
        profile_spec = yaml.safe_load(
            yaml_file
        ).get('Specification')

    domains = []
    if not profile_spec.get('Domains'):
        click.secho('Profile includes no domains. Exiting', err=True, fg='red')
        sys.exit(1)

    for domain in profile_spec.get('Domains'):
        capabilities = []

        spec = sub_specification_helper(domain, domain_files)
        domain_override = overrides_helper(spec, profile)
        domain_drops = [drop['ID'] for drop in domain_override.get('DropIDs')]

        if domain_override.get('TitleUpdate'):
            spec['Title'] = domain_override.get('TitleUpdate')
        title = spec.get('Title')

        if domain_override.get('DescriptionUpdate'):
            spec['Description'] = domain_override.get('DescriptionUpdate')

        if spec.get('Capabilities') is None:
            spec['Capabilities'] = []
        if not isinstance(spec.get('Capabilities'), list):
            click.secho(
                f'Capabilities for domain={title} must be null or a list. Exiting',
                err=True,
                fg='red'
            )
            sys.exit(1)

        spec_id = spec.get('ID')
        serial_number = None
        if spec_id:
            spec_id = str(spec.get('ID'))
            serial_number = '0'*(3-len(spec_id)) + spec_id

        domains.append({
            'serial_number': serial_number,
            'domain': title,
            'capabilities': capabilities
        })
        spec.get('Capabilities').extend(domain_override.get('AddIDs'))
        for capability in spec.get('Capabilities'):
            actions = []

            spec = sub_specification_helper(capability, cap_files)

            # continue early if the Capability ID is one to be dropped
            spec_id = spec.get('ID')
            if spec_id and spec_id in domain_drops:
                continue

            cap_override = overrides_helper(spec, profile)
            cap_drops = [drop['ID'] for drop in cap_override.get('DropIDs')]

            if cap_override.get('TitleUpdate'):
                spec['Title'] = cap_override.get('TitleUpdate')
            title = spec.get('Title')

            if cap_override.get('DescriptionUpdate'):
                spec['Description'] = cap_override.get('DescriptionUpdate')

            if spec.get('Actions') is None:
                spec['Actions'] = []
            if not isinstance(spec.get('Actions'), list):
                click.secho(
                    f'Actions for capability={title} must be null or a list. Exiting',
                    err=True,
                    fg='red'
                )
                sys.exit(1)

            serial_number = None
            if spec_id:
                spec_id = str(spec.get('ID'))
                serial_number = '0'*(3-len(spec_id)) + spec_id

            capabilities.append({
                'serial_number': serial_number,
                'capability': title,
                'actions': actions
            })
            spec.get('Actions').extend(cap_override.get('AddIDs'))
            for action in spec.get('Actions'):
                spec = sub_specification_helper(action, action_files)

                # continue early if the Action ID is one to be dropped
                spec_id = spec.get('ID')
                if spec_id and spec_id in cap_drops:
                    continue

                act_override = overrides_helper(spec, profile, 'action')

                if act_override.get('TitleUpdate'):
                    spec['Title'] = act_override.get('TitleUpdate')
                title = spec.get('Title')

                if act_override.get('DescriptionUpdate'):
                    spec['Description'] = act_override.get('DescriptionUpdate')

                if act_override.get('WeightUpdate'):
                    spec['Weight'] = act_override.get('WeightUpdate')

                spec_id = str(spec_id)
                serial_number = '0'*(3-len(spec_id)) + spec_id

                # since not every action has a title yet, fall back to
                # description when it does not exist or is None.
                actions.append({
                    'action': spec.get('Title') or spec.get('Description'),
                    'serial_number': serial_number,
                    'weights': spec.get('Weight'),
                    'formula': spec.get('Formula'),
                    'scoring': spec.get('Scoring'),
                    'weighted score': None
                })

    # check if assessment directory exists for this profile
    # and if it does not create it
    base_path = os.path.join(
        os.getcwd(),
        'assessments',
        profile
    )
    if not os.path.exists(base_path):
        os.mkdir(base_path)

    # create assessment framework overview markdown
    markdown.assessment_generate(profile, profile_spec, base_path, domains)

    # next try and create the workbook for this profile.
    excel.assessment_generate(profile, base_path, domains)


@generate.command()
def documents():
    """Generate schema documents markdown files from code"""
    schemas = {}
    for definition in [definitions.Action, definitions.Capability, definitions.Domain, definitions.Profile]:
        schemas[definition.__name__.lower()] = yaml.dump(
            TypeAdapter(definition).json_schema(mode='serialization'),
            default_flow_style=False,
            sort_keys=False,
            indent=2
        )
    markdown.schemas_generate(schemas)



@generate.command()
@click.option(
    '--specification-type',
    default='profiles',
    type=click.Choice(list(SpecSubspecMap.keys())),
    help='Which specification type to generate. Defaults to "profiles"'
)
def components(specification_type):
    """Generate component markdown files from their specifications"""
    spec_files = files(f'finopspp.specifications.{specification_type}')

    # get subspec to help fill in names and other important pieces of
    # information from the sub specification.
    subspec_type = SpecSubspecMap[specification_type]
    subspec_files = None
    if subspec_type:
        subspec_files = files(f'finopspp.specifications.{subspec_type}')

    # iterate over the specification files and generate markdown files
    for spec in spec_files.iterdir():
        number, _ = os.path.splitext(spec.name)
        # skip over example 0 specs
        if not int(number):
            continue

        path = spec_files.joinpath(spec.name)
        with open(path, 'r', encoding='utf-8') as yaml_file:
            spec = yaml.safe_load(yaml_file).get('Specification')

        for subspec in spec.get(subspec_type.capitalize(), []):
            subspec_doc = sub_specification_helper(subspec, subspec_files)
            subspec_id = str(subspec_doc.get('ID'))
            subspec['File'] = f'/components/{subspec_type}/{"0"*(3-len(subspec_id))}{subspec_id}.md'
            subspec['Title'] = subspec_doc.get('Title')

        markdown.components_generate(specification_type, spec)


@cli.group()
def specifications():
    """Informational command on Specifications"""


@specifications.command()
@click.option(
    '--specification-type',
    type=click.Choice(list(SpecSubspecMap.keys())),
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
    type=click.Choice(list(profiles().keys())),
    help='Which assessment profile to list. Defaults to "FinOps++"'
)
def list_specs(show_action_status, status_by, profile):
    """List all Specifications by fully qualified ID per profile
    
    Fully qualified ID is of the format Domain.Capability-Action"""
    with open(ProfilesMap[profile], 'r', encoding='utf-8') as yaml_file:
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
    type=click.Choice(list(SpecSubspecMap.keys())),
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

    with open(path, 'r', encoding='utf-8') as file:
        specification_data = yaml.safe_load(file)
        click.echo_via_pager(
            yaml.dump(
                specification_data[data_type],
                default_flow_style=False,
                sort_keys=False,
                indent=2
            )
        )


@specifications.command()
@click.option(
    '--specification-type',
    type=click.Choice(list(SpecSubspecMap.keys())),
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

    click.echo_via_pager(
        yaml.dump(
            spec_schema,
            default_flow_style=False,
            sort_keys=False,
            indent=2
        ),
        color=True
    )


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
    type=click.Choice(list(SpecSubspecMap.keys())),
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
    type=click.Choice(list(SpecSubspecMap.keys())),
    help='Which specification type to show. Defaults to "profiles"'
)
@click.option(
    '--major',
    is_flag=True,
    default=False,
    help='Specifies that the update should increase the major version. By default the minor version increases'
)
@click.argument('selection', type=AllOrIntRangeParamType())
def update(selection, specification_type, major):
    """Mass update the Specification format per type based on model"""
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
        with open(path, 'r', encoding='utf-8') as yaml_file:
            specification_data = yaml.safe_load(yaml_file)

        passthrough_data = None
        try:
            passthrough_data = json.loads(
                model(**specification_data).model_dump_json()
            )

            # update version
            spec_version = semver.Version.parse(passthrough_data['Metadata']['Version'])
            if major:
                spec_version = spec_version.bump_major()
            else:
                spec_version = spec_version.bump_minor()
            passthrough_data['Metadata']['Version'] = str(spec_version)

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


if __name__ == "__main__":
    cli()
