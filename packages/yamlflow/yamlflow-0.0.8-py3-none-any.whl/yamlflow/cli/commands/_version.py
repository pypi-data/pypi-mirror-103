import click

from yamlflow import __version__

@click.command()
def version():
    """Version of yamlflow"""
    click.echo(f"""{click.style('yamlflow', fg='green')} ({click.style(f'{__version__}', fg='blue')})""")