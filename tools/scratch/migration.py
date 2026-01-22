"""Migration of info from different spreadsheets.

This should not be used as it will change frequently to meet the needs
of the project of migrating data from every changing spreadsheets to
the specifications for mass migrations of data.
"""
import argparse
import datetime
import re
from importlib.resources import files

import pandas
import semver
import gspread
import yaml

# presenters based on answers from
# https://stackoverflow.com/questions/8640959/how-can-i-control-what-scalar-form-pyyaml-uses-for-my-data 
def str_presenter(dumper, data):
    # for multi-line strings
    if len(data.splitlines()) > 1:
        return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')

    # for standard strings
    return dumper.represent_scalar('tag:yaml.org,2002:str', data)

yaml.add_representer(str, str_presenter)

def get_data_gsheet():
    """Return gsheet data used to update sheets"""
    # Authenticate and create the client
    client = gspread.oauth(
        credentials_filename='credentials.json'
    )

    # Open the spreadsheet
    sheet = client.open(
        'FinOps KPI vs FOCUS Use Cases'
    )
    mappings = sheet.worksheet('Mapping')

    # Load data and return
    data = mappings.get_all_records()
    return pandas.DataFrame(data)


def get_data_local():
    """Pull in data from a specific file in scratch"""
    # Configure the spreadsheet location
    # make sure the file is renamed to updates.xlsx before running
    scratch_files = files('finopspp.scratch')
    updates = scratch_files.joinpath('updates.xlsx')

    # Load data and return
    # make sure to check the index before running local
    return pandas.read_excel(updates, index_col=[0, 1, 2])


def process_row_gsheet(row, specification_files, today):
    """Process gsheet the row and update the data in the yaml files"""
    # only work on rows that have scoring
    if not row['Scoring']:
        return False

    spec_id = str(row['Code'])
    serial_number = '0'*(3-len(spec_id)) + spec_id
    specification_file = specification_files.joinpath(f'{serial_number}.yaml')

    data = None
    with open(specification_file, 'r', encoding='utf-8') as file:
        data = yaml.safe_load(file)

    # set metadata for updated actions
    # set version
    data['Metadata']['Version'] = '1.0.0'

    # set approvers
    data['Metadata']['Approvers'] = [
        {'Name': 'Victoria Levy', 'Email': 'victoria.levy@alteryx.com', 'Date': today},
        {'Name': 'Andrew Quigley', 'Email': 'andrewquigley@northwesternmutual.com', 'Date': today}
    ]

    # set approval date
    data['Metadata']['Adopted'] = today

    # set status
    data['Metadata']['Status'] = 'Adopted'

    # Now set the specification data
    # set default weight
    data['Specification']['Weight'] = 1.0

    # create scoring list
    scoring_list = []
    data['Specification']['Scoring'] = scoring_list
    for score in row['Scoring'].splitlines():
        split_score = score.split(') ', maxsplit=1)
        scoring_list.append({
            'Score': int(split_score[0]),
            'Condition': split_score[1]
        })

    # set formula
    if row['Measurement']:
        formula = row['Measurement']
        # this might change based on how the sheet specified the formula
        # be careful.
        formula = re.sub(r'\d -', '*', formula)
        data['Specification']['Formula'] = formula

    # finally write back out
    with open(specification_file, 'w', encoding='utf-8') as yaml_file:
        yaml.dump(
            data,
            yaml_file,
            default_flow_style=False,
            sort_keys=False,
            indent=2
        )

    return True


def process_row_local(row, specification_files, today):
    """Process local the row and update the data in the yaml files"""
    # only work on rows that have an Action Name
    if not isinstance(row['Action Name'], str):
        return False

    spec_id, spec_name = row['Action Name'].split(':', maxsplit=1)
    serial_number = '0'*(3-len(spec_id)) + spec_id
    specification_file = specification_files.joinpath(f'{serial_number}.yaml')

    data = None
    with open(specification_file, 'r', encoding='utf-8') as file:
        data = yaml.safe_load(file)

    # set metadata for updated actions
    # set version
    spec_version = semver.Version.parse(data['Metadata']['Version'])
    data['Metadata']['Version'] = str(spec_version.bump_minor())

    # set approval date
    data['Metadata']['Modified'] = today

    # set new titles
    data['Specification']['Title'] = spec_name.strip()

    # set new slug
    data['Specification']['Slug'] = row['Action Slug'].strip()

    # finally write back out
    with open(specification_file, 'w', encoding='utf-8') as yaml_file:
        yaml.dump(
            data,
            yaml_file,
            default_flow_style=False,
            sort_keys=False,
            indent=2
        )

    return True


def main(local=False):
    """Main function"""
    today = str(datetime.date.today())
    specification_files = files('finopspp.specifications.actions')

    # pull data based on if we are pulling data from gsheet or locally
    # and configure how that will be processed
    dataframe = None
    process_row = None
    if not local:
        dataframe = get_data_gsheet()
        process_row = process_row_gsheet
    else:
        dataframe = get_data_local()
        process_row = process_row_local

    # process data
    for _, row in dataframe.iterrows():
        process_row(row, specification_files, today)


# set args and run main
parser = argparse.ArgumentParser(description ='Migrate Specification Data')
parser.add_argument(
    '--local',
    action='store_true',
    help='Using GSheets or a Local Excel doc. Local should be stored in scratch'
)
args = parser.parse_args()
main(local=args.local)
