# Summary of the project

This project implements an Extract-Transform-Load (ETL) pipeline for a startup called Sparkify that wants to analyze the data they've been collecting on songs and user activity on their new music streaming app. The analytics team was particularly interested in understanding what songs users are listening to but they didn't have an easy way to query their data, which resides in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.  The output of this project is a PostgreSQL database which is optimized for queries on song play analysis.

The database uses a star schema made up of a single fact and multiple dimension tables for a particular analytic focus.  The fact table is named songplays and records log data associated with song plays i.e. records with page NextSong.  It's attributes are songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, and user_agent.  These are mostly foreign key references to the dimension tables.

The dimension tables are the following:
users records users in the app and has the attributes: user_id, first_name, last_name, gender, level
songs records songs in the music database and has the attributes: song_id, title, artist_id, year, duration
artists records artists in the music database and has the attributes: artist_id, name, location, latitude, longitude
time records timestamps of records in songplays broken down into specific units and has the attributes: start_time, hour, day, week, month, year, weekday

The ETL pipeline processes the song and log data separately but shares code to do that where possible.  Both the song and log data are stored in subdirectory structures several levels deep representing partitioning of the data and this means the directory walking code can be the same whereas the code to process the song metadata is unique from that of the log data. Finally the database create/reset script (create_tables.py) and the ETL script (ety.py) are separate despite sharing code from sql_queries.py because the ETL process may be used multiple times as new sets of song and log data become available.

## How to run the Python scripts

First create the database tables. From a terminal window run: "python create_tables.py"

Next perform the extract-transform-load steps of the JSON song and log data into the Sparkify database by running: "python etl.py"

Lastly load the notebook test.ipynb and run all the cells to examine the data from the Sparkify database.

## Explanation of the files in the repository. 

The data folder consists of two subfolders, one each for song and log data. The songs_data subfolder contains metadata about a song and the artist of that song and is a subset of real data from the Million Song Dataset. The files are partitioned by the first three letters of each song's track ID. The log_data subfolder contains simulated activity logs from a music streaming app based on specified configurations and partitioned by year and month. 

The remaining files in the root folder as as follows:
sql_queries.py: Python code which implements SQL queries to create, delete, and populate the tables of the database.  Used by the other Python files and by etl.ipynb.
create_tables.py: Python code which uses sql_queries.py functions to recreate the tables of the database.
etl.py: Python code which uses sql_queries.py functions to perform the Extract-Transform-Load steps to populate the database from the JSON files in the data subfolders.

etl.ipynb: Jupyter notebook used to construct and validate code for use in etl.py.
test.ipynb: Jupyter notebook used to validate data in the database.

README.md: This file
