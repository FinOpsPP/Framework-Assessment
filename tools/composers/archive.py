"""Generate Archive files used by FinOps++"""
import datetime
import gzip
import json
import os

import click

def assessment_generate(profile, profile_spec, base_path, domains, suffix):
    """Generate Assessment archive files"""
    click.echo(f'Attempting to historical archive entry for profile={profile}:')
    today = str(datetime.date.today())

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

    # create a new "json" file (really a gzipped file)
    # for a pared-down framework that can be "rehydrated"
    # to an assessment.xlsx if need be.
    archive_path = os.path.join(
        history_path,
        f'{today}{suffix}.json'
    )

    # create compressed file gz file with the json data utf-8 encoded
    with gzip.open(f'{archive_path}.gz', 'wb') as outfile:
        outfile.write(json.dumps(profile_spec).encode('utf-8'))

    click.secho(f'Attempt to generate historical archive "{archive_path}.gz" succeeded', fg='green')
