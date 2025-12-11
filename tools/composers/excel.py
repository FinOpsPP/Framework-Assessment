"""Generate excel files used for FinOps++"""
import os

import click
import pandas

from finopspp.composers import helpers

def create_overview_sheet(profile, dataframe, workbook):
    """Create overview sheet"""
    overview_sheet = workbook.add_worksheet('Overview')
    overview_sheet.add_table('A1:D2', {
        'style': 'Table Style Light 11',
        'autofilter': False,
        'columns': [
            {'header': 'Sum of Weights'},
            {'header': 'Maximum Possible Score'},
            {'header': 'Calculated Weighted Average Score'},
            {'header': 'Difference from Maximum Score'}
        ]
    })

    shape = dataframe.shape[0]
    overview_sheet.write_formula('A2', f'=SUM(Scoring!E2:E{shape + 1})') # sum of weights
    overview_sheet.write_number('B2', 10) # max score
    overview_sheet.write_formula('C2', f'=SUM(Scoring!H2:H{shape + 1})/A2') # average score
    overview_sheet.write_formula('D2', '=B2-C2') # score diff (max - average)

    # overview domain table
    domains_size = dataframe.groupby(level=0).size()

    domain_shift = 4 + len(domains_size)
    overview_sheet.add_table(f'A4:B{domain_shift}', {
        'style': 'Table Style Light 11',
        'autofilter': False,
        'data': domains_size.to_frame().to_records(),
        'columns': [
            {'header': 'Domain'},
            {'header': 'Action Count'}
        ]
    })
    overview_sheet.write_formula(
        f'B{domain_shift + 1}',
        f'=SUM(Overview!$B$5:$B${domain_shift})'
    )

    weight_col = f'Scoring!E2:E{shape + 1}'
    index_col = f'Scoring!I2:I{shape + 1}'
    score_col = f'Scoring!H2:H{shape + 1}'
    for index in range(5, domain_shift + 1):
        overview_sheet.write_formula(
            f'U{index}',
            f'=SUMIF({index_col},A{index},{score_col})/SUMIF({index_col},A{index},{weight_col})'
        )

    # overview capabilities table
    capabilities_size = dataframe.groupby(level=1).size()

    extended_shift = domain_shift + 3
    capabilities_shift = extended_shift + len(capabilities_size)
    overview_sheet.add_table(f'A{extended_shift}:B{capabilities_shift}', {
        'style': 'Table Style Light 11',
        'autofilter': False,
        'data': capabilities_size.to_frame().to_records(),
        'columns': [
            {'header': 'Capability'},
            {'header': 'Action Count'}
        ]
    })
    overview_sheet.write_formula(
        f'B{capabilities_shift + 1}',
        f'=SUM(Overview!$B${extended_shift + 1}:$B${capabilities_shift})'
    )

    index_col = f'Scoring!J2:J{shape + 1}'
    for index in range(extended_shift + 1, capabilities_shift + 1):
        overview_sheet.write_formula(
            f'U{index}',
            f'=SUMIF({index_col},A{index},{score_col})/SUMIF({index_col},A{index},{weight_col})'
        )

    # set charts
    score_diff_chart = workbook.add_chart({'type': 'pie'})
    score_diff_chart.add_series({
        'name': f'Attained Percentage of Maximum Possible Score for {profile}',
        'categories': '=Overview!$C$1:$D$1',
        'values': '=Overview!$C$2:$D$2',
        'data_labels': {
            'percentage': True
        }
    })
    score_diff_chart.set_style(37)

    overview_sheet.insert_chart('C4', score_diff_chart)

    # hide columns that should be hidden
    #overview_sheet.set_column('G:XFD', None, None, {'hidden': True})

    overview_sheet.autofit()
    overview_sheet.activate()


def create_domains_chart(dataframe, workbook):
    """Setup the sheet for overall score per each domain"""
    domains_size = dataframe.groupby(level=0).size()

    domain_shift = 4 + len(domains_size)
    domain_chart = workbook.add_chart({'type': 'radar', 'subtype': 'filled'})
    domain_chart.add_series({
        'name': 'Attained Maturity by Domain',
        'categories': f'=Overview!$A$5:$A${domain_shift}',
        'values': f'=Overview!$U$5:$U${domain_shift}'
    })
    domain_chart.set_style(37)
    domain_chart.set_legend({'none': True})

    domain_chart_sheet = workbook.add_chartsheet('Maturity - Domains')
    domain_chart_sheet.set_chart(domain_chart)


def create_capabilities_chart(dataframe, workbook):
    """Setup the sheet for capabilities for all actions"""
    domains_size = dataframe.groupby(level=0).size()

    domain_shift = 4 + len(domains_size)
    capabilities_size = dataframe.groupby(level=1).size()

    extended_shift = domain_shift + 3
    capabilities_shift = extended_shift + len(capabilities_size)
    capabilities_chart = workbook.add_chart({'type': 'radar', 'subtype': 'filled'})
    capabilities_chart.add_series({
        'name': 'Attained Maturity by Capability',
        'categories': f'=Overview!$A${extended_shift + 1}:$A${capabilities_shift}',
        'values': f'=Overview!$U${extended_shift + 1}:$U${capabilities_shift}'
    })
    capabilities_chart.set_style(37)
    capabilities_chart.set_legend({'none': True})

    capabilities_chart_sheet = workbook.add_chartsheet('Maturity - Capabilities')
    capabilities_chart_sheet.set_chart(capabilities_chart)



def format_scoring_sheet(scoring_sheet, dataframe, workbook):
    """Setup main sheet of assessment, includes all score formatting"""
    # format cells for scoring sheet
    text_wrap_format = workbook.add_format({'text_wrap': True})
    scoring_sheet.set_column('F:F', None, text_wrap_format)

    link_format = workbook.add_format({
        'align': 'center',
        'bold': True,
        'underline': True,
        'font_color': 'blue'
    })

    for counter, (_, row) in enumerate(dataframe.iterrows(), start=2):
        scores = [f'{scoring['Score']}: {scoring["Condition"]}' for scoring in row.scoring]
        scoring_sheet.write(f'G{counter}', scores[0]) # overwrite with correct default scores
        scoring_sheet.data_validation(f'G{counter}', {
            'validate' : 'list',
            'source': scores
        })
        scoring_sheet.write_formula(
            f'H{counter}', f'=E{counter}*VALUE(LEFT(G{counter}, FIND(":", G{counter})-1))'
        )

        # overwrite serial numbers with links to github markdown pages for the numbers
        serial_number = row['serial number']
        scoring_sheet.write_url(
            f'D{counter}',
            f'https://github.com/FinOpsPP/Framework-Assessment/tree/main/components/actions/{serial_number}.md',
            link_format,
            string=serial_number
        )

    # hide columns that should be hidden
    scoring_sheet.set_column('I:XFD', None, None, {'hidden': True})

    # Autofit the scoring sheet and fix warning.
    scoring_sheet.autofit()
    scoring_sheet.ignore_errors({'number_stored_as_text': 'D:D'})


def assessment_generate(profile, base_path, domains):
    """Generate Excel files"""
    click.echo(f'Attempting to generate assessment.xlsx for profile={profile}:')
    dataframe = helpers.normalize(domains)

    out_path = os.path.join(
        base_path,
        'assessment.xlsx'
    )
    with pandas.ExcelWriter(out_path, engine='xlsxwriter') as writer:
        workbook = writer.book

        # write Overview sheet first
        create_overview_sheet(profile, dataframe, workbook)

        # domain maturity chart
        create_domains_chart(dataframe, workbook)

        # capability maturity chart
        create_capabilities_chart(dataframe, workbook)

        # pandas uses an incredible opinionated format for indices and headers
        # which, luckily, for this project is sufficient to meet the needs of the
        # assessments.
        # As such, will not try to update the index or header formatting given by pandas
        dataframe['_domain'] = dataframe.index.get_level_values(0)
        dataframe['_capability'] = dataframe.index.get_level_values(1)
        dataframe.to_excel(
            writer, sheet_name='Scoring'
        )
        scoring_sheet = writer.sheets['Scoring']

        # now format the scoring sheet
        format_scoring_sheet(scoring_sheet, dataframe, workbook)

        click.secho(f'Attempt to generate assessment.xlsx "{out_path}" succeeded', fg='green')
