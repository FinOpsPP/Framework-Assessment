"""Command file for all Generate group commands"""
import os
import sys
from importlib.resources import files

import click
import yaml
from pydantic import TypeAdapter, ValidationError
from rich.progress import track

from finopspp.models import definitions
from finopspp.composers import archive, excel, markdown
from finopspp.commands import utils

@click.group(cls=utils.ClickGroup)
def generate():
    """Generate files from YAML specifications"""


def sub_specification_helper(spec, spec_file):
    """Helps find and pull Specification subsection from a specification

    Note: metadata is only expected to be returned if it is defined. It might not
    be if the component is stubbed out without complete usage of the component
    specification blocks. In this case, only an empty dict is returned along
    with the spec that was passed in
    
    Returns:
        Metadata (dict) - dictionary for a sub-specifications metadata
        Specification (dict) - the actual specification for a component
    """
    spec_id = spec.get('ID')
    # if no ID, or it is ID 0, assume the full sub-specification is given and return
    if not spec_id:
        return {}, spec

    # else look up sub-specification file ID
    spec_id = str(spec_id)
    file = '0'*(3-len(spec_id)) + spec_id
    complete_path = spec_file.joinpath(f'{file}.yaml')
    with open(complete_path, 'r', encoding='utf-8') as yaml_file:
        full_sub = yaml.safe_load(yaml_file)
        sub_metadata = full_sub.get('Metadata') or {}
        sub_spec = full_sub.get('Specification') or {}
        return sub_metadata, sub_spec

def overrides_helper(spec, profile, override_type='std'):
    """Helper for receiving the overrides for a profile if they exist
    
    Also ensure that if an override exists, it conforms to the specification of an
    override

    Returns:
        Override (dict) - valid dictionary for the first override for a profile
    """
    # if there are no overrides, which should be a list type or None,
    # set an empty list
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
    type=click.Choice(list(utils.profiles().keys())),
    help='Which assessment profile to generate. Defaults to "FinOps++"',
)
def assessment(profile): # pylint: disable=too-many-branches,too-many-statements,too-many-locals
    """Generate assessment files from their specifications"""
    click.echo(f'Attempting to create assessment for profile={profile}:')

    domain_files = files('finopspp.specifications.domains')
    cap_files = files('finopspp.specifications.capabilities')
    action_files = files('finopspp.specifications.actions')
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

    domains = []
    for domain in track(profile_spec.get('Domains'), 'Loading profile'):
        capabilities = []

        metadata, spec = sub_specification_helper(domain, domain_files)
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
            'version': metadata.get('Version'),
            'domain': title,
            'capabilities': capabilities
        })
        spec.get('Capabilities').extend(domain_override.get('AddIDs'))
        for capability in spec.get('Capabilities'):
            actions = []

            metadata, spec = sub_specification_helper(capability, cap_files)

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
                'version': metadata.get('Version'),
                'capability': title,
                'actions': actions
            })
            spec.get('Actions').extend(cap_override.get('AddIDs'))
            for action in spec.get('Actions'):
                metadata, spec = sub_specification_helper(action, action_files)

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
                    'version': metadata.get('Version'),
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

    # finally, create the assessment archive file for the current version
    archive.assessment_generate(profile, profile_spec, base_path, domains)


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

        # update all the immediate subspecs listed on the spec in places
        for subspec in spec.get(subspec_type.capitalize(), []):
            _, subspec_doc = sub_specification_helper(subspec, subspec_files)
            subspec_id = str(subspec_doc.get('ID'))
            subspec['file'] = f'/components/{subspec_type}/{"0"*(3-len(subspec_id))}{subspec_id}.md'
            subspec['title'] = subspec_doc.get('Title')

        markdown.components_generate(specification_type, spec)
