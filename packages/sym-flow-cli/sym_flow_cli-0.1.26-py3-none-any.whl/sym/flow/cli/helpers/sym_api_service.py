from enum import Enum
from typing import Dict, List, Optional

from sym.flow.cli.errors import SymAPIRequestError, SymAPIUnknownError, UnknownOrgError
from sym.flow.cli.helpers.sym_api_client import BaseSymAPIClient
from sym.flow.cli.models import Organization


class ConnectorType(Enum):
    SLACK = "slack"


class SymAPIService:
    def __init__(self, api_client: BaseSymAPIClient):
        self.api_client = api_client

    def set_access_token(self, access_token: str):
        self.api_client.set_access_token(access_token)

    def get_integration_table_data(self) -> List[List[str]]:
        integration_data, request_id = self.api_client.get_integrations()

        try:
            data = []
            for i in integration_data:
                updated_at = i["updated_at"].strftime("%d %b %Y %I:%M%p")
                data.append([i["slug"], i["type"], updated_at])

            return data
        except KeyError:
            raise SymAPIRequestError(
                "Failed to parse data received from the Sym API", request_id
            )

    def get_slack_connectors_table_data(self) -> List[List[str]]:
        """Returns data on available Slack connectors in a form ready
        to pass to tabulate.
        """
        connector_data, request_id = self.api_client.get_connectors(
            ConnectorType.SLACK.value
        )
        try:
            data = []
            for c in connector_data:
                settings = c["settings"]
                data.append([settings["team_name"], settings["team_id"]])

            return data
        except KeyError:
            raise SymAPIRequestError(
                "Failed to parse data received fro the Sym API", request_id
            )

    def get_user_integration_table_data(self) -> List[List[str]]:
        integration_data, request_id = self.api_client.get_user_integrations()
        try:
            data = []
            for i in integration_data:
                data.append([i["name"], i["type"]])
            return data
        except KeyError:
            raise SymAPIRequestError(
                "Failed to parse data received from the Sym API", request_id
            )

    def get_user_integrations(self) -> List[Dict[str, str]]:
        integration_data, request_id = self.api_client.get_user_integrations()
        return integration_data

    def get_user_table_data(
        self, service_type: Optional[str] = None, service: Optional[str] = None
    ) -> List[List[str]]:
        identity_data, request_id = self.api_client.get_users(
            params={
                "service_slugs": [service_type],
                "service_identifiers": [service],
                "include_missing": True,
            }
        )

        return identity_data

    def patch_user_table_data(self, csv_data: str) -> List[Dict[str, str]]:
        identity_data, request_id = self.api_client.patch_users(csv_data)
        return identity_data

    def get_organization_from_email(self, email: str) -> Organization:
        try:
            org_data, _ = self.api_client.get_organization_from_email(email)

            return Organization(slug=org_data["slug"], client_id=org_data["client_id"])
        except KeyError:
            raise UnknownOrgError(email)

    def verify_login(self, email: str) -> bool:
        """Verifies Auth0 login was successful and the access token received
        will be respected by the Sym API.

        Returns True if login has been verified.
        """

        try:
            status_code, _ = self.api_client.verify_login(email)
        except SymAPIRequestError:
            return False
        except SymAPIUnknownError:
            return False
        return status_code == 200
