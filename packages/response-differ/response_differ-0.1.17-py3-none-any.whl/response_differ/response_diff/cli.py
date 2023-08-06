import click
import yaml

from ..cheks import check_diff_responses
from ..exceptions import get_grouped_exception
from ..play import Replayed, replay


def bold(message):
    return click.style(message, bold=True)


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
@click.version_option()
def differ():
    """Command line tool for testing your web application"""


@differ.command()
@click.argument("cassette_path", type=click.Path(exists=True))
@click.option("--uri", help="A regexp that filters interactions by their request URI.", required=False, type=str)
@click.option("--diff", '-d',  help="Comparing new response with the old", required=False, type=bool)
@click.option("--config", '-c',  help="Comparing new response with the old", required=False, type=click.Path())
def run(cassette_path, status=None, uri=None, diff=False, config=None):
    click.secho(f"{bold('Replaying cassette')}: {cassette_path}")
    with open(cassette_path) as fd:
        cassette = yaml.load(fd, Loader=yaml.SafeLoader)
    click.secho(f"{bold('Total interactions')}: {len(cassette['interactions'])}\n")
    for replayed in replay(cassette, cassette_path, status=status, uri=uri, diff=diff):
        click.secho(f"  {bold('ID')}              | {replayed.interaction['id']}")
        click.secho(f"  {bold('URI')}             | {replayed.interaction['request']['uri']}")
        if replayed.interaction.get('response'):
            click.secho(f"  {bold('Old status code')} | {replayed.interaction['response']['status']['code']}")
        if hasattr(replayed, 'response'):
            click.secho(f"  {bold('New status code')} | {replayed.response.status_code}")
        click.secho(f"  {bold('Old request')}     | {replayed.interaction['request']}")
        if hasattr(replayed, 'response'):
            click.secho(f"  {bold('New request')}     | {replayed.response.request.body}\n")
    if Replayed.errors:
        exception_cls = get_grouped_exception(*Replayed.errors)
        raise exception_cls(Replayed.errors)
    if diff:
        with open(config) as fd2:
            Replayed.config =yaml.load(fd2, Loader=yaml.SafeLoader)
        check_diff_responses()
