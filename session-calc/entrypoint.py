import os
from pyspark.sql import SparkSession

from session_calc_utils import get_user_sessions, get_sessions_by_group, write_first_row_as_json


READ_PATH = os.environ['READ_PATH']
USER_KEY = os.environ['USER_KEY']
TIMESTAMP_KEY = os.environ['TIMESTAMP_KEY']
MAX_SESSION_SECONDS = os.environ['MAX_SESSION_SECONDS']
GROUP_KEY = os.environ['GROUP_KEY']


def main(spark):
    events = spark.read.json(READ_PATH)

    user_sessions = get_user_sessions(
        spark, events, USER_KEY, TIMESTAMP_KEY, MAX_SESSION_SECONDS)

    sessions_by_group = get_sessions_by_group(user_sessions, GROUP_KEY)

    write_first_row_as_json(sessions_by_group,
                            f'/app/output/sessions_by_{GROUP_KEY}.json')


if __name__ == '__main__':
    spark = SparkSession.builder.appName('session-calc').getOrCreate()
    main(spark)
