from app import *
import dash_bootstrap_components as dbc
from apps.mysql_database import register_customer
######################################################## support ######################################################################
def navbar():
    navbar = dbc.NavbarSimple(
    children=[
    ],
    brand="Stock Market Prediction",
    brand_href="#",
    color="primary",
    dark=True,
    )
    return navbar


######################################################## layout ####################################################################
layout=html.Div(style={'backgroundColor': '#111111'},
    children=[
        html.Div(
            id="banner",
            className="banner",
            children=[
                html.H2("AI Based Predictive Analysis of Stock Market Prediction"),
                
                ],
        ),
        html.A(html.Button('register !'),href="/apps/app1"),
    
        dbc.Form(
            [
                dbc.FormGroup(
                    [
                        dbc.Label("First Name", className="mr-2"),
                        dbc.Input(id="firstname",type="text", placeholder="Enter First Name"),
                    ],
                    className="mr-3",
                ),
                dbc.FormGroup(
                    [
                        dbc.Label("Last Name", className="mr-2"),
                        dbc.Input(id="lastname",type="text", placeholder="Enter Last Name"),
                    ],
                    className="mr-3",
                ),
                dbc.FormGroup(
                    [
                        dbc.Label("Email", className="mr-2"),
                        dbc.Input(id="email",type="email", placeholder="Enter Email"),
                    ],
                    className="mr-3",
                ),
                dbc.FormGroup(
                    [
                        dbc.Label("Username", className="mr-2"),
                        dbc.Input(id="username",type="text", placeholder="Enter Username"),
                    ],
                    className="mr-3",
                ),
                dbc.FormGroup(
                    [
                        dbc.Label("Password", className="mr-2"),
                        dbc.Input(id="password",type="password", placeholder="Enter Password"),
                    ],
                    className="mr-3",
                ),

                dbc.Button("Submit", color="primary"),
            ],
            inline=True,
        ),

        dcc.ConfirmDialog(
            id='Popup',
            message='',
        ),


    ])
        
    


####################################################### callbacks ##################################################################
@app.callback(
    [dash.dependencies.Output('Popup','message'),
    dash.dependencies.Output('Popup','displayed')],
    [Input("Submit", "n_clicks")],
    state=[
    dash.dependencies.State('firstname', 'value'),
    dash.dependencies.State('lastname', 'value'),
    dash.dependencies.State('email', 'value'),
    dash.dependencies.State('username', 'value'),
    dash.dependencies.State('password', 'value'),
    ]
)
def on_button_click(n,firstname,lastname,email,username,password):
    print("hi clicked")
    value=register_customer(firstname,lastname,email,username,password)
    if value==0:
        return ("Customer cannot be registered ",True)
    else:
        return ("Customer registered successfully",True)
        


