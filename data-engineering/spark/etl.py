import configparser
from datetime import datetime
import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, col
from pyspark.sql.functions import year, month, dayofmonth, hour, weekofyear, date_format
from pyspark.sql.types import *

config = configparser.ConfigParser()
config.read('dl.cfg')

os.environ['AWS_ACCESS_KEY_ID'] = config.get('Config', 'AWS_ACCESS_KEY_ID')
os.environ['AWS_SECRET_ACCESS_KEY'] = config.get('Config', 'AWS_SECRET_ACCESS_KEY')


def create_spark_session():
    spark = SparkSession \
        .builder \
        .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:2.7.0") \
        .getOrCreate()
    return spark


def process_song_data(spark, input_data, output_data):
    # get filepath to song data file
    song_data = input_data + 'song_data/*/*/*/*.json'

    # read song data file
    songdata_schema = StructType([
        StructField('num_songs', IntegerType()),
        StructField('artist_id', StringType()),
        StructField('artist_latitude', StringType()),
        StructField('artist_longitude', StringType()),
        StructField('artist_location', StringType()),
        StructField('artist_name', StringType()),
        StructField('song_id', StringType()),
        StructField('title', StringType()),
        StructField('duration', FloatType()),
        StructField('year', IntegerType())
    ])
    song_data_file = spark.read.json(song_data, schema=songdata_schema)

    # extract columns to create songs table
    songs = song_data_file.select('song_id', 'title', 'artist_id', 'year', 'duration').dropDuplicates()

    # write songs table to parquet files partitioned by year and artist
    songs.write.partitionBy("year", "artist_id").parquet(output_data + 'songs')

    # extract columns to create artists table
    artists = song_data_file.selectExpr("artist_id", "artist_name as name", "artist_location as location",
                                        "artist_latitude as latitude", "artist_longitude as longitude").dropDuplicates()
    # write artists table to parquet files
    artists.write.parquet(output_data + 'artists')


def process_log_data(spark, input_data, output_data):
    # get filepath to log data file
    log_data = input_data + 'log_data/*/*/*.json'

    # read log data file
    log_data_file = spark.read.json(log_data)

    # filter by actions for song plays
    log_data_file = log_data_file.filter(log_data_file.page == 'NextSong')

    # extract columns for users table
    users = log_data_file.selectExpr("userId as user_id", "firstName as first_name", "lastName as last_name", "gender",
                                     "level").dropDuplicates()

    # write users table to parquet files
    users.write.parquet(output_data + 'users')

    # create timestamp column from original timestamp column
    get_timestamp = udf(lambda ts: ts // 1000, IntegerType())
    log_data_file = log_data_file.withColumn('timestamp', get_timestamp(col('ts')))

    # create datetime column from original timestamp column
    get_datetime = udf(lambda ts: datetime.fromtimestamp(ts // 1000), TimestampType())
    log_data_file = log_data_file.withColumn('datetime', get_datetime(col('ts')))

    # extract columns to create time table
    times = log_data_file.selectExpr("datetime as start_time", "hour(datetime) as hour", "dayofmonth(datetime) as day",
                                     "weekofyear(datetime) as week", "month(datetime) as month",
                                     "year(datetime) as year", "date_format(datetime, 'E') as weekday").dropDuplicates()

    # write time table to parquet files partitioned by year and month
    times.write.partitionBy("year", "month").parquet(output_data + 'times')

    # read in song data to use for songplays table
    songs = spark.read.parquet(output_data + 'songs')
    artists = spark.read.parquet(output_data + 'artists')
    artists_songs = artists.alias("artists").join(songs.alias("songs"), artists.artist_id == songs.artist_id)

    # extract columns from joined song and log datasets to create songplays table
    songplays = artists_songs.join(log_data_file.alias("log_data_file"),
                                   (artists_songs.name == log_data_file.artist) & (
                                               artists_songs.title == log_data_file.song)).selectExpr(
        "monotonically_increasing_id() as songplay_id", "datetime as start_time", "userId as user_id", "level",
        "song_id", "artists.artist_id as artist_id", "sessionId as session_id", "log_data_file.location as location",
        "userAgent as user_agent", "year(datetime) as year", "month(datetime) as month").dropDuplicates()

    # write songplays table to parquet files partitioned by year and month
    songplays.write.partitionBy("year", "month").parquet(output_data + 'songplays')


def main():
    spark = create_spark_session()
    input_data = "s3a://udacity-dend/"
    output_data = "s3a://<Fill with your S3 bucket name>"

    process_song_data(spark, input_data, output_data)
    process_log_data(spark, input_data, output_data)


if __name__ == "__main__":
    main()
