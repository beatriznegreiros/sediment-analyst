""" Accessory elements for the web app

Author: Beatriz Negreiros

"""

from sedimentanalyst.app.appconfig import *
from sedimentanalyst.analyzer.statistical_analyzer import StatisticalAnalyzer


class Accessories:
    """
    A class for allocating accessories elements for the Dash app, including layout and Dash component settings,
    extensive callouts and parsing of input contents.

    Attributes:
        style_upload (dict): style information for a dropbox component
        intro_text (dash.dcc.Markdown.Markdown): markdown test for introducing the app
        inputs_text (dash.dcc.Markdown.Markdown): markdown text for explaining the inputs
        img_style(dict): style information for formatting images
        input_boxes (list): list of Input objects for enabling user to enter the indexing information to read from
        his/her files
        style_graph (dict) style information for the graph components
        style_statistic (dict): style information for the statistic dropdown

    Methods:
        parse_contents (tuple): tuple of object (sedimentanalyst.analyzer.StatisticalAnalyzer) plus an object of
        type html.Div with reading messages.
    """

    def __init__(self):
        """
        Initializes object of the class Accessories, no input parameter is required
        """
        # Variables for style args
        self.style_upload = {
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        }

        self.intro_text = dcc.Markdown(
            '''
                ### Welcome
                
                Sediment Analyst is a web application coded in Python-3 to leverage a quick, interactive, and 
                visual sedimentological analyses. By inputting datasets of sieved class weights (see examples 
                [here](https://github.com/federicascolari8/PythonProject/blob/main/templates/template-sample-file.xlsx)),
                Sediment Analyst computes characteristic grain sizes (namely, d10, d16, d25, d30, d50, d60, d75, d84, 
                d90), mean grain size, geometrical mean grain size, porosity, and hydraulic conductivity estimators. 
                Checkout our video 
                [tutorial](https://youtu.be/zXfN9-M12i0).
                
                '''
        )

        self.inputs_text = dcc.Markdown(
            '''
                ### Inputs
                Enter below the information regarding your files. When *index* is indicated, enter the
                __row index__, __column index__, separated by comma (,) in the fields below. For instance, if the 
                sample name lives on the row 0 (first row) and column 2 (third column): type 0,2 in the field *samplename*.
                The fields are currently filled in by default according to our template, which we made available 
                [here](https://github.com/federicascolari8/PythonProject/blob/main/templates/template-sample-file.xlsx).
                
                '''
        )

        self.img_style = {'width': '100%',
                          'height': '500px',
                          'display': 'inline-block !important',
                          'margin': 'auto !important'}

        self.input_boxes = [
            dcc.Markdown(
                '''
                Delete default input values below for personalizing the parsing of the files contents when not using our 
                [template](https://github.com/federicascolari8/PythonProject/blob/main/templates/template-sample-file.xlsx).
                In following, press the 'RUN' button below '''),
            dcc.Input(id="header", type="number", placeholder="table's header", value=9),
            dcc.Input(id="gs_clm", type="number", placeholder="grain sizes column index (start from zero)",
                      value=1),
            dcc.Input(id="cw_clm", type="number", placeholder="class weight column index (start from zero)",
                      value=2),
            dcc.Input(id="n_rows", type="number", placeholder="number of rows (sieves) to read",
                      value=16),
            dcc.Input(id="porosity", type="number", placeholder="porosity index", value=2.4),
            dcc.Input(id="SF_porosity", type="number", placeholder="SF_porosity index", value=2.5),
            dcc.Input(id="index_lat", type="number", placeholder="latitude index", value=5.2),
            dcc.Input(id="index_long", type="number", placeholder="longitude index", value=5.3),
            dcc.Input(id="index_sample_name", type="number", placeholder="sample name index", value=6.2),
            dcc.Input(id="index_sample_date", type="number", placeholder="sample date index", value=4.2),
            dcc.Input(id="projection", type="text", placeholder="projection as epsg", value="epsg:3857"),
        ]

        self.style_graph = {'display': 'inline-table',
                            'width': '75%',
                            'text-align': 'center'}

        self.style_statistic = {'display': 'inline-table',
                                'width': '75%',
                                'text-align': 'left'}

    # Auxiliary function for parsing contents of the files
    def parse_contents(self, contents, filename, date, input_dict_app):
        """
        Args:
            contents (dash.dcc.Input.Input): Contents of the file containing the sample data (class weights and
            corresponding grain sizes)
            filename (dash.dcc.State.State): Filename
            date (dash.dcc.State.State):  date of last modified
            input_dict_app (dict): Index parameters input by the user necessary to read and parse the contents
                of the file

        Returns:
            StatisticalAnalyzer: object for accessing necessary attributes of the class.
        """
        content_type, content_string = contents.split(',')

        decoded = base64.b64decode(content_string)
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded), engine="openpyxl", header=None)

        # clean the dataset by catching only inputs indicated with the indexes
        dff = df.copy()
        columns_to_get = [input_dict_app["gs_clm"], input_dict_app["cw_clm"]]
        dff_gs = dff.iloc[input_dict_app["header"]: input_dict_app["header"] + input_dict_app["n_rows"],
                 columns_to_get]
        dff_gs.reset_index(inplace=True, drop=True)
        dff_gs = dff_gs.astype(float)

        # Get metadata from the dataframe
        # get sample name
        try:
            samplename = dff.iat[input_dict_app["index_sample_name"][0], input_dict_app["index_sample_name"][1]]
        except:
            samplename = None
            pass

        # get sample date
        try:
            sampledate = dff.iat[input_dict_app["index_sample_date"][0], input_dict_app["index_sample_date"][1]]
        except:
            sampledate = None
            pass

        # get sample coordinates
        try:
            lat = dff.iat[input_dict_app["index_lat"][0], input_dict_app["index_lat"][1]]
            long = dff.iat[input_dict_app["index_long"][0], input_dict_app["index_long"][1]]
        except:
            lat, long = None, None
            pass

        # get porosity
        try:
            porosity = dff.iat[input_dict_app["porosity"][0], input_dict_app["porosity"][1]]
        except:
            porosity = None
            pass

        # get sf_porosity
        try:
            sf_porosity = float(dff.iat[input_dict_app["SF_porosity"][0], input_dict_app["SF_porosity"][1]])
        except:
            sf_porosity = 6.1  # default for rounded sediments
            pass

        metadata = [samplename, sampledate, (lat, long), porosity, sf_porosity]

        # Rename and standardize the Grain Size dataframe
        dff_gs.rename(columns={dff_gs.columns[0]: "Grain Sizes [mm]", dff_gs.columns[1]: "Fraction Mass [g]"},
                      inplace=True)

        analyzer = StatisticalAnalyzer(sieving_df=dff_gs, metadata=metadata)

        return analyzer
