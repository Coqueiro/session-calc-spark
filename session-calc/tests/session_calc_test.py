import logging
import unittest
from pyspark.sql import SparkSession, Row

from session_calc_utils import get_user_sessions, get_sessions_by_group, write_first_row_as_json


class SparkTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        logger = logging.getLogger("py4j")
        logger.setLevel(logging.ERROR)
        cls.spark = SparkSession.builder.appName("test").getOrCreate()

    @classmethod
    def tearDownClass(cls):
        cls.spark.stop()


class SessionCalcUtilsTest(SparkTest):

    def test_get_user_sessions(self):
        events = self.spark.createDataFrame([
            Row(user_key="1", timestamp_key=1000, group_field="A"),
            Row(user_key="1", timestamp_key=2000, group_field="A"),
            Row(user_key="1", timestamp_key=6000, group_field="A"),
            Row(user_key="1", timestamp_key=9600, group_field="A"),
            Row(user_key="2", timestamp_key=1000, group_field="A"),
            Row(user_key="2", timestamp_key=1000, group_field="A"),
            Row(user_key="2", timestamp_key=8000, group_field="B")
        ])

        user_sessions = get_user_sessions(
            self.spark, events, "user_key", "timestamp_key", 3600)

        expected_user_sessions = self.spark.createDataFrame([
            Row(user_key="1", session_timestamp=1000, group_field="A"),
            Row(user_key="1", session_timestamp=6000, group_field="A"),
            Row(user_key="2", session_timestamp=1000, group_field="A"),
            Row(user_key="2", session_timestamp=8000, group_field="B")
        ])

        self.assertEqual(set(user_sessions.collect()),
                         set(expected_user_sessions.collect()))

    def test_write(self):
        outfile_path = tempfile.mkstemp()[1]
        try:
            lamb.write_lamb(outfile_path)
            contents = open(tempfile_path).read()
        finally:
            # NOTE: To retain the tempfile if the test fails, remove
            # the try-finally clauses
            os.remove(outfile_path)
        self.assertEqual(result, "Mary had a little lamb.\n")
