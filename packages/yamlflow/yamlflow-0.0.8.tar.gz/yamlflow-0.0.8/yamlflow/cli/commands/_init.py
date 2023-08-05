import os
import sys
import shutil
from pathlib import Path

import click
import docker

from yamlflow import dockerfiles, APP_DOCKERFILE
from yamlflow.cli.constants import BASE_DIR


client = docker.from_env()


def _init():
    os.mkdir(BASE_DIR)
    for dockerfile in dockerfiles:
        client.images.build(**dockerfile._asdict(), rm=True)
    shutil.copyfile(f"{APP_DOCKERFILE}/Dockerfile", f"{BASE_DIR}/Dockerfile")


@click.command()
def init():
    """Initialize yamlflow configs"""
    click.echo(click.style("Initializing yamlflow ...", fg="green"))
    start_again = None
    if os.path.exists(BASE_DIR):
        start_again = click.confirm(
            click.style(
                "It seams that yamlflow is already initialized, do you want to override? ",
                fg="red"
            )
        )

    if start_again == None:
        # pure initialization
        _init()
    if start_again == True:
        # directory exists and user does want to override
        shutil.rmtree(BASE_DIR)
        _init()
    if start_again == False:
        # directory exists and user doesn't want ot override
        sys.exit(1)
    