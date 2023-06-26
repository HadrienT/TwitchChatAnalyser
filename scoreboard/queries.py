import psycopg2
import os
import pandas as pd
from dotenv import load_dotenv


def db_create_connection():
    if os.getenv("RUNNING_IN_DOCKER"):
        print("Running in Docker")
        connection = psycopg2.connect(
            host="postgres",
            port="5432",
            dbname="twitch_analysis",
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
        )
    else:
        print("Running locally")
        connection = psycopg2.connect(
            host="localhost",
            port="5432",
            dbname="twitch_analysis",
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
        )
    print("Connection established")    
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

        # Fetch all the rows
        data = cursor.fetchall()

    except Exception as e:
        print("An error occurred:", e)

    finally:
        # Close the cursor and connection
        if cursor is not None:
            cursor.close()

    return data


if __name__ == "__main__":
    load_dotenv()
    try:
        connection = db_create_connection()
    except Exception as e:
        print("An error occurred:", e)
        
    print("Number of rows:", db_retrieve("SELECT COUNT(*) FROM users")[0][0])
    print("Weight of the DB:", db_retrieve("SELECT pg_size_pretty(pg_database_size(current_database())) AS database_size;")[0][0])
    # data = db_retrieve("SELECT text, display_name  FROM users JOIN messages  ON users.user_id = messages.user_id WHERE channel = 'wankilstudio' ")
    data = db_retrieve("""SELECT 
    Messages.text AS message_content, 
    Messages.channel AS channel, 
    Users.user_id AS user_id, 
    Users.display_name AS user_display_name
FROM 
    Messages
JOIN 
    Users ON Messages.user_id = Users.user_id
WHERE 
    Messages.sent_date >= NOW() - INTERVAL '10 minutes';
""")
    if data:
        # df = pd.DataFrame(data, columns=["user_id", "display_name", "color"])
        # df.to_csv("users.csv", index=False)
        # print("Data retrieved and saved to 'users.csv'")
        # df = pd.DataFrame(data, columns=["Name", "message"])
        # df.to_csv("msg.csv", index=False)
        # print("Data retrieved and saved to 'msg.csv'")
        df = pd.DataFrame(data, columns=["Message", "Streamer", "User ID", "User Name"])
        df.to_csv("msg.csv", index=False)
        print("Data retrieved and saved to 'msg.csv'")
        
    else:
        print("No data to retrieve")
