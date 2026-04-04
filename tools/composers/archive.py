"""Generate Archive files used by FinOps++"""
import datetime
import os
import json
import zipfile

import click

def action_cleaner(domains):
    """helper to clean up actions and leave only fields useful for archives"""
    for domain in domains:
        for capability in domain.get('capabilities'):
            for action in capability.get('actions'):
                del action['weights']
                del action['formula']
                del action['scoring']
                del action['weighted score']

def assessment_generate(profile, profile_spec, base_path, domains):
    """Generate Assessment archive files"""
    click.echo(f'Attempting to historical archive entry for profile={profile}:')
    today = datetime.date.today()

    # check if assessment history directory exists for this profile
    # and if it does not create it
    history_path = os.path.join(
        base_path,
        'history'
    )
    if not os.path.exists(history_path):
        os.mkdir(history_path)

    # as the archive is designed to be run last
    # we will physical change the data for
    # profile_spec and domains. This will mean
    # that they will not be the same as when they
    # were passed in to this function.
    del profile_spec['profile_link_title']
    del profile_spec['Description']
    del profile_spec['Domains']

    profile_id = str(profile_spec.pop('ID'))
    serial_number = '0'*(3-len(profile_id)) + profile_id
    profile_spec['serial_number'] = serial_number
    profile_spec['profile'] = profile_spec.pop('Title')
    profile_spec['version'] = profile_spec.pop('version')
    profile_spec['domains'] = domains

    # clean actions setup on profile_spec
    action_cleaner(domains)

    # create a new json file for a pared-down framework
    framework_path = os.path.join(
        history_path,
        'framework.json'
    )
    with open(framework_path, 'w', encoding='utf-8') as outfile:
        json.dump(profile_spec, outfile)

    # now create the assessment zip for the given day
    archive_path = os.path.join(
        history_path,
        f'{today}.zip'
    )
    with zipfile.ZipFile(archive_path, 'w') as archive_file:
        archive_file.write(framework_path)
        archive_file.write(os.path.join(base_path, 'assessment.xlsx'))

    # finally clean out framework.json that was created
    os.remove(framework_path)
    click.secho(f'Attempt to generate historical archive "{archive_path}" succeeded', fg='green')
