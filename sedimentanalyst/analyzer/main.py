""" Main script to exemplify the use of Sediment Analyst

This script contains the step-by-step process
It should be clean, short, and tell a "story" of the
functionality of the entire code

Functions:
----
* first_function: ...


"""

from sedimentanalyst.analyzer.statistical_analyzer import StatisticalAnalyzer
from sedimentanalyst.analyzer.utils import *
from sedimentanalyst.analyzer.static_plotter import StaticPlotter
from sedimentanalyst.analyzer.config import get_input


def main():

    # Instantiate a dataframe to hold all the  the samples statistics
    df_global = pd.DataFrame()

    # Input indexes without been global variable (same function used by the web application)
    input_local = get_input()

    # List of files in the user-selected folder (given in the config)
    files_to_loop = find_files(input_local["folder_path"])

    # loop through all the samples and compute corresponding
    for i, file_name in enumerate(files_to_loop):
        print(file_name)
        # extract the sieving table from excel or csv
        sieving_df, metadata = extract_df(dic=input_local, file=file_name)

        # call the class StatisticalAnalyzer
        analyzer = StatisticalAnalyzer(sieving_df=sieving_df, metadata=metadata)

        print(analyzer.statistics_df)
        # print(analyzer.sampledate, analyzer.samplename, analyzer.coords)

        # append global dataframe
        df_global = append_global(obj=analyzer,
                                  df=df_global
                                  )
        df_global.to_excel("global_dataframe.xlsx")

        # call the class StaticPlotter
        plotter = StaticPlotter(analyzer)

        # outputs the cumulative grain size distribution curve
        plotter.cum_plotter('outputs/' + file_name[8:-5] + '.png')

    pass


if __name__ == "__main__":
    # Call main function
    main()
