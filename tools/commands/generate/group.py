"""Command file for all Generate group commands"""
import os
import sys
from importlib.resources import files

import click
import yaml
from pydantic import TypeAdapter

from finopspp.models import Action, Capability, Domain, Profile
from finopspp.models.specs import StatusEnum
from finopspp.commands import utils
from finopspp.commands.generate import helpers
from finopspp.commands.generate.composers import archive, excel, markdown

@click.group(cls=utils.ClickGroup)
def generate():
    """Generate files from YAML specifications"""


@generate.command()
@click.option(
    '--profile',
    default='FinOps++',
    type=click.Choice(list(utils.profiles().keys())),
    help='Which assessment profile to generate. Defaults to "FinOps++"',
)
@click.option(
    '--proposed',
    is_flag=True,
    default=False,
    help='Include Proposed components'
)
@click.option(
    '--deprecated',
    is_flag=True,
    default=False,
    help='Include Deprecated components'
)
@click.option(
    '--variables',
    type=click.Choice(list(utils.variables().keys())),
    help='Optional variables file to overright default assessment settings for a given profile'
)
def assessment(profile, proposed, deprecated, variables):
    """Generate assessment files from their specifications
    
    By default, this will generate an assessment and its' corresponding files
    for Accepted components. To include Proposed or Deprecated components that are
    attached to a higher level component, include those flags. Each flag must be
    passed in to include both.
    
    When these are included, a special assessment excel and framework markdown is
    created in the Profile directory for that assessment. They will have the suffix
    of '-proposed', '-deprecated' or '-proposed-deprecated' depending on which flags
    are passed in. These special files cannot not be checked in.

    Components that are manually specified, i.e not listed by ID, are included by
    default to aid with prototypes of new specifications.
    """
    click.echo(f'Attempting to create assessment for profile={profile}:')
    with open(utils.ProfilesMap[profile], 'r', encoding='utf-8') as yaml_file:
        profile_yaml = yaml.safe_load(
            yaml_file
        )
        profile_spec = profile_yaml.get('Specification') or {}
        profile_metadata = profile_yaml.get('Metadata') or {}
        # edits to a specification in code should always be lowercase!
        # to help show that it is a transformation from the uppercase
        # version used in the actual yaml specification.
        profile_spec['version'] = profile_metadata.get('Version')

    if not profile_spec.get('Domains'):
        click.secho('Profile includes no domains. Exiting', err=True, fg='red')
        sys.exit(1)

    if not isinstance(profile_spec['Domains'], list):
        click.secho(f'Domains for profile={profile} must be a list', err=True, fg='red')
        sys.exit(1)

    allowed_statuses = [StatusEnum.accepted.value]
    suffix = ''
    if proposed:
        allowed_statuses.append(
            StatusEnum.proposed.value
        )
        suffix += '.proposed'
    if deprecated:
        allowed_statuses.append(
            StatusEnum.deprecated.value
        )
        suffix += '.deprecated'
    if variables:
        suffix += '.variables'

    # pull in formatted domains data-dict
    variables_spec = helpers.variables_collector(
        profile, variables
    )
    specification = helpers.specification_collector(
        profile, profile_spec, allowed_statuses, variables_spec
    )

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
    markdown.assessment_generate(profile, profile_spec, base_path, specification, suffix)

    # next try and create the workbook for this profile.
    excel.assessment_generate(profile, base_path, specification, suffix)

    # finally, create the assessment archive file for the current version
    # NOTE: The data structure for specification will not be the same after running the
    # following
    archive.assessment_generate(profile, profile_spec, base_path, specification, suffix)


@generate.command()
def documents():
    """Generate schema documents markdown files from code"""
    schemas = {}
    for definition in [Action, Capability, Domain, Profile]:
        schemas[definition.__name__.lower()] = yaml.dump(
            TypeAdapter(definition).json_schema(mode='serialization'),
            default_flow_style=False,
            sort_keys=False,
            indent=2,
            width=120 # will always be longer that what is allowed by yamllint
        )

    markdown.schemas_generate(schemas)



@generate.command()
@click.option(
    '--specification-type',
    default='profiles',
    type=click.Choice(list(utils.SpecSubspecMap.keys())),
    help='Which specification type to generate. Defaults to "profiles"'
)
def components(specification_type):
    """Generate component markdown files from their specifications"""
    spec_files = files(f'finopspp.specifications.{specification_type}')

    # get subspec to help fill in names and other important pieces of
    # information from the sub specification.
    subspec_type = utils.SpecSubspecMap[specification_type]
    subspec_files = None
    if subspec_type:
        subspec_files = files(f'finopspp.specifications.{subspec_type}')

    # iterate over the specification files and generate markdown files
    for spec in spec_files.iterdir():
        number, _ = os.path.splitext(spec.name)
        # skip over example 0 specs
        if not int(number):
            continue

        # all added fields to a specification should be in lowercase!
        # to help differentiate them against the uppercase fields in
        # the specifications itself.
        path = spec_files.joinpath(spec.name)
        with open(path, 'r', encoding='utf-8') as yaml_file:
            full_yaml = yaml.safe_load(yaml_file)
            spec = full_yaml.get('Specification')
            metadata = full_yaml.get('Metadata') or {}
            spec['version'] = metadata.get('Version')
            spec['status'] = metadata.get('Status')

        # update all the immediate subspecs listed on the spec in places
        for subspec in spec.get(subspec_type.capitalize(), []):
            _, subspec_doc = helpers.sub_specification_collector(subspec, subspec_files)
            subspec_id = str(subspec_doc.get('ID'))
            subspec['file'] = f'/components/{subspec_type}/{"0"*(3-len(subspec_id))}{subspec_id}.md'
            subspec['title'] = subspec_doc.get('Title')

        markdown.components_generate(specification_type, spec)
