# Yahoo Mail OAuth 2.0 Client

This is a Python script that demonstrates the usage of Yahoo Mail OAuth 2.0 to
perform various operations such as getting the authorization URL, exchanging the
authorization code for an access token, getting user information, and revoking
the grant.

## Installation

1. Create a virtual environment:

   ```shell
   $ python3 -m venv venv
   $ . venv/bin/activate
   ```

2. Install the required packages:

   ```shell
   $ pip install -r requirements.txt
   ```

## Configuration

- `CLIENT_ID`: Your Yahoo Mail OAuth 2.0 client ID.
- `CLIENT_SECRET`: Your Yahoo Mail OAuth 2.0 client secret.
- `REDIRECT_URI`: Your redirect URI.
- `API_BASE_URL`: Base URL for Yahoo Mail API.
- `TOKEN_FILE`: Path to the token JSON file.
- `INFO_FILE`: Path to the profile information JSON file.

## Usage

Available commands:

- `authorization-url`: Get the authorization URL.

```shell
$ python3 yahoo_oauth.py authorization-url
```

- `exchange-code`: Exchange the authorization code for an access token.

```shell
$ python3 yahoo_oauth.py exchange-code <authorization_code>
```

- `get-userinfo`: Get the authenticated user's profile information.

```shell
$ python3 yahoo_oauth.py get-userinfo
```

- `revoke-grant`: Revoke the grant.

> **Note**: By the time of this writing, this feature does not seem to have been
> implemented by the Yahoo team yet. However, software development is an ongoing
> process, and the status of features can change over time. If you have any new
> information or if the status of this feature has changed, please feel free to
> make a contribution to the project.

```shell
$ python3 yahoo_oauth.py revoke-grant
```

---

> **Note**: Follow the command-line prompts or check the output for the
> respective command.

## License

This project is licensed under the [MIT License](LICENSE).
