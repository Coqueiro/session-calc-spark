import os

from .test_spark import SparkTest
from entrypoint import main

WRITE_PATH = os.environ['WRITE_PATH']


class SessionCalcTest(SparkTest):

    def test_main(self):
        expected_json_text = '{"A":3,"B":1}'
        path = f'{WRITE_PATH}/sessions_by_group_field1.json'
        try:
            os.system(f'mkdir {WRITE_PATH}')
            main(self.spark)
            json_text = open(path).read()
        finally:
            os.remove(path)
        self.assertEqual(json_text, expected_json_text)
