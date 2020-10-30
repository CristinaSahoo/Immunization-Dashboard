import dash
import dash_core_components as dcc
import dash_html_components as html 
from dash.dependencies import Input, Output 

import requests 
import plotly.graph_objects as go
import pandas as pd

pd.set_option("display.max_rows", 999)
pd.set_option("display.max_columns", 999)

df = pd.read_csv('WHS8_110.csv')

new_columns = {
    'Country' : 'country'
}

df.columns = df.iloc[0].values
df = df[1:]
df = df.fillna(0).copy()
df.columns = df.columns.astype(str)
df.columns = [col.replace('.0','') for col in df.columns]
df.rename(columns=new_columns, inplace=True)

#df_country = df.head(30)
#df_year = df.head(30)

app = dash.Dash() 

server = app.server

app.layout = html.Div(
    [ 
        html.H1(
            'Immunization Dashboard',
            style = {'text-align' : 'center'}
        ), 
        html.Div([ 
            dcc.Dropdown(
                id='year_selection',
                options=[
                    {'label': '2019', 'value': '2019'},
                    {'label': '2018', 'value': '2018'},
                    {'label': '2017', 'value': '2017'},
                    {'label': '2016', 'value': '2016'},
                    {'label': '2015', 'value': '2015'},
                    {'label': '2014', 'value': '2014'},
                    {'label': '2013', 'value': '2013'},
                    {'label': '2012', 'value': '2012'}
                ],
                value = '2019'
            ),
            dcc.Graph(id ='bargraph'),
            dcc.Dropdown(
                id='country_selection',
                options=[
                    {'label': 'Romania', 'value': 'Romania'},
                    {'label': 'United States of America', 'value': 'United States of America'},
                    {'label': 'France', 'value': 'France'},
                    {'label': 'Hungary', 'value': 'Hungary'},
                    {'label': 'Italy', 'value': 'Italy'},
                    {'label': 'Sudan', 'value': 'Sudan'},
                    {'label': 'Spain', 'value': 'Spain'},
                    {'label': 'Egypt', 'value': 'Egypt'},
                    {'label': 'India', 'value': 'India'},
                ],
                value = 'Romania'
            ),
            dcc.Graph(id ='linegraph'),
        ],
    style= {'padding':10})
    ]
)

@app.callback(
    Output('bargraph','figure'),         
    [Input('year_selection','value')]
)
def retrieve_revenue(year):
    df_country = df['country'].head(20)
    df_year = df[year].head(20)
    datapoints = {'data': [go.Bar(x=df_country, y=df_year)],'layout': dict(yaxis={'title':'Vaccination %'}, )} 
    return datapoints
 
@app.callback(
    Output('linegraph','figure'), 
    [Input('country_selection','value')]
) 
def retrieve_revenue(country): 
    df_country = df[df['country'] == country]
    df_country = df_country.T.drop('country', axis=0)
    df_country.columns = ['rate']
    df_country = df_country.rename(columns={df_country.columns[0] : 'rate'})
    years = list(df_country.index)
    rates = list(df_country['rate'].values)
    datapoints = {'data': [go.Scatter(x=years, y=rates, mode="lines+markers")], 'layout' : dict(yaxis=dict(range=[0,100]))}
    return datapoints 

if __name__ == '__main__': 
    app.run_server(debug=True)