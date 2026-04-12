"""Test composers"""
import json
import os
from importlib.resources import files

import yaml

from finopspp.commands import utils
from finopspp.commands.generate.helpers import domains_collector
from finopspp.composers.helpers import normalize


def test_normalize():
    """Test for the composer util 'normalize'"""
    profile = 'Example Profile'
    domain_files = files('finopspp.specifications.domains')
    cap_files = files('finopspp.specifications.capabilities')
    action_files = files('finopspp.specifications.actions')
    profile_map = utils.profiles()
    with open(profile_map[profile], 'r', encoding='utf-8') as yaml_file:
        profile_yaml = yaml.safe_load(
            yaml_file
        )
        profile_spec = profile_yaml['Specification']
        profile_spec['version'] = profile_yaml['Metadata']['Version']

    # pull in formatted domains data-dict
    domains = domains_collector(
        profile, profile_spec, domain_files, cap_files, action_files
    )
    assert domains is not []

    data_path = os.path.join(os.getcwd(), 'tools/tests/data/expected_example_domains.json')
    with open(data_path, mode='r', encoding='utf-8') as in_file:
        expected_domains = json.load(in_file)

    assert domains == expected_domains

    # now normalize the domains
    normalized_domains = normalize(domains)
    assert normalized_domains is not None

    data_path = os.path.join(os.getcwd(), 'tools/tests/data/expected_example_dataframe.json')
    with open(data_path, mode='r', encoding='utf-8') as in_file:
        expected_dataframe = json.load(in_file)

    json_dataframe = json.loads(normalized_domains.to_json())
    assert json_dataframe == expected_dataframe
