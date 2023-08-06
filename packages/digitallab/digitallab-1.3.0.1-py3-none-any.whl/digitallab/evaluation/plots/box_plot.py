#  Copyright 2021 Dennis Kreber
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import seaborn as sns

import matplotlib.pyplot as plt
import matplotlib.colors as mc
import colorsys

from digitallab.evaluation.plots.aggregate_plot_skeleton import XYAggregatePlotSkeleton


class BoxPlot(XYAggregatePlotSkeleton):
    def __init__(self, version):
        super().__init__(version)

    def build_axes_without_grid(self):
        ax = sns.boxplot(x=self._xaxis, y=self._yaxis, hue=self._legend_title,
                         data=self.data, hue_order=self._names_of_comparison_units)

        ax.set(xlabel=self._xaxis_name, ylabel=self._yaxis_name)
        self.decorate_box_plots(ax)
        if self._legend_is_hidden:
            ax.legend('', frameon=False)
        else:
            ax.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

    def build_axes_with_grid(self):
        pass

    def plot(self):
        sns.set(style="whitegrid", palette="colorblind", font_scale=self.font_scale)

        if self._use_grid:
            super().collect()
            if self._grid_row_key is not None:
                facetgrid = sns.catplot(x=self._xaxis, y=self._yaxis, hue=self._legend_title,
                                        data=self.data,
                                        col=self._grid_col_key if self._grid_col_label is None else self._grid_col_label,
                                        row=self._grid_row_key if self._grid_row_label is None else self._grid_row_label,
                                        kind="box", sharex=self._sharex, sharey=self._sharey,
                                        legend=(not self._legend_is_hidden))
            else:
                facetgrid = sns.catplot(x=self._xaxis, y=self._yaxis, hue=self._legend_title,
                                        data=self.data,
                                        col=self._grid_col_key if self._grid_col_label is None else self._grid_col_label,
                                        kind="box", sharex=self._sharex, sharey=self._sharey,
                                        legend=(not self._legend_is_hidden))

            for ax in facetgrid.axes.flat:
                self.decorate_box_plots(ax)
            facetgrid.set(xlabel=self._xaxis_name, ylabel=self._yaxis_name)
        else:
            super().collect()
            ax = self.build_axes_without_grid()

        if self.save_file_name is not None:
            plt.savefig(self.save_file_name, bbox_inches='tight', dpi=self.dpi)
        plt.show()

    @staticmethod
    def decorate_box_plots(ax):
        for i, artist in enumerate(ax.artists):
            col = BoxPlot.darken_color(artist.get_facecolor(), 0.3)
            artist.set_edgecolor(artist.get_facecolor())

            # Each box has 6 associated Line2D objects (to make the whiskers, fliers, etc.)
            # Loop over them here, and use the same colour as above
            for j in range(i * 6, i * 6 + 6):
                line = ax.lines[j]
                line.set_color(col)
                line.set_mfc(col)
                line.set_mec(col)
                if j == i * 6 + 4:
                    line.set_linewidth(3)  # ADDITIONAL ADJUSTMENT

    @staticmethod
    def darken_color(color, amount=0.5):
        try:
            c = mc.cnames[color]
        except:
            c = color
        c = colorsys.rgb_to_hls(*mc.to_rgb(c))
        return colorsys.hls_to_rgb(c[0], c[1] - amount * (c[1]), c[2])
