import click
from tabulate import tabulate

from sym.flow.cli.helpers.global_options import GlobalOptions
from sym.flow.cli.helpers.sym_api_client import SymAPIClient
from sym.flow.cli.helpers.sym_api_service import SymAPIService


@click.command(
    name="list",
    short_help="List your Users",
)
@click.make_pass_decorator(GlobalOptions, ensure=True)
def users_list(options: GlobalOptions) -> None:
    api_service = SymAPIService(api_client=SymAPIClient(url=options.api_url))
    users = api_service.get_user_table_data()
    integrations = api_service.get_user_integrations()
    fields = ["email"] + [x["name"] for x in integrations]

    rows = []
    for user in users:
        row_data = dict(
            {i["integration"]["name"]: i["identifier"] for i in user["identities"]},
            **{"email": user["email"]},
        )
        rows.append([row_data.get(f, "") for f in fields])

    click.echo(tabulate(rows, headers=fields) + "\n")
