#  Copyright 2021 Dennis Kreber
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from typing import Iterable, Union
import abc

import pandas as pd

from digitallab.evaluation.data_processing.facetoface_database_collector import FaceToFaceDatabaseCollector
from digitallab.evaluation.plots.plot_skeleton import PlotSkeleton


class FaceToFacePlotSkeleton(FaceToFaceDatabaseCollector, PlotSkeleton, abc.ABC):
    """
    Skeleton class to build face-to-face-plots. A face-to-face plot is meant to visualize direct comparisons between
    runs.
    """

    def __init__(self, version):
        PlotSkeleton.__init__(self)
        FaceToFaceDatabaseCollector.__init__(self, version)

        self._comparison_metric_key = None
        """Name of column which includes the value of interest, e.g., runtimes, objective values, etc."""

        self._first_face_name = None
        """Name of first face"""

        self._second_face_name = None
        """Name of second face"""

        self._comp_metric = None

        self.__check_first_face = False
        self.__check_second_face = False

    def add_face(self, name: str, **kwargs):
        """
        Same as `digitallab.evaluation.data_processing.FaceToFaceDataProcessing.add_face`.
        Additionally, this method throws an `AssertionError` if more than two faces are added.

        Args:
            name: Name of the face.
            **kwargs: Same as
            `digitallab.evaluation.data_processing.FaceToFaceDataProcessing.add_face`
        """
        if not self._faces:
            self._first_face_name = name
            self.__check_first_face = True
        elif len(self._faces) == 1:
            self._second_face_name = name
            self.__check_second_face = True
        if len(self._faces) >= 2:
            raise ValueError("Only two faces are supported.")
        return super().add_face(**kwargs)

    def set_first_face(self, name: str, **kwargs):
        """
        Same as `add_face` but does not append a face. Instead the first face is set.

        Args:
            name: Name of the face.
            **kwargs: Same as `add_face`.

        Returns: Itself.

        """
        self._first_face_name = name
        if len(self._faces) >= 1:
            self._faces[0] = kwargs
        elif not self._faces:
            self.add_face(name, **kwargs)
        self.__check_first_face = True
        return self

    def set_second_face(self, name, **kwargs):
        """
        Same as `add_face` but does not append a face. Instead the second face is set.

        Args:
            name: Name of the face.
            **kwargs: Same as `add_face`.

        Returns: Itself.

        """
        self._second_face_name = name
        if len(self._faces) >= 2:
            self._faces[1] = kwargs
        elif len(self._faces) == 1:
            self.add_face(name, **kwargs)
        else:
            self.add_face(name, **kwargs)
            self.add_face(name, **kwargs)
        self.__check_second_face = True
        return self

    def set_value_of_interest(self, key: str, label: Union[str, None] = None):
        self._comparison_metric_key = key
        self._yaxis_label = label
        return self

    def __assert(self):
        assert self.__check_first_face and self.__check_second_face, "Both faces were not set. Please call " \
                                                                     "'set_first_face' and 'set_second_face' " \
                                                                     "before calling 'process'."
        assert self._comparison_metric_key, "'set_value_of_interest' was not called before 'process'."

    def collect(self) -> pd.DataFrame:
        """
        Processes the data and returns it. 'FaceToFacePlotSkeleton.set_first_face',
        'FaceToFacePlotSkeleton.set_second_face', 'FaceToFacePlotSkeleton.set_index_cols',
        `FaceToFacePlotSkeleton.set_value_of_interest`, and
        `FaceToFacePlotSkeleton.set_key_to_be_compared` must be called
        before calling 'FaceToFacePlotSkeleton.process'.

        Returns: Processed data

        """
        self.__assert()
        super().collect()

        return self.data

    @abc.abstractmethod
    def build_axes_without_grid(self):
        pass

    @abc.abstractmethod
    def plot(self):
        pass
