import configparser

# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs"
songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS times"

# CREATE TABLES

staging_events_table_create = ("""
    CREATE TABLE staging_events(
        artist        TEXT,
        auth          TEXT,
        first_name    TEXT,
        gender        CHAR,
        itemInSession INT,
        last_name     TEXT,
        length        FLOAT,
        level         TEXT,
        location      TEXT,
        method        TEXT,
        page          TEXT,
        registration  FLOAT,
        session_id    INT,
        song          TEXT,
        status        INT,
        ts            TIMESTAMP,
        user_agent    TEXT,
        user_id       INT
    )
""")

staging_songs_table_create = ("""
    CREATE TABLE staging_songs(
        num_songs        INT,
        artist_id        TEXT,
        artist_latitude  TEXT,
        artist_longitude TEXT,
        artist_location  TEXT,
        artist_name      TEXT,
        song_id          TEXT,
        title            TEXT,
        duration         FLOAT,
        year             INT
    )
""")

songplay_table_create = ("""
    CREATE TABLE songplays(
        songplay_id INT PRIMARY KEY IDENTITY (0,1),
        start_time  TIMESTAMP NOT NULL, 
        user_id     INT NOT NULL, 
        level       TEXT NOT NULL, 
        song_id     TEXT NOT NULL, 
        artist_id   TEXT NOT NULL, 
        session_id  INT NOT NULL, 
        location    TEXT NOT NULL, 
        user_agent  TEXT NOT NULL
    )
""")

user_table_create = ("""
    CREATE TABLE users(
        user_id    INT PRIMARY KEY NOT NULL, 
        first_name TEXT NOT NULL,
        last_name  TEXT NOT NULL, 
        gender     CHAR NOT NULL, 
        level      TEXT NOT NULL
    )
""")

song_table_create = ("""
    CREATE TABLE songs(
        song_id   TEXT PRIMARY KEY NOT NULL, 
        title     TEXT NOT NULL, 
        artist_id TEXT NOT NULL, 
        year      INT NOT NULL, 
        duration  FLOAT NOT NULL
    )
""")

artist_table_create = ("""
    CREATE TABLE artists(
        artist_id TEXT PRIMARY KEY NOT NULL, 
        name      TEXT NOT NULL, 
        location  TEXT, 
        latitude  TEXT, 
        longitude TEXT
    )
""")

time_table_create = ("""
    CREATE TABLE times(
        start_time TIMESTAMP PRIMARY KEY NOT NULL, 
        hour       INT NULL, 
        day        INT NULL, 
        week       INT NULL, 
        month      INT NULL, 
        year       INT NULL, 
        weekday    INT NULL
    )
""")

# STAGING TABLES

staging_events_copy = ("""
    COPY staging_events
    FROM {s3_log_data}
    JSON {s3_log_jsonpath}
    TIMEFORMAT 'epochmillisecs'
    IAM_ROLE {iam_role_arn}
    REGION 'us-west-2'
    ;
""").format(s3_log_data=config['S3']['LOG_DATA'], s3_log_jsonpath=config['S3']['LOG_JSONPATH'],
            iam_role_arn=config['IAM_ROLE']['ARN'])

staging_songs_copy = ("""
    COPY staging_songs
    FROM {s3_song_data}
    JSON 'auto'
    IAM_ROLE {iam_role_arn}
    REGION 'us-west-2'
    ;
""").format(s3_song_data=config['S3']['SONG_DATA'], iam_role_arn=config['IAM_ROLE']['ARN'])

# FINAL TABLES

songplay_table_insert = ("""
    INSERT INTO songplays (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
    SELECT                 ts, user_id, level, s.song_id, s.artist_id, session_id, location, user_agent
    FROM staging_events
    JOIN staging_songs s
    ON artist=s.artist_name AND song=s.title
    WHERE page = 'NextSong'
""")

user_table_insert = ("""
    INSERT INTO users (user_id, first_name, last_name, gender, level)
    SELECT    DISTINCT(user_id), first_name, last_name, gender, level
    FROM staging_events
    WHERE user_id IS NOT NULL
""")

song_table_insert = ("""
    INSERT INTO songs (song_id, title, artist_id, year, duration)
    SELECT             song_id, title, artist_id, year, duration
    FROM staging_songs
""")

artist_table_insert = ("""
    INSERT INTO artists (artist_id, name, location, latitude, longitude)
    SELECT      DISTINCT(artist_id), artist_name AS name, artist_location AS location, artist_latitude AS latitude, artist_longitude AS longitude
    FROM staging_songs
""")

time_table_insert = ("""
    INSERT INTO times (start_time, hour, day, week, month, year, weekday)
    SELECT             start_time, DATE_PART(h,start_time) AS hour, DATE_PART(d,start_time) AS day, DATE_PART(w,start_time) AS week, DATE_PART(mon,start_time) AS month, DATE_PART(y,start_time) AS year, DATE_PART(dow,start_time) AS weekday
    FROM songplays
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create,
                        user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop,
                      song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert,
                        time_table_insert]
