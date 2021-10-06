import pandas as pd
import plotly.express as px
import dash_core_components as dcc
import dash
import dash_table
import dash_html_components as html
from dash.dependencies import Input, Output

df2=pd.read_csv('df2.csv')
bardfcontinent=pd.read_csv('bardfcontinent.csv')
bardfcountry=pd.read_csv('bardfcountry.csv')
mapdf=pd.read_csv('mapdf.csv')

app = dash.Dash(__name__)
server = app.server
app.layout = html.Div([
    html.Div([
        html.Div([
            html.Div([
							html.H4("Max. hourly rate:", className='text1'),
							html.P('300 USD ', className='text1'),
						],)
        ], className='topcol1'),
        

        html.Div([
            html.Div([
							html.H4("Average hourly rate:", className='text1'),
							html.P('32.6 USD', className='text1'),
						],)
        ], className='topcol'),
        


        html.Div([
            html.Div([
							html.H4("Min. hourly rate:", className='text1'),
							html.P('3 USD', className='text1'),
							
						],)
        ], className='topcol'),


        html.Div([
            html.Div([
							html.H4("The country with the heighest average:", className='text1'),
							html.P('Luxembourg at 109.5 USD', className='text1'),

						],)
        ], className='topcol'),


        
        html.Div([
            html.Div([
							html.H4("The country with the lowest average:", className='text1'),
							html.P('Azerbaijan at 5 USD', className='text1'),
						],)
        ], className='topcol'),
        


        html.Div([
            html.Div(
						[
							html.H4("The most represented country:", className='text1'),
							html.P('Philippines', className='text1'),
							
						],)
        ], className='topcol'),
    ],id='top_row'),

    html.Div([
        html.Div([
            html.P(['Filter the data by continent'], className='text1'),
            dcc.Dropdown(id='dropdown',
                options=[
                    {'label':x, 'value':x} for x in mapdf.sort_values('country')['continent'].unique()
                
                 ],
            value=['Africa', 'Asia', 'North America', 'South America', 'Europe', 'Oceania'],
            multi=True,
            clearable=False,
            searchable=False, ), 

            html.P(['An interactive data table, filter the data yourself!'], className='text1'),
            html.Div([
            #     
                dash_table.DataTable(
                    id='datatable',
                    columns=[{"name": 'country', "id": 'country'},
                             {"name": 'hourly rate', "id": 'hourly rate'},
                             {"name": 'number of people', "id": 'number of people'},],
                    style_table={'height': '770px', 'overflowY': 'auto'},
                    editable=False,
                    style_as_list_view=True,
                    filter_action="native",
                    sort_action="native",
                    sort_mode="single",
                    column_selectable="multi",
                    row_selectable="multi",
                    row_deletable=True,
                    selected_columns=[],
                    selected_rows=[],
                    page_action="native",
                    page_current=0,
                    page_size=125,
                    style_cell={
                        'minWidth': 75, 'maxWidth': 75, 'width': 75, 
                        'backgroundColor': '#111111',
                        'color': '#00df43',
                        'textAlign': 'left',
                    },

                    style_header={'backgroundColor': '#111111'},
                   
                    style_data={
                        'whiteSpace': 'normal',
                        'height': 'auto'
                    }
                ),
            ], id='dashtable')
        ],id='side_col'),
        html.Div([
            html.Div([
                html.Div([
                    html.P(["Select a range of hourly rates to view on the map and scatter plot"], className='text1'), 

                    dcc.RangeSlider(
                    id='range_slider', 
                    marks={
                        5: '5',     
                        10: '10',
                        15: '15',
                        20: '20',
                        25: '25',
                        30: '30',
                        35: '35',
                        40: '40',
                        45: '45',
                        50: '50',
                        55: '55', 
                        60: '60',
                        
                    },
                    step=1, 
                    min=5,
                    max=60,
                    dots=False,
                    updatemode='mouseup',
                    value=[5, 60]
                    ),
                ], id='slider_container'),
                html.Div(
                    dcc.Graph(
                        id='graph1'
                    ),
                id='graph_container1'),

                html.Div(
                    dcc.Graph(
                        id='graph2'
                    ),
                id='graph_container2'),
            ], id='main_graphs'),

            html.Div([
                html.Div([
                    html.P(['Show number of people according to:'], className='text1'),
                    dcc.Dropdown(
                        id='dropdown1', 
                        value='country', 
                        options=[{'value': x, 'label': x} 
                                for x in ['country', 'continent']],
                        clearable=False,
                    ),
                ], id='dropdown_container'),
                html.Div(
                    dcc.Graph(
                        id='graph3'
                    ),
                id='graph_container3'),
                
                html.Div(
                    dcc.Graph(
                        id='graph4'
                    ),
                id='graph_container4'),
            ], id='secondary_graphs')
        ], id='main')
    ],id='bottom_row')
])

@app.callback(
   Output("graph3", "figure"), 
   [Input("dropdown1", "value"),] 
   )
def generate_chart(options):
   df = df2
   fig = px.pie(df, options,
           template='plotly_dark',
           hole=0.6, 
           color_discrete_sequence=px.colors.sequential.Aggrnyl,
        )
   fig.update_layout(showlegend=False)

   return fig


@app.callback(
   Output("graph4", "figure"), 
   [Input("dropdown1", "value"),] 
   )
def generate_chart(options):
   if options =='country':
       df=bardfcountry
   else:
        df=bardfcontinent


   fig = px.bar(df, x=options,
           y='number of people',
           color='hourly rate',
           color_continuous_scale='aggrnyl',
           template='plotly_dark',
        )
   fig.update_layout(showlegend=False)

   return fig

@app.callback(
    Output('datatable', 'data'),
    [Input('dropdown', 'value'), 
    Input('range_slider', 'value')]
)
def update_rows(selected_values, slider_values):
    dataframe=mapdf[mapdf['continent'].isin(selected_values)]
    dataframe=dataframe[(dataframe['hourly rate']>=slider_values[0])&(dataframe['hourly rate']<=slider_values[1])]
    
    data = dataframe
    
    return data.to_dict('records')




@app.callback(
    Output(component_id='graph1', component_property='figure'),
    [Input(component_id='datatable', component_property="derived_virtual_data")]
)

def update_scatter(all_rows_data):
#     emptyframe=""" Empty DataFrame
# Columns: []
# Index: []"""
    bool_statement=pd.DataFrame(all_rows_data).empty
    if bool_statement == True:
        data1=mapdf
    else:
        data1=pd.DataFrame(all_rows_data)

    
    
    dff = data1

    # for i in range(len(dff)):
    #     if i in slctd_row_indices:
    #         colors='#7FDBFF'
    #     else:
    #         colors='#0074D9'

    scatter=px.scatter(dff, x='country',
                     y='hourly rate',
                     size='number of people',
                    #  height=700,
                     size_max=40,
                     template = 'plotly_dark',
#                      width=1400,
                    #  text='country',
                     color='hourly rate',
                     color_continuous_scale='aggrnyl',
                     title='size represents number of people')
    
    return scatter

@app.callback(
    Output(component_id='graph2', component_property='figure'),
    [Input(component_id='datatable', component_property="derived_virtual_data"),
     Input(component_id='datatable', component_property='derived_virtual_selected_rows')]
)

def update_map(all_rows_data, slctd_row_indices):
#     emptyframe=""" Empty DataFrame
# Columns: []
# Index: []"""
    bool_statement=pd.DataFrame(all_rows_data).empty
    if bool_statement == True:
        data1=mapdf
    else:
        data1=pd.DataFrame(all_rows_data)


    dff = data1
    # print(type(dff))
    # if type(dff) == NoneType:
    #     time.sleep(60)

    

    map=px.choropleth(dff, locations='country',
                   locationmode='country names', 
                   color='hourly rate', 
                   template='plotly_dark',
                #    height=700,
                   color_continuous_scale='aggrnyl',
                #    width=800,
                )
    
    borders = [5 if i in slctd_row_indices else 1
                for i in dff]

    map.update_traces(marker_line_width=borders,)
    return map

if __name__ == "__main__":
   app.run_server(host='0.0.0.0', port=8050, debug=False)

