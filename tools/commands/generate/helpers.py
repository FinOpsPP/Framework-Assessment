"""Helpers file for generate command group"""
import sys
import tomllib
from importlib.resources import files

import click
import yaml
from pydantic import ValidationError
from rich.progress import track

from finopspp.models.actions import WeightValidator
from finopspp.models.overrides import OverrideMap
from finopspp.commands import utils


def sub_specification_collector(spec, spec_file):
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
    # if ID is not an int, assume the full sub-specification is given and return
    if not isinstance(spec_id, int):
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


def overrides_collector(spec, profile, override_type='std'):
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
    model = OverrideMap[override_type]

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


def variables_collector(profile, variables):
    """Collect variables name for a profile"""
    # look up variable path, and if none if found
    # return early
    path = utils.variables().get(variables)
    if not path:
        return {}

    # at this point, we expect a real path
    # so just open it and feed it into tomllib
    # to parse
    with open(path, 'rb') as toml_file:
        variables_spec = tomllib.load(toml_file)

    variables_profile = variables_spec.get('profile').get('title')
    if profile != variables_profile:
        click.secho(
            f'Variables="{variables}" requires profile="{variables_profile}". Cannot be used for profile="{profile}"',
            fg='yellow'
        )
        return {}

    return variables_spec


def domain_collector(profile, domain, domain_files, allowed_statuses):
    """Helper designed to collect a domain for a profile
    
    NOTE: Extends the spec's data structure to include capability
    IDs to be added and dropped. Also applies any overrides for the
    profile
    """
    metadata, spec = sub_specification_collector(domain, domain_files)

    # continue early if the Domain Status exists and is not in the
    # allowed statuses list
    status = metadata.get('Status')
    if status and status not in allowed_statuses:
        return {}, {}

    domain_override = overrides_collector(spec, profile)
    spec['domain_drops'] = [drop['ID'] for drop in domain_override.get('DropIDs')]

    if domain_override.get('TitleUpdate'):
        spec['Title'] = domain_override.get('TitleUpdate')

    if domain_override.get('DescriptionUpdate'):
        spec['Description'] = domain_override.get('DescriptionUpdate')

    if spec.get('Capabilities') is None:
        spec['Capabilities'] = []
    if not isinstance(spec['Capabilities'], list):
        click.secho(
            f'Capabilities for domain={spec["Title"]} must be null or a list. Exiting',
            err=True,
            fg='red'
        )
        sys.exit(1)

    spec.get('Capabilities').extend(domain_override.get('AddIDs'))

    return metadata, spec


def capability_collector(profile, capability, capability_files, domain_drops, allowed_statuses):
    """Helper designed to collect a capability for a domain
    
    NOTE: Extends the spec's data structure to include action
    IDs to be added and dropped. Also applies any overrides for
    the profile
    """
    metadata, spec = sub_specification_collector(capability, capability_files)

    # continue early if the Capability ID is one to be dropped
    # NOTE: there might not always be a Capability ID if a profile
    # is made "Manually" or ad-hoc
    capability_id = spec.get('ID')
    if capability_id and capability_id in domain_drops:
        return {}, {}

    # continue early if the Capability Status exists and is not in the
    # allowed statuses list
    status = metadata.get('Status')
    if status and status not in allowed_statuses:
        return {}, {}

    capability_override = overrides_collector(spec, profile)
    spec['capability_drops'] = [drop['ID'] for drop in capability_override.get('DropIDs')]

    if capability_override.get('TitleUpdate'):
        spec['Title'] = capability_override.get('TitleUpdate')

    if capability_override.get('DescriptionUpdate'):
        spec['Description'] = capability_override.get('DescriptionUpdate')

    if spec.get('Actions') is None:
        spec['Actions'] = []
    if not isinstance(spec.get('Actions'), list):
        click.secho(
            f'Actions for capability={spec["TItle"]} must be null or a list. Exiting',
            err=True,
            fg='red'
        )
        sys.exit(1)

    spec.get('Actions').extend(capability_override.get('AddIDs'))

    return metadata, spec


def action_collector(profile, action, action_files, capability_drops, allowed_statuses):
    """Helper designed to collect an action for a capability
    
    NOTE: Also applies any overrides for the profile
    """
    metadata, spec = sub_specification_collector(action, action_files)

    # continue early if the Action ID is one to be dropped
    action_id = spec['ID']
    if action_id in capability_drops:
        return {}, {}

    # continue early if the Action Status exists and is not in the
    # allowed statuses list
    status = metadata.get('Status')
    if status and status not in allowed_statuses:
        return {}, {}

    act_override = overrides_collector(spec, profile, 'action')

    if act_override.get('TitleUpdate'):
        spec['Title'] = act_override.get('TitleUpdate')

    if act_override.get('DescriptionUpdate'):
        spec['Description'] = act_override.get('DescriptionUpdate')

    if act_override.get('SlugUpdate'):
        spec['Slug'] = act_override.get('SlugUpdate')

    return metadata, spec


def specification_collector(profile, profile_spec, allowed_statuses, variables):
    """Helper designed to collect and return a specific format for a top-level
    specification dict
    
    This format is required to work properly with the composers to
    generate the different parts of an assessment.

    NOTE: there is a UI component to this in the form of the Rich Progress Tracker.
    When testing, this will most likely show in your terminal, but can be safely
    ignored.
    """
    domain_files = files('finopspp.specifications.domains')
    capability_files = files('finopspp.specifications.capabilities')
    action_files = files('finopspp.specifications.actions')

    weights = variables.get('weights', {})

    domains = []
    # all profile specs should have a Domains field that is a list by this point.
    # if it doesn't exist, just let it fail out on a python error
    profile_domains = profile_spec['Domains']
    for domain in track(profile_domains, 'Loading profile'):
        capabilities = []

        metadata, spec = domain_collector(
            profile,
            domain,
            domain_files,
            allowed_statuses
        )
        if not spec:
            continue

        domain_id = spec.get('ID')
        domain_title = spec['Title']
        domain_drops = spec['domain_drops']

        serial_number = None
        if isinstance(domain_id, int): # will skip over None type IDs
            domain_id = str(domain_id)
            serial_number = '0'*(3-len(domain_id)) + domain_id

        domains.append({
            'serial_number': serial_number,
            'version': metadata.get('Version'),
            'domain': domain_title,
            'capabilities': capabilities
        })
        for capability in spec.get('Capabilities'):
            actions = []

            metadata, spec = capability_collector(
                profile,
                capability,
                capability_files,
                domain_drops,
                allowed_statuses
            )
            if not spec:
                continue

            capability_id = spec.get('ID')
            capability_title = spec['Title']
            capability_drops = spec['capability_drops']

            serial_number = None
            if isinstance(capability_id, int): # will skip over None type IDs
                capability_id = str(capability_id)
                serial_number = '0'*(3-len(capability_id)) + capability_id

            capabilities.append({
                'serial_number': serial_number,
                'version': metadata.get('Version'),
                'capability': capability_title,
                'actions': actions
            })
            for action in spec.get('Actions'):
                metadata, spec = action_collector(
                    profile,
                    action,
                    action_files,
                    capability_drops,
                    allowed_statuses
                )
                if not spec:
                    continue

                action_id = str(spec['ID'])
                serial_number = '0'*(3-len(action_id)) + action_id

                # if there is a weights override, use that
                # else fallback to the spec default
                weight = spec.get('Weight')

                domain_id = domain_id or domain_title
                capability_id = capability_id or capability_title
                action_id = spec.get('Slug') or action_id
                variable_weight = weights.get(domain_id, {}).get(capability_id, {}).get(action_id)

                if variable_weight is not None:
                    try:
                        weight = WeightValidator.validate_python(variable_weight, strict=True)
                    except ValidationError as val_error:
                        click.secho(
                            f'\nValidation for "{domain_id}.{capability_id}.{action_id}" failed with --\n', fg='yellow'
                        )
                        click.secho(str(val_error), err=True, fg='red')
                        sys.exit(1)


                # since not every action has a title yet, fall back to
                # description when it does not exist or is None.
                actions.append({
                    'action': spec['Title'] or spec.get('Description'),
                    'serial_number': serial_number,
                    'version': metadata.get('Version'),
                    'weights': weight,
                    'formula': spec.get('Formula'),
                    'scoring': spec.get('Scoring'),
                    'weighted score': None
                })

    return domains
