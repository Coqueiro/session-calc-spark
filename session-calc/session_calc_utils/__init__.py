from pyspark.sql import functions as f


def get_user_sessions(spark, events, user_key, timestamp_key, max_session_seconds):
    events.registerTempTable('events')
    user_sessions = spark.sql(f'''
        SELECT
            *,
            {timestamp_key} AS session_timestamp
        FROM (
            SELECT
                *,
                CASE WHEN {timestamp_key} - last_{timestamp_key} > {max_session_seconds}
                    OR last_{timestamp_key} IS NULL
                   THEN 1 ELSE 0 END AS is_new_session
            FROM (
                SELECT
                    *,
                    LAG({timestamp_key}, 1) OVER (
                        PARTITION BY {user_key} ORDER BY {timestamp_key}
                    ) AS last_{timestamp_key}
                FROM events
            ) last_events
        ) sessions
        WHERE is_new_session = 1
    ''').drop(*[timestamp_key, f"last_{timestamp_key}", "is_new_session"])

    return user_sessions


def get_sessions_by_group(user_sessions, group_key):
    return (
        user_sessions
        .withColumn('pivot', f.lit(0))
        .groupBy('pivot').pivot(group_key).agg(f.count(f.lit(1)))
        .drop('pivot')
    )


def write_first_row_as_json(df, path):
    with open(path, 'w') as output_file:
        output_file.write(df.toJSON().first())
