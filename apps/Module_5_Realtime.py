from app import *

####################################################### support ##########################################################################

### for getting the company codes and storing in reqd format
sc = nse.get_stock_codes()
codes = [
    {"label": str(sc[code]), "value": str(code)}
    for code in sc
]

### getting historical prices of a particular stocks
def get_history_of_some_stock(symbol="SBIN",start_date=date(2020,8,1),end_date=date.today(),print_to_csv=False):
    historical_data_df = nsepy.get_history(symbol=symbol, start=start_date, end=end_date)
    if print_to_csv==True:
        historical_data_df.to_csv("{0}-{1}-{2}".format(symbol,start_date,end_date))
    return historical_data_df


### picking to and from dates
def datepicker_for_historical_data():
    dp=dcc.DatePickerRange(
        id='my-date-picker-range',
        start_date_placeholder_text="Start Period",
        end_date_placeholder_text="End Period",
        min_date_allowed=date(2000,1,1),
        max_date_allowed=date.today(),
        initial_visible_month=date.today(),
        #end_date=date.today(),
        start_date=date(2020,12,1),
        end_date=date(2020,12,30),
        #end_date=dt(2020, 5, 15).date(),
        day_size=39,  # size of calendar image. Default is 39
        updatemode='bothdates'
    )
    return dp


def navbar():
    navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Page 1", href="#")),
        dbc.DropdownMenu(
            children=[
            ],
            nav=True,
            in_navbar=True,
            label="More",
        ),
    ],
    brand="Stock Market Prediction",
    brand_href="#",
    color="primary",
    dark=True,
    )
    return navbar


######################################################## layout ##########################################################################

layout=html.Div(
    [
        html.Div(
            id="banner",
            className="banner",
            children=[
                html.H2("AI Based Predictive Analysis of Stock Market Prediction"),
                
                ],
        ),
        dbc.Row([
            dbc.Col(html.Div([
                dcc.Dropdown(
                    id='company-dropdown',
                    options=codes,value="Company"
                    ),
                datepicker_for_historical_data()
            ]),width=3),
            dbc.Col(html.Div([
                dbc.Card(dbc.Row(
                    dcc.Graph(id='historical-graph')))
            ]),width=9)
        ])
    ]
)


######################################################## callbacks ##################################################################

# @app.callback(
#     dash.dependencies.Output('historical-graph', 'figure'),
#     [dash.dependencies.Input('company-dropdown', 'value'),
#     dash.dependencies.Input('my-date-picker-range', 'start_date'),
#      dash.dependencies.Input('my-date-picker-range', 'end_date')])
# def update_graph_scatter(value,start_date,end_date):
#     print(start_date)
#     print(end_date)
#     print(value)


    # if start_date is not None and end_date is not None:
    #     historical_data_df=get_history_of_some_stock(symbol=value,start_date=start_date,end_date=end_date)
    #     print(start_date)
    #     print(type(start_date))
    #     #print("historical_data_df : ",historical_data_df)
    #     trace = go.Scatter(
    #     x = historical_data_df.index,
    #     y = historical_data_df['Close'],
    #     mode = 'lines',
    #     name = 'Predicted_Price'
    
    #     )
    #     data=[trace]
    #     layout = go.Layout(
    #     title = 'Historical Data',
    #     xaxis = dict(title = 'Date'),
    #     yaxis = dict(title = 'Price'),
    #     height=700,
    #     width=1400
    #     )
    #     fig = go.Figure(data = data, layout = layout)
    #     fig.update_xaxes(
    #     rangebreaks=[dict(bounds=["sat", "mon"])])
    #     #chart=plot(fig, output_type='div')
    #     return fig
    # else:
    #     print(start_date)
    #     print(type(start_date))
    #     historical_data_df=get_history_of_some_stock(symbol=value,start_date=date.today(),end_date=date.today())
    #     #print("historical_data_df : ",historical_data_df)
    #     trace = go.Scatter(
    #     x = historical_data_df.index,
    #     y = historical_data_df['Close'],
    #     mode = 'lines',
    #     name = 'Predicted_Price'
    
    #     )
    #     data=[trace]
    #     layout = go.Layout(
    #     title = 'Historical Data',
    #     xaxis = dict(title = 'Date'),
    #     yaxis = dict(title = 'Price'),
    #     height=700,
    #     width=1400
    #     )
    #     fig = go.Figure(data = data, layout = layout)
    #     fig.update_xaxes(
    #     rangebreaks=[dict(bounds=["sat", "mon"])])
    #     #chart=plot(fig, output_type='div')
    #     return fig
