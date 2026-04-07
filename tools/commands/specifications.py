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
from click import UsageError
from pydantic import TypeAdapter, ValidationError
from rich.console import Console
from rich.syntax import Syntax
from textual import on
from textual.app import App
from textual.containers import Horizontal, Vertical
from textual.events import Mount
from textual.widgets import Footer, Header, Label, Pretty, SelectionList, Switch
from textual.widgets.selection_list import Selection

from finopspp.models import definitions, defaults
from finopspp.commands import utils


yaml.add_representer(str, utils.str_presenter)

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
@click.option(
    '--no-numbers',
    is_flag=True,
    default=False,
    help='Disable numbers on pager if one should exist'
)
@click.argument('id_', metavar='<spec ID>', type=click.IntRange(1, 999))
def show(id_, metadata, specification_type, no_numbers):
    """Show information on a given specification by ID by type
    
    Information is shown in a Pager, if one is available.

    NOTE: Line numbers are added by default, if your default pager
    already uses this and you would like to disable it, pass in the
    "--no-numbers" flag
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
        'yaml',
        line_numbers=(not no_numbers)
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
@click.option(
    '--no-numbers',
    is_flag=True,
    default=False,
    help='Disable numbers on pager if one should exist'
)
def schema(specification_type, no_numbers):
    """Give schema (in YAML format) for a given specification type
    
    The schema is based on the pydantic version of the JSON and OpenAPI
    Schemas. For more info on this type of schema specification, please view:
    https://docs.pydantic.dev/latest/concepts/json_schema/

    Schemas are shown in a Pager, if one is available.

    NOTE: Line numbers are added by default, if your default pager
    already uses this and you would like to disable it, pass in the
    "--no-numbers" flag
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
        'yaml',
        line_numbers=(not no_numbers)
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


def approval_helper(approvers, number, today, specs):
    """Helper to add approval to a specification by number"""
    path = specs.joinpath(f'{number}.yaml')
    with open(path, 'r', encoding='utf-8') as yaml_file:
        specification_data = yaml.safe_load(yaml_file)

    # update basic metadata
    metadata = specification_data['Metadata']
    metadata['Version'] = '1.0.0'
    metadata['Adopted'] = today
    metadata['Modified'] = today
    metadata['Status'] = definitions.StatusEnum.accepted.value

    # now update metadata approvers list with selected approvers
    approval_list = []
    for name, email in approvers:
        approval_list.append(
            {
                'Name': name,
                'Email': email,
                'Date': today
            }
        )
    metadata['Approvers'] = approval_list

    with open(path, 'w', encoding='utf-8') as yaml_file:
        yaml.dump(
            specification_data,
            yaml_file,
            default_flow_style=False,
            sort_keys=False,
            indent=2
        )

def approval_options_helper(specification_type):
    """Helper to pull information on what should should be approved"""
    spec_options = {}
    specs = files(f'finopspp.specifications.{specification_type}')
    for spec in specs.iterdir():
        number, _ = os.path.splitext(spec.name)

        # skip over example 0 specs
        if not int(number):
            continue

        path = specs.joinpath(spec.name)

        # load up previous data first
        with open(path, 'r', encoding='utf-8') as yaml_file:
            specification_data = yaml.safe_load(yaml_file)

        # check if status is Proposed, and if it is, add as option to approve
        if specification_data['Metadata']['Status'] != definitions.StatusEnum.proposed.value:
            continue

        spec = specification_data['Specification']

        # only accept specifications with titles
        title = spec['Title']
        if not title:
            continue

        # new a few additional filters for actions
        if specification_type == 'actions':
            # skip if weight is still 0 or does not exist.
            if not spec['Weight']:
                continue

            # also skip if the last score is not 10
            last_score = spec['Scoring'].pop()
            if last_score['Score'] != 10:
                continue

        spec_options[title] = number

    return spec_options

def approval_selector_helper(options, specification_type, approval_map):
    """Helper for building the selector interface"""
    selection_list = []
    for title, serial_number in options.items():
        selection_list.append(Selection(title, serial_number))

    # now we create the terminal app that allows selections
    class Approvals(App):
        """Terminal application

        that will provide an selection inferface for specifications to approve"""
        CSS_PATH = "approvals.tcss"

        def compose(self):
            """Layout of app in terminal"""
            yield Header()
            with Vertical():
                yield Label(
                    'Please select from this list and press [b]ctrl-q[/] to save & exit'
                )
                with Horizontal():
                    yield SelectionList(*selection_list)
                    yield Pretty(approval_map[specification_type])
                with Horizontal(id='horizontal-two'):
                    yield Label('(De)Select All:')
                    yield Switch()
            yield Footer()

        def on_mount(self):
            """What to do when the app is loaded"""
            self.query_one(
                SelectionList
            ).border_title = 'Which specifications should be approved?'
            self.query_one(
                Pretty
            ).border_title = 'Selected specifications (by ID)'
            self.title = f'Approvals for "{specification_type.title()}"'

        @on(Mount)
        @on(SelectionList.SelectedChanged)
        def update_selected_view(self):
            """How the view should update on selection changes"""
            approval_map[specification_type] = self.query_one(SelectionList).selected
            self.query_one(
                Pretty
            ).update(
                approval_map[specification_type]
            )

        @on(Switch.Changed)
        def update_switched_view(self):
            """How the view should update on switch changes"""
            self.query_one(SelectionList).toggle_all()


    Approvals().run()

@specifications.command()
def approvals():
    """Command to help do mass approvals for each component type
    
    NOTE: An approver should match up, in order, with an approver email
    """
    # prompt list of approvers and their associated emails
    approvers = []
    prompt = True
    while prompt:
        approver = click.prompt(
            'Please add full name of approver or press enter to quit',
            default='',
            show_default=False,
            type=str
        )
        if not approver:
            prompt = False
            continue

        approver_email = click.prompt(
            'Please add email for approver',
            default='',
            show_default=False,
            type=str
        )
        if not approver_email:
            raise UsageError(
                'Every approver must have an approval email'
            )

        if not click.confirm(f'Include ({approver}, {approver_email}) pair?'):
            click.secho('Dropping pair', fg='red')
            continue

        click.secho('Accepting pair', fg='green')
        approvers.append((approver, approver_email))

    click.confirm(f'Take full list of approvers {approvers}?', abort=True)

    # start with profiles
    approval_map = {
        'profiles': [],
        'domains': [],
        'capabilities': [],
        'actions': []
    }
    specification_types = list(approval_map.keys())
    for spec_type in specification_types:
        spec_options = approval_options_helper(spec_type)

        if not spec_options:
            click.secho(f'No approvals needed for {spec_type}.')
            click.pause()
        else:
            approval_selector_helper(spec_options, spec_type, approval_map)

    # get todays date
    today = str(datetime.date.today())

    # do approvals for profiles first
    specs = files('finopspp.specifications.profiles')
    for number in approval_map['profiles']:
        approval_helper(approvers, number, today, specs)

    # next do domains
    specs = files('finopspp.specifications.domains')
    for number in approval_map['domains']:
        approval_helper(approvers, number, today, specs)

    # next do capabilities
    specs = files('finopspp.specifications.capabilities')
    for number in approval_map['capabilities']:
        approval_helper(approvers, number, today, specs)

    # finally do actions
    specs = files('finopspp.specifications.actions')
    for number in approval_map['actions']:
        approval_helper(approvers, number, today, specs)

    click.secho('Approval completed', fg='green')
