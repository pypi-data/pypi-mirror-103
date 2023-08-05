import click

from yamlflow.cli.commands import (
    version,
    init,
    build
)

@click.group()
def main():
    """Yet Another ML flow"""
    pass


main.add_command(version)
main.add_command(init)
main.add_command(build)
