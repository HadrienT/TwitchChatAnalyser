import os
import asyncio

from twitchAPI.twitch import Twitch
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.types import AuthScope
from dotenv import load_dotenv


async def get_token():
    USER_SCOPE = [AuthScope.CHAT_READ, AuthScope.CHAT_EDIT]
    load_dotenv()
    # Access environment variables
    app_id = os.getenv("APP_ID")
    app_secret = os.getenv("APP_SECRET")
    twitch = await Twitch(app_id, app_secret)
    auth = UserAuthenticator(twitch, USER_SCOPE)
    token, refresh_token = await auth.authenticate()
    return token, refresh_token


def update_env(token, refresh_token):
    # Read in the file
    with open('.env', 'r') as file:
        lines = file.readlines()
    # Replace the target string
    for index, line in enumerate(lines):
        if line.startswith('TWITCH_OAUTH_TOKEN='):
            lines[index] = f'TWITCH_OAUTH_TOKEN="{token}"\n'
        elif line.startswith('TWITCH_REFRESH_TOKEN='):
            lines[index] = f'TWITCH_REFRESH_TOKEN="{refresh_token}"\n'
    # Write the file out again
    with open('.env', 'w') as file:
        file.writelines(lines)


def main():
    token, refresh_token = asyncio.run(get_token())
    update_env(token, refresh_token)


if __name__ == "__main__":
    main()
