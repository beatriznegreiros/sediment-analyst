# Sediment Analyst
![Inn River](https://github.com/federicascolari8/PythonProject_Other/raw/main/assets/river_inn.png "Sample Location")

## Welcome

Sediment Analyst is a modularized Python package and dash app that enables sedimentological analyses. By using sieving datasets as input, Sediment Analyst computes sediment statistics. For a complete list of computed statistics see section below (*Outputs*). For using our app, please watch our video tutorial [here](https://youtu.be/zXfN9-M12i0).


## Requirements

Python > 3.0 is required, but Python 3.9 is preferable due to stable behaviors in regard to the packages.

The used *Python* libraries are: *numpy*, *scipy*, *pathlib*, *matplotlib*, *openpyxl*, *pandas*, *seaborn*, *dash*, *pyproj*, *plotly*.

Standard libraries include: *re*, *locale*, *logging*, *glob*, *sys*, *os*, *math*

Important! Checkout the ```requirements.txt``` file for the version requirements of the packages.



## Running the Codes and preparing Inputs

The input data for sediment-analyst consists of Excel/csv files for each sediment sample. Accepted extensions are therefore ```.csv``` and ```.xlsx```. 

Use Sediment Analyst locally by cloning this repository or online with our app. Checkout:

### Clone the repository

    $ git clone https://github.com/beatriznegreiros/sediment-analyst

For running the code in your computer, clone this repository and make sure to install the necessary packages (checkout the ```requirements.txt``` file). Change the input parameters in the ```config.py``` and run ```main.py``` in the subpackage *analyzer*. 

Please note that the plots provided in the *analyzer* subpackage are static (not interactive plots). These may be useful for reports and single sediment sample analyses. 


Sediment Analyst features a novel app for enabling interactive analyses. The app can be hosted locally if you run  ```web_application.py``` in the *app* subpackage. 
Click on the link provided by your console (the link is similar to http://000.0.0.0:0000/). We provide a full video [tutorial](https://youtu.be/zXfN9-M12i0) on how 
you can correctly input where the index information is, so that Sediment Analyst can parse your data files, in case you are not using our template as input file. **Optional inputs** for the app are: latitude and longitude, SF (sphericity index) and Porosity index.

### Use the app

The app can be also accessed [here](https://sedimentanalyst.herokuapp.com), which runs with a [heroku](https://www.heroku.com/) server. Note that here there is a maximum limit of 500 MB when loading in the app. For inputting very large datasets (> 500 MB) we recommend using the app locally. 

[![Image](assets/intro_w_image.jpg)](https://sedimentanalyst.herokuapp.com/)


## Outputs and Capabilities

Sediment Analyst computes the following:
* A summary of sediment characteristics, which can be exported as csv:
    * d10, d16, d25, d30, d50, d84, d90.
    * Mean grain size, geometric mean grain size [(Bunte and Abt, 2001)](https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1752-1688.2001.tb05528.x), grain size standard deviation, geometric standard deviation [(Frings et al., 2011)](https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2010WR009690).
    * Sorting index, Fredle index.
    * Skewness and kurtosis.
    * Coefficient of uniformity, curvature coefficient.
    * Porosity estimators according to empirical equations available in the literature:
        * [Carling and Reader (1982)](https://onlinelibrary.wiley.com/doi/abs/10.1002/esp.3290070407)
        * [Wu and Wang (2006)](https://ascelibrary.org/doi/full/10.1061/%28ASCE%290733-9429%282006%29132%3A8%28858%29)
        * [Wooster et al. (2008)](https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2006WR005815): recommended for gravel-beds with geometric standard deviation between 0.004 m and 0.018 m.
        * [Frings et al. (2011)](https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2010WR009690)
    * Hydraulic conductivity estimators computed with the [Kozeny-Carman Equation](https://link.springer.com/content/pdf/10.1007%2F978-3-642-40872-4_1995-1.pdf). Hydraulic Conductivity (kf) is computed in m/s with each of the above-mentioned computed porosity values.
    * Cumulative percentages according to the [Wentworth scale](https://www.planetary.org/space-images/wentworth-1922-grain-size).
 * Cumulative grain size distribution curves, which are available as:
    * Static plots per sample with the *analyzer* subpackage.
    * Interactive plots with user-selected samples using the *app* subpackage.
 * Only in the app:
    * Bar chart of statistics.
    * Interactive map listing sample information (optional, is generated when latitude (y) and longitude (x) values are available).
 
 *For more information see the documentation of the class StatisticalAnalyzer.*


## Package Structure
Sediment Analyst is structured in two Python subpackagess: *analyzer* and *app*. The app subpackage imports the *analyzer* subpackage for computing sediment statistics and for using utils.
![Code UML](https://github.com/federicascolari8/PythonProject_Other/raw/main/assets/code_uml_sediment_analyst.png "Code UML")


## Code description

##config.py

Module containing all the imported packages and the user inputs necessary for running the StatisticalAnalyzer and StaticPlotter Classes.

| Input | Type | Description |
|-----------------|------|-------------|
|`sample_name`| STR | Name of the sample |
|`header`| INT | Number of lines with a header before the dataset|
|`gs_clm`| INT | Grain size column index|
|`cw_clm`| INT | Class weight column index |
|`porosity`| LIST | Option to provide the porosity manually |
|`SF_porosity`| LIST | Statistical parameter which is/are plotted |
|`index_lat`| LIST | Sample latitudinal coordinate |
|`index_long`| LIST | Sample longitudinal coordinate |
|`folder_path`| STR | Path of folder from which the data is read |
|`index_sample_name`| LIST | Index of the Excel sheet containing the sample name |
|`index_sample_date`| LIST | Index of the Excel sheet containing the date in which the sample was collected |
|`projection`| STR | Definition of the projection |

##utils.py

##statistical_analyzer.py

<br/>

##static_plotter.py

File in which the `StaticPlotter` Class is stored. This Class defines the methods which allow the
plotting and saving as an image of the cumulative grain size distribution curve for each collected sample.

The methods composing the `StaticPlotter` Class are the following:

### `__init__()`

Initializes a StatisticalAnalyzer variable and a dataframe by using the analyzer object.

| Input argument | Type | Description |
|-----------------|------|-------------|
|`analyzer`| StatisticalAnalyzer  | Internally used StatisticalAnalyzer object. |


### `cum_plotter()`
Plots the cumulative grain size distribution curve and saves it as an image.

| Input argument | Type | Description |
|-----------------|------|-------------|
|`output`| STR  | Name of the saved image containing the plot. |

**return:** None

### `__set_main_sec_axis()`

Private method used to set the main secondary axis with the axis *ax* as input argument.

**return:** None

### `__set_min_sec_axis()`

Private method used to set the minor secondary axis with the axis *ax2* as input argument.

**return:** None

### `__set_axis_colour_and_format()`

Private method with the axis *ax* as input, used to define the following:
- Axis tick values for the x-axis.
- Axis tick values for the y-axis. 
- Vertical line across the axis properties.
- Axes labels.

**return:** None

<br/>

##main.py

File where the DataFrame is instantiated, the user-input in retrieved and a list of the files in the user selected folder is created.
Samples contained in the files are then computed.

<br/>

##appconfig.py

Module containing the imported packages necessary to correctly configure the environment for *web_application.py* and *interac_plotter.py*

<br/>

##apputils.py


<br/>

##interac_plotter.py
Module containing the `InteractivePlotter` Class. It has been designed for the creation of the map, 
used to indicate the location of the collected samples, and the interactive plots necessary for the 
comparison of the results of the statistical analysis.  
Here below the description of the methods defined in the `InteractivePlotter` Class:

### `convert_coordinates()`

Transforms the coordinates of a give projection in degrees.

| Input argument | Type | Description |
|-----------------|------|-------------|
|`df`| DataFrame  | DataFrame on which the coordinate transformation is applied. |
|`projection`| STR  | Name of the initial projection. |

**return:** df (DataFrame)

### `create_map()`
Creates a scatter map based on the data contained in the dataframe.

| Input argument | Type | Description |
|-----------------|------|-------------|
|`df`| DataFrame  | DataFrame on which the coordinate transformation is applied. |
|`projection`| STR  | Name of the initial projection. |
|`samples`| LIST  | Names of the samples. |

**return:** fig (Figure)

### `plot_histogram()`

Plots the results in a bar chart based on the statistical parameters selected by the user.

| Input argument | Type | Description |
|-----------------|------|-------------|
|`param`| STR  | Parameters among which the user can choose for the results visualization. |
|`samples`| LIST  | Names of the samples. |

**return:** fig (Figure)

### `plot_gsd()`

Plots the cumulative grain size distribution curve for all selected samples.

| Input argument | Type | Description |
|-----------------|------|-------------|
|`samples`| LIST  | Names of the samples. |

**return:** fig (Figure)

<br/>

### `plot_diameters()`

Plots the calculated sediment diameters in a bar chart for all selected samples.

| Input argument | Type | Description |
|-----------------|------|-------------|
|`samples`| LIST  | Names of the samples. |

**return:** fig (Figure)



