import csv
import os
import sys

import click

from sym.flow.cli.helpers.csv import set_connectors
from sym.flow.cli.helpers.global_options import GlobalOptions
from sym.flow.cli.helpers.sym_api_client import SymAPIClient
from sym.flow.cli.helpers.sym_api_service import SymAPIService


@click.command(name="template", short_help="Create a CSV template for new Users.")
@click.make_pass_decorator(GlobalOptions, ensure=True)
@click.argument("path", type=click.Path(writable=True))
@click.option("-f/--force", default=False)
def users_template(options: GlobalOptions, path: str, force: bool) -> None:
    api_service = SymAPIService(api_client=SymAPIClient(url=options.api_url))
    integrations = api_service.get_user_integrations()
    fields = ["email"] + [x["name"] for x in integrations]

    if not force and os.path.exists(path):
        click.secho(f"File already exists: '{path}'", fg="red", bold=True)
        click.secho("Try running `symflow users template --force PATH`.", fg="cyan")
        sys.exit(1)

    with open(path, "w") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()

    set_connectors(path, integrations)
