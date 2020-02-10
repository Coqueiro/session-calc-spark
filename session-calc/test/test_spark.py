import logging
import unittest
from pyspark.sql import SparkSession


class SparkTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        logger = logging.getLogger('py4j')
        logger.setLevel(logging.ERROR)
        cls.spark = SparkSession.builder.appName('test').getOrCreate()

    @classmethod
    def tearDownClass(cls):
        cls.spark.stop()
