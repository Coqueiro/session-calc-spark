import os
import tempfile
import unittest

from .spark_test import SparkTest
from session_calc_utils import get_user_sessions, get_sessions_by_group, write_first_row_as_json


class SessionCalcUtilsTest(SparkTest):

    def test_get_user_sessions(self):
        events = self.spark.createDataFrame([
            {"user_key": "1", "timestamp_key": 1000, "group_field1": "A"},
            {"user_key": "1", "timestamp_key": 2000, "group_field1": "A"},
            {"user_key": "1", "timestamp_key": 6000, "group_field1": "A"},
            {"user_key": "1", "timestamp_key": 9600, "group_field1": "A"},
            {"user_key": "2", "timestamp_key": 1000, "group_field1": "A"},
            {"user_key": "2", "timestamp_key": 1000, "group_field1": "A"},
            {"user_key": "2", "timestamp_key": 8000, "group_field1": "B"},
        ])

        expected_user_sessions = self.spark.createDataFrame([
            {"user_key": "1", "session_timestamp": 1000, "group_field1": "A"},
            {"user_key": "1", "session_timestamp": 6000, "group_field1": "A"},
            {"user_key": "2", "session_timestamp": 1000, "group_field1": "A"},
            {"user_key": "2", "session_timestamp": 8000, "group_field1": "B"},
        ])
        columns = expected_user_sessions.schema.names

        user_sessions = get_user_sessions(
            self.spark, events, "user_key", "timestamp_key", 3600
        ).select(*columns)

        self.assertEqual(user_sessions.collect(),
                         expected_user_sessions.collect())

    def test_get_sessions_by_group(self):
        user_sessions = self.spark.createDataFrame([
            {"user_key": "1", "session_timestamp": 1000,
                "group_field1": "A", "group_field2": "X"},
            {"user_key": "1", "session_timestamp": 6000,
                "group_field1": "A", "group_field2": "Y"},
            {"user_key": "2", "session_timestamp": 1000,
                "group_field1": "A", "group_field2": "Z"},
            {"user_key": "2", "session_timestamp": 8000,
                "group_field1": "B", "group_field2": "W"},
        ])

        expected_sessions_by_group = self.spark.createDataFrame([
            {"A": 3, "B": 1},
        ])
        columns = expected_sessions_by_group.schema.names

        sessions_by_group = get_sessions_by_group(
            user_sessions, "group_field1").select(*columns)

        self.assertEqual(sessions_by_group.collect(),
                         expected_sessions_by_group.collect())

    def test_write_first_row_as_json(self):
        df = self.spark.createDataFrame([
            {"A": 3, "B": 1},
        ])
        path = tempfile.mkstemp()[1]
        expected_json_text = '{"A":3,"B":1}'

        try:
            write_first_row_as_json(df, path)
            json_text = open(path).read()
        finally:
            os.remove(path)
        self.assertEqual(json_text, expected_json_text)
