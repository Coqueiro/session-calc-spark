import pyspark.sql.functions as f
from pyspark.sql import SparkSession

MAX_SESSION_SECONDS = 1800
GROUP_KEY = "device_family"


def main():
    df = spark.read.json('s3a://lucas-spark-read-test/')
    df.registerTempTable('events')
    spark.sql(f'''
        SELECT
            anonymous_id,
            device_sent_timestamp AS session_timestamp,
            browser_family,
            device_family,
            os_family
        FROM (
            SELECT
                *,
                CASE WHEN device_sent_timestamp - last_device_sent_timestamp >= {MAX_SESSION_SECONDS}
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
    ''').registerTempTable('user_sessions')

    sessions_by_group = spark.sql(f'''
        SELECT
            {GROUP_KEY},
            COUNT(1) AS sessions_count
        FROM user_sessions
        GROUP BY {GROUP_KEY}
    ''')

    sessions_by_group.show()


if __name__ == "__main__":
    spark = SparkSession.builder.appName('session_calc').getOrCreate()
    main()
