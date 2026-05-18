"""Helpers file for specifications command group"""
import os
from importlib.resources import files

import yaml
from textual import on
from textual.app import App
from textual.containers import Horizontal, Vertical
from textual.events import Mount
from textual.widgets import Footer, Header, Label, Pretty, SelectionList, Switch
from textual.widgets.selection_list import Selection

from finopspp.models import definitions

def approval(approvers, number, today, specs):
    """Helper to add approval to a specification by number"""
    path = specs.joinpath(f'{number}.yaml')
    with open(path, 'r', encoding='utf-8') as yaml_file:
        specification_data = yaml.safe_load(yaml_file)

    # update basic metadata
    metadata = specification_data['Metadata']
    metadata['Version'] = '1.0.0'
    metadata['Adopted'] = today
    metadata['Modified'] = today
    metadata['Status'] = definitions.StatusEnum.accepted.value

    # now update metadata approvers list with selected approvers
    approval_list = []
    for name, email in approvers:
        approval_list.append(
            {
                'Name': name,
                'Email': email,
                'Date': today
            }
        )
    metadata['Approvers'] = approval_list

    with open(path, 'w', encoding='utf-8') as yaml_file:
        yaml.dump(
            specification_data,
            yaml_file,
            default_flow_style=False,
            sort_keys=False,
            indent=2,
            width=120 # will always be longer that what is allowed by yamllint
        )

def approval_options(specification_type):
    """Helper to pull information on what should should be approved"""
    spec_options = {}
    specs = files(f'finopspp.specifications.{specification_type}')
    for spec in specs.iterdir():
        number, _ = os.path.splitext(spec.name)

        # skip over example 0 specs
        if not int(number):
            continue

        path = specs.joinpath(spec.name)

        # load up previous data first
        with open(path, 'r', encoding='utf-8') as yaml_file:
            specification_data = yaml.safe_load(yaml_file)

        # check if status is Proposed, and if it is, add as option to approve
        if specification_data['Metadata']['Status'] != definitions.StatusEnum.proposed.value:
            continue

        spec = specification_data['Specification']

        # only accept specifications with titles
        title = spec['Title']
        if not title:
            continue

        # new a few additional filters for actions
        if specification_type == 'actions':
            # skip if weight is still 0 or does not exist.
            if not spec['Weight']:
                continue

            # also skip if the last score is not 10
            last_score = spec['Scoring'].pop()
            if last_score['Score'] != 10:
                continue

        spec_options[title] = number

    return spec_options

def approval_selector(options, specification_type, approval_map):
    """Helper for building the selector interface"""
    selection_list = []
    for title, serial_number in options.items():
        selection_list.append(Selection(title, serial_number))

    # now we create the terminal app that allows selections
    class Approvals(App):
        """Terminal application

        that will provide an selection inferface for specifications to approve"""
        CSS_PATH = "approvals.tcss"

        def compose(self):
            """Layout of app in terminal"""
            yield Header()
            with Vertical():
                yield Label(
                    'Please select from this list and press [b]ctrl-q[/] to save & exit'
                )
                with Horizontal():
                    yield SelectionList(*selection_list)
                    yield Pretty(approval_map[specification_type])
                with Horizontal(id='horizontal-two'):
                    yield Label('(De)Select All:')
                    yield Switch()
            yield Footer()

        def on_mount(self):
            """What to do when the app is loaded"""
            self.query_one(
                SelectionList
            ).border_title = 'Which specifications should be approved?'
            self.query_one(
                Pretty
            ).border_title = 'Selected specifications (by ID)'
            self.title = f'Approvals for "{specification_type.title()}"'

        @on(Mount)
        @on(SelectionList.SelectedChanged)
        def update_selected_view(self):
            """How the view should update on selection changes"""
            approval_map[specification_type] = self.query_one(SelectionList).selected
            self.query_one(
                Pretty
            ).update(
                approval_map[specification_type]
            )

        @on(Switch.Changed)
        def update_switched_view(self):
            """How the view should update on switch changes"""
            self.query_one(SelectionList).toggle_all()


    Approvals().run()
