from app import *

############################################### support ##########################################################################

columns=[{'label': 'Prev Close', 'value': 'Prev Close'}, {'label': 'Open', 'value': 'Open'}, {'label': 'High', 'value': 'High'}, {'label': 'Low', 'value': 'Low'}, {'label': 'Last', 'value': 'Last'}, {'label': 'Close', 'value': 'Close'}, {'label': 'VWAP', 'value': 'VWAP'}, {'label': 'Volume', 'value': 'Volume'}, {'label': 'Turnover', 'value': 'Turnover'}, {'label': 'Trades', 'value': 'Trades'}, {'label': 'Deliverable Volume', 'value': 'Deliverable Volume'}, {'label': '%Deliverble', 'value': '%Deliverble'}]

## getting company codes
nse = Nse()
sc = nse.get_stock_codes()
company_options = [
    {"label": str(sc[code]), "value": str(code)}
    for code in sc
]

## processing the data for plotting only 
def process_data_for_plotting(df):
    df.index=pd.to_datetime(df.index)
    df=df.asfreq('b')
    df=df.fillna(method='ffill')
    #df_log = np.log(df['Close'])  # stationarize data
    #train_data, test_data = df_log[3:int(len(df_log)*split_ratio)], df_log[int(len(df_log)*split_ratio):]   # train and test split
    return df

## processing the data for model
def process_data_for_model(df,column,split_ratio=0.8):
    df.index = pd.to_datetime(df.index)
    df = df.asfreq('b')
    df=df.fillna(method='ffill')
    df_log = np.log(df[column])  # stationarize data
    train_data, test_data = df_log[3:int(len(df_log)*split_ratio)], df_log[int(len(df_log)*split_ratio):]   # train and test split
    return df_log,train_data,test_data

## decompose function
def seasonal_decompose_function(df,column="Close",model='mul'):
    result = sm.tsa.seasonal_decompose(df['Close'], model=model)
    observed=result.observed
    trend=result.trend
    seasonal=result.seasonal
    resid=result.resid
    return observed,trend,resid,seasonal

## get stock symbols 
def get_symbols():
    nse = Nse()
    all_stock_codes = nse.get_stock_codes()
    sl=list(all_stock_codes.keys())
    sl=sl[2:]
    return sl

## get historical data of some stock 
def get_history_of_some_stock(symbol="SBIN",start_date=date(2020,8,1),end_date=date.today(),print_to_csv=False):
    historical_data_df = nsepy.get_history(symbol=symbol, start=start_date, end=end_date)
    print(type(historical_data_df))
    if print_to_csv==True:
        historical_data_df.to_csv("{0}-{1}-{2}".format(symbol,start_date,end_date))
    return historical_data_df

#Test for staionarity
def test_stationarity(timeseries):
    # #Determing rolling statistics
    # rolmean = timeseries.rolling(12).mean()
    # rolstd = timeseries.rolling(12).std()
    # #Plot rolling statistics:
    # plt.plot(timeseries, color='blue',label='Original')
    # plt.plot(rolmean, color='red', label='Rolling Mean')
    # plt.plot(rolstd, color='black', label = 'Rolling Std')
    # plt.legend(loc='best')
    # plt.title('Rolling Mean and Standard Deviation')
    # plt.show(block=False)
    # print("Results of dickey fuller test")
    adft = adfuller(timeseries,autolag='AIC')
    # output for dft will give us without defining what the values are.
    #hence we manually write what values does it explains using a for loop
    output = pd.Series(adft[0:4],index=['Test Statistics','p-value','No. of lags used','Number of observations used'])
    for key,values in adft[4].items():
        output['critical value (%s)'%key] =  values
    return(output)

# obtain order
def obtain_order_through_auto_arima(df,column="Close"):
    auto_arima_result = auto_arima(df["{0}".format(column)], start_p=0, start_q=0,
                        test='adf',       # use adftest to find             optimal 'd'
                        max_p=3, max_q=3, # maximum p and q
                        m=1,              # frequency of series
                        d=None,           # let model determine 'd'
                        seasonal=False,   # No Seasonality
                        start_P=0, 
                        D=0, 
                        trace=True,
                        error_action='ignore',  
                        suppress_warnings=True, 
                        stepwise=True).summary()
    table1=auto_arima_result.tables[0]
    order=table1.data[1][1]   # order
    no_of_values=table1.data[0][3]   # no. of observation
    p=int(order[8:9])
    d=int(order[11:12])
    q=int(order[14:15])
    #print(auto_arima_result.summary())
    return p,d,q,no_of_values,auto_arima_result


## models
def AR_function(df,column="Close",split_ratio=0.8):     # AutoRegressive model
    train_data,test_data=process_data_for_model(df,split_ratio)   # apply datetime index , set freq as b, fill null values, and train test split
    p,d,q,no_of_values=obtain_order_through_auto_arima(df,column="Close")   # extract order from auto_arima_result
    model = ARIMA(train_data["{0}".format(column)], order=(p, d, q), seasonal_order=(0, 1, 0, 4), enforce_stationarity=True, enforce_invertibility=False)   # training the model
    fitted_model=model.fit()    # Fitting the model
    fc, se, conf = fitted_model.forecast(len(test_data), alpha=0.05)  # Forecast , 95% confidence


def MA_function(df,column="Close",split_ratio=0.8):     # Moving Average model
    train_data,test_data=process_data_for_model(df,split_ratio)   # apply datetime index , set freq as b, fill null values, and train test split
    p,d,q,no_of_values=obtain_order_through_auto_arima(df,column="Close")   # extract order from auto_arima_result
    model = ARIMA(train_data["{0}".format(column)], order=(p, d, q), seasonal_order=(0, 1, 0, 4), enforce_stationarity=True, enforce_invertibility=False)   # training the model
    fitted_model=model.fit()    # Fitting the model
    fc, se, conf = fitted_model.forecast(len(test_data), alpha=0.05)  # Forecast , 95% confidence


def ARMA_function(df,column="Close",split_ratio=0.8):   # AutoRegressive Moving Average model
    train_data,test_data=process_data_for_model(df,split_ratio)   # apply datetime index , set freq as b, fill null values, and train test split
    p,d,q,no_of_values=obtain_order_through_auto_arima(df,column="Close")   # extract order from auto_arima_result
    model = ARIMA(train_data["{0}".format(column)], order=(p, d, q), seasonal_order=(0, 1, 0, 4), enforce_stationarity=True, enforce_invertibility=False)   # training the model
    fitted_model=model.fit()    # Fitting the model
    fc, se, conf = fitted_model.forecast(len(test_data), alpha=0.05)  # Forecast , 95% confidence


def ARIMA_function(df,column="Close",split_ratio=0.8):  # AutoRegressive Integrated Moving Average model
    train_data,test_data=process_data_for_model(df,split_ratio)   # apply datetime index , set freq as b, fill null values, and train test split
    p,d,q,no_of_values=obtain_order_through_auto_arima(df,column="Close")   # extract order from auto_arima_result
    model = ARIMA(train_data["{0}".format(column)], order=(p, d, q), seasonal_order=(0, 1, 0, 4), enforce_stationarity=True, enforce_invertibility=False)   # training the model
    fitted_model=model.fit()    # Fitting the model
    fc, se, conf = fitted_model.forecast(len(test_data), alpha=0.05)  # Forecast , 95% confidence


def ARIMAX_function(df,column="Close",split_ratio=0.8):     # AutoRegressive Integrated Moving Average model with Exogeneous factors
    train_data,test_data=process_data_for_model(df,split_ratio)   # apply datetime index , set freq as b, fill null values, and train test split
    p,d,q,no_of_values=obtain_order_through_auto_arima(df,column="Close")   # extract order from auto_arima_result
    model = sm.tsa.statespace.SARIMAX(train_data["{0}".format(column)], order=(p, d, q), seasonal_order=(0, 1, 0, 4), enforce_stationarity=True, enforce_invertibility=False)   # training the model
    fitted_model=model.fit()    # Fitting the model
    fc, se, conf = fitted_model.forecast(len(test_data), alpha=0.05)  # Forecast , 95% confidence


def SARIMA_function(df,column="Close",split_ratio=0.8):     # Seasonal AutoRegressive Integrated Moving Average model
    train_data,test_data=process_data_for_model(df,split_ratio)   # apply datetime index , set freq as b, fill null values, and train test split
    p,d,q,no_of_values,auto_arima_result=obtain_order_through_auto_arima(df,column="Close")   # extract order from auto_arima_result
    model = sm.tsa.statespace.SARIMAX(train_data, order=(p, d, q), seasonal_order=(0, 1, 0, 4), enforce_stationarity=True, enforce_invertibility=False)   # training the model
    fitted_model=model.fit()    # Fitting the model
    #a=fitted_model.forecast(len(test_data), alpha=0.05)  # Forecast , 95% confidence
    fc,se,conf=fitted_model.forecast(len(test_data), alpha=0.05)  # Forecast , 95% confidence
    return train_data,test_data,fc,se,conf


def SARIMAX_function(df,column="Close",split_ratio=0.8):    # Seasonal AutoRegressive Integrated Moving Average model with Exogeneous factors
    train_data,test_data=process_data_for_model(df,split_ratio)   # apply datetime index , set freq as b, fill null values, and train test split
    p,d,q,no_of_values=obtain_order_through_auto_arima(df,column="Close")   # extract order from auto_arima_result
    model = sm.tsa.statespace.SARIMAX(train_data["{0}".format(column)], order=(p, d, q), seasonal_order=(0, 1, 0, 4), enforce_stationarity=True, enforce_invertibility=False)   # training the model
    fitted_model=model.fit()    # Fitting the model
    fc, se, conf = fitted_model.forecast(len(test_data), alpha=0.05)  # Forecast , 95% confidence

## for calculating accuracy
# def calculate_accuracy(test_data,prediction):

def test_ARIMA_function(df,column="Close",split_ratio=0.8):  # AutoRegressive Integrated Moving Average model
    train_data,test_data=process_data_for_model(df,split_ratio)   # apply datetime index , set freq as b, fill null values, and train test split
    #p,d,q,no_of_values=obtain_order_through_auto_arima(df,column="Close")   # extract order from auto_arima_result
    model = ARIMA(train_data, order=(0, 0, 0))   # training the model
    fitted_model=model.fit(disp=-1)    # Fitting the model
    fc, se, conf = fitted_model.forecast(len(test_data), alpha=0.05)  # Forecast , 95% confidence
    return fc, se, conf


############## realtime forecasting
def random_data_generator():
    return 0

## reatime functions
def realtime_by_nsepy(symbol="SBIN"):
    quote_dictionary=nsepy.get_quote(symbol="{0}".format(symbol))
    data_list=quote_dictionary["data"]
    data_dictionary=data_list[0]
    last_value=data_dictionary["lastPrice"]
    print(last_value)

def realtime_by_nsetools(symbol='SBIN'):
    nse = Nse()
    a = 1
    while a==1: #infinite loop  
        quote_dictionary = nse.get_quote("{0}".format(symbol))
        #print(quote_dictionary)
        last_value=quote_dictionary["lastPrice"]
        print(last_value)   #only printing for now
        time.sleep(1)

#######################

#app = dash.Dash(__name__)

### variables
df=pd.DataFrame()
data1,data2,data3,data4,data5,data6,data7,data8=[[[]],[[]],[[]],[[]],[[]],[[]],[[]],[[]]]
columns1,columns2,columns3,columns4,columns5,columns6,columns7,columns8=[[[]],[[]],[[]],[[]],[[]],[[]],[[]],[[]]]  #[[[]],[[]],[[]],[[]],[[]],[[]],[[]],[[]]]
fig1=go.Figure()
fig2=go.Figure()
fig3=go.Figure()
fig4=go.Figure()
fig5=go.Figure()
fig6=go.Figure()

######################################################## layout ########################################################################

layout = html.Div(
    id="app-container",
    children=[
        # Banner
        html.Div(
            id="banner",
            className="banner",
            children=[html.H2("AI Based Predictive Analysis of Stock Market Prediction")],
        ),
        # Left column
        html.Div(
            id="left-column",
            className="three columns",
            children=[
                html.Div(
                    [
                        html.B("Select Company"),
                        dcc.Dropdown(id='company-dropdown',options=company_options,value="Company",placeholder="Select a Company...",),
                        html.Br(),
                        
                        html.Div(children=[
                            html.Center([html.B("Select Start Date and End Date"),
                            dcc.DatePickerRange(
                                id='my-date-picker-range',
                                start_date_placeholder_text="Start Period",
                                end_date_placeholder_text="End Period",
                                min_date_allowed=date(2000,1,1),
                                max_date_allowed=date.today(),
                                initial_visible_month=date.today(),
                                #end_date=date.today(),
                                #start_date=date(2020,12,1),
                                #end_date=date.today(),
                                #end_date=dt(2020, 5, 15).date(),
                                day_size=39,  # size of calendar image. Default is 39
                                updatemode='bothdates'
                            )]),
                        ],style={'width': '100%'}),


                        html.Br(),
                        html.Button(id="fetch_data_button", children="Fetch Data", n_clicks=0,style={"width":"100%"},),
                        html.Br(),
                        html.Br(),
                        html.Button(id="historical_data_plot_button", children="Plot", n_clicks=0,style={"width":"100%"},),
                        html.Br(),

                        html.B("Select Column"),
                        dcc.Dropdown(id='column-dropdown',options=columns,placeholder="Column",),
                        html.Br(),
                        html.Br(),
                        html.Button(id="stationarity_check_button", children="stationarity check", n_clicks=0,style={"width":"100%"},),
                        html.Br(),
                        html.Br(),
                        html.Hr(),
                        html.Br(),
                        html.B("Seasonal Decomposition"),
                        html.Br(),
                        dcc.Dropdown(id='decompose_dropdown',options=[{'label': 'additive', 'value': 'additive'}, {'label': 'multiplicative', 'value': 'multiplicative'}],placeholder="Model type",),
                        html.Br(),
                        html.Button(id="decompose_button", children="Seasonal Decompose", n_clicks=0,style={"margin-left": "40px","width":"80%"},),
                        html.Br(),
                        html.Br(),
                        html.Hr(),
                        html.Br(),
                        html.B("Select Train Test Split Ratio"),
                        dcc.Slider(
                            id="split_slider",
                            min=0,
                            max=100,
                            marks={ i:'{}'.format(i) for i in range(0,101,10)},
                            step=5,
                            value=80,
                        ),
                        html.Br(),
                        html.Br(),
                        html.Button(id="auto_arima_button", children="Auto Arima", n_clicks=0,style={"width":"100%"},),
                        html.Br(),
                        html.Br(),
                        html.Hr(),
                        html.Br(),
                        html.Button(id="predict_button", children="Get Predictions", n_clicks=0,style={"margin-left": "40px","width":"80%"},),
                        html.Br(),
                        html.Hr(),
                        html.Br(),
                        html.Button(id="forecast_button", children="Forecast", n_clicks=0,style={"margin-left": "40px","width":"80%"},),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                    ],
                    style={"width": "90%"},
                ),
            ],
        ),
        # Right column
        html.Br(),
        html.Div(
            id="right-column",
            className="nine columns",
            children=[
                dcc.Tabs(
                    id="tabs-with-classes",
                    value='tab-1',
                    parent_className='custom-tabs',
                    className='custom-tabs-container',
                    children=[
                        dcc.Tab(
                            label='Raw Data',
                            value='tab-1',
                            className='custom-tab',
                            selected_className='custom-tab--selected',
                            children=[
                                    dash_table.DataTable(
                                    id='historical_data_table',
                                    # columns=[
                                    #     {'name': 'Property', 'id': 'column1'},
                                    #     {'name': 'Value', 'id': 'column2'},
                                    # ],
                                    data=[],
                                )      
                            ]
                        ),
                        dcc.Tab(
                            label='Historical Data Plot',
                            value='tab-2',
                            className='custom-tab',
                            selected_className='custom-tab--selected',
                            children=[
                            html.Div(
                                id="historical_data_graph_card",
                                children=[
                                    html.B("Historical Data"),
                                    html.Hr(),
                                    dcc.Graph(id='historical-graph'),
                                    ]
                            ),
                            ]
                        ),
                        dcc.Tab(
                            label='Stationarity check',
                            value='tab-3',
                            className='custom-tab',
                            selected_className='custom-tab--selected',
                            children=[
                            html.Div(
                                id="stationarity_card",
                                children=[
                                    html.B("Stationarity Check"),
                                    html.Hr(),
                                    dash_table.DataTable(
                                    id='stationarity_check_table',
                                    columns=[
                                        {'name': '', 'id': 'column1'},
                                        {'name': 'Value', 'id': 'column2'},
                                    ],
                                    data=[],
                                )                             
                                ]

                            ),
                            ]
                        ),
                        dcc.Tab(
                            label='Seasonal Decomposition',
                            value='tab-4',
                            className='custom-tab',
                            selected_className='custom-tab--selected',
                            children=[
                            html.Div(
                                id="decompose_card",
                                children=[
                                    html.B("Seasonal Decompose"),
                                    html.Hr(),
                                    dcc.Graph(id='decompose_graph'),]
                                )
                            ]
                            ),
                        dcc.Tab(
                            label='Auto ARIMA Results',
                            value='tab-5',
                            className='custom-tab',
                            selected_className='custom-tab--selected',
                            children=[
                                html.Div(
                                id="auto_arima_card_main",
                                children=[
                                    html.B("Auto ARIMA Results"),
                                    html.Hr(),
                                    html.Div(
                                    id="auto_arima_card1",
                                    children=[
                                        dash_table.DataTable(
                                        id='auto_arima_table1',
                                        columns=[],
                                        data=[],
                                        ),
                                        ]
                                    ),
                                    html.Br(),
                                    html.Br(),
                                    html.Div(
                                    id="auto_arima_card2",
                                    children=[
                                        dash_table.DataTable(
                                        id='auto_arima_table2',
                                        columns=[],
                                        data=[],
                                        ),
                                        ]
                                    ),
                                    html.Br(),
                                    html.Br(),
                                    html.Div(
                                    id="auto_arima_card3",
                                    children=[
                                        dash_table.DataTable(
                                        id='auto_arima_table3',
                                        columns=[],
                                        data=[],
                                        ),  
                                        ]
                                    ),
                                    html.Br(),
                                    html.Br(),
                                    ]
                                ),

                            ]
                        ),
                        dcc.Tab(
                            label='Predictions and Accuracy',
                            value='tab-6',
                            className='custom-tab',
                            selected_className='custom-tab--selected',
                            children=[
                                html.Div(
                                    id="prediction_card",
                                    children=[
                                        html.B("Getting Predictions"),
                                        html.Hr(),
                                        dcc.Graph(id='prediction_graph'),]
                                    )
                            ]
                        ),
                        dcc.Tab(
                            label='Forecasting',
                            value='tab-7',
                            className='custom-tab',
                            selected_className='custom-tab--selected',
                            children=[
                                html.Div(
                                    id="forecast_card",
                                    children=[
                                        html.B("Forecasting Values"),
                                        html.Hr(),
                                        dcc.Graph(id='forecast_graph'),
                                        ]
                                    )
                            ]
                        ),
                ]),            
            ],
        ),
    ],
)


#################################################### callbacks ######################################################################
@app.callback(
    [
    dash.dependencies.Output('historical_data_table','data'),
    dash.dependencies.Output('historical_data_table','columns'),
    dash.dependencies.Output('historical-graph', 'figure'),
    dash.dependencies.Output('stationarity_check_table','data'),
    dash.dependencies.Output('stationarity_check_table','columns'),
    dash.dependencies.Output('decompose_graph','figure'),
    dash.dependencies.Output('auto_arima_table1','data'),
    dash.dependencies.Output('auto_arima_table1','columns'),
    dash.dependencies.Output('auto_arima_table2','data'),
    dash.dependencies.Output('auto_arima_table2','columns'),
    dash.dependencies.Output('auto_arima_table3','data'),
    dash.dependencies.Output('auto_arima_table3','columns'),
    dash.dependencies.Output('prediction_graph','figure'),
    dash.dependencies.Output('forecast_graph','figure'),
    dash.dependencies.Output('tabs-with-classes','value'),
    ],
    [
    dash.dependencies.Input('fetch_data_button', 'n_clicks'),
    dash.dependencies.Input('historical_data_plot_button', 'n_clicks'),
    dash.dependencies.Input('stationarity_check_button', 'n_clicks'),
    dash.dependencies.Input('decompose_button', 'n_clicks'),
    dash.dependencies.Input('auto_arima_button', 'n_clicks'),
    dash.dependencies.Input('predict_button', 'n_clicks'),
    dash.dependencies.Input('forecast_button', 'n_clicks'),
    ],
    state=[
    dash.dependencies.State('company-dropdown', 'value'),
    dash.dependencies.State('column-dropdown', 'value'),
    dash.dependencies.State('my-date-picker-range', 'start_date'),
    dash.dependencies.State('my-date-picker-range', 'end_date'),
    dash.dependencies.State('decompose_dropdown', 'value'),
    dash.dependencies.State('split_slider', 'value'),
    ])
def update(n_clicks_1,n_clicks_2,n_clicks_3,n_clicks_4,n_clicks_5,n_clicks_6,n_clicks_7,sym,column,startdate,enddate,model,ratio):
    global data1,data2,data3,data4,data5,data6,data7,data8,columns1,columns2,columns3,columns4,columns5,columns6,columns7,columns8,fig1,fig2,fig3,fig4,fig5,fig6
    ctx=dash.callback_context
    if not ctx.triggered:
        raise PreventUpdate
    elif ctx.triggered[0]['prop_id']=="fetch_data_button.n_clicks":
        fig1.data,fig2.data,fig3.data,fig4.data=[[],[],[],[]]
        data1,data2,data3,data4,data5,data6,data7,data8=[[[]],[[]],[[]],[[]],[[]],[[]],[[]],[[]]]
        columns1,columns2,columns3,columns4,columns5,columns6,columns7,columns8=[[[]],[[]],[[]],[[]],[[]],[[]],[[]],[[]]]
        start_time_obj = datetime.datetime.strptime(startdate, '%Y-%m-%d')
        end_time_obj = datetime.datetime.strptime(enddate, '%Y-%m-%d')
        df=nsepy.get_history(symbol=sym, start=start_time_obj, end=end_time_obj)
        df=process_data_for_plotting(df)
        df_raw=df
        df_raw.reset_index(inplace=True)
        df_raw['Date'] = pd.to_datetime(df_raw['Date']).dt.normalize()
        columns1=[{"name": i, "id": i} for i in df_raw.columns],
        data1=df_raw.to_dict('records'),
        return data1[0],columns1[0],fig1,data2[0],columns2[0],fig2,data3[0],columns3[0],data4[0],columns4[0],data5[0],columns5[0],fig3,fig4,"tab-1"
    elif ctx.triggered[0]['prop_id']=="historical_data_plot_button.n_clicks":
        start_time_obj = datetime.datetime.strptime(startdate, '%Y-%m-%d')
        end_time_obj = datetime.datetime.strptime(enddate, '%Y-%m-%d')
        df=nsepy.get_history(symbol=sym, start=start_time_obj, end=end_time_obj)
        df=process_data_for_plotting(df)
        trace = go.Scatter(x = df.index,y = df['Close'],mode = 'markers+lines',name = 'Predicted_Price')
        data=[trace]
        layout = go.Layout(
        #title = 'Historical Data',
        xaxis = dict(title = 'Date'),
        yaxis = dict(title = 'Price'),
        height=650,
        width=1300,
        )
        fig1 = go.Figure(data = data, layout = layout)
        return data1[0],columns1[0],fig1,data2[0],columns2[0],fig2,data3[0],columns3[0],data4[0],columns4[0],data5[0],columns5[0],fig3,fig4,"tab-2"
    elif ctx.triggered[0]['prop_id']=="stationarity_check_button.n_clicks":
        start_time_obj = datetime.datetime.strptime(startdate, '%Y-%m-%d')
        end_time_obj = datetime.datetime.strptime(enddate, '%Y-%m-%d')
        df=nsepy.get_history(symbol=sym, start=start_time_obj, end=end_time_obj)
        df=process_data_for_plotting(df)
        output=test_stationarity(df['Close'])
        output=pd.DataFrame(output)
        output.reset_index(inplace=True)
        output = output.rename(columns = {0:'Values'})
        print(output)
        columns2=[{"name": i, "id": i} for i in output.columns],
        data2=output.to_dict('records'),
        return data1[0],columns1[0],fig1,data2[0],columns2[0],fig2,data3[0],columns3[0],data4[0],columns4[0],data5[0],columns5[0],fig3,fig4,"tab-3"
    elif ctx.triggered[0]['prop_id']=="decompose_button.n_clicks":
        start_time_obj = datetime.datetime.strptime(startdate, '%Y-%m-%d')
        end_time_obj = datetime.datetime.strptime(enddate, '%Y-%m-%d')
        df=nsepy.get_history(symbol=sym, start=start_time_obj, end=end_time_obj)
        df_processed=process_data_for_plotting(df)
        observed,trend,resid,seasonal=seasonal_decompose_function(df_processed,model=model)
        fig2 = make_subplots(rows=2, cols=2)
        fig2.add_trace(go.Scatter(y=observed, mode="lines"), row=1, col=1)
        fig2.add_trace(go.Scatter(y=trend, mode="lines"), row=1, col=2)
        fig2.add_trace(go.Scatter(y=resid, mode="lines"), row=2, col=1)
        fig2.add_trace(go.Scatter(y=seasonal, mode="lines"), row=2, col=2)
        fig2.update_layout(height=650,width=1300)
        return data1[0],columns1[0],fig1,data2[0],columns2[0],fig2,data3[0],columns3[0],data4[0],columns4[0],data5[0],columns5[0],fig3,fig4,"tab-4"
    elif ctx.triggered[0]['prop_id']=="auto_arima_button.n_clicks":
        start_time_obj = datetime.datetime.strptime(startdate, '%Y-%m-%d')
        end_time_obj = datetime.datetime.strptime(enddate, '%Y-%m-%d')
        df=nsepy.get_history(symbol=sym, start=start_time_obj, end=end_time_obj)
        df=process_data_for_plotting(df)
        p,d,q,no_of_values,auto_arima_result=obtain_order_through_auto_arima(df)
        results_as_html1= auto_arima_result.tables[0].as_html()
        results_as_html2= auto_arima_result.tables[1].as_html()
        results_as_html3= auto_arima_result.tables[2].as_html()
        t1=pd.read_html(results_as_html1,header=0, index_col=0)[0]
        t2=pd.read_html(results_as_html2,header=0, index_col=0)[0]
        t3=pd.read_html(results_as_html3,header=0, index_col=0)[0]
        t1.reset_index(inplace=True)    # table 1
        t1 = t1.rename(columns = {0:'Values'})
        columns3=[{"name": i, "id": i} for i in t1.columns],
        data3=t1.to_dict('records'),
        t2.reset_index(inplace=True)    # table 1
        t2 = t2.rename(columns = {0:'Values'})
        columns4=[{"name": i, "id": i} for i in t2.columns],
        data4=t2.to_dict('records'),
        t3.reset_index(inplace=True)    # table 1
        t3 = t3.rename(columns = {0:'Values'})
        columns5=[{"name": i, "id": i} for i in t3.columns],
        data5=t3.to_dict('records'),
        return data1[0],columns1[0],fig1,data2[0],columns2[0],fig2,data3[0],columns3[0],data4[0],columns4[0],data5[0],columns5[0],fig3,fig4,"tab-5"
    elif ctx.triggered[0]['prop_id']=="predict_button.n_clicks":
        start_time_obj = datetime.datetime.strptime(startdate, '%Y-%m-%d')
        end_time_obj = datetime.datetime.strptime(enddate, '%Y-%m-%d')
        df=nsepy.get_history(symbol=sym, start=start_time_obj, end=end_time_obj)
        df_log,train_data,test_data=process_data_for_model(df,column)   # apply datetime index , set freq as b, fill null values, and train test split
        p,d,q,no_of_values,auto_arima_result=obtain_order_through_auto_arima(df,column="Close")   # extract order from auto_arima_result
        model = sm.tsa.statespace.SARIMAX(train_data, order=(p, d, q), seasonal_order=(0, 1, 0, 4), enforce_stationarity=True, enforce_invertibility=False)   # training the model
        fitted_model=model.fit()    # Fitting the model
        predictions=fitted_model.predict(start=len(train_data),end=len(df_log))
        fig3.add_trace(go.Scatter(name="Train Data",mode="markers+lines",x=train_data.index, y=train_data,))
        fig3.add_trace(go.Scatter(name="Test",mode="markers+lines", x=test_data.index, y=test_data,))
        fig3.add_trace(go.Scatter(name="Predicted",mode="markers+lines", x=predictions.index,y=predictions,))
        fig3.update_layout(height=650,width=1300)
        return data1[0],columns1[0],fig1,data2[0],columns2[0],fig2,data3[0],columns3[0],data4[0],columns4[0],data5[0],columns5[0],fig3,fig4,"tab-6"
    elif ctx.triggered[0]['prop_id']=="forecast_button.n_clicks":
        start_time_obj = datetime.datetime.strptime(startdate, '%Y-%m-%d')
        end_time_obj = datetime.datetime.strptime(enddate, '%Y-%m-%d')
        df=nsepy.get_history(symbol=sym, start=start_time_obj, end=end_time_obj)
        df_log,train_data,test_data=process_data_for_model(df,column)
        p,d,q,no_of_values,auto_arima_result=obtain_order_through_auto_arima(df,column="Close")   # extract order from auto_arima_result
        #model=sm.tsa.statespace.SARIMAX(train_data, order=(p, d, q), seasonal_order=(0, 1, 0, 4), enforce_stationarity=True, enforce_invertibility=False)   # training the model
        model=ARIMA(df_log, order=(p, d, q))
        fitted_model=model.fit()    # Fitting the model
        fc, se, conf = fitted_model.forecast(steps=len(test_data), alpha=0.6)
        fc_series = pd.Series(fc, index=test_data.index)
        lower_series = pd.Series(conf[:, 0], index=test_data.index)
        upper_series = pd.Series(conf[:, 1], index=test_data.index)
        index_for_forecast=test_data.index
        index_for_forecast=index_for_forecast.shift(periods=len(test_data))
        fig4.add_trace(go.Scatter(name="Actual Data",mode="markers+lines", x=df_log.index, y=df_log,))
        fig4.add_trace(go.Scatter(name="Predicted",mode="markers+lines",x=index_for_forecast,y=fc_series))
        fig4.add_trace(go.Line(name="Lower Series",x=index_for_forecast,y=lower_series,fillcolor='rgba(26,150,65,0.5)',fill='tonexty',))
        fig4.add_trace(go.Line(name="Upper Series",x=index_for_forecast,y=upper_series,fillcolor='rgba(26,150,65,0.5)',fill='tonexty',))
        fig4.update_layout(height=650,width=1300)
        return data1[0],columns1[0],fig1,data2[0],columns2[0],fig2,data3[0],columns3[0],data4[0],columns4[0],data5[0],columns5[0],fig3,fig4,"tab-7"


# ###### start the server
# if __name__ == '__main__':
#     app.run_server(debug=True)
