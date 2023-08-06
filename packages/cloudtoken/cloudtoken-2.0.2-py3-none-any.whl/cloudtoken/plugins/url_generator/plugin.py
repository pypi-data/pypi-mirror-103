from typing import List
from urllib.parse import urlencode

import click
import requests
from cloudtoken.core import utils
from cloudtoken.core.abstract_classes import CloudtokenPlugin
from cloudtoken.core.exceptions import PluginError
from cloudtoken.core.helper_classes import CloudtokenOption


class Plugin(CloudtokenPlugin):
    name = "url_generator"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    @classmethod
    def options(cls) -> List[CloudtokenOption]:
        options = [
            cls.add_option(
                ["--generate-url", "-g"], is_flag=True, help="Generate a sign in URL that can be used in a browser."
            ),
            cls.add_option(
                ["--generate-url-duration"],
                type=int,
                help="Duration of the temporary role to create for URL sign-in (in seconds). Must be less than the maximum session duration for the role.",
            ),
            cls.add_option(
                ["--generate-url-suffix"],
                type=str,
                help="Suffix to add to the destination URL. e.g. rds | cloudformation | sqs",
            ),
            cls.add_option(
                ["--generate-url-print"],
                type=str,
                help="Print out the URL in addition to attempting to open it in a browser.",
            ),
        ]

        return options

    def execute(self, data: dict) -> dict:
        credentials = utils.find_credentials(data)
        if not credentials:
            raise PluginError("Unable to find credetials provided by previous plugin.")

        if not self._get_plugin_config(["generate_url"]):
            return {}

        url_duration = self._get_plugin_config(["generate_url_duration"], 43200)  # 12 hours
        url_suffix = self._get_plugin_config(["generate_url_suffix"])
        sign_in_url = self._generate_sign_in_url(credentials, url_duration, url_suffix)

        if self._get_plugin_config(["generate_url_print"]):
            utils.echo(f"Sign-In URL: {sign_in_url}")

        click.launch(sign_in_url)

        data = {"sign_in_url": sign_in_url}
        return data

    def _generate_sign_in_url(self, credentials, duration, suffix):
        if not suffix:
            suffix = ""

        # boto does not support getSigninToken...yet
        sign_in_url = "https://signin.aws.amazon.com/federation?"
        destination_url = "https://console.aws.amazon.com/" + suffix

        session_data = {
            "sessionId": credentials["AccessKeyId"],
            "sessionKey": credentials["SecretAccessKey"],
            "sessionToken": credentials["Token"],
        }

        sign_in_token_parameters = {
            "Action": "getSigninToken",
            "SessionDuration": duration,
            "Session": session_data,
        }

        resp = requests.get(sign_in_url, params=urlencode(sign_in_token_parameters))
        resp.raise_for_status()

        sign_in_token = resp.json()["SigninToken"]
        sign_in_params = {
            "Action": "login",
            "Issuer": credentials["Issuer"],
            "SigninToken": sign_in_token,
            "Destination": destination_url,
        }

        return sign_in_url + urlencode(sign_in_params)
