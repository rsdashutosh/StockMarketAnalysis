from app import *



####################################################### support ###################################################################

# API Call to update news
def update_news():
    json_data = news_requests.json()["articles"]
    df = pd.DataFrame(json_data)
    df = pd.DataFrame(df[["title", "url"]])
    max_rows = 15
    return html.Div(
        children=[
            dbc.Row([
                dbc.Col(html.P(className="p-news", children="Headlines"),width=9),
               dbc.Col(html.P(
                    id="live_clock",
                    className="three-col",
                    children=datetime.datetime.now().strftime("%H:%M:%S"),
                ),width=3),
            ]),

            html.Table(
                className="table-news",
                children=[
                    html.Tr(
                        children=[
                            html.Td(
                                children=[
                                    html.A(
                                        className="td-link",
                                        children=df.iloc[i]["title"],
                                        href=df.iloc[i]["url"],
                                        target="_blank",
                                    )
                                ]
                            )
                        ]
                    )
                    for i in range(min(len(df), max_rows))
                ],
            ),
        ]
    )

def build_right_sidebar():
    card = dbc.Card(
        [
            dbc.CardBody(
                [
                    html.Div(id="news", children=update_news())
                ]
            ),
        ],
    )
    return card


def build_left_side_whole():
    card = dbc.Card(
        [
            dbc.CardBody(
                [   
                    build_left_side_row1(),
                    build_left_side_row2(),
                    build_left_side_row3(),
                    build_left_side_row4()
                ]
            ),
        ],
    )
    return card


def build_left_side_row1():
    card = dbc.Card(
        [
            dbc.CardBody(
                [   
                    dbc.Row([
                        dbc.Col(build_nifty(),width="4"),
                        dbc.Col(build_sensex(),width="4"),
                        dbc.Col(build_usdinr(),width="4")
                        ])
                ]
            ),
        ],
    )
    return card


def build_left_side_row2():
    card = dbc.Card(
        [
            dbc.CardBody(
                [   
                    dbc.Row([
                        dbc.Col(build_market_action(),width="6"),
                        dbc.Col(build_most_active(),width="6")
                        ])
                ]
            ),
        ],
    )
    return card


def build_left_side_row3():
    card = dbc.Card(
        [
            dbc.CardBody(
                [   
                    dbc.Row([
                        dbc.Col(build_top_gainers(),width="6"),
                        dbc.Col(build_top_losers(),width="6")
                        ])
                ]
            ),
        ],
    )
    return card


def build_left_side_row4():
    card = dbc.Card(
        [
            dbc.CardBody(
                [   
                    dbc.Row([
                        dbc.Col(build_commodities(),width="6"),
                        dbc.Col(build_currencies(),width="6")
                        ])
                ]
            ),
        ],
    )
    return card


def build_sensex():
    card = dbc.Card(
        [
            dbc.CardHeader("SENSEX"),
            dbc.CardBody(
                [
                    html.P(id="sensex",children=update_sensex()),
                ]
            ),
        ],
        
    )
    return card

def update_sensex():
    rs = nse.get_index_quote("nifty bank")
    df=pd.DataFrame.from_dict(rs,orient="index")
    nifty_current=df[1:2].iloc[0].iloc[0]
    return nifty_current

def build_nifty():
    card = dbc.Card(
        [
            dbc.CardHeader("NIFTY 50"),
            dbc.CardBody(
                [
                    html.P(id="nifty",children=update_nifty()),
                ]
            ),
        ],
        
    )
    return card

def update_nifty():
    rs = nse.get_index_quote("NIFTY 50")
    df=pd.DataFrame.from_dict(rs,orient="index")
    nifty_current=df[1:2].iloc[0].iloc[0]
    return nifty_current


def build_usdinr():
    card = dbc.Card(
        [
            dbc.CardHeader("USD INR"),
            dbc.CardBody(
                [
                    html.P(id="usdinr",children=update_usdinr()),
                ]
            ),
        ],
    )
    return card

def update_usdinr():
    rs = nse.get_index_quote("NIFTY 50")
    df=pd.DataFrame.from_dict(rs,orient="index")
    nifty_current=df[1:2].iloc[0].iloc[0]
    return nifty_current

def build_market_action():
    card = dbc.Card(
        [
            dbc.CardHeader("Market Action"),
            dbc.CardBody(
                [
                    html.P(id="market_action",children=update_market_action()),
                ]
            ),
            
        ],
        
    )
    return card

def update_market_action():
    rs = nse.get_advances_declines()
    df=pd.DataFrame.from_dict(rs)
    table=dash_table.DataTable(
        id='ad_table',
        columns=[{"name": i, "id": i} 
                for i in df.columns],
        data=df.to_dict('records'),
        style_cell=dict(textAlign='left'),
        style_header=dict(backgroundColor="paleturquoise"),
        style_data=dict(backgroundColor="lavender")
    )
    return table


def build_most_active():
    card = dbc.Card(
        [
            dbc.CardHeader("Most Active"),
            dbc.CardBody(
                [
                    html.Div(id="most_active",children=update_most_active())
                ]
            ),
        ], 
    )
    return card


def update_most_active():
    rs = nse.get_active_monthly()
    df=pd.DataFrame.from_dict(rs)
    table=dash_table.DataTable(
        id='active_table',
        columns=[{"name": i, "id": i} 
                for i in df.columns],
        data=df.to_dict('records'),
        style_cell=dict(textAlign='left'),
        style_header=dict(backgroundColor="paleturquoise"),
        style_data=dict(backgroundColor="lavender")
    )
    return table

def build_top_gainers():
    card = dbc.Card(
        [
            dbc.CardHeader("Top Gainers"),
            dbc.CardBody(
                [        
                    html.P(id="top_gainers",children=update_top_gainers()),
                ]
            ),
            
        ],
        
    )
    return card

def update_top_gainers():
    rs = nse.get_top_gainers()
    df=pd.DataFrame.from_dict(rs)
    table=dash_table.DataTable(
        id='gainers_table',
        columns=[{"name": i, "id": i} 
                for i in df.columns],
        data=df.to_dict('records'),
        style_cell=dict(textAlign='left'),
        style_header=dict(backgroundColor="paleturquoise"),
        style_data=dict(backgroundColor="lavender")
    )
    return table

def build_top_losers():
    card = dbc.Card(
        [
            dbc.CardHeader("Top Losers"),
            dbc.CardBody(
                [                  
                    html.P(id="top_losers",children=update_top_losers()),
                ]
            ),  
        ],
    )
    return card

def update_top_losers():
    rs = nse.get_top_losers()
    df=pd.DataFrame.from_dict(rs)
    table=dash_table.DataTable(
        id='losers_table',
        columns=[{"name": i, "id": i} 
                for i in df.columns],
        data=df.to_dict('records'),
        style_cell=dict(textAlign='left'),
        style_header=dict(backgroundColor="paleturquoise"),
        style_data=dict(backgroundColor="lavender")
    )
    return table

def build_currencies():
    card = dbc.Card(
        [
            dbc.CardHeader("Currencies"),
            dbc.CardBody(
                [                   
                    html.P(id="currencies",children=update_currencies()),
                ]
            ),
            
        ],
        
    )
    return card

def update_currencies():
    return "This is some card text"

def build_commodities():
    card = dbc.Card(
        [
            dbc.CardHeader("Commodities"),
            dbc.CardBody(
                [
                    html.P(id="commodities",children=update_commodities()),
                ]
            ),
            
        ],
        
    )
    return card

def update_commodities():
    return "This is some card text"


def navbar():
    navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Historical Module", href="/apps/app4")),
        dbc.NavItem(dbc.NavLink("Realtime Module", href="/apps/app5")),
        dbc.NavItem(dbc.NavLink("Log Out", href="/apps/app1")),
    ],
    brand="Stock Market Prediction",
    brand_href="#",
    color="#119dff",
    dark=True,
    )
    return navbar


########################################################## layout ######################################################################
layout=html.Div(
    [
        # Interval component for live clock
        dcc.Interval(id="interval", interval=1 * 1000, n_intervals=0),
        # Interval component for news updates
        dcc.Interval(id="i_news", interval=1 * 60000, n_intervals=0),
        # Interval component for sensex updates
        dcc.Interval(id="i_sensex", interval=1 * 5000, n_intervals=0),
        # Interval component for nifty updates
        dcc.Interval(id="i_nifty", interval=1 * 5000, n_intervals=0),
        # Interval component for market action clock
        dcc.Interval(id="i_marketaction", interval=1 * 5000, n_intervals=0),
        # Interval component for most active updates
        dcc.Interval(id="i_mostactive", interval=1 * 5000, n_intervals=0),
        # Interval component for top gainers updates
        dcc.Interval(id="i_topgainers", interval=1 * 5000, n_intervals=0),
        # Interval component for top losers updates
        dcc.Interval(id="i_toplosers", interval=1 * 5000, n_intervals=0),
        # Interval component for commodities updates
        dcc.Interval(id="i_commodities", interval=1 * 5000, n_intervals=0),
        # Interval component for currencies updates
        dcc.Interval(id="i_currencies", interval=1 * 5000, n_intervals=0),

        dbc.Row([
            dbc.Col(html.Div([navbar()]),width=12)
        ]),
        dbc.Row([
            dbc.Col(html.Div([build_left_side_whole()]),width=8),
            dbc.Col(html.Div(build_right_sidebar()),width=4)
        ])
    ]
)



##################################################### callbacks ##################################################################
#Callback to update news
@app.callback(Output("news", "children"), [Input("i_news", "n_intervals")])
def update_news_div(n):
    return update_news()

# Callback to update live clock
@app.callback(Output("live_clock", "children"), [Input("interval", "n_intervals")])
def update_time(n):
    return datetime.datetime.now().strftime("%H:%M:%S")

# Callback to update sensex
@app.callback(Output("sensex", "children"), [Input("i_sensex", "n_intervals")])
def update_sensex_div(n):
    return update_sensex()

# Callback to update nifty
@app.callback(Output("nifty", "children"), [Input("i_nifty", "n_intervals")])
def update_nifty_div(n):
    return update_nifty()

# Callback to update usd inr
@app.callback(Output("usdinr", "children"), [Input("i_marketaction", "n_intervals")])
def update_market_action_div(n):
    return update_usdinr()

# Callback to update market action
@app.callback(Output("market_action", "children"), [Input("i_marketaction", "n_intervals")])
def update_market_action_div(n):
    return update_market_action()

# Callback to update most active
@app.callback(Output("most_active", "children"), [Input("i_mostactive", "n_intervals")])
def update_most_active_div(n):
    return update_most_active()

# Callback to update top gainers
@app.callback(Output("top_gainers", "children"), [Input("i_topgainers", "n_intervals")])
def update_top_gainers_div(n):
    return update_top_gainers()

# Callback to update top losers
@app.callback(Output("top_losers", "children"), [Input("i_toplosers", "n_intervals")])
def update_top_losers_div(n):
    return update_top_losers()

# Callback to update commodities
@app.callback(Output("commodities", "children"), [Input("i_commodities", "n_intervals")])
def update_commodities_div(n):
    return update_commodities()

# Callback to update currencies
@app.callback(Output("currencies", "children"), [Input("i_currencies", "n_intervals")])
def update_currencies_div(n):
    return update_currencies()
