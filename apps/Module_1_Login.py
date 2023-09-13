from app import *


########################################################### support ################################################################

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


PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"

search_bar = dbc.Row(
    [
        dbc.Col(dbc.Input(type="search", placeholder="Search")),
        dbc.Col(
            dbc.Button("Search", color="primary", className="ml-2"),
            width="auto",
        ),
    ],
    no_gutters=True,
    className="ml-auto flex-nowrap mt-3 mt-md-0",
    align="center",
)

navbar = dbc.Navbar(
    [
        html.A(
            # Use row and col to control vertical alignment of logo / brand
            dbc.Row(
                [
                    dbc.Col(dbc.NavbarBrand("AI Based Predictive Analysis of Stock Market",)),
                    dbc.NavItem(dbc.NavLink("Historical Module", href="/apps/app4")),
                    dbc.NavItem(dbc.NavLink("Realtime Module", href="/apps/app5")),
                    dbc.NavItem(dbc.NavLink("Log Out", href="/apps/app1")),
                ],
                align="center",
                no_gutters=True,
            ),
            href="https://plot.ly",
        ),
        dbc.NavbarToggler(id="navbar-toggler"),
        dbc.Collapse(search_bar, id="navbar-collapse", navbar=True),
    ],
    color="dark",
    dark=True,
)

form = dbc.Form(
    [
        dbc.FormGroup(
            [
                dbc.Label("Email", className="mr-2"),
                dbc.Input(type="email", placeholder="Enter email"),
            ],
            className="mr-3",
        ),
        dbc.FormGroup(
            [
                dbc.Label("Password", className="mr-2"),
                dbc.Input(type="password", placeholder="Enter password"),
            ],
            className="mr-3",
        ),
        dbc.Button("Submit", color="primary"),
    ],
    inline=True,
)




############################################################ layout #############################################################

layout=html.Div(
    [   
        navbar,

        #html.A(html.Button('login!'),href="/apps/app3"),
        #html.A(html.Button('register!'),href="/apps/app2"),
        form
    ]
)


########################################################### callbacks ##############################################################




