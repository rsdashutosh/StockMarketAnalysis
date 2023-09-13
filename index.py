import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from apps import Module_1_Login, Module_2_Registration, Module_3_Homepage, Module_4_Historical, Module_5_Realtime,mysql_database

# build database
mysql_database.build_database()

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/apps/app2':
        return Module_2_Registration.layout
    elif pathname == '/apps/app3':
        return Module_3_Homepage.layout
    elif pathname == '/apps/app4':
        return Module_4_Historical.layout
    elif pathname == '/apps/app5':
        return Module_5_Realtime.layout
    else:
        return Module_1_Login.layout

if __name__ == '__main__':
    app.run_server(debug=True)
