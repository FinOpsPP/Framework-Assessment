"""Markdown excel files used for FinOps++"""
import os

import click
from jinja2 import Environment, PackageLoader

Templates = PackageLoader('finopspp', 'templates')

def assessment_generate(profile_id, profile, base_path, domains):
    """Generate Assessment markdown files"""
    # pull in template and specification files for given specification type
    env = Environment(loader=Templates)
    template = env.get_template('framework.md.j2')

    # render file before writing it
    # include profile title with linkable ID.
    click.echo(f'Attempting to generate framework for profile={profile}:')
    spec_id = str(profile_id)
    file = '0'*(3-len(spec_id)) + spec_id
    profile_title = f'<a href="/components/profiles/{file}.md">{file}</a>: {profile}'
    output = template.render(profile=profile_title, domains=domains)

    # finally, create framework markdown for this profile
    # from the rendered output
    out_path = os.path.join(
        base_path,
        'framework.md'
    )
    with open(out_path, 'w', encoding='utf-8') as outfile:
        outfile.write(output)

    click.secho(f'Attempt to generate framework markdown "{out_path}" succeeded', fg='green')


def components_generate(specification_type, spec):
    """Generate Components markdown files"""
    # pull in template and specification files for given specification type
    env = Environment(loader=Templates)
    template = env.get_template(f'{specification_type}.md.j2')

    output = template.render(spec=spec)

    # finally, write out rendered output to file
    # make sure serialized ID is the same as the one
    # used in the specification files.
    spec_id = spec.get('ID')
    spec_id = str(spec_id)
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

    with open(out_path, 'w', encoding='utf-8') as outfile:
        outfile.write(output)

    click.secho(f'Attempt to generate "{out_path}" succeeded', fg='green')
