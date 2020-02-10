import os
from pyspark.sql import SparkSession
from pyspark.sql import functions as f


READ_PATH = os.environ['READ_PATH']


def main(spark):
    events = spark.read.json(READ_PATH)

    events.cache()

    null_keys = events.select([f.count(f.when(f.isnan(c), c)).alias(c)
                               for c in events.columns]).collect()

    total_count = events.count()

    count_multiple_group_keys = (
        events.groupBy("anonymous_id").agg(
            f.countDistinct("browser_family").alias("browser_family_uniques"),
            f.countDistinct("device_family").alias("device_family_uniques"),
            f.countDistinct("os_family").alias("os_family_uniques")
        ).filter(
            (f.col("browser_family_uniques") > 1) |
            (f.col("device_family_uniques") > 1) |
            (f.col("os_family_uniques") > 1)
        ).count()
    )
    print("Quantidade de linhas com valores nulos por coluna:")
    print(null_keys)

    print("Quantidade total de eventos:")
    print(total_count)

    print("Quantidade de anonymous_id's com mais de um valor possível de browser_family, device_family ou os_family:")
    print(count_multiple_group_keys)


if __name__ == '__main__':
    spark = SparkSession.builder.appName('eda').getOrCreate()
    main(spark)
