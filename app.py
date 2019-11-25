
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd

app = dash.Dash(__name__)
server = app.server

app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

df = pd.read_csv(
    'https://gist.githubusercontent.com/chriddyp/'
    'cb5392c35661370d95f300086accea51/raw/'
    '8e0768211f6b747c0db42a9ce9a0937dafcbd8b2/'
    'indicators.csv')

available_indicators = df['Indicator Name'].unique()

app.layout = html.Div([
    html.Div([

        html.Div([
            dcc.Dropdown(
                id='xaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Fertility rate, total (births per woman)'
            ),
            dcc.RadioItems(
                id='xaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ],
        style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='yaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Life expectancy at birth, total (years)'
            ),
            dcc.RadioItems(
                id='yaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ],style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ]),

    dcc.Graph(id='indicator-graphic'),

    dcc.Slider(
        id='year--slider',
        min=df['Year'].min(),
        max=df['Year'].max(),
        value=df['Year'].max(),
        step=None,
        marks={str(year): str(year) for year in df['Year'].unique()}
    )
])

@app.callback(
    dash.dependencies.Output('indicator-graphic', 'figure'),
    [dash.dependencies.Input('xaxis-column', 'value'),
     dash.dependencies.Input('yaxis-column', 'value'),
     dash.dependencies.Input('xaxis-type', 'value'),
     dash.dependencies.Input('yaxis-type', 'value'),
     dash.dependencies.Input('year--slider', 'value')])
def update_graph(xaxis_column_name, yaxis_column_name,
                 xaxis_type, yaxis_type,
                 year_value):
    dff = df[df['Year'] == year_value]
    
    return {
        'data': [go.Scatter(
            x=dff[dff['Indicator Name'] == xaxis_column_name]['Value'],
            y=dff[dff['Indicator Name'] == yaxis_column_name]['Value'],
            text=dff[dff['Indicator Name'] == yaxis_column_name]['Country Name'],
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            xaxis={
                'title': xaxis_column_name,
                'type': 'linear' if xaxis_type == 'Linear' else 'log'
            },
            yaxis={
                'title': yaxis_column_name,
                'type': 'linear' if yaxis_type == 'Linear' else 'log'
            },
            margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest'
        )
    }

if __name__ == '__main__':
    app.run_server()


# <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.3.0/css/font-awesome.min.css">
# 
# [http://localhost:8050](http://localhost:8050)
# 
# Press  <i class="fa fa-stop"></i>  in the tool bar before execute the next cell

# <div><p><!-- react-text: 7938 -->In this example, the <!-- /react-text --><code>update_graph</code><!-- react-text: 7940 --> function gets called whenever the
# <!-- /react-text --><code>value</code><!-- react-text: 7942 --> property of the <!-- /react-text --><code>Dropdown</code><!-- react-text: 7944 -->, <!-- /react-text --><code>Slider</code><!-- react-text: 7946 -->, or <!-- /react-text --><code>RadioItems</code><!-- react-text: 7948 --> components
# change.<!-- /react-text --></p><p><!-- react-text: 7950 -->The input arguments of the <!-- /react-text --><code>update_graph</code><!-- react-text: 7952 --> function are the new or current
# value of the each of the <!-- /react-text --><code>Input</code><!-- react-text: 7954 --> properties, in the order that they were
# specified.<!-- /react-text --></p><p><!-- react-text: 7956 -->Even though only a single <!-- /react-text --><code>Input</code><!-- react-text: 7958 --> changes at a time (a user can only change
# the value of a single Dropdown in a given moment), Dash collects the current
# state of all of the specified <!-- /react-text --><code>Input</code><!-- react-text: 7960 --> properties and passes them into your
# function for you. Your callback functions are always guarenteed to be passed
# the representative state of the app.<!-- /react-text --></p><p><!-- react-text: 7962 -->Let's extend our example to include multiple outputs.<!-- /react-text --></p><h4>Multiple Outputs</h4><p><!-- react-text: 7965 -->Each Dash callback function can only update a single Output property.
# To update multiple Outputs, just write multiple functions.<!-- /react-text --></p></div>

# In[7]:


import dash
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash('')
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

app.layout = html.Div([
    dcc.RadioItems(
        id='dropdown-a',
        options=[{'label': i, 'value': i} for i in ['Canada', 'USA', 'Mexico']],
        value='Canada'
    ),
    html.Div(id='output-a'),

    dcc.RadioItems(
        id='dropdown-b',
        options=[{'label': i, 'value': i} for i in ['MTL', 'NYC', 'SF']],
        value='MTL'
    ),
    html.Div(id='output-b')

])

@app.callback(
    dash.dependencies.Output('output-a', 'children'),
    [dash.dependencies.Input('dropdown-a', 'value')])
def callback_a(dropdown_value):
    return 'You\'ve selected "{}"'.format(dropdown_value)

@app.callback(
    dash.dependencies.Output('output-b', 'children'),
    [dash.dependencies.Input('dropdown-b', 'value')])
def callback_b(dropdown_value):
    return 'You\'ve selected "{}"'.format(dropdown_value)

if __name__ == '__main__':
    app.run_server()


# <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.3.0/css/font-awesome.min.css">
# 
# [http://localhost:8050](http://localhost:8050)
# 
# Press  <i class="fa fa-stop"></i>  in the tool bar before execute the next cell

# <div><p><!-- react-text: 8140 -->You can also chain outputs and inputs together: the output of one callback
# function could be the input of another callback function.<!-- /react-text --></p><p><!-- react-text: 8142 -->This pattern can be used to create dynamic UIs where one input component
# updates the available options of the next input component.
# Here's a simple example.<!-- /react-text --></p></div>

# In[8]:


# -*- coding: utf-8 -*-
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash(__name__)

all_options = {
    'America': ['New York City', 'San Francisco', 'Cincinnati'],
    'Canada': [u'Montréal', 'Toronto', 'Ottawa']
}
app.layout = html.Div([
    dcc.RadioItems(
        id='countries-dropdown',
        options=[{'label': k, 'value': k} for k in all_options.keys()],
        value='America'
    ),

    html.Hr(),

    dcc.RadioItems(id='cities-dropdown'),

    html.Hr(),

    html.Div(id='display-selected-values')
])

@app.callback(
    dash.dependencies.Output('cities-dropdown', 'options'),
    [dash.dependencies.Input('countries-dropdown', 'value')])
def set_cities_options(selected_country):
    return [{'label': i, 'value': i} for i in all_options[selected_country]]

@app.callback(
    dash.dependencies.Output('cities-dropdown', 'value'),
    [dash.dependencies.Input('cities-dropdown', 'options')])
def set_cities_value(available_options):
    return available_options[0]['value']

@app.callback(
    dash.dependencies.Output('display-selected-values', 'children'),
    [dash.dependencies.Input('countries-dropdown', 'value'),
     dash.dependencies.Input('cities-dropdown', 'value')])
def set_display_children(selected_country, selected_city):
    return u'{} is a city in {}'.format(
        selected_city, selected_country,
    )

if __name__ == '__main__':
    app.run_server()


# <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.3.0/css/font-awesome.min.css">
# 
# [http://localhost:8050](http://localhost:8050)
# 
# Press  <i class="fa fa-stop"></i>  in the tool bar before execute the next cell

# <div><p><!-- react-text: 8352 -->The first callback updates the available options in the second <!-- /react-text --><code>RadioItems</code><!-- react-text: 8354 -->
# component based off of the selected value in the first <!-- /react-text --><code>RadioItems</code><!-- react-text: 8356 --> component.<!-- /react-text --></p><p><!-- react-text: 8358 -->The second callback sets an initial value when the <!-- /react-text --><code>options</code><!-- react-text: 8360 --> property changes:
# it sets it to the first value in that <!-- /react-text --><code>options</code><!-- react-text: 8362 --> array.<!-- /react-text --></p><p><!-- react-text: 8364 -->The final callback displays the selected <!-- /react-text --><code>value</code><!-- react-text: 8366 --> of each component.
# If you change the <!-- /react-text --><code>value</code><!-- react-text: 8368 --> of the countries <!-- /react-text --><code>RadioItems</code><!-- react-text: 8370 --> component, Dash
# will wait until the <!-- /react-text --><code>value</code><!-- react-text: 8372 --> of the cities component is updated
# before calling the final callback. This prevents your callbacks from being
# called with inconsistent state like with <!-- /react-text --><code>"USA"</code><!-- react-text: 8374 --> and <!-- /react-text --><code>"Montréal"</code><!-- react-text: 8376 -->.<!-- /react-text --></p></div>

# <div><h3>Summary</h3><p><!-- react-text: 8380 -->We've covered the fundamentals of callbacks in Dash.
# Dash apps are built off of a set
# of simple but powerful principles: declarative UIs that are customizable
# through reactive and functional Python callbacks.
# Every element attribute of the declarative components can be updated through
# a callback and a subset of the attributes, like the <!-- /react-text --><code>value</code><!-- react-text: 8382 --> properties of
# the <!-- /react-text --><code>dcc.Dropdown</code><!-- react-text: 8384 -->, are editable by the user in the interface.<!-- /react-text --></p><hr></div>

# # Final Project
# 
# Create a Dashboard taking data from [Eurostat, GDP and main components (output, expenditure and income)](http://ec.europa.eu/eurostat/web/products-datasets/-/nama_10_gdp). 
# The dashboard will have two graphs: 
# 
# * The first one will be a scatterplot with two DropDown boxes for the different indicators. It will have also a slide for the different years in the data. 
# * The other graph will be a line chart with two DropDown boxes, one for the country and the other for selecting one of the indicators. (hint use Scatter object using mode = 'lines' [(more here)](https://plot.ly/python/line-charts/) 
# 
# 

# In[4]:


# for the final project: make the two graphs/dashboards interdepented
# click propterty on the first one should change output on the second one


# In[ ]:




