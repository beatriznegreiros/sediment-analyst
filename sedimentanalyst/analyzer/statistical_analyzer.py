""" Module designated for class StatisticalAnalyzer

Author : Beatriz Negreiros

"""

from sedimentanalyst.analyzer.config import *


class StatisticalAnalyzer:
    """
    A class for computing statistical sedimentological parameters using sieving datasets (class weights
    and grain size).

    Attributes:
        original_df (df): dataframe containing in the first column the grain sizes diameters (in mm) and in the second
            column the fraction mass that passes through the corresponding diameter.
        cumulative_df (df): dataframe containing in the first column the grain sizes diameters (in mm) and in the second
            column the cumulative percentages (% in mass, in grams) that passes through the corresponding grain size diameters.
        statistics_df (df): dataframe containing all the statistics of the sample, which includes:
            d10, d16, d25, d30, d50, d60, d75, d84, d90, Mean Grain Site dm [mm], Geometrical mean grain size dg [mm],
            Sorting Index, Fredle Index, Grain Size standard deviation, skewness, kurtosis, coefficient of uniformity Cu,
            curvature coefficient Cc.
        porosity_conductivity_df (df): dataframe containing the porosity estimators (estimated from the grain size
            analysis) according to different literature, as well as the corresponding hydraulic conductivity estimator for
            each of the porosity values according to the Kozeny Carman Equation.
        samplename (str): sample name
        coords (tuple): x and y coordinates, in this order
        porosity (float): porosity values set up by the user, possibly via alternative measurements, such as
            with photogramic approaches.
        sf_porosity (float): sphericity index. For rounded sediments it equals 6.10

    Methods:
        compute_cumulative_df (df): computes cumulative_df dataframe
        compute_statistics_df (df): computes statistics_df dataframe
        compute_porosity_conductivity_df (df): computes porosity_conductivity_df dataframe

    Note:
        See more on the determination of riverbed porosity from Freezecore samples via a Structure from Motion approach
        at Seitz 2020.

    """

    def __init__(self, sieving_df=None, metadata=None):
        """
        Initializes attributes and direct calling of class methods

        Args:
            input (dict): dictionary containing the necessary indexes (rows and columns from the xlsx or csv files)
                for reading relevant sample information.
            sieving_df (df): dataframe containing the sieving results of a sediment sample (1st column containing grain
                sizes and 2nd sample containing the class weights in grams.
            metadata (list): list of single values as metadata, [samplename (str), sampledate (str), (lat (float), long (float)),
                porosity (float), sf_porosity (float)]
        """

        # Attributes
        self.original_df = sieving_df
        self.cumulative_df = pd.DataFrame()
        self.statistics_df = pd.DataFrame()
        self.__interpolation_df = pd.DataFrame()
        self.porosity_conductivity_df = pd.DataFrame()
        self.samplename = metadata[0]
        self.sampledate = metadata[1]
        self.coords = metadata[2]
        self.porosity = metadata[3]
        self.sf_porosity = metadata[4]

        # Methods
        self.compute_cumulative_df()
        self.__compute_interp_dfs()
        self.compute_statistics_df()
        self.compute_porosity_conductivity_df()

    def compute_cumulative_df(self):
        """
        Compute two new columns in the grain size dataframe, which are
        + Percentage Fraction [%] and
        + Cumulative Percentage [%]

        """
        # initialize cumulative dataframe
        self.cumulative_df = pd.concat([self.cumulative_df, self.original_df])
        # create new columns float type in dataframe
        self.cumulative_df["Percentage Fraction [%]"] = np.nan
        self.cumulative_df["Cumulative Percentage [%]"] = np.nan

        # compute percentage fraction
        total_weight = self.original_df.sum()[1]
        self.cumulative_df["Percentage Fraction [%]"] = 100 * self.cumulative_df["Fraction Mass [g]"] / total_weight

        # fill cumulative percentage column
        for i, value in reversed(list(enumerate(self.cumulative_df["Percentage Fraction [%]"]))):
            if i + 1 == len(self.cumulative_df["Percentage Fraction [%]"]):
                self.cumulative_df.at[i, "Cumulative Percentage [%]"] = self.cumulative_df["Percentage Fraction [%]"][
                    i]
            else:
                cumulative = self.cumulative_df.at[i, "Percentage Fraction [%]"] \
                             + self.cumulative_df.at[i + 1, "Cumulative Percentage [%]"]
                self.cumulative_df.at[i, "Cumulative Percentage [%]"] = cumulative
        pass

    def compute_statistics_df(self):
        """
        Fills a dataframe (self.statistics_df) with all relevant statistics by calling smaller private methods

        """
        # create columns to same statistic name and value
        self.statistics_df["Name"] = np.nan
        self.statistics_df["Value"] = np.nan

        # compute statistics
        self.__compute_ds()
        self.__mean_grain_size_dm()
        self.__geometrical_mean_dg()
        self.__sorting_index_1_ds()
        self.__fredle_index()
        self.__standard_deviation()
        self.__geometric_standard_deviation()
        self.__skewness()
        self.__kurtosis()
        self.__uniformity_coefficient()
        self.__curvature_coefficient()

        pass

    def __mean_grain_size_dm(self):
        """
        Computes mean grain size and fills it in the statistics dataframe (self.statistics_df)

        """
        self.statistics_df.at[9, "Name"] = "Mean Grain Size dm [mm]"
        mean_gsdm = 0.0025 * self.__interpolation_df["Grain size (interpolated) "].sum()
        self.statistics_df.at[9, "Value"] = mean_gsdm
        pass

    def __geometrical_mean_dg(self):
        """
        Computes Geometrical mean dg (simplified) by Bunte & Abt 2001 and
        fill statistics dataframe

        """
        self.statistics_df.at[10, "Name"] = "Geometrical mean dg [mm]"

        d16 = self.statistics_df.at[1, "Value"]
        d84 = self.statistics_df.at[7, "Value"]
        self.statistics_df.at[10, "Value"] = np.sqrt([d16 * d84])

        pass

    def __sorting_index_1_ds(self):
        """
        Computes Sorting Index by Bunte & Abt 2001 sqrt(d84/d16) and
        fill statistics dataframe.

        Note: the Sorting Index (SO) is an indicator of available pore space. The higher the SO, the less is the
        available pore space.

        """
        self.statistics_df.at[11, "Name"] = "Sorting Index 1 ds"

        d16 = self.statistics_df.at[1, "Value"]
        d84 = self.statistics_df.at[7, "Value"]
        self.statistics_df.at[11, "Value"] = np.sqrt([d84 / d16])

        pass

    def __fredle_index(self):
        """
        Compute the Fredle Index and fills the statistics dataframe. The Fredle Index is defined as the as quotient of
        the geometric grain size and sorting coefficient.

        Note: the Fredle Index (FI) is an indicator of available pore space. The higher the FI, the higher is the
        available pore space.

        """
        self.statistics_df.at[12, "Name"] = "Fredle - Index"
        fredle_index = self.statistics_df.at[10, "Value"] / self.statistics_df.at[11, "Value"]
        self.statistics_df.at[12, "Value"] = fredle_index
        pass

    def __standard_deviation(self):
        """
        Computes grain size standard deviation and fills statistic dataframe.

        Note: Standard deviation is a measure of the spread and scatter of these sizes around the average or mean
        grain size (Baiyegunhi, C., Liu, K., & Gwavava, O. , 2017).

        """
        self.statistics_df.at[13, "Name"] = "Grain Size std"
        grain_size_std = np.nanstd(self.__interpolation_df["Grain size (interpolated) "].to_numpy())
        self.statistics_df.at[13, "Value"] = grain_size_std

        pass

    def __geometric_standard_deviation(self):
        """
        Computes geometric_standard_deviation by Frings 2001 et. al.

        """
        self.statistics_df.at[14, "Name"] = "Geometric Standard Deviation"

        # temporary dataframe geo_df to compute elements of Frings et al. (2011) equation
        geo_df = self.cumulative_df.drop("Fraction Mass [g]", axis=1)
        geo_df["Percentage Fraction [%]"] = geo_df["Percentage Fraction [%]"].shift(1, fill_value=0)
        geo_df["Teta"] = -np.log2(geo_df["Grain Sizes [mm]"])
        geo_df["Teta(i)"] = (geo_df["Teta"] + geo_df["Teta"].shift(1, fill_value=np.nan)) / 2
        geo_df["fi*Teta(i)"] = geo_df["Teta(i)"] * geo_df["Percentage Fraction [%]"] / 100
        geo_df["result"] = (geo_df["Percentage Fraction [%]"] / 100) * (
                geo_df["Teta(i)"] - geo_df["fi*Teta(i)"].sum()) ** 2

        # compute geometric_std
        geometric_std = np.sqrt(geo_df["result"].sum())
        self.statistics_df.at[14, "Value"] = geometric_std

        pass

    def __skewness(self):
        """
        Computes skewness of grain sizes

        """
        self.statistics_df.at[15, "Name"] = "Skewness"

        skewness = stats.skew(self.__interpolation_df["Grain size (interpolated) "])
        self.statistics_df.at[15, "Value"] = skewness
        pass

    def __kurtosis(self):
        """
        Computes kurtosis of grain sizes

        """
        self.statistics_df.at[16, "Name"] = "Kurtosis"

        kurtosis = stats.kurtosis(self.__interpolation_df["Grain size (interpolated) "])
        self.statistics_df.at[16, "Value"] = kurtosis
        pass

    def __compute_ds(self):
        """
        Computes characteristic grain sizes (d10, d16, d25, d30, d50, d60, d75, d84, d90)
        and fills statistic dataframe

        """
        # type of characteristic grain size (cgs)
        ds = [10, 16, 25, 30, 50,
              60, 75, 84, 90]

        # assign each ds value to a line of the dataframe
        for n in range(0, 9):
            # name ds
            self.statistics_df.at[n, "Name"] = "d{s}".format(s=ds[n])

            # assign value to ds
            boolean_filter = self.__interpolation_df["Cumulative (interpolated) "] == ds[n]
            ds_value = self.__interpolation_df[boolean_filter.to_list()].iat[0, 1]
            self.statistics_df.at[n, "Value"] = ds_value
        pass

    def __uniformity_coefficient(self):
        """
        Computes uniformity coefficient and fills statistics dataframe

        """
        self.statistics_df.at[17, "Name"] = "Coefficient of uniformity - Cu"

        d10 = self.statistics_df.at[0, "Value"]
        d60 = self.statistics_df.at[5, "Value"]
        self.statistics_df.at[17, "Value"] = d60 / d10
        pass

    def __curvature_coefficient(self):
        """
        Computes curvature coefficient and fills statistics dataframe

        """
        self.statistics_df.at[18, "Name"] = "Curvature coefficient - Cc"

        d10 = self.statistics_df.at[0, "Value"]
        d30 = self.statistics_df.at[3, "Value"]
        d60 = self.statistics_df.at[5, "Value"]
        self.statistics_df.at[18, "Value"] = d30 ** 2 / (d60 * d10)
        pass

    def __compute_interp_dfs(self):
        """
        Computes linearly interpolated grain sizes for several cumulative percentages (every 0.25%)

        """
        # extract data from sample
        y = np.flip(np.array(self.cumulative_df["Grain Sizes [mm]"]))
        x = np.flip(np.array(self.cumulative_df["Cumulative Percentage [%]"]))

        # estimate grain size linearly for a increase of 0.25% of cumulative percentage
        x_vals = np.linspace(0, 100, 401)
        y_interpolated = np.interp(x_vals, x, y)

        # fill dataframe with results of interpolation
        self.__interpolation_df["Cumulative (interpolated) "] = x_vals
        self.__interpolation_df["Grain size (interpolated) "] = y_interpolated

        pass

    def compute_porosity_conductivity_df(self):
        """
        Compute porosity predictors and corresponding hydraulic conductivities (for each estimated porosity
        value)

        """
        # create columns to same statistic name and value
        self.porosity_conductivity_df["Name"] = np.nan
        self.porosity_conductivity_df["Porosity"] = np.nan

        # name porosity predictions by author
        self.__porosity_name()

        # compute predictors
        self.__porosity_carling()
        self.__porosity_wu()
        self.__porosity_wooster()
        self.__porosity_frings()
        self.__porosity_user()

        # compute kfs based on porosity predictors and input
        self.__compute_kfs()

        pass

    def __porosity_name(self):
        """
        Create columns the porosity estimators according to available literature

        """
        authors = ["Carling and Reader (1982)",
                   "Wu and Wang (2006)",
                   "Wooster et al. (2008)",
                   "Frings et al. (2011) ",
                   "User input"]
        for k, name in enumerate(authors):
            self.porosity_conductivity_df.at[k, "Name"] = name

        pass

    def __porosity_carling(self):
        """
        Calculates porosity estimator according to Carling & Reader (1982)

        """
        d50 = self.statistics_df.at[4, "Value"]
        carling = -0.0333 + (0.4665 / ((1000 * d50 / 1000) ** 0.21))
        self.porosity_conductivity_df.at[0, "Porosity"] = carling
        pass

    def __porosity_wu(self):
        """
        Calculates porosity estimator according to Wu and Wang (2006)

        """
        d50 = self.statistics_df.at[4, "Value"]
        wu = 0.13 + (0.21 / ((1000 * d50 / 1000 + 0.002) ** 0.21))
        self.porosity_conductivity_df.at[1, "Porosity"] = wu
        pass

    def __porosity_wooster(self):
        """
           Calculates porosity estimator according to Wooster et al. (2008)

        """
        geometric_std = self.statistics_df.at[14, "Value"]
        wooster = 0.621 * np.exp(-0.457 * geometric_std)
        self.porosity_conductivity_df.at[2, "Porosity"] = wooster
        pass

    def __porosity_frings(self):
        """
        Calculates porosity estimator according to Frings et al. (2011)

        """
        geometric_std = self.statistics_df.at[14, "Value"]
        cumulative_5mm = self.cumulative_df.at[9, "Cumulative Percentage [%]"] / 100
        frings = 0.353 - 0.068 * geometric_std + 0.146 * cumulative_5mm
        self.porosity_conductivity_df.at[3, "Porosity"] = frings
        pass

    def __porosity_user(self):
        """
        Set porosity value from the user into the summary statistics dataframe
        """
        try:
            self.porosity_conductivity_df.at[4, "Porosity"] = self.porosity
        except:
            self.porosity_conductivity_df.at[4, "Porosity"] = np.nan
        pass

    def print_excel(self, file_name="statistics.xlsx"):
        """
        Print all attribute dataframes into excel sheet output is saved
        into local folder "outputs"

        Args:
            file_name (str): Path to save the file

        """
        # Creating Excel Writer Object from Pandas
        wb = openpyxl.Workbook()
        wb.save(file_name)
        with pd.ExcelWriter(file_name) as writer:
            self.cumulative_df.to_excel(writer, sheet_name="Sample Summary")
            self.statistics_df.to_excel(writer, sheet_name="Statistics")
            self.porosity_conductivity_df.to_excel(writer, sheet_name="PorosityAndConductivity")
        pass

    def __compute_kfs(self):
        """
        Computes hydraulic conductivity values based on porosity from the user input
        and porosity predictions

        """

        self.porosity_conductivity_df["Corresponding kf [m/s]"] = np.nan

        for k, porosity in enumerate(self.porosity_conductivity_df["Porosity"]):
            kf = self.__kozeny_carman(porosity=porosity)
            self.porosity_conductivity_df.at[k, "Corresponding kf [m/s]"] = kf

        pass

    def __kozeny_carman(self, porosity=np.nan):
        """
        Computes the hydraulic conductivity according to the Kozeny Carman Equation

        Args:
             porosity (float): Sample porosity

        Returns:
             float: Sample hydraulic conductivity [m\s]
        """
        kozeny_df = pd.DataFrame()
        kozeny_df = pd.concat([kozeny_df, self.cumulative_df])
        kozeny_df["D_ave_i [cm]"] = ((kozeny_df["Grain Sizes [mm]"].shift(1, fill_value=0) / 10) ** 0.404) * (
                kozeny_df["Grain Sizes [mm]"] / 10) ** 0.595
        kozeny_df["Deff_i [cm]"] = kozeny_df["Percentage Fraction [%]"] / kozeny_df["D_ave_i [cm]"]
        Deff_i_cm = 100 / kozeny_df["Deff_i [cm]"].sum()
        SF = self.sf_porosity
        e = porosity / (1 - porosity)
        cte = 19900

        kozeny_carman_kf = cte * ((Deff_i_cm / 100) ** 2) * (1 / (SF ** 2)) * ((e ** 3) / (1 + e))

        return kozeny_carman_kf
