"""Common utilities used by the finopspp commands"""
from importlib.resources import files

import click
import yaml
from click_didyoumean import DYMGroup
from click_help_colors import HelpColorsGroup

# presenters based on answers from
# https://stackoverflow.com/questions/8640959/how-can-i-control-what-scalar-form-pyyaml-uses-for-my-data
def str_presenter(dumper, data):
    """Custom presenter for yaml dumper
    
    Returns:
        dumper (obj) - scalar formatter matching specific string use case (multi-line vs single-line)
    """
    # for long-line or multi-line strings
    if len(data) > 120 or len(data.splitlines()) > 1:
        return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')

    # for standard, single-line strings
    return dumper.represent_scalar('tag:yaml.org,2002:str', data)

yaml.add_representer(str, str_presenter)


def patched_show(self, file=None): # pylint: disable=unused-argument
    """Patched version of UsageError Show
    
    will show UsageError types in nice colors rather than the boring
    default ones
    """
    # pull these imports in here rather than at the top level to keep this
    # patch self contained
    from gettext import gettext as _ # pylint: disable=import-outside-toplevel
    from click_help_colors import _colorize # pylint: disable=import-outside-toplevel

    hint = ""
    if (
        self.ctx is not None
        and self.ctx.command.get_help_option(self.ctx) is not None
    ):
        hint = _('{color_try}').format(
            color_try=_colorize(
                f"Try '{self.ctx.command_path} {self.ctx.help_option_names[0]}' for help",
                'yellow'
            )
        )
        hint = f"{hint}\n"

    if self.ctx is not None:
        click.echo(
            f"{_colorize('Usage', 'magenta')}: {self.ctx.get_usage().split(': ', maxsplit=1).pop()}\n{hint}",
            color=True
        )

    click.echo(
        _("{color_error}: {message}").format(
            color_error=_colorize('Error', 'red'),
            message=self.format_message()
        ),
        color=True,
    )

click.UsageError.show = patched_show


ProfilesMap = {}
def profiles():
    """Return all profiles. Including proposed one"""
    if ProfilesMap:
        return ProfilesMap

    profile_specs = files('finopspp.specifications.profiles')
    for file in profile_specs.iterdir():
        path = profile_specs.joinpath(file.name)
        with open(path, 'r', encoding='utf-8') as yaml_file:
            # we only include profiles in the map that include a title
            title = yaml.safe_load(yaml_file).get('Specification').get('Title')
            if not title:
                continue

            ProfilesMap[title] = path

    return ProfilesMap

SpecSubspecMap = {
    'profiles': 'domains',
    'domains': 'capabilities',
    'capabilities': 'actions',
    'actions': '' # empty string just to help with functionality below
}

class ClickGroup(DYMGroup, HelpColorsGroup):
    """Class to bring together the different Group extensions"""

    def __init__(self, name=None, **kwargs):
        kwargs['help_headers_color'] = 'magenta'
        kwargs['help_options_color'] = 'green'
        super().__init__(
            name=name,
            **kwargs
        )
