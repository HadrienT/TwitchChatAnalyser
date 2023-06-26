import os
import asyncio
import json
from datetime import datetime
import signal

from twitchAPI.twitch import Twitch
from twitchAPI.types import AuthScope, ChatEvent
from twitchAPI.chat import Chat, EventData, ChatMessage
from dotenv import load_dotenv
import psycopg2


def signal_handler(signal, frame):
    global twitch, chat, connection, cursor
    loop = asyncio.get_event_loop()
    if chat is not None:
        chat.stop()
    if twitch is not None:
        loop.run_until_complete(twitch.close())
    if cursor is not None:
        cursor.close()
    if connection is not None:
        connection.close()
    print('Bot stopped.')
    loop.close()
    exit(0)


def db_create_connection():
    if os.getenv("RUNNING_IN_DOCKER"):
        connection = psycopg2.connect(
            host="postgres",
            port="5432",
            dbname="twitch_analysis",
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
        )
    else:
        connection = psycopg2.connect(
            host="localhost",
            port="5432",
            dbname="twitch_analysis",
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
        )
    print(connection)
    # Create a new cursor object
    cursor = connection.cursor()
    print("Connected to PostgreSQL database")
    return connection, cursor


# this will be called when the event READY is triggered, which will be on bot start
async def on_ready(ready_event: EventData):
    print("Bot is ready for work, joining channels")
    await ready_event.chat.join_room(TARGET_CHANNEL)
    # you can do other bot initialization things in here


# this will be called whenever a message in a channel was send by either the bot OR another user
async def on_message(msg: ChatMessage):
    global log_counter
    # Now, let's insert the message data into the database
    msg = msg.__dict__
    try:
        # Insert data into Users table
        cursor.execute(
            """
            INSERT INTO Users(user_id, display_name, color)
            VALUES (%s, %s, %s)
            ON CONFLICT (user_id) DO NOTHING
            """,
            (
                msg["_parsed"]["tags"]["user-id"],
                msg["_parsed"]["tags"]["display-name"],
                msg["_parsed"]["tags"]["color"],
            ),
        )

        # Insert data into UserChannelRelations table
        cursor.execute(
            """
            INSERT INTO UserChannelRelations(user_id, channel, badge, mod, subscriber, turbo, behavior_score)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (user_id, channel) DO NOTHING
            """,
            (
                msg["_parsed"]["tags"]["user-id"],
                msg["_parsed"]["command"]["channel"].replace("#", ""),
                json.dumps(msg["_parsed"]["tags"]["badges"]),
                msg["_parsed"]["tags"]["mod"] == "1",
                msg["_parsed"]["tags"]["subscriber"] == "1",
                msg["_parsed"]["tags"]["turbo"] == "1",
                50,
            ),
        )
        # Insert data into Messages table
        cursor.execute(
            """
            INSERT INTO Messages(message_id, user_id, text, bits, sent_timestamp, sent_date, channel, reply_parent_msg_id, reply_parent_user_id, emotes, first_msg, returning_chatter, room_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                msg["_parsed"]["tags"]["id"],
                msg["_parsed"]["tags"]["user-id"],
                msg["text"],
                msg["bits"],
                msg["_parsed"]["tags"]["tmi-sent-ts"],
                datetime.fromtimestamp(int(msg["_parsed"]["tags"]["tmi-sent-ts"])/1000).strftime('%Y-%m-%d %H:%M:%S'),
                msg["_parsed"]["command"]["channel"].replace("#", ""),
                msg["reply_parent_msg_id"],
                msg["reply_parent_user_id"],
                json.dumps(msg["_parsed"]["tags"]["emotes"]),
                msg["_parsed"]["tags"]["first-msg"] == "1",
                msg["_parsed"]["tags"]["returning-chatter"] == "1",
                msg["_parsed"]["tags"]["room-id"],
            ),
        )
        connection.commit()
        log_counter += 1
        if log_counter % 100 == 0:
            print(f"Logged {log_counter} messages")
    except Exception as e:
        # If an error occurred, rollback the transaction
        connection.rollback()
        print(f"An error occurred: {e}")


async def run():
    app_id = os.getenv("APP_ID")
    app_secret = os.getenv("APP_SECRET")
    token = os.getenv("TWITCH_OAUTH_TOKEN")
    refresh_token = os.getenv("TWITCH_REFRESH_TOKEN")

    twitch = await Twitch(app_id, app_secret)
    await twitch.set_user_authentication(token, USER_SCOPE, refresh_token)

    chat = await Chat(twitch)
    chat.register_event(ChatEvent.READY, on_ready)
    chat.register_event(ChatEvent.MESSAGE, on_message)
    chat.start()


if __name__ == "__main__":
    load_dotenv()

    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)
    USER_SCOPE = [AuthScope.CHAT_READ, AuthScope.CHAT_EDIT]
    TARGET_CHANNEL = "ipav999"
    # Initialize global variables
    twitch = None
    chat = None
    connection = None
    cursor = None
    log_counter = 0
    # Establish a connection to the PostgreSQL database and get a cursor
    connection, cursor = db_create_connection()

    asyncio.run(run())
