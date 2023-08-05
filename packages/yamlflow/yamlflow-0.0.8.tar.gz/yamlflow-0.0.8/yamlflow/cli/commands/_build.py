import os
import shutil

import click
import docker

from yamlflow.cli.manifest import Manifest
from yamlflow.cli.constants import(
    BASE_DIR,
    MODEL_DIR,
    SERVICE_DIR,
    MANIFEST_FILE
    )


client = docker.from_env()

_copy_ignore = shutil.ignore_patterns('*.pyc', "__pycache__", "objects")

@click.command()
def build():
    """Build a deployable unit, based on initialization"""
    manifest = Manifest(MANIFEST_FILE)
    TMP_MODEL_DIR = os.path.join(BASE_DIR, MODEL_DIR)
    TMP_SERVICE_DIR = os.path.join(BASE_DIR, SERVICE_DIR)
    shutil.copytree(MODEL_DIR, TMP_MODEL_DIR, ignore=_copy_ignore)
    shutil.copytree(SERVICE_DIR, TMP_SERVICE_DIR, ignore=_copy_ignore)
    build_info = manifest.build_info()
    click.echo(
        click.style(
            f"""
            Building image ....
            Service: {build_info["tag"]}
            Backend: {build_info["buildargs"]["BACKEND"]}
            """,
            fg="blue"
        )
    )
    try:
        client.images.build(**build_info, rm=True)
    except (TypeError, docker.errors.APIError, docker.errors.BuildError) as err:
        print(f"Failed building image: {err}")
    finally:
        shutil.rmtree(TMP_MODEL_DIR)
        shutil.rmtree(TMP_SERVICE_DIR)
