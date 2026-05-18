"""Markdown excel files used for FinOps++"""
import datetime
import os

import click
from jinja2 import Environment, PackageLoader

Templates = PackageLoader('finopspp', 'templates')

def assessment_generate(profile, profile_spec, base_path, domains, suffix):
    """Generate Assessment markdown files"""
    click.echo(f'Attempting to generate framework for profile={profile}:')

    # pull in template and specification files for given specification type
    env = Environment(loader=Templates, keep_trailing_newline=True)
    template = env.get_template('framework.md.j2')

    # get profile id from spec
    profile_id = str(profile_spec['ID'])

    # include profile title with linkable ID.
    file = '0'*(3-len(profile_id)) + profile_id
    profile_title = f'<a href="/components/profiles/{file}.md">{file}</a>: {profile}'
    profile_spec['profile_link_title'] = profile_title

    # assessment link
    assessment_link = f'<a href="/assessments/{profile}/assessment.xlsx">assessment.xlsx</a>'

    # render file before writing it
    output = template.render(
        today=datetime.date.today(),
        profile=profile_spec,
        domains=domains,
        assessment=assessment_link
    )

    # finally, create framework markdown for this profile
    # from the rendered output
    out_path = os.path.join(
        base_path,
        f'framework{suffix}.md'
    )
    with open(out_path, 'w', encoding='utf-8') as outfile:
        outfile.write(output)

    click.secho(f'Attempt to generate framework markdown "{out_path}" succeeded', fg='green')


def components_generate(specification_type, spec):
    """Generate Components markdown files"""
    # write out rendered output to file
    # make sure serialized ID is the same as the one
    # used in the specification files.
    spec_id = str(spec['ID'])
    file_prefix = '0'*(3-len(spec_id)) + spec_id
    out_path = os.path.join(
        os.getcwd(),
        'components',
        specification_type,
        f'{file_prefix}.md'
    )
    click.echo(
        f'Attempting to generate component "{out_path}" for specification-type={specification_type}:'
    )

    # pull in template and specification files for given specification type
    env = Environment(loader=Templates)
    template = env.get_template(f'{specification_type}.md.j2')

    # render file before writing it
    output = template.render(spec=spec)

    # finally, write specific component markdown
    # from the rendered output
    with open(out_path, 'w', encoding='utf-8') as outfile:
        outfile.write(output)

    click.secho(f'Attempt to generate "{out_path}" succeeded', fg='green')


def schemas_generate(schemas):
    """Generate Document markdown files"""
    out_path = os.path.join(
        os.getcwd(),
        'specifications',
        'README.md'
    )
    click.echo(
        f'Attempting to generate schemas document "{out_path}":'
    )

    # pull in template and specification files for given specification type
    env = Environment(loader=Templates)
    template = env.get_template('schemas.md.j2')

    # render file before writing it
    output = template.render(schemas=schemas)

    # finally, write README.md for the schemas
    # from the rendered output
    with open(out_path, 'w', encoding='utf-8') as outfile:
        outfile.write(output)

    click.secho(f'Attempt to generate "{out_path}" succeeded', fg='green')
