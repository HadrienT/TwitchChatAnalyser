import psycopg2
import os
import streamlit as st
import pandas as pd
from dotenv import load_dotenv


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
    return connection


def db_retrieve(query, params=None):
    global connection
    cursor = None
    data = None
    try:
        # Create a new cursor object
        cursor = connection.cursor()

        # Execute a query
        cursor.execute(query, params)

        # Fetch all the data
        data = cursor.fetchall()

    except Exception as e:
        print("An error occurred:", e)

    finally:
        # Close the cursor and connection
        if cursor is not None:
            cursor.close()

    return data
    
    
def streamlit_display():
    # Create a title
    st.title('My first Streamlit aaaaapp')

    # Ask the user for input
    streamer_channel = st.text_input(label="Enter a channel name", placeholder='Example: xQc')
    viewer_username = st.text_input(label="Enter a username", placeholder='Example: Ludwig')

    # Construct the base query
    query = """
        SELECT Users.display_name, UserChannelRelations.channel, UserChannelRelations.behavior_score
        FROM Users
        INNER JOIN UserChannelRelations ON Users.user_id = UserChannelRelations.user_id
        WHERE 1=1
    """

    # Set up parameters and append WHERE conditions based on user input
    params = {}
    if viewer_username:
        query += " AND LOWER(Users.display_name) ILIKE %(username)s"
        params['username'] = f"%{viewer_username.lower()}%"
    if streamer_channel:
        query += " AND LOWER(UserChannelRelations.channel) = %(channel)s"
        params['channel'] = streamer_channel.lower()

    data = db_retrieve(query, params)
    if data:
        df = pd.DataFrame(data, columns=["username", "channel", "behavior_score"])
        df_styled = df.style.bar(subset=['behavior_score'], align='mid', color=['#d65f5f', '#FFFFF'])  # apply a gradient based on the 'behavior_score' column
        st.dataframe(df_styled)  # Show the dataframe
    else:
        st.write("No data to display")


if __name__ == "__main__":
    load_dotenv()
    try:
        connection = db_create_connection()
        streamlit_display()
    except Exception as e:
        print("An error occurred:", e)
