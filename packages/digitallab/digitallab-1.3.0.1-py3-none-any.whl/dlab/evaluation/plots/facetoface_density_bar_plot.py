#  Copyright 2021 Dennis Kreber
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from typing import Union

import matplotlib.pyplot as plt
import seaborn as sns

from digitallab.evaluation.plots.facetoface_plot_skeleton import FaceToFacePlotSkeleton


class FaceToFaceDensityBarPlot(FaceToFacePlotSkeleton):
    """
    Density plot which shows the density of a point-wise metric. For example, this plot is suitable for comparing
    runtimes between different methods.

    The following member functions must be called before calling `FaceToFaceDensityBarPlot.plot`:
    `FaceToFaceDensityBarPlot.set_key_to_be_compared`, `set_index_cols`,
    `set_value_of_interest`, `set_first_face`, and `set_second_face`.
    """

    def build_axes_with_grid(self):
        raise NotImplementedError

    def build_legend_for_non_grid(self, axes):
        raise NotImplementedError

    def build_legend_for_grid(self, axes):
        raise NotImplementedError

    def __init__(self, version):
        super().__init__(version)
        self._n_bins = 10

    def set_number_of_bins(self, bw: Union[int, None]):
        """
        Sets the number of bins for the density plot.

        Args:
            bw: Number of bins. Can be None, if number of bins should be determined automatically.

        Returns: Itself

        """
        self._n_bins = bw
        return self

    def build_axes_without_grid(self):
        """
        Builds the matplotlib axes for the plot.
        """
        sns.set(style="ticks", palette="pastel")

        self.filter_data(**self._data_filter)
        self.collect()

        median = self.data[self._comparison_metric_key].median()
        mean = self.data[self._comparison_metric_key].mean()

        ax = sns.distplot(self.data[self._comparison_metric_key], hist=True, kde=False,
                          color=sns.color_palette("colorblind", 3)[0], bins=self._n_bins,
                          hist_kws={"range": self._x_range})
        ax.axvline(median, color=sns.color_palette("colorblind", 3)[1], linestyle="--",
                   label="Median = " + str(round(median, 4)))
        ax.axvline(mean, color=sns.color_palette("colorblind", 3)[2], label="Mean = " + str(round(mean, 4)))

        super()._decorate_axes(ax)

        ax.legend()

        return ax

    def plot(self):
        """
        Builds the plot and displays it. If a save path was specified with `FaceToFacePlotSkeleton.set_save_file`,
        then the generated plot is saved.
        """
        ax = self.build_axes_without_grid()

        if self.save_file_name is not None:
            plt.savefig(self.save_file_name)
        plt.show()
