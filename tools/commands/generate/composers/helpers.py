"""Shared helper functions used for formatting different generated content"""
import pandas

def normalize(domains):
    """Takes in the domains and returns a dataframe

    the normalization that is done will remove domains and capabilities that
    do not have actions. That means, there can be divergences between the
    framework markdown, which does include these, and the assessment doc that
    does not. They are not included because without actions, nothing can be scored.
    """
    dataframe = pandas.json_normalize(
        domains,
        record_path=['capabilities', 'actions'], # path to actions
        meta=['domain', ['capabilities', 'capability']]
    )
    dataframe.rename(
        columns={
            'capabilities.capability': 'capability',
            'serial_number': 'serial number'
        },
        inplace=True
    )
    dataframe.set_index(['domain', 'capability', 'action'], inplace=True)

    return dataframe
