import pyspark.sql.functions as f
from pyspark.sql import SparkSession

MAX_SESSION_SECONDS = 1800
GROUP_KEY = "browser_family"


def main():
    df = spark.read.json('s3a://lucas-spark-read-test/')
    df.select([f.count(f.when(f.isnan(c), c)).alias(c)
               for c in df.columns]).show()
    # df.show()


if __name__ == "__main__":
    spark = SparkSession.builder.appName('session_calc').getOrCreate()
    main()
