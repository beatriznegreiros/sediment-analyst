"""
This module contains all the imported packages (dependencies) and
user inputs for running the classes StatisticalAnalyzer and StaticPlotter.
"""

try:
    import numpy as np
    from scipy import stats
    from pathlib import Path
    from matplotlib import pyplot as plt
    from matplotlib.ticker import FormatStrFormatter
    import pandas as pd
    import openpyxl
    import matplotlib.ticker as mtick
    import seaborn as sns
    import re
    import locale
    import logging
    import glob
    import sys
    import os
    import math
except ImportError:
    print(
        "Error importing necessary packages")

# Dataset path
# sieving_data_add = Path(os.path.abspath(os.getcwd()) + "/datasets/KB08_FC_1-2_nachher.xlsx")
sieving_data_add = "datasets/KB08_FC_1-2_nachher.xlsx"


# USER INPUTS:
# head and columns of the Grain Size (GS) and Class Weight (CW)
def get_input():
    input = {"sample_name": None,
             "header": 9,  # number of lines with a header before the dataset
             "gs_clm": 1,  # grain size column index (start with 0)
             "cw_clm": 2,  # class weight column index (start with 0)
             "n_rows": 16,  # number of rows (available class weights)
             "porosity": [2, 4],  # option to give porosity manually
             "SF_porosity": [2, 5],  # default for rounded sediment
             "index_lat": [5, 2],  # coordinates of the sample (tuple variable)
             "index_long": [5, 3],
             "folder_path": "datasets",
             "index_sample_name": [6, 2],  # index of excel sheet that contains the name of the sample
             "index_sample_date": [3, 2],  # index of excel sheet that contains date that the sample was collected
             "projection": "epsg:3857",  # add projection
             }
    return input
