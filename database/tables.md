**Users Table**

| Column Name  | Data Type                | Description                         |
| ------------ | ------------------------ | ----------------------------------- |
| user_id      | VARCHAR(255) PRIMARY KEY | User ID from Twitch API             |
| display_name | VARCHAR(255)             | Display name of the user            |
| color        | VARCHAR(7)               | Color code associated with the user |

**UserChannelRelations Table**

| Column Name       | Data Type                              | Description                                                           |
| ----------------- | -------------------------------------- | --------------------------------------------------------------------- |
| user_id           | VARCHAR(255) REFERENCES Users(user_id) | The user in relation                                                  |
| channel           | VARCHAR(255)                           | The channel in which the user has the role                            |
| broadcaster_badge | BOOLEAN                                | True if the user has a broadcaster badge in the channel               |
| mod               | BOOLEAN                                | True if the user is a mod in the channel                              |
| subscriber        | BOOLEAN                                | True if the user is a subscriber in the channel                       |
| turbo             | BOOLEAN                                | True if the user has turbo in the channel                             |
| behavior_score    | INTEGER                                | Score representing the behavior of the user in the channel (0 to 100) |

Primary Key: (user_id, channel)

**Messages Table**

| Column Name          | Data Type                                                | Description                                                  |
| -------------------- | -------------------------------------------------------- | ------------------------------------------------------------ |
| message_id           | VARCHAR(255) PRIMARY KEY                                 | Message ID from Twitch API                                   |
| user_id              | INTEGER, FOREIGN KEY (user_id) REFERENCES Users(user_id) | User who sent the message                                    |
| text                 | TEXT                                                     | Content of the message                                       |
| bits                 | INTEGER                                                  | Number of bits in the message                                |
| sent_timestamp       | BIGINT                                                   | Timestamp when the message was sent                          |
| channel              | VARCHAR(255)                                             | Channel in which the message was sent                        |
| reply_parent_msg_id  | VARCHAR(255)                                             | Message ID of the message being replied to                   |
| reply_parent_user_id | VARCHAR(255)                                             | User ID of the user being replied to                         |
| emotes               | JSONB                                                    | Emotes used in the message                                   |
| first_msg            | BOOLEAN                                                  | True if this is the first message of the user in the channel |
| returning_chatter    | BOOLEAN                                                  | True if the user is a returning chatter                      |
| room_id              | VARCHAR(255)                                             | ID of the room the user is in                                |
