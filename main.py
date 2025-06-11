import os

import dotenv
from pyrogram import Client, filters

is_prod = os.getenv("PRODUCTION")

if not is_prod:
    dotenv.load_dotenv()

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
SESSION_STRING = os.getenv("SESSION_STRING")
CHAT1_USERNAME = os.getenv("CHAT1_USERNAME")
CHAT2_USERNAME = os.getenv("CHAT2_USERNAME")


def main():
    if not (
        API_ID and API_HASH and SESSION_STRING and CHAT1_USERNAME and CHAT2_USERNAME
    ):
        print("incomplete variables")
        if is_prod:
            return

    app = Client(
        "forwarder", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING
    )

    @app.on_message(filters.chat(CHAT1_USERNAME))
    async def forward(client, message):
        if not message.photo or not message.from_user.username in CHAT1_USERNAME:
            return

        await message.forward(CHAT2_USERNAME)

    @app.on_message(filters.chat(CHAT2_USERNAME))
    async def respond(client, message):
        if (
            not message.text
            or message.text == "no photo"
            or not message.from_user.username in CHAT2_USERNAME
        ):
            return

        await message.forward(CHAT1_USERNAME)

    app.run()


if __name__ == "__main__":
    main()
