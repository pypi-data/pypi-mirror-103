#  Copyright 2021 Dennis Kreber
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import matplotlib.pyplot as plt
import seaborn as sns

from digitallab.evaluation.plots.aggregate_plot_skeleton import XAggregatePlotSkeleton


class ECDFPlot(XAggregatePlotSkeleton):
    def __init__(self, version):
        super().__init__(version)

    def build_axes_without_grid(self):
        super().collect()
        sns.set(style="whitegrid", palette="colorblind", font_scale=self.font_scale)

        ax = sns.ecdfplot(self.data, x=self._xaxis, hue=self._methods_key_print_label, hue_order=self._names_of_comparison_units)

        super()._decorate_axes(ax)

        self.build_legend_for_non_grid(ax)

    def build_axes_with_grid(self):
        super().collect()
        sns.set(style="whitegrid", palette="colorblind", font_scale=self.font_scale)

        facet_grid = sns.FacetGrid(self.data,
                                   col=self._grid_col_key if self._grid_col_label is None else self._grid_col_label,
                                   row=self._grid_row_key if self._grid_row_label is None else self._grid_row_label,
                                   hue=self._methods_key_print_label,
                                   legend_out=True,
                                   sharex=self._sharex,
                                   sharey=self._sharey)
        facet_grid.map(sns.ecdfplot, self._xaxis)
        facet_grid.add_legend()

    def plot(self):
        if self._use_grid:
            self.build_axes_with_grid()
        else:
            self.build_axes_without_grid()

        if self.save_fig_size is not None:
            fig = plt.gcf()
            fig.set_size_inches(self.save_fig_size[0], self.save_fig_size[1])

        if not self._use_grid:
            plt.tight_layout()

        if self.save_file_name is not None:
            plt.savefig(self.save_file_name, bbox_inches='tight', dpi=self.dpi)
        plt.show()
