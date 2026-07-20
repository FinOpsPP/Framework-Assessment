"""Command file for the Inventory command"""
from importlib.resources import files

import click
import yaml

from finopspp.models.specs import StatusEnum
from finopspp.commands import utils

@click.group(cls=utils.ClickGroup)
def inventory():
    """Do operations related to the action inventory of profiles"""


@inventory.command(name='list')
@click.option(
    '--show-action-status',
    is_flag=True,
    help='Show status of action'
)
@click.option(
    '--status-by',
    default=None,
    type=click.Choice([enum.value for enum in StatusEnum] + [None]),
    help='Filter by status. Defaults to "None"'
)
@click.option(
    '--profile',
    default='FinOps++',
    type=click.Choice(list(utils.profiles().keys())),
    help='Which assessment profile to list. Takes preference over specification type'
)
def list_inventory(show_action_status, status_by, profile):
    """Inventory fully qualified ID (FQID) per profile

    FQID is of the format Domain.Capability.ActionID-ActionSlug. When a Domain or
    Capability has an ID, that ID will be used in the fully qualified ID. Else the
    Title minus spaces of the Domain or Capability will be used. But only if a FQID
    contains all components that make it up. This will ensure that profiles being
    built out will include all IDs that are defined down to the action level"""
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

                action_status = raw_action['Metadata']['Status']
                if status_by and status_by != action_status:
                    continue

                action_id = raw_action['Specification'].get('Slug') or action_id
                unique_id = f'{domain_id}.{capability_id}.{action_id}'.replace(' ', '')
                if show_action_status:
                    unique_id += f': (Action {action_status})'

                click.echo(unique_id)
