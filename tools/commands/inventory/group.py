"""Command file for the Inventory command"""
from importlib.resources import files

import click
import yaml

from finopspp.models.specs import StatusEnum
from finopspp.commands import utils
from finopspp.commands.generate import helpers as generate_helpers

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
    help='Filter on status per component. Defaults to "None"'
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
        profile_id = spec.get('ID')

    domain_files = files('finopspp.specifications.domains')
    capability_files = files('finopspp.specifications.capabilities')
    action_files = files('finopspp.specifications.actions')

    allowed_statuses = [
        StatusEnum.accepted.value,
        StatusEnum.proposed.value,
        StatusEnum.deprecated.value
    ]
    if status_by:
        allowed_statuses = [status_by]

    click.echo(f'Fully qualified IDs for {profile}. Profile ID: {profile_id}')
    for domain in spec.get('Domains'):
        metadata, spec = generate_helpers.domain_collector(
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
                metadata, spec = generate_helpers.action_collector(
                    profile,
                    action,
                    action_files,
                    capability_drops,
                    allowed_statuses
                )
                if not spec:
                    continue

                action_id = spec['ID']
                if not action_id:
                    continue

                action_id = spec.get('Slug') or str(action_id)
                unique_id = f'{domain_id}.{capability_id}.{action_id}'.replace(' ', '')
                if show_action_status:
                    unique_id += f': (Action {metadata["Status"]})'

                click.echo(unique_id)
