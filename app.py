import dash
import dash_bootstrap_components as dbc
from dash_bootstrap_components._components.Row import Row
import plotly.express as px
import plotly.graph_objs as go
import dash_core_components as dcc
import dash_html_components as html
import dash_html_components as html
from dash_html_components.Br import Br
from dash.exceptions import PreventUpdate
from plotly.subplots import make_subplots
import plotly.express as px
import plotly.graph_objs as go
import plotly.io as pio
from plotly import tools
import plotly
import plotly.io as pio
import dash_table
import warnings
import pandas as pd
import numpy as np

from dash.dependencies import Input, Output, State
import chart_studio.plotly as py
import plotly as plt
pd.options.plotting.backend = "plotly"
import pathlib
from typing import Container
import requests
from collections import deque
from datetime import date
from datetime import datetime
import datetime
import time

#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

warnings.filterwarnings("ignore")   # Ignore harmless warnings
pd.options.plotting.backend = "plotly"
from pandas.plotting import register_matplotlib_converters
from sklearn.utils.validation import column_or_1d
register_matplotlib_converters()
from dateutil.relativedelta import relativedelta

from nsetools import Nse    # for obtaining stock market data
import nsepy     # for obtaining stock market data
nse = Nse()

# Load specific forecasting tools
from sklearn.model_selection import train_test_split
from pmdarima import auto_arima                              # for determining ARIMA orders
from statsmodels.tools.eval_measures import rmse
import statsmodels.api as sm
from statsmodels.tsa.ar_model import AR,ARResults
from statsmodels.tsa.arima_model import ARMA,ARMAResults,ARIMA,ARIMAResults
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.graphics.tsaplots import plot_acf,plot_pacf # for determining (p,q) orders
from statsmodels.tsa.stattools import acovf,acf,pacf,pacf_yw,pacf_ols
from statsmodels.tsa.seasonal import seasonal_decompose      # for ETS Plots
from statsmodels.tsa.stattools import adfuller
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

### for news ####
# API Requests for news div
news_requests = requests.get(
    "https://newsapi.org/v2/top-headlines?country=in&category=business&apiKey=46b907e7f21d40b4bd4b43e1f83d0a14"
)

# Path
BASE_PATH = pathlib.Path(__file__).parent.resolve()
DATA_PATH = BASE_PATH.joinpath("data").resolve()
# Read data
df = pd.read_csv(DATA_PATH.joinpath("clinical_analytics.csv"))

app = dash.Dash(__name__, suppress_callback_exceptions=True,meta_tags=[{"name": "viewport", "content": "width=device-width"}],external_stylesheets=[dbc.themes.BOOTSTRAP])

server = app.server

# if __name__ == "__main__":
#     app.run_server(debug=True)



