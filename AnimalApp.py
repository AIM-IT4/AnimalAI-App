#!/usr/bin/env python
# coding: utf-8

# In[1]:


import dash                     # pip install dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px     # pip install plotly==5.2.2

import pandas as pd  


# In[2]:


df = pd.read_csv("https://raw.githubusercontent.com/Coding-with-Adam/Dash-by-Plotly/master/Analytic_Web_Apps/Excel_to_Dash_Animal_Shelter/Animals_Inventory.csv")
df["intake_time"] = pd.to_datetime(df["intake_time"])
df["intake_time"] = df["intake_time"].dt.hour
print(df.head())


# In[3]:


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


# In[4]:


app.layout = html.Div([
    html.H1("Analytics Dashboard of Dallas Animal Shelter (Dash Plotly)", style={"textAlign":"center"}),
    html.Hr(),
    html.P("Choose animal of interest:"),
    html.Div(html.Div([
        dcc.Dropdown(id='animal-type', clearable=False,
                     value="DOG",
                     options=[{'label': x, 'value': x} for x in
                              df["animal_type"].unique()]),
    ],className="two columns"),className="row"),

    html.Div(id="output-div", children=[]),
])


# In[5]:


@app.callback(Output(component_id="output-div", component_property="children"),
              Input(component_id="animal-type", component_property="value"),
)
def make_graphs(animal_chosen):
    # HISTOGRAM
    df_hist = df[df["animal_type"]==animal_chosen]
    fig_hist = px.histogram(df_hist, x="animal_breed")
    fig_hist.update_xaxes(categoryorder="total descending")

    # STRIP CHART
    fig_strip = px.strip(df_hist, x="animal_stay_days", y="intake_type")

    # SUNBURST
    df_sburst = df.dropna(subset=['chip_status'])
    df_sburst = df_sburst[df_sburst["intake_type"].isin(["STRAY", "FOSTER", "OWNER SURRENDER"])]
    fig_sunburst = px.sunburst(df_sburst, path=["animal_type", "intake_type", "chip_status"])

    # Empirical Cumulative Distribution
    df_ecdf = df[df["animal_type"].isin(["DOG","CAT"])]
    fig_ecdf = px.ecdf(df_ecdf, x="animal_stay_days", color="animal_type")
    df_line = df.sort_values(by=["intake_time"], ascending=True)
    df_line = df_line.groupby(
        ["intake_time", "animal_type"]).size().reset_index(name="count")
    print(df_line.head())
    fig_line = px.line(df_line, x="intake_time", y="count",
                       color="animal_type", markers=True)

    return [
        html.Div([
            html.Div([dcc.Graph(figure=fig_hist)], className="six columns"),
            html.Div([dcc.Graph(figure=fig_strip)], className="six columns"),
        ], className="row"),
        html.H2("All Animals", style={"textAlign":"center"}),
        html.Hr(),
        html.Div([
            html.Div([dcc.Graph(figure=fig_sunburst)], className="six columns"),
            html.Div([dcc.Graph(figure=fig_ecdf)], className="six columns"),
        ], className="row"),
        html.Div([
            html.Div([dcc.Graph(figure=fig_line)], className="twelve columns"),
        ], className="row"),
    ]


# In[ ]:


app.run_server(port = 8097, dev_tools_ui=True, #debug=True,
              dev_tools_hot_reload =True, threaded=True)


# In[ ]:


pip install nbconvert

