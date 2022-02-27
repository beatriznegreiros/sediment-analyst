""" Stand-alone designated for the web application

Author : Beatriz Negreiros

"""

from sedimentanalyst.app import interac_plotter
from sedimentanalyst.analyzer.utils import *
from sedimentanalyst.app.accessories import *
from sedimentanalyst.app.appconfig import *

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Instantiates object app of the class Dash
app = dash.Dash(__name__, external_stylesheets=external_stylesheets,
                suppress_callback_exceptions=True, title='Sediment Analyst')
# server = app.server  # method to serve the app, allows heroku to recognize the server

# Instantiates to get accessories of the app from the class Accessories (accessories.py)
acc = Accessories()


# App layout
app.layout = html.Div(
    children=[  # this code section taken from Dash docs https://dash.plotly.com/dash-core-components/upload
        html.H1("Sediment Analyst", style={'text-align': 'center'}),  # header
        html.Img(src='https://raw.githubusercontent.com/federicascolari8/PythonProject_Other/main/sedimentanalyst/app'
                     '/assets/Ering_Germany.jpg',
                 style=acc.img_style),  # Image
        acc.intro_text,
        html.Br(),
        acc.inputs_text,
        html.Br(),

        # Manual inputs set as default according to the excel template, but can be changed in the interface
        # Provides necessary State objects, which are parameters for Callback 1
        html.Div(acc.input_boxes),
        html.Br(),

        # Component for collecting State objects for future calling Callback 1
        # Component for uploading files
        dcc.Upload(  # drop and drag upload area for inputting files
            id='upload-data',

            # returns elements for future firing and Callback 2
            children=html.Div([
                'Drag and Drop or ',
                html.A('Select Files')
            ]),
            style=acc.style_upload,
            multiple=True  # Allow multiple files to be uploaded
        ),
        html.Br(),

        # store input indexes (row column containing sample information)
        dcc.Store(id='store_manual_inputs'),

        # [fires up Callback 3...]
        html.Button('Run analysis', id='btn_run'),
        html.Br(),

        # store global dataframe
        dcc.Store(id='stored-data'),
        html.Br(),

        # html.Div(id='output-div'),
        html.Div(id='download-buttom'),
        html.Br(),

        # drop box with sample names
        html.Div(id='dropdown-sample_id'),
        html.Br(),

        # map
        html.Div(id='div-map'),
        html.Br(),

        # grain size distribution
        html.Div(id='div-gsd'),
        html.Br(),

        # diameters barchart
        html.Div(id='div-diameters'),
        html.Br(),

        # dropdown with type of statistics
        html.Div(id='div-stat-drop'),

        # barchart
        html.Div(id='div-barchart'),
    ])


# Callback 1: for storing input dictionary necessary to read the user-inputed files
@app.callback(
    Output('store_manual_inputs', 'data'),
    Input('header', 'value'),
    Input('gs_clm', 'value'),
    Input('cw_clm', 'value'),
    Input('n_rows', 'value'),
    Input('porosity', 'value'),
    Input('SF_porosity', 'value'),
    Input('index_lat', 'value'),
    Input('index_long', 'value'),
    Input('index_sample_name', 'value'),
    Input('index_sample_date', 'value'),
    Input('projection', 'value'),
    Input('btn_run', 'n_clicks'),
    # prevent_initial_call=True,
)
def save_inputs(header, gs_clm, cw_clm, n_rows, porosity,
                sf_porosity, index_lat, index_lon,
                sample_name_index, sample_date_index,
                projection, n_clicks):
    # transform float values into list
    porosity_index = list(map(int, str(porosity).split("."))) if porosity is not None else None
    sf_porosity_index = list(map(int, str(sf_porosity).split("."))) if sf_porosity is not None else None
    lat_index = list(map(int, str(index_lat).split("."))) if index_lat is not None else None
    lon_index = list(map(int, str(index_lon).split("."))) if index_lon is not None else None
    name_index = list(map(int, str(sample_name_index).split("."))) if sample_name_index is not None else None
    date_index = list(map(int, str(sample_date_index).split("."))) if sample_date_index is not None else None

    # create dictionary with all inputs
    input_dic = dict(header=header, gs_clm=gs_clm, cw_clm=cw_clm, n_rows=n_rows, porosity=porosity_index,
                     SF_porosity=sf_porosity_index, index_lat=lat_index, index_long=lon_index,
                     index_sample_name=name_index, index_sample_date=date_index, projection=projection)
    return input_dic


# Callback 2: for parsing inputs, computing and storing summary statistics of the files and returning button component
# "Download Summary Statistics", which fires up Callback 3
@app.callback(Output('download-buttom', 'children'),
              Output('stored-data', 'data'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'),
              State('store_manual_inputs', 'data'),
              Input('btn_run', 'n_clicks'),
              prevent_initial_call=True,
              )
def parse_and_analyse(list_of_contents, list_of_names, list_of_dates, input_dict_in_layout, click):
    if list_of_contents is not None:
        df_global = pd.DataFrame()
        children = []
        list_analyzers = []

        # iterating through files and appending reading messages as well as
        # analysis objects (analyzers)
        for c, n, d in zip(list_of_contents, list_of_names, list_of_dates):
            from_parsing = acc.parse_contents(c, n, d, input_dict_in_layout)
            list_analyzers.append(from_parsing)

        # append all information from the list of analyzers into a global df
        for inter_analyzer in list_analyzers:
            df_global = append_global(obj=inter_analyzer,
                                      df=df_global)

        # return summary statistics
        data2 = df_global.to_dict('split')
        children.append(html.Div([
            html.Button('Download Summary Statistics', id='btn_download'),
            dcc.Download(id='download-dataframe-csv'),
        ])
        )
        children.append(data2)

        return children


# Callback 3: for enabling the download of summary statistics of all input samples, it is fired up by 'btn_download'
@app.callback(
    Output('download-dataframe-csv', 'data'),
    State('stored-data', 'data'),
    Input('btn_download', 'n_clicks'),
    prevent_initial_call=True,
)
def download_summary_stats(data, n_clicks):
    dataframe_global = pd.DataFrame(data=data['data'], columns=data['columns'])
    return dcc.send_data_frame(dataframe_global.to_csv, 'overall_statistics.csv')


# Callback 4: for outputing dropdown of sample for selection, returns
@app.callback(Output('dropdown-sample_id', 'children'),
              Input('btn_run', 'n_clicks'),
              State('stored-data', 'data'),
              prevent_initial_call=True  # prevents that this callback is ran
              # before the inputs (outputs of previous callbacks) are available
              )
def update_sample_id(n_clicks, data):  # n_clicks is mandatory even if not used
    df = pd.DataFrame(data=data['data'], columns=data['columns'])
    samples = df['sample name'].tolist()

    return html.Div([dcc.Markdown('''##### Filter by sample: '''),
                     dcc.Dropdown(id='sample_id',
                                  options=[{'label': x, 'value': x}
                                           for x in samples],
                                  value=samples,
                                  multi=True
                                  )
                     ])


# Callback 5: for creating a mapbox with sample locations and computed sed. statistics, it is fired up by 'sample_id'
@app.callback(
    Output('div-map', 'children'),
    State('stored-data', 'data'),
    State('store_manual_inputs', 'data'),
    Input('sample_id', 'value'),
    prevent_initial_call=True
)

def update_map(data, dict_to_get_proj, samples):
    df = pd.DataFrame(data=data['data'], columns=data['columns'])
    int_plot = interac_plotter.InteractivePlotter(df)
    fig = int_plot.create_map(df=df, samples=samples, projection=dict_to_get_proj['projection'])
    fig.update_layout(transition_duration=500)
    return dcc.Graph(id='map', figure=fig)


# Callback 6: for dropdown for the user to select the desired statistic
@app.callback(Output('div-stat-drop', 'children'),
              Input('btn_run', 'n_clicks'),
              State('stored-data', 'data'),
              prevent_initial_call=True,
              )
def update_stat_drop(n_clicks, data):
    df = pd.DataFrame(data=data['data'], columns=data['columns'])
    statistics = df.columns[4:23].tolist()

    return html.Div([dcc.Markdown('''##### Filter by statistic: '''),
                     dcc.Dropdown(id='statistics_id',
                                  options=[{'label': x, 'value': x}
                                           for x in statistics],
                                  value=statistics[0],
                                  multi=False,
                                  style=acc.style_statistic
                                  )
                     ])


# Callback 7: for plotting/updating histogram of the statistic; uses the class InteractivePlotter
@app.callback(
    Output('div-barchart', 'children'),
    State('stored-data', 'data'),
    Input('statistics_id', 'value'),
    Input('sample_id', 'value'),
    prevent_initial_call=True
)
def update_barchart(data, stat_value, samples):
    # save into dataframe
    df = pd.DataFrame(data=data['data'], columns=data['columns'])

    # filter samples given sample name
    df = df[df['sample name'].isin(samples)]

    # filter samples given statistic
    df = df.iloc[:, 4:23]
    i_plotter = interac_plotter.InteractivePlotter(df)
    fig = i_plotter.plot_barchart(param=stat_value, samples=samples)
    # fig.update_layout(transition_duration=500)
    return dcc.Graph(id='output-barchart',
                     figure=fig,
                     style=acc.style_graph
                     )

# Callback 8: for plotting/updating grain size distribution graph
@app.callback(
    Output('div-gsd', 'children'),
    State('stored-data', 'data'),
    Input('sample_id', 'value'),
    prevent_initial_call=True
)
def update_gsd(data, samples):
    # save into dataframe
    df = pd.DataFrame(data=data['data'], columns=data['columns'])

    # filter samples given sample name
    df = df[df['sample name'].isin(samples)]

    i_plotter_2 = interac_plotter.InteractivePlotter(df)
    fig = i_plotter_2.plot_gsd(samples)

    return dcc.Graph(id='gsd',
                     figure=fig,
                     style=acc.style_graph
                     )

# Callback 9: for plotting the diameters
@app.callback(
    Output('div-diameters', 'children'),
    State('stored-data', 'data'),
    Input('sample_id', 'value'),
    prevent_initial_call=True
)

def update_diameters(data, samples):
    # save into dataframe
    df = pd.DataFrame(data=data['data'], columns=data['columns'])

    # filter samples given sample name
    df = df[df['sample name'].isin(samples)]

    i_plotter_2 = interac_plotter.InteractivePlotter(df)
    fig = i_plotter_2.plot_diameters(samples)

    return dcc.Graph(id='diameters',
                     figure=fig,
                     style=acc.style_graph
                     )


if __name__ == '__main__':
    app.run_server(debug=False)
