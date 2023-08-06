#  Copyright 2021 Dennis Kreber
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from collections import Iterable
from typing import Union

import numpy as np

from digitallab.evaluation.data_processing.global_comparison_database_collector import GlobalComparisonDatabaseCollector


class AveragesTable(GlobalComparisonDatabaseCollector):
    def __init__(self, version):
        super().__init__(version)
        self._save_path = None
        self._highlight_min = False
        self._highlight_max = False

        self._instance_keys = None
        self._instance_keys_print_labels = None

        self._pivot_value_key = None

    def set_instance_keys(self, keys: Iterable, labels: Union[None, Iterable] = None):
        self._instance_keys = keys
        if labels is None:
            self._instance_keys_print_labels = keys
        else:
            self._instance_keys_print_labels = labels
        return self

    def set_value_of_interest(self, key: str):
        self._pivot_value_key = key
        return self

    def set_highlight_min(self, b):
        self._highlight_min = b
        if b:
            self._highlight_max = False

    def set_highlight_max(self, b):
        self._highlight_max = b
        if b:
            self._highlight_min = False

    def __assert(self):
        pass

    def collect(self):
        self.__assert()
        super().collect()
        self.__rename_instances()
        self.__rename_method()

    def __rename_instances(self):
        rename_dict = {key: label for key, label in
                       zip(self._instance_keys, self._instance_keys_print_labels)}
        self.data.rename(columns=rename_dict, inplace=True)

    def __rename_method(self):
        rename_dict = dict()
        rename_dict[self._methods_key] = self._methods_key_print_label
        self.data.rename(columns=rename_dict, inplace=True)

    def build_table(self):
        self.collect()
        table = self.data.pivot_table(values=self._pivot_value_key, index=self._instance_keys_print_labels,
                                      columns=self._methods_key_print_label, aggfunc=np.mean)
        return table

    def set_save_path(self, path):
        self._save_path = path
