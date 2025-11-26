"""Migration of info from g-sheets"""
import datetime
import re
from importlib.resources import files

import pandas
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

def get_data():
    """Return data used to update sheets"""
    # Authenticate and create the client
    client = gspread.oauth(
        credentials_filename='credentials.json'
    )

    # Open the spreadsheet
    sheet = client.open(
        'FinOps KPI vs FOCUS Use Cases'
    )
    mappings = sheet.worksheet('Mapping')

    # Load data and print
    data = mappings.get_all_records()
    return pandas.DataFrame(data)

def process_row(row, specification_files, today):
    """Process the row and update the data in the yaml files"""
    # only work on rows that have scoring
    if not row['Scoring']:
        return False

    spec_id = str(row['Code'])
    serial_number = '0'*(3-len(spec_id)) + spec_id
    specification_file = specification_files.joinpath(f'{serial_number}.yaml')

    data = None
    with open(specification_file, 'r') as file:
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
        formula = re.sub(r'\d -', '*', formula)
        data['Specification']['Formula'] = formula

    # finally write backout
    with open(specification_file, 'w') as yaml_file:
        yaml.dump(
            data,
            yaml_file,
            default_flow_style=False,
            sort_keys=False,
            indent=2
        )

    return True



def main():
    """Main function"""
    today = str(datetime.date.today())
    specification_files = files('finopspp.specifications.actions')
    dataframe = get_data()
    for _, row in dataframe.iterrows():
        process_row(row, specification_files, today)

main()