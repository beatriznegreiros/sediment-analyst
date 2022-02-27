""" Module containing auxiliary functions to handle the StatisticalAnalyzer class and for running
main.py

Author: Beatriz Negreiros and Federica Scolari

"""
from sedimentanalyst.analyzer.config import *


def extract_df(dic=input, file=None):
    """
    Function to extract parsed datafiles and tabularize it into dataframe.

    Args:
        dic (dict):  global input parameters that can be altered in the config.py file
        file (str): path name of the file containing a sieving sample

    Returns:
        df: dataframe containing grain sizes and class weights (parsed according to the config.py)
        list: list of sample's information as following: [samplename, sampledate, (lat, long), porosity,
            sf_porosity], parsed accoridng to the config.py.
    """
    df = pd.read_excel(file, engine="openpyxl", header=None)
    dff = df.copy()
    columns_to_get = [dic["gs_clm"], dic["cw_clm"]]
    dff_gs = dff.iloc[dic["header"]: dic["header"] + dic["n_rows"], columns_to_get]
    dff_gs.reset_index(inplace=True, drop=True)
    dff_gs = dff_gs.astype(float)

    # Get metadata from the dataframe
    # get sample name
    try:
        samplename = dff.iat[dic["index_sample_name"][0], dic["index_sample_name"][1]]
    except Exception as e:
        logging.error("Index for sample name not recognized, "
                      "assigning None to the sample name.")
        samplename = None
        print(e)
        pass

    # get sample date
    try:
        sampledate = dff.iat[dic["index_sample_date"][0], dic["index_sample_date"][1]]
    except Exception as e:
        logging.error("Index for sample date not recognized, "
                      "assigning None to the sample date.")
        sampledate = None
        print(e)
        pass

    # get sample coordinates
    try:
        lat = dff.iat[dic["index_lat"][0], dic["index_lat"][1]]
        long = dff.iat[dic["index_long"][0], dic["index_long"][1]]
    except Exception as e:
        logging.error("Index for latitude and longitude not recognized, "
                      "assigning None to both latitude and longitude.")
        lat, long = None, None
        print(e)
        pass

    # get porosity
    try:
        porosity = dff.iat[dic["porosity"][0], dic["porosity"][1]]
    except Exception as e:
        logging.error("Index for porosity not recognized, "
                      "assigning None User defined porosity.")
        porosity = None
        print(e)
        pass

    # get sf_porosity
    try:
        sf_porosity = dff.iat[dic["SF_porosity"][0], dic["SF_porosity"][1]]
    except Exception as e:
        logging.error("Index for sf_porosity not recognized, "
                      "assigning 6.1 which corresponds to rounded sediments.")
        sf_porosity = 6.1  # default for rounded sediments
        print(e)
        pass

    metadata = [samplename, sampledate, (lat, long), porosity, sf_porosity]

    # Rename and standardize the Grain Size dataframe
    dff_gs.rename(columns={dff_gs.columns[0]: "Grain Sizes [mm]", dff_gs.columns[1]: "Fraction Mass [g]"},
                  inplace=True)
    return dff_gs, metadata


def find_files(folder=None):
    """
    Lists the files in the folder indicated

    Args:
        folder (str): path of the folder to scan (to look for .xlxs files)

    Returns:
        list: list of strings from addresses of all files inside the folder
    """

    # Append / or / in director name if it does not have
    if not str(folder).endswith("/") and not str(folder).endswith("\\"):
        folder = Path(str(folder) + "/")

    # Create a list of shape files or raster files names
    file_list = glob.glob(str(folder) + "/*.xlsx")

    return file_list


def append_global(obj=None, df=None):
    """
    A function to append all information stemming from the class
    Statistical Analyzer into one dataframe for further filtering and analyses

    Args:
        obj (StatisticalAnalyzer) object of the class StatisticalAnalyzer to append
        df (df) dataframe to be appended

    Returns:
        df: appended dataframe with statistics of sample file
    """

    # organize statistics to append in global df
    df_stat = pd.DataFrame()
    df_stat = df_stat.append(obj.statistics_df.transpose())
    df_stat.columns = df_stat.iloc[0]
    df_stat.drop("Name", axis=0, inplace=True)
    df_stat.reset_index(drop=True, inplace=True)

    # extract name and date of the sample
    np.warnings.filterwarnings('ignore', category=np.VisibleDeprecationWarning)
    df_meta = pd.DataFrame(columns=["sample name", "date", "lat", "lon"],
                           data=np.array([[obj.samplename, obj.sampledate, obj.coords[0], obj.coords[1]]]))

    # extract porosity and conductivity
    list_name = obj.porosity_conductivity_df["Name"].to_list()
    list_name_new = []
    for name in list_name:
        list_name_new.append("{} [Porosity]".format(name))
    for name in list_name:
        list_name_new.append("{} [Estimated kf]".format(name))

    df_copo = pd.DataFrame(columns=list_name_new)
    new_row = obj.porosity_conductivity_df["Porosity"].to_list()
    new_row = new_row + obj.porosity_conductivity_df["Corresponding kf [m/s]"].to_list()
    df_copo.loc[0] = new_row

    # extract cumulative
    df_cum = pd.DataFrame(data=[obj.cumulative_df["Cumulative Percentage [%]"].to_numpy()],
                          columns=obj.cumulative_df["Grain Sizes [mm]"].to_numpy())

    # join dataframes
    df_add = pd.concat([df_meta, df_stat, df_copo, df_cum], axis=1)

    # append global dataframe in global
    if df.empty:
        df = df_add
    else:
        df = df.append(df_add, ignore_index=True)

    return df

