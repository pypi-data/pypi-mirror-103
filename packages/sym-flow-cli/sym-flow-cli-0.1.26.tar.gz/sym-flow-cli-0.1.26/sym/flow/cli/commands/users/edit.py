import csv

import click

from sym.flow.cli.helpers.csv import set_connectors
from sym.flow.cli.helpers.global_options import GlobalOptions
from sym.flow.cli.helpers.sym_api_client import SymAPIClient
from sym.flow.cli.helpers.sym_api_service import SymAPIService


@click.command(
    name="edit",
    short_help="Edit your Users in a CSV",
)
@click.make_pass_decorator(GlobalOptions, ensure=True)
@click.argument("csv_path", type=click.Path(writable=True))
def users_edit(options: GlobalOptions, csv_path: str) -> None:
    api_service = SymAPIService(api_client=SymAPIClient(url=options.api_url))
    users = api_service.get_user_table_data()
    integrations = api_service.get_user_integrations()
    fields = ["email"] + [x["name"] for x in integrations]

    with open(csv_path, "w") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for user in users:
            writer.writerow(
                dict(
                    {
                        i["integration"]["name"]: i["identifier"]
                        for i in user["identities"]
                    },
                    **{"email": user["email"]},
                )
            )
    set_connectors(csv_path, integrations)
