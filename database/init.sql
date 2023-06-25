CREATE TABLE IF NOT EXISTS Users (
    user_id VARCHAR(255) PRIMARY KEY,
    display_name VARCHAR(255),
    color VARCHAR(7)
);

CREATE TABLE IF NOT EXISTS UserChannelRelations (
    user_id VARCHAR(255) REFERENCES Users(user_id),
    channel VARCHAR(255),
    badge JSONB,
    mod BOOLEAN,
    subscriber BOOLEAN,
    turbo BOOLEAN,
    behavior_score INTEGER,
    PRIMARY KEY(user_id, channel)
);

CREATE TABLE IF NOT EXISTS Messages (
    message_id VARCHAR(255) PRIMARY KEY,
    user_id VARCHAR(255) REFERENCES Users(user_id),
    text TEXT,
    bits INTEGER,
    sent_timestamp BIGINT,
    sent_date TIMESTAMP,
    channel VARCHAR(255),
    reply_parent_msg_id VARCHAR(255),
    reply_parent_user_id VARCHAR(255),
    emotes JSONB,
    first_msg BOOLEAN,
    returning_chatter BOOLEAN,
    room_id VARCHAR(255)
);
