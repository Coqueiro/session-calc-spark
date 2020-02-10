import os
import pyspark.sql.functions as f
from pyspark.sql import SparkSession


MAX_SESSION_SECONDS = os.environ['MAX_SESSION_SECONDS']
GROUP_KEY = os.environ['GROUP_KEY']


def main():
    events = spark.read.json('s3a://lucas-spark-read-test/')
    events.registerTempTable('events')
    user_sessions = spark.sql(f'''
        SELECT
            anonymous_id,
            device_sent_timestamp AS session_timestamp,
            browser_family,
            device_family,
            os_family
        FROM (
            SELECT
                *,
                CASE WHEN device_sent_timestamp - last_device_sent_timestamp > {MAX_SESSION_SECONDS}
                    OR last_device_sent_timestamp IS NULL
                   THEN 1 ELSE 0 END AS is_new_session
            FROM (
                SELECT
                    anonymous_id,
                    browser_family,
                    device_family,
                    os_family,
                    device_sent_timestamp,
                    LAG(device_sent_timestamp, 1) OVER (PARTITION BY anonymous_id ORDER BY device_sent_timestamp) AS last_device_sent_timestamp
                FROM events
            ) last_events
        ) sessions
        WHERE is_new_session = 1
    ''')

    count_sessions_by_group = (
        user_sessions
        .withColumn('pivot', f.lit(0))
        .groupBy('pivot').pivot(GROUP_KEY).agg(f.count(f.lit(1)))
        .drop('pivot')
    )

    with open(f'/app/output/sessions_by_{GROUP_KEY}.json', 'w') as output_file:
        output_file.write(count_sessions_by_group.toJSON().first())


if __name__ == '__main__':
    spark = SparkSession.builder.appName('session-calc').getOrCreate()
    main()
