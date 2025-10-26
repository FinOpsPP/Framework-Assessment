import json
import os
import sys
from collections import namedtuple
from importlib.resources import files

import click
import pandas
import yaml
from jinja2 import Environment, PackageLoader
from pydantic import TypeAdapter, ValidationError

from finopspp import models
from finopspp import defaults

# presenters based on answers from
# https://stackoverflow.com/questions/8640959/how-can-i-control-what-scalar-form-pyyaml-uses-for-my-data 
def str_presenter(dumper, data):
    # for multi-line strings
    dumped = None
    if len(data.splitlines()) > 1:
        return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')

    # for standard strings
    return dumper.represent_scalar('tag:yaml.org,2002:str', data)

yaml.add_representer(str, str_presenter)


PROFILES_MAP = {}
def profiles():
    """Return all profiles. Including proposed one"""
    global PROFILES_MAP
    if PROFILES_MAP:
        return PROFILES_MAP

    profiles = files('finopspp.specifications.profiles')
    for file in profiles.iterdir():
        path = profiles.joinpath(file.name)
        with open(path, 'r') as yaml_file:
            title = yaml.safe_load(yaml_file).get('Specification').get('Title')
            if not title:
                continue

            PROFILES_MAP[title] = path
    
    return PROFILES_MAP

SPEC_SUBSPEC_MAP = {
    'profiles': 'domains',
    'domains': 'capabilities',
    'capabilities': 'actions',
    'actions': '' # empty string just to help with functionality below
}


@click.group()
def cli():
    """FinOps++ administration tool"""
    pass


@cli.group()
def generate():
    """Generate files from YAML specifications"""
    pass


def sub_specification_helper(spec, spec_file):
    """Helps find and pull Specification subsection from a specification"""
    spec_id = spec.get('ID')
    # if no ID, or it is ID 0, assume the full sub-specification is given and return
    if not spec_id:
        return spec

    # else look up sub-specification file ID
    spec_id = str(spec_id)
    file = '0'*(3-len(spec_id)) + spec_id
    with open(spec_file.joinpath(f'{file}.yaml'), 'r') as yaml_file:
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
    model = models.OVERRIDE_MAP[override_type]

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
def assessment(profile):
    """Generate assessment files from their specifications"""
    click.echo(f'Attempting to create assessment for profile={profile}:')
    # pull in template and specification files for given specification type
    env = Environment(loader=PackageLoader('finopspp', 'templates'))
    template = env.get_template('framework.md.j2')

    domain_files = files('finopspp.specifications.domains')
    cap_files = files('finopspp.specifications.capabilities')
    action_files = files('finopspp.specifications.actions')
    with open(PROFILES_MAP[profile], 'r') as yaml_file:
        spec = yaml.safe_load(
            yaml_file
        ).get('Specification')

    domains = []
    if not spec.get('Domains'):
        click.secho('Profile includes no domains. Exiting', err=True, fg='red')
        sys.exit(1)

    profile_id = spec.get('ID')
    for domain in spec.get('Domains'):
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

                actions.append({
                    'action': spec.get('Description'),
                    'serial number': serial_number,
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

    # render file before writing it
    # include profile title with linkable ID.
    click.echo(f'Attempting to generate framework for profile={profile}:')
    spec_id = str(profile_id)
    file = '0'*(3-len(spec_id)) + spec_id
    profile_title = f'<a href="/components/profiles/{file}.md">{file}</a>: {profile}'
    output = template.render(profile=profile_title, domains=domains)

    # finally, create framework markdown for this profile
    # from the rendered output
    out_path = os.path.join(
        base_path,
        'framework.md'
    )
    with open(out_path, 'w') as outfile:
        outfile.write(output)

    click.secho(f'Attempt to generate framework markdown "{out_path}" succeeded', fg='green')

    # next try and create the excel workbook for this profile.
    # the normalization that is done will remove domains and capabilities that
    # do not have actions. That means, there can be divergences between the
    # framework markdown, which does include these, and the assessment doc that
    # does not. They are not included because without actions, nothing can be scored.  
    click.echo(f'Attempting to generate assessment.xlsx for profile={profile}:')
    dataframe = pandas.json_normalize(
        domains,
        record_path=['capabilities', 'actions'], # path to actions
        meta=['domain', ['capabilities', 'capability']]
    )
    dataframe.rename(
        columns={
            'capabilities.capability': 'capability'
        },
        inplace=True
    )
    dataframe.set_index(['domain', 'capability', 'action'], inplace=True)

    out_path = os.path.join(
        base_path,
        'assessment.xlsx'
    )
    with pandas.ExcelWriter(out_path, engine='xlsxwriter') as writer:
        # pandas uses an incredible opinionated format for indices and headers
        # which for this project is sufficient to meet the needs of the assessments.
        # as such, will not try to update the index or header formatting given by pandas
        dataframe.to_excel(
            writer, sheet_name='Overview'
        )

        # format cells
        workbook = writer.book
        worksheet = writer.sheets['Overview']

        # Add a sample alternative link format.
        link_format = workbook.add_format(
            {
                'align': 'center',
                'bold': True,
                'underline': True,
                'font_color': 'blue'
            }
        )

        for index, (_, row) in enumerate(dataframe.iterrows(), start=2):
            scores = [f'{scoring['Score']}: {scoring["Condition"]}' for scoring in row.scoring]
            worksheet.write(f'G{index}', scores[0]) # overwrite with correct default scores
            worksheet.data_validation(
                f'F{index}',
                {
                    'validate' : 'list',
                    'source': scores
                }
            )
            worksheet.write_formula(f'H{index}', f'=E{index}*VALUE(LEFT(G{index}, FIND(":", G{index})-1))')

            # overwrite serial numbers with links to github markdown pages for the numbers
            serial_number = row['serial number']
            worksheet.write_url(
                f'D{index}',
                f'https://github.com/FinOpsPP/Framework-Assessment/tree/main/components/actions/{serial_number}.md',
                link_format,
                string=serial_number
            )

        # write score info
        worksheet.write_formula('J2', f'=SUM(E2:E{dataframe.shape[0]+1})') # sum of weights
        worksheet.write_formula('K2', f'=SUM(H2:H{dataframe.shape[0]+1})/J2') # weighted scores

        # Autofit the worksheet.
        worksheet.autofit()

        # ignore certain warnings
        worksheet.ignore_errors({'number_stored_as_text': 'D:D'})

    click.secho(f'Attempt to generate assessment.xlsx "{out_path}" succeeded', fg='green')


@generate.command()
@click.option(
    '--specification-type',
    type=click.Choice(list(SPEC_SUBSPEC_MAP.keys())),
    help='Which specification type to generate. Defaults to "profiles"'
)
def components(specification_type):
    """Generate component markdown files from their specifications"""
    # pull in template and specification files for given specification type
    env = Environment(loader=PackageLoader('finopspp', 'templates'))
    template = env.get_template(f'{specification_type}.md.j2')
    spec_files = files(f'finopspp.specifications.{specification_type}')
    
    # get subspec to help fill in names and other important pieces of
    # information from the sub specification.
    subspec_type = SPEC_SUBSPEC_MAP[specification_type]
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
        with open(path, 'r') as yaml_file:
            spec = yaml.safe_load(yaml_file).get('Specification')

        for subspec in spec.get(subspec_type.capitalize(), []):
            subspec_doc = sub_specification_helper(subspec, subspec_files)
            subspec_id = str(subspec_doc.get('ID'))
            subspec['File'] = f'/components/{subspec_type}/{"0"*(3-len(subspec_id))}{subspec_id}.md'
            subspec['Title'] = subspec_doc.get('Title')

        output = template.render(spec=spec)

        # finally, write out rendered output to file
        # make sure serialized ID is the same as the one
        # used in the specification files.
        spec_id = spec.get('ID')
        spec_id = str(spec_id)
        file_prefix = '0'*(3-len(spec_id)) + spec_id
        out_path = os.path.join(
            os.getcwd(),
            'components',
            specification_type,
            f'{file_prefix}.md'
        )
        click.echo(
            f'Attempting to generate component "{out_path}" for specification-type={specification_type}:'
        )

        with open(out_path, 'w') as outfile:
            outfile.write(output)

        click.secho(f'Attempt to generate "{out_path}" succeeded', fg='green')


@cli.group()
def specifications():
    """Informational command on Specifications"""
    pass


@specifications.command()
@click.option(
    '--specification-type',
    type=click.Choice(list(SPEC_SUBSPEC_MAP.keys())),
    default='profiles',
    help='Which specification type to use. Defaults to "profiles"'
)
@click.argument('id', type=click.IntRange(1, 999))
def new(id, specification_type):
    """Create a new specification for a new ID

    It is required that the ID be new itself for a given specification.
    The command will fail otherwise.
    """
    spec_id = str(id)
    file = '0'*(3-len(spec_id)) + spec_id
    path = files(
        f'finopspp.specifications.{path}'
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

    data['Specification']['ID'] = id
    with open(path, 'w') as file:
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
    '--profile',
    default='FinOps++',
    type=click.Choice(list(profiles().keys())),
    help='Which assessment profile to list. Defaults to "FinOps++"'
)
def list_specs(profile):
    """List all Specifications by fully qualified ID per profile
    
    Fully qualified ID is of the format Domain.Capability-Action"""
    with open(PROFILES_MAP[profile], 'r') as yaml_file:
        spec = yaml.safe_load(
            yaml_file
        ).get('Specification')
        domains = spec.get('Domains')
        profile_id = spec.get('ID')

    domain_files = files('finopspp.specifications.domains')
    cap_files = files('finopspp.specifications.capabilities')
    click.echo(f'Fully qualified IDs for {profile}. Profile ID: {profile_id}')
    for domain in domains:
        domain_id = domain.get('ID')
        if not domain_id:
            continue

        domain_id = str(domain_id)
        file = '0'*(3-len(domain_id)) + domain_id
        with open(domain_files.joinpath(f'{file}.yaml'), 'r') as yaml_file:
            capabilities = yaml.safe_load(
                yaml_file
            ).get('Specification').get('Capabilities')

        for capability in capabilities:
            capability_id = capability.get('ID')
            if not capability_id:
                continue

            capability_id = str(capability_id)
            file = '0'*(3-len(capability_id)) + capability_id
            with open(cap_files.joinpath(f'{file}.yaml'), 'r') as yaml_file:
                actions = yaml.safe_load(
                    yaml_file
                ).get('Specification').get('Actions')

            for action in actions:
                action_id = action.get('ID')
                unique_id = f'{domain_id}.{capability_id}-{action_id}'
                click.echo(unique_id)


@specifications.command()
@click.option(
    '--metadata',
    is_flag=True,
    help='Show the Metadata for a Specifications'
)
@click.option(
    '--specification-type',
    type=click.Choice(list(SPEC_SUBSPEC_MAP.keys())),
    default='profiles',
    help='Which specification type to show. Defaults to "profiles"'
)
@click.argument('id', type=click.IntRange(1, 999))
def show(id, metadata, specification_type):
    """Show information on a given specification by ID by type"""
    data_type = 'Specification'
    if metadata:
        data_type = 'Metadata'

    spec_id = str(id)
    file = '0'*(3-len(spec_id)) + spec_id
    specification_file = files(
        f'finopspp.specifications.{specification_type}'
    ).joinpath(f'{file}.yaml')

    with open(specification_file, 'r') as file:
        specification_data = yaml.safe_load(file)
        click.echo(
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
    type=click.Choice(list(SPEC_SUBSPEC_MAP.keys())),
    default='profiles',
    help='Which schema specification type to show. Defaults to "profiles"'
)
def schema(specification_type):
    """Give schema (in YAML format) for a given specification type
    
    The schema is based on the pydantic version of the JSON and OpenAPI
    Schemas. For more info on this type of schema specification, please view:
    https://docs.pydantic.dev/latest/concepts/json_schema/
    """
    schema = None
    click.echo(f'Schema definition for specification-type={specification_type}:\n')
    match specification_type:
        case 'actions':
            schema = TypeAdapter(models.Action).json_schema(mode='serialization')
        case 'capabilities':
            schema = TypeAdapter(models.Capability).json_schema(mode='serialization')
        case 'domains':
            schema = TypeAdapter(models.Domain).json_schema(mode='serialization')
        case 'profiles':
            schema = TypeAdapter(models.Profile).json_schema(mode='serialization')
    click.echo(            
        yaml.dump(
            schema,
            default_flow_style=False,
            sort_keys=False,
            indent=2
        )
    )


class AllOrIntRangeParamType(click.ParamType):
    name = 'All or ID'

    def get_metavar(self, param, ctx):
        return f'{param.name.upper()} [all|1-999]'

    def convert(self, value, param, ctx):
        try:
            if value == 'all':
                return value
            else:
                return str(click.IntRange(1, 999).convert(value, param, ctx))
        except:
            self.fail(f"'{value}' must be \"all\" or an int between 1-999")

@specifications.command()
@click.option(
    '--specification-type',
    type=click.Choice(list(SPEC_SUBSPEC_MAP.keys())),
    default='profiles',
    help='Which specification type to show. Defaults to "profiles"'
)
@click.argument('selection', type=AllOrIntRangeParamType())
def validate(selection, specification_type):
    """Validate all or a specific specification ID, for a given specification type."""
    model = None
    match specification_type:
        case 'actions':
            model = models.Action
        case 'capabilities':
            model = models.Capability
        case 'domains':
            model = models.Domain
        case 'profiles':
            model = models.Profile

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
        click.echo(f'Validating "{path}" for specification-type={specification_type}:')
        with open(path, 'r') as yaml_file:
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
    type=click.Choice(list(SPEC_SUBSPEC_MAP.keys())),
    help='Which specification type to show. Defaults to "profiles"'
)
@click.argument('selection', type=AllOrIntRangeParamType())
def update(selection, specification_type):
    """Mass update the Specification format per type based on model"""
    model = None
    match specification_type:
        case 'actions':
            model = models.Action
        case 'capabilities':
            model = models.Capability
        case 'domains':
            model = models.Domain
        case 'profiles':
            model = models.Profile

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
        with open(path, 'r') as yaml_file:
            specification_data = yaml.safe_load(yaml_file)
        
        passthrough_data = None
        try:
            passthrough_data = json.loads(
                model(**specification_data).model_dump_json()
            )

            # write out modified data back to spec file
            with open(path, 'w') as yaml_file:
                yaml.dump(
                    passthrough_data,
                    yaml_file,
                    default_flow_style=False,
                    sort_keys=False,
                    indent=2
                )
        except Exception as error:
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
