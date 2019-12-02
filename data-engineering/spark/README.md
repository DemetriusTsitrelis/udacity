# Summary of the project

A music streaming startup, Sparkify, has grown their user base and song database even more and want to move their data warehouse to a data lake. Their data resides in S3, in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.

This project implements an Extract-Transform-Load (ETL) pipeline for Sparkify that extracts their data from S3, processes them using Spark, and loads the data back into S3 as a set of dimensional tables. This will allow their analytics team to continue finding insights in what songs their users are listening to.

that wants to analyze the data they've been collecting on songs and user activity on their new music streaming app. The analytics team was particularly interested in understanding what songs users are listening to but they didn't have an easy way to query their data, which resides in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.  The output of this project is a PostgreSQL database which is optimized for queries on song play analysis.

Schema for Song Play Analysis

The database uses a star schema made up of a single fact and multiple dimension tables for a particular analytic focus.  

Fact Table

    songplays - records in log data associated with song plays i.e. records with page NextSong
        songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent

Dimension Tables

    users - users in the app
        user_id, first_name, last_name, gender, level
    songs - songs in music database
        song_id, title, artist_id, year, duration
    artists - artists in music database
        artist_id, name, location, lattitude, longitude
    time - timestamps of records in songplays broken down into specific units
        start_time, hour, day, week, month, year, weekday


## How to run the Python scripts

First create an EMR cluster in AWS.

Second create an S3 bucket to hold the output from the ETL process.

Next ensure that your AWS user has programmatic (i.e., API) access to the AWS API.  Record the user's access key and secret key in the the AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY keys in the dl.cfg file.

Modify etl.py with the name of the your S3 bucket in the output_data variable in the main() function.

To perform the ETL process, from a terminal window run: "python etl.py"

## Explanation of the files in the repository. 

The data folder consists of two .zip files, one each for song and log data. The song-data archive contains metadata about a song and the artist of that song and is a subset of real data from the Million Song Dataset. The log-data archive contains simulated activity logs from a music streaming app based on specified configurations and partitioned by year and month. 

The remaining files in the root folder as as follows:
dl.cfg: An INI-type configuration file used to specify AWS API credentials to interact with an EMR cluster.
etl.py: Python code which interacts with an EMR cluster to perform the Extract-Transform-Load steps to generate a Parquet format file into the destination S3 bucket with songplay data.
README.md: This file