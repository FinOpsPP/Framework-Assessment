"""Helpers file for generate command group"""
import sys

import click
import yaml
from pydantic import ValidationError
from rich.progress import track

from finopspp.models import definitions

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

def domains_collector(profile, profile_spec, domain_files, cap_files, action_files):
    """Helper designed to collect and return a specific format for a domains dict
    
    This format is required to work properly with the composers to
    generate the different parts of an assessment.

    NOTE: there is a UI component to this in the form of the Rich Progress Tracker.
    When testing, this will most likely show in your terminal, but can be safely
    ignored.
    """
    domains = []
    for domain in track(profile_spec.get('Domains'), 'Loading profile'):
        capabilities = []

        metadata, spec = sub_specification_collector(domain, domain_files)
        domain_override = overrides_collector(spec, profile)
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

            metadata, spec = sub_specification_collector(capability, cap_files)

            # continue early if the Capability ID is one to be dropped
            spec_id = spec.get('ID')
            if spec_id and spec_id in domain_drops:
                continue

            cap_override = overrides_collector(spec, profile)
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
                metadata, spec = sub_specification_collector(action, action_files)

                # continue early if the Action ID is one to be dropped
                spec_id = spec.get('ID')
                if spec_id and spec_id in cap_drops:
                    continue

                act_override = overrides_collector(spec, profile, 'action')

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

        return domains
