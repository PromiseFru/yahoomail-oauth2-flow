"""
Yahoo Mail OAuth 2.0 Client

This script provides functionality to interact with the Yahoo Mail OAuth 2.0 API. It allows users to perform operations such as getting the authorization URL, exchanging an authorization code for an access token, getting user information, and revoking the grant.
"""

import os
import logging
import argparse
import json
from urllib.parse import urljoin

from requests_oauthlib import OAuth2Session

logging.basicConfig(level=logging.DEBUG)

CLIENT_ID = os.environ["CLIENT_ID"]
CLIENT_SECRET = os.environ["CLIENT_SECRET"]
REDIRECT_URI = os.environ["REDIRECT_URI"]
TOKEN_FILE = os.environ["TOKEN_FILE"]
INFO_FILE = os.environ["INFO_FILE"]

API_BASE_URL = "https://api.login.yahoo.com"


def __read_file__(file_name):
    """
    Read data from a JSON file.

    :param file_name: The name of the JSON file to read.
    :return: The loaded data from the file as a dictionary, or None if the file does not exist or cannot be parsed as JSON.
    """
    try:
        with open(file_name, "r", encoding="utf-8") as f:
            token = json.load(f)
        return token
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def __write_file__(data, file_name):
    """
    Write data to a JSON file.

    :param data: The data to write to the file.
    :param file_name: The name of the JSON file to write.
    :return: None
    """
    existing_data = __read_file__(file_name=file_name) or {}
    existing_data.update(data)

    with open(file_name, "w", encoding="utf-8") as f:
        json.dump(existing_data, f)


def __del_file__(file_name):
    """
    Delete a file.

    :param file_name: The name of the file to delete.
    :return: None
    """
    try:
        os.remove(file_name)
    except OSError:
        pass


def __refresh_access_token__(new_token):
    """
    Refresh the access token and update the token file.

    :param new_token: The new access token.
    :return: The updated access token.
    """
    __write_file__(data=new_token, file_name=TOKEN_FILE)
    return new_token


oauth = OAuth2Session(
    client_id=CLIENT_ID,
    redirect_uri=REDIRECT_URI,
    scope="openid email profile",
    auto_refresh_url=urljoin(API_BASE_URL, "/oauth2/get_token"),
    token_updater=__refresh_access_token__,
)


def get_authorization_url():
    """
    Get the authorization URL.

    :return: The authorization URL.
    """
    authorization_url, state = oauth.authorization_url(
        url=urljoin(API_BASE_URL, "/oauth2/request_auth")
    )
    return authorization_url


def exchange_authorization_code(code):
    """
    Exchange an authorization code for an access token.

    :param code: The authorization code.
    :return: The access token.
    """
    token = oauth.fetch_token(
        token_url=urljoin(API_BASE_URL, "/oauth2/get_token"),
        code=code,
        client_secret=CLIENT_SECRET,
    )
    __write_file__(data=token, file_name=TOKEN_FILE)
    return token


def get_userinfo():
    """
    Get user information.

    :return: User information.
    """
    oauth.token = __read_file__(file_name=TOKEN_FILE)
    response = oauth.request(
        method="POST",
        url=urljoin(API_BASE_URL, "/openid/v1/userinfo"),
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
    )

    if response.status_code == 200:
        userinfo = response.json()
        __write_file__(data=userinfo, file_name=INFO_FILE)
        return userinfo

    return {}


def revoke_grant():
    """
    Revoke the grant.

    :return: True if the grant was successfully revoked, False otherwise.

    Note:
        By the time of this writing, this feature does not seem to have been
        implemented by the Yahoo team yet. However, software development is an ongoing
        process, and the status of features can change over time. If you have any new
        information or if the status of this feature has changed, please feel free to
        make a contribution to the project.
    """
    token = __read_file__(file_name=TOKEN_FILE)
    response = oauth.request(
        method="POST",
        url=urljoin(API_BASE_URL, "/oauth2/revoke"),
        auth=(CLIENT_ID, CLIENT_SECRET),
        data={"token": token["refresh_token"], "token_type_hint": "refresh_token"},
    )

    if response.status_code == 200:
        __del_file__(file_name=TOKEN_FILE)
        return True
    return False


def parse_arguments():
    """
    Parse command-line arguments.

    :return: The parsed command-line arguments.
    """
    parser = argparse.ArgumentParser(description="Yahoo Mail OAuth 2.0 Client")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    subparsers.add_parser("authorization-url", help="Get the authorization URL")
    subparsers.add_parser("get-userinfo", help="Get user information")
    subparsers.add_parser("revoke-grant", help="Revoke the grant")

    exchange_parser = subparsers.add_parser(
        "exchange-code", help="Exchange authorization code for access token"
    )
    exchange_parser.add_argument("code", help="Authorization code")

    return parser.parse_args()


def main():
    """
    Main entry point of the script.
    """
    args = parse_arguments()

    if args.command == "authorization-url":
        authorization_url = get_authorization_url()
        print("Authorization URL:", authorization_url)
    elif args.command == "exchange-code":
        token = exchange_authorization_code(args.code)
        print("Token:", token)
    elif args.command == "revoke-grant":
        revoke_success = revoke_grant()
        print("Revoke Grant Success:", revoke_success)
    elif args.command == "get-userinfo":
        userinfo = get_userinfo()
        print("User Info:", userinfo)


if __name__ == "__main__":
    main()
