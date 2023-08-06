#  Copyright 2021 Dennis Kreber
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from typing import Union

from digitallab.evaluation.data_processing.database_collector_interface import DatabaseCollectorInterface


class GlobalComparisonDatabaseCollector(DatabaseCollectorInterface):
    def __init__(self, version):
        super().__init__(version)
        self._names_of_comparison_units = list()

    def add_unit_to_compare(self, label, **kwargs):
        self._comparison_unit_filters.append(kwargs)
        self._names_of_comparison_units.append(label)
        return self

    def __assert(self):
        assert self._names_of_comparison_units and self._comparison_unit_filters, \
            "You have call 'add_unit_to_compare' at least one time " \
            "before calling 'process'."

    def collect(self):
        self.__assert()
        super().collect()
        self.__replace_comparison_unit_names_with_labels()

        return self.data

    def __replace_comparison_unit_names_with_labels(self):
        replace_dict = dict()
        for comparison_filter, name in zip(self._comparison_unit_filters, self._names_of_comparison_units):
            if name:
                replace_dict[comparison_filter["method"]] = name
        self.data[self._methods_key] = self.data[self._methods_key].replace(replace_dict)
