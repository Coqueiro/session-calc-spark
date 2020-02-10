import os

from .test_spark import SparkTest
from entrypoint import main

WRITE_PATH = os.environ['WRITE_PATH']


class SessionCalcTest(SparkTest):

    def test_main(self):
        expected_json_text = '{"A":3,"B":1}'

        try:
            os.system('mkdir /output')
            main(self.spark)
            json_text = open(
                f'{WRITE_PATH}/sessions_by_group_field1.json').read()
        finally:
            os.remove(f'{WRITE_PATH}/sessions_by_group_field1.json')
        self.assertEqual(json_text, expected_json_text)
