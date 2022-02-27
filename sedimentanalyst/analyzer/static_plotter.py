""" Module designated for the class StaticPlotter

Author : Federica Scolari

"""

from sedimentanalyst.analyzer.config import *


class StaticPlotter:
    """
    A class for creating the static plots of the cumulative grain size distribution curves

    Attributes:
        analyzer (StatisticalAnalyzer): StatisticalAnalyzer object containing all the computed sample statistics.
                                        For more information check the Class StatisticalAnalyzer
        cum_df: DataFrame containing the Grain Sizes [mm] and the corresponding Cumulative Percentage [%]

    Methods:
        cum_plotter(output): Plots the cumulative grain size distribution curve for each sample
    """

    def __init__(self, analyzer):
        self.actual_analyzer = analyzer
        self.cum_df = self.actual_analyzer.cumulative_df

    def cum_plotter(self, output):
        """
        Method to output the cumulative grain size distribution curve and save it as an image

        Args:
             output: str, name of the image containing the outputs

        Returns:
             None
        """

        fig, ax = plt.subplots(figsize=(8.0, 5.0))
        plt.xscale('log')
        ax.grid(which='both', alpha=0.5)
        ax.set_ylim(bottom=0, top=100)
        plt.plot(self.cum_df.iloc[:, 0], self.cum_df.iloc[:, 3], label=self.actual_analyzer.samplename, color="blue")

        # call private method to set the main secondary axis
        self.__set_main_sec_axis(ax)
        ax2 = ax.twiny()
        # call private method to set minor secondary axis
        self.__set_min_sec_axis(ax2)
        # private method to edit and modify axis' look
        self.__set_axis_colour_and_format(ax)

        fig.suptitle('Cumulative Grain Size Distribution Curve')
        plt.tight_layout()
        # figure is saved
        plt.savefig(output, dpi=200)
        plt.show()

    def __set_main_sec_axis(self, ax):
        """
        Private method that defines the main secondary axis

        Args:
             ax: matplotlib.axes._subplots.AxesSubplot, axesSubplot object defining the main axis

        Returns:
             None
        """
        # setting text and appearance of the various ticks

        ax.text(0.22, 1.18, 'Sand', fontsize=10, transform=ax.transAxes, verticalalignment='top')
        ax.add_patch(plt.Rectangle((0.074, 1), 0.389, 0.21, clip_on=False, transform=ax.transAxes,
                                   linewidth=1, fill=False))
        ax.text(0.60, 1.18, 'Gravel', fontsize=10, transform=ax.transAxes, verticalalignment='top')
        ax.add_patch(plt.Rectangle((0.074 + 0.389, 1), 0.384, 0.21, clip_on=False, transform=ax.transAxes,
                                   linewidth=1, fill=False))
        ax.text(0.88, 1.13, 'Cobble', fontsize=10, transform=ax.transAxes, verticalalignment='top')
        ax.add_patch(plt.Rectangle((0.847, 1), 0.1533, 0.21, clip_on=False, transform=ax.transAxes,
                                   linewidth=1, fill=False))
        ax.text(0.003, 1.13, 'Silt', fontsize=10, transform=ax.transAxes, verticalalignment='top')
        ax.add_patch(plt.Rectangle((0, 1), 0.074, 0.21, clip_on=False, transform=ax.transAxes, linewidth=1, fill=False))

    def __set_min_sec_axis(self, ax2):
        """
        Private method defining the minor secondary axis

        Args:
             ax2: matplotlib.axes._subplots.AxesSubplot, axesSubplot object defining the minor secondary axis

        Returns:
             None
        """

        # Secondary axis to outputs sediment classes
        categories = ['', 'fine', 'medium', 'coarse', 'fine', 'medium', 'coarse', '']
        ticks = [0.06, 0.2, 0.63, 2, 6, 20, 63, 250]
        ax2.set_xscale('log')
        ax2.set_xlim(left=0.031, right=250)
        ax2.set_xticks(ticks, minor=False)
        ax2.set_xticklabels(categories, minor=False, horizontalalignment='right')
        ax2.tick_params(which='major', length=8)
        ax2.tick_params(which='minor', length=0)
        ax2.xaxis.tick_top()
        props = dict(boxstyle='square', fill=False, alpha=1)

    def __set_axis_colour_and_format(self, ax):
        """
        Private method which sets the output properties

        Args:
             ax: matplotlib.axes._subplots.AxesSubplot, axesSubplot object defining the main secondary axis

        Returns:
             None
        """

        a = [0.06, 0.20, 0.63, 2.00, 6.00, 20.00, 63.00, 250]
        b = np.arange(0, 110, 10)
        ax.axvline(0.1, color='black', alpha=0.3, linewidth=0.5)
        ax.axvline(1.0, color='black', alpha=0.3, linewidth=0.5)
        ax.axvline(10, color='black', alpha=0.3, linewidth=0.5)
        ax.axvline(100, color='black', alpha=0.3, linewidth=0.5)
        ax.set_xticks(a)
        ax.set_yticks(b)
        ax.tick_params(which='minor', length=0)
        ax.xaxis.set_major_formatter(mtick.FormatStrFormatter('%1.2f'))
        ax.set_xlim(left=0.031, right=250)
        ax.set_xlabel('Grain Size [mm]')
        ax.set_ylabel('Percentage [%]')
