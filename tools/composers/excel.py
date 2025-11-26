"""Generate excel files used for FinOps++"""
import os

import click
import pandas

from finopspp.composers import helpers

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

        overview_sheet.write_formula('A2', f'=SUM(Scoring!E2:E{dataframe.shape[0]+1})')
        overview_sheet.write_number('B2', 10)
        overview_sheet.write_formula('C2', f'=SUM(Scoring!H2:H{dataframe.shape[0]+1})/A2')
        overview_sheet.write_formula('D2', '=B2-C2')

        # overview sheet charts
        domain_size = dataframe.groupby(level=0).size()

        overview_sheet.write_column('AA1', domain_size.index)
        overview_sheet.write_column('BB1', domain_size)

        domain_chart = workbook.add_chart({'type': 'doughnut'})
        domain_chart.add_series({
            'name': f'Domains for {profile} by Action count',
            'categories': f'=Overview!$AA$1:$AA${len(domain_size)}',
            'values': f'=Overview!$BB$1:$BB${len(domain_size)}',
            'data_labels': {
                'value': True
            }
        })
        domain_chart.set_style(37)

        overview_sheet.insert_chart('A4', domain_chart)

        overview_sheet.autofit()
        overview_sheet.activate()

        # add chart sheet with percentage difference between max
        # score and the calculated score
        score_diff_chart = workbook.add_chart({'type': 'pie'})
        score_diff_chart.add_series({
            'categories': '=Overview!$C$1:$D$1',
            'values':     '=Overview!$C$2:$D$2',
            'data_labels': {
                'percentage': True
            }
        })
        score_diff_chart.set_title({
            'name': 'Attained Percentage of Maximum Possible Score'
        })
        score_diff_chart.set_style(37)

        scoring_chart_sheet = workbook.add_chartsheet('Attained Percentage')
        scoring_chart_sheet.set_chart(score_diff_chart)

        # pandas uses an incredible opinionated format for indices and headers
        # which for this project is sufficient to meet the needs of the assessments.
        # as such, will not try to update the index or header formatting given by pandas
        dataframe.to_excel(
            writer, sheet_name='Scoring'
        )

        # format cells for scoring sheet
        scoring_sheet = writer.sheets['Scoring']
        text_wrap_format = workbook.add_format({'text_wrap': True})
        scoring_sheet.set_column('F:F', 20, text_wrap_format)

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

        # Autofit the scoring sheet and fix warning.
        scoring_sheet.autofit()
        scoring_sheet.ignore_errors({'number_stored_as_text': 'D:D'})
        click.secho(f'Attempt to generate assessment.xlsx "{out_path}" succeeded', fg='green')
