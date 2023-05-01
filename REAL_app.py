from dash import Dash, html, dash_table, dcc, callback, Output, Input, State
from collections import OrderedDict
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

import mysql_utils
import mongodb_utils
import neo4j_utils



#List of keywords
keywords = mysql_utils.getNames('keyword')
universities = mysql_utils.getNames('university')
professors = mysql_utils.getNames('faculty')


prof_df = pd.DataFrame(OrderedDict([
    ('professors', professors),
]))


keywords_df = pd.DataFrame(OrderedDict([
    ('keywords', keywords),
]))



app = Dash(__name__)

app.layout = html.Div([

    html.H1("Identifying Potential Research Topics, Universities, and Professors to Work w/in the Academic World"),

    html.Br(),
    html.Hr(),
    html.Br(),

    html.Div(
        children=[
            html.Div(
                children=[
                    html.Div(children='Search by Keyword for # of Publications Written Over Time'),
                    dcc.Dropdown(keywords, value='xml', id='widget_ONE_dropdown_selection'),
                    dcc.Graph(figure={}, id='keyword-publications-line-graph'),
                ],
                style={'display': 'inline-block', 'marginRight': '10px', 'verticalAlign': 'top', 'width': '49%', 'border': '2px solid lightblue'},
            ),
            html.Div(
                children=[
                    html.Div(children='Search for Most Accomplished Researchers by Keyword'),
                    dcc.Dropdown(keywords, value='deep learning', id='widget_TWO_dropdown_selection'),
                    dcc.Graph(figure={}, id='profs-krc-ranking-horizontal-bar-graph'),
                ],
                style={'display': 'inline-block', 'marginLeft': '10px', 'verticalAlign': 'top', 'width': '49%', 'border': '2px solid lightblue'},
            ),
        ],
        style={'border': '2px solid lightblue', 'padding': '10px'},
    ),

    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),

    html.Div(
        children=[
            html.Div(
                children=[
                    html.Div(children="Top 10 Research Keywords by University"),
                    dcc.Dropdown(universities, value='College of William Mary', id='widget_THREE_dropdown_selection'),
                    dcc.Graph(figure={}, id='university-focus-pie-chart'),
                ],
                style={'display': 'inline-block', 'marginRight': '10px', 'verticalAlign': 'top', 'width': '49%',
                       'border': '2px solid lightblue'},
            ),
            html.Div(
                children=[
                    html.Div(children='Professor Lookup'),
                    dcc.Dropdown(universities, value='University of illinois at Urbana Champaign', id='widget_FOUR_dropdown_selection'),
                    dcc.Dropdown(options={}, value='Abdussalam Alawini', id='dropdown-prof-names'),
                    html.Img(height="250", width="250", id='prof-picture'),
                    html.P(id='prof-name'),
                    html.P(id='prof-position-title'),
                    html.P(id='prof-phone'),
                    html.P(id='prof-email'),
                    html.P(id='prof-research-interest')
                ],
                style={'display': 'inline-block', 'marginLeft': '10px', 'verticalAlign': 'top', 'width': '49%',
                       'border': '2px solid lightblue'},
            ),
        ],
        style={'border': '2px solid lightblue', 'padding': '10px'},
    ),

    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),

    #Widget 5
    html.Div([
        dash_table.DataTable(
            id='table-dropdown',
            data=pd.DataFrame().to_dict('records'),
            columns=[
                {'id': 'professors', 'name': 'professors', 'presentation': 'dropdown'}
            ],
            editable=True,
            row_deletable=False,
            dropdown={
                'professors': {
                    'options': [
                        # {'label': "stevie", 'value': "johnson"}
                        {'label': i, 'value': i}
                        for i in prof_df['professors'].unique()
                    ]
                },
            }
        ),
        html.Button('Add Prof To Favorites', id='table-dropdown-button', n_clicks=0),
        html.H3(id='selected-professor')
    ]),

    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),


    #Widget 6
    html.Div([
        dash_table.DataTable(
            id='keywords-table-dropdown',
            data=pd.DataFrame().to_dict('records'),
            columns=[
                {'id': 'keywords', 'name': 'keywords', 'presentation': 'dropdown'}
            ],
            editable=True,
            row_deletable=False,
            dropdown={
                'keywords': {
                    'options': [
                        # {'label': "stevie", 'value': "johnson"}
                        {'label': i, 'value': i}
                        for i in keywords_df['keywords'].unique()
                    ]
                },
            }
        ),
        html.Button('Add Keyword To Favorites', id='keyword-table-dropdown-button', n_clicks=0),
        html.H3(id='selected-keyword')
    ]),


    html.Div(style={'padding-bottom' : 500})
])



#Widget 6 - Favorite Keywords
@app.callback(
    Output('selected-keyword', 'children'),
    Input('keyword-table-dropdown-button', 'n_clicks'),
    State('keywords-table-dropdown', 'data'),
)
def update_professor(n_clicks, table_data):
    if table_data:
        # extract the selected professor from the table data
        selected_keyword = table_data[-1]['keywords']
        # add newly added professor to userfavoritekeywords relation
        mysql_utils.add_user_favorite_keyword(selected_keyword)
        return "{0} added to favorites!".format(selected_keyword)

    return ""


@app.callback(
    Output('keywords-table-dropdown', 'data'),
    Input('keyword-table-dropdown-button', 'n_clicks'),
    State('keywords-table-dropdown', 'data'),
    State('keywords-table-dropdown', 'columns')
)
def add_row(n_clicks, rows, columns):
    if n_clicks > 0:
        rows.append({c['id']: '' for c in columns})
    return rows









#Widget 5 - Favorite Profs
@app.callback(
    Output('selected-professor', 'children'),
    Input('table-dropdown-button', 'n_clicks'),
    State('table-dropdown', 'data'),
)
def update_professor(n_clicks, table_data):
    if table_data:
        # extract the selected professor from the table data
        selected_professor = table_data[-1]['professors']
        # add newly added professor to userprofessorfavorites relation
        mysql_utils.add_user_favorite_professor(selected_professor)
        return "{0} added to favorites!".format(selected_professor)

    return ""


@app.callback(
    Output('table-dropdown', 'data'),
    Input('table-dropdown-button', 'n_clicks'),
    State('table-dropdown', 'data'),
    State('table-dropdown', 'columns')
)
def add_row(n_clicks, rows, columns):
    if n_clicks > 0:
        rows.append({c['id']: '' for c in columns})
    return rows









#Widget 4 - Part 2 : Update Prof Info
@app.callback(
    Output(component_id='prof-picture', component_property='src'),
    Output(component_id='prof-name', component_property='children'),
    Output(component_id='prof-position-title', component_property='children'),
    Output(component_id='prof-phone', component_property='children'),
    Output(component_id='prof-email', component_property='children'),
    Output(component_id='prof-research-interest', component_property='children'),
    Input(component_id='dropdown-prof-names', component_property='value')
)
def update_prof_profile(value):
    list_of_prof_records = neo4j_utils.CurrentUniProfRecords.prof_records_list
    for i in range(len(list_of_prof_records)):
        if(list_of_prof_records[i].data()['faculty']['name'] == value):
            photoUrl = safe_execute(list_of_prof_records[i], 'photoUrl')
            name = safe_execute(list_of_prof_records[i], 'name')
            position = safe_execute(list_of_prof_records[i], 'position')
            phone = safe_execute(list_of_prof_records[i], 'phone')
            email = safe_execute(list_of_prof_records[i], 'email')
            researchInterest = safe_execute(list_of_prof_records[i], 'researchInterest')

            return (photoUrl, name, position, phone, email, researchInterest)
    return ("IMG/blackboard.png", "_", "_", "_", "_", "_")

def safe_execute(prof_info_record, info_field):
    try:
        return prof_info_record.data()['faculty'][info_field]
    except KeyError:
        pass  # does nothing
    else:
        return "_"



#Widget 4 - Part 1 : Update Uni Prof Dropdown List After User Selects Uni
@app.callback(
    Output(component_id='dropdown-prof-names', component_property='options'),
    Input(component_id='widget_FOUR_dropdown_selection', component_property='value')
)
def update_prof_profile(value):
    #TO-DO
    list_prof_names = neo4j_utils.get_prof_names_by_university(value)
    return list_prof_names







#Widget 1 - Keyword Publications Count Line Graph
@app.callback(
    Output(component_id='keyword-publications-line-graph', component_property='figure'),
    Input(component_id='widget_ONE_dropdown_selection', component_property='value')
)
def update_line_plot(value):
    df_kw_years_pub_counts = mysql_utils.get_keyword_years_and_publication_counts(value)
    fig = px.line(df_kw_years_pub_counts, x='Year', y='Publication Count', markers=True)
    return fig


#Widget 2 - Profs KRC Horizontal Bar Graph
@app.callback(
    Output(component_id='profs-krc-ranking-horizontal-bar-graph', component_property='figure'),
    Input(component_id='widget_TWO_dropdown_selection', component_property='value')
)
def update_horizontal_bar_graph(value):
    df_krc_profs = mysql_utils.get_krc_profs_ranking_by_keyword(value)
    fig = px.bar(df_krc_profs, x="KRC Score", y="Professor", orientation='h')
    return fig


#Widget 3 - Uni Pie Chart
@app.callback(
    Output(component_id='university-focus-pie-chart', component_property='figure'),
    Input(component_id='widget_THREE_dropdown_selection', component_property='value')
)
def update_university_focus_pie_chart(value):
    #TO-DO
    df_pie_chart = mongodb_utils.version_TWO(value)
    fig = px.pie(df_pie_chart, values=df_pie_chart.columns[1], names=df_pie_chart.columns[0], hole=.3)
    return fig










if __name__ == '__main__':
    app.run_server(debug=True)