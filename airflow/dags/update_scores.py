import psycopg2  

conn = psycopg2.connect(database="your_database", user="your_user", password="your_password", host="your_host", port="your_port")
cursor = conn.cursor()

cursor.execute("SELECT message_id, text FROM Messages;")
messages = cursor.fetchall()

for message_id, message_text in messages:

    # Update the behavior score based on sentiment label and score
    if sentiment_label == 'positive':
        behavior_score_change = sentiment_score * 10  # Example: Increase the score by a factor of 10
    elif sentiment_label == 'negative':
        behavior_score_change = -sentiment_score * 10  # Example: Decrease the score by a factor of 10
    else:
        behavior_score_change = 0  # No change in score for neutral sentiment

    # Update the behavior score of the user associated with the message
    cursor.execute("UPDATE UserChannelRelations SET behavior_score = behavior_score + %s WHERE user_id = %s;", (behavior_score_change, user_id))

# Commit the changes and close the connection
conn.commit()
cursor.close()
conn.close()
