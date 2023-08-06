#  Copyright 2021 Dennis Kreber
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from collections import Iterable

import pandas as pd

from digitallab.evaluation.data_processing.database_collector_interface import DatabaseCollectorInterface


class FaceToFaceDatabaseCollector(DatabaseCollectorInterface):
    def __init__(self, version):
        super().__init__(version)
        self._faces = []
        self._pivot_index_columns = None
        self._pivot_value_key = None

    def set_index_columns(self, index_cols: Iterable):
        """
        Set the name of the variables/columns which uniquely define similar runs/settings.

        Args:
            index_cols: A collection of strings determining the names of the identifying columns
        """
        self._pivot_index_columns = index_cols
        return self

    def add_face(self, **kwargs):
        """
        Adds a face to compare. A face is meant to be a unit/method. Each experiment setting is run for multiple
        units/methods. Even though a setting is repeated with different units/methods they are stored consecutively. To
        compare them directly the units/methods must be defined by this method.

        Example:
        We have methods 'a' and 'b'. For method 'a' we can choose between variant 'c' or 'd'. So our data includes the
        columns 'method' and 'variant'. Let's say we want to compare method 'a' (variant 'c') with method 'b', Then we
        have to call

            add_face(method='a', variant='c')
            add_face(method='b')

        Args:
            **kwargs: Key-value-pairs defining a unit/method
        """
        self._faces.append(kwargs)
        return self

    def set_pivot(self, key):
        self._pivot_value_key = key
        return self

    def __assert(self):
        assert self._pivot_index_columns, "The method 'set_index_columns' was not called before 'process'."
        assert self._pivot_value_key, "The method 'pivot' was not called before 'process'."
        assert self._faces, "The method 'add_face' must be called at least one time before calling 'process'."
        for face in self._faces:
            assert self._methods_key in face.keys(), "Each face must include the pivot key as a dictionary key."
        method_values = {face[self._methods_key] for face in self._faces}
        assert len(method_values) == len(self._faces), "Multiple faces have the same value for the key '" + \
                                                       self._methods_key + "'."

    def collect(self) -> pd.DataFrame:
        """
        Processes the data and returns it. 'set_first_face', 'set_second_face', and 'pivot' must be called
        before calling 'process'

        :return: The dataframe with comparable columns.
        """
        super().collect()
        self.__assert()
        self._comparison_unit_filters = [self._faces[0], self._faces[1]]
        self._preprocess()

        self.data = self.data.pivot_table(index=self._pivot_index_columns, columns=self._methods_key,
                                          values=self._pivot_value_key).dropna()

        self._process_procedural_columns()

        return self.data
