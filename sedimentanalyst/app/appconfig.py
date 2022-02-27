try:
    import base64
    import io
    import dash
    import plotly.express as px
    import plotly.graph_objects as go
    from dash import dcc, Input, Output, State, html
    from pyproj import transform, CRS
    import pandas as pd
except ImportError:
    print(
        "Error importing necessary packages")

