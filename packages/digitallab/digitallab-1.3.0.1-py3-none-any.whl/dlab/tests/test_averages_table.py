from unittest import TestCase
import importlib

class MockSingleton:
    def __init__(self, decorated):
        self._decorated = decorated

    def instance(self):
        return self._decorated()


import digitallab.helper.db_access


@MockSingleton
class MockDBAccess:
    def connect(self, mongodb_url, mongodb_db, keys_json_path: str, cache_id: str = "default"):
        self.is_connected = True

    def get_dataframe(self):
        return pd.read_csv("mock_data.csv")


digitallab.helper.db_access.DBAccess = MockDBAccess

import pandas as pd
from digitallab.evaluation.tables.averages import AveragesTable


def relative_time(low, high):
    return low / high


class TestFaceToFaceDensityBarPlotPlot(TestCase):
    @classmethod
    def tearDownClass(cls) -> None:
        importlib.reload(digitallab.helper.db_access)

    def test_plot_shows_without_errors(self):
        table = AveragesTable("test"). \
            set_methods_key("method", label="Method"). \
            add_unit_to_compare("Low", method="low"). \
            add_unit_to_compare("High", method="high"). \
            set_value_of_interest("runtime"). \
            set_instance_keys(("prop1", "prop2"), labels=("Property 1", "Property 2")). \
            build_table()
        print(table)
