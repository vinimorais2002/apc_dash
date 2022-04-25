from click import style
import dash
import dash_core_components as dcc
from dash import html
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc

import plotly.graph_objects as go
import plotly.express as px

import pandas as pd
import numpy as np
import json


url = 'https://raw.githubusercontent.com/TrabalhoAPC2021-02/Trabalho_Final/main/arquivos/02.1_salarios_CLT_Terceirizado.xlsx'
df = pd.read_excel(url)

df['Cargo'].value_counts()

# criando um data frame para os cargos mais repetidos

programador = df[df['Cargo'] == 'Programador']
anpro = df[df['Cargo'] == 'Analista Programador']
ansup = df[df['Cargo'] == 'Analista de Suporte']
ansis = df[df['Cargo'] == 'Analista de sistemas']

# tratando os dados para calcular a soma e a media
# para terceirizado

t_programador = programador['Terceiro'].tolist()
t_anpro = anpro['Terceiro'].tolist()
t_ansup =ansup['Terceiro'].tolist()
t_ansis = ansis['Terceiro'].tolist()

# usando o for para criar uma média para cada cargo

soma_t_pro = 0
for i in range (len(t_programador)):
  soma_t_pro = soma_t_pro + t_programador[i]
media_pro = soma_t_pro/len(t_programador)
print('Terc_programador',soma_t_pro, media_pro)

soma_t_anpro = 0
for i in range (len(t_anpro)):
  soma_t_anpro = soma_t_anpro + t_anpro[i]
media_anpro = soma_t_anpro/len(t_anpro)
print('Terc_analista_programador',soma_t_anpro, media_anpro)

soma_t_ansup = 0
for i in range (len(t_ansup)):
  soma_t_ansup = soma_t_ansup + t_ansup[i]
media_ansup = soma_t_ansup/len(t_ansup)
print('Terc_analista_suporte', soma_t_ansup, media_ansup)

soma_t_ansis = 0
for i in range (len(t_ansis)):
  soma_t_ansis = soma_t_ansis + t_ansis[i]
media_ansis = soma_t_ansis/len(t_ansis)
print('Terc_analista_sistemas',soma_t_ansis, media_ansis)

# criando um novo dataframe
# para terceirizado

column = ['Cargo', 'Terceiro']
line = ['', '','','']
dados = [['Analista de Suporte', media_ansup], ['Programador', media_pro]
         , ['Analista programador', media_anpro], ['Analista de sistemas', media_ansis]]
tb_terceiro = pd.DataFrame(data=dados, index=line, columns=column) 
print(tb_terceiro)    

# tratando os dados para calcular a soma e a media
# para o CLT

clt_programador = programador['CLT'].tolist()
clt_anpro = anpro['CLT'].tolist()
clt_ansup =ansup['CLT'].tolist()
clt_ansis = ansis['CLT'].tolist()

soma_clt_pro = 0
for i in range (len(clt_programador)):
  soma_clt_pro = soma_clt_pro + clt_programador[i]
media_clt_pro = soma_clt_pro/len(clt_programador)
print('CLT_programador', soma_clt_pro, media_clt_pro)

soma_clt_anpro = 0
for i in range (len(clt_anpro)):
  soma_clt_anpro = soma_clt_anpro + clt_anpro[i]
media_clt_anpro = soma_clt_anpro/len(clt_anpro)
print('CLT_analista_programador', soma_clt_anpro, media_clt_anpro)

soma_clt_ansup = 0
for i in range (len(clt_ansup)):
  soma_clt_ansup = soma_clt_ansup + clt_ansup[i]
media_clt_ansup = soma_clt_ansup/len(clt_ansup)
print('CLT_analista_suporte', soma_clt_ansup, media_clt_ansup)

soma_clt_ansis = 0
for i in range (len(clt_ansis)):
  soma_clt_ansis = soma_clt_ansis + clt_ansis[i]
media_clt_ansis = soma_clt_ansis/len(clt_ansis)
print('CLT_analista_sistemas',soma_clt_ansis, media_clt_ansis)

# criando um novo dataframe
# para o CLT
column = ['Cargo', 'CLT']
line = ['', '','','']
dados = [['Analista de Suporte', media_clt_ansup], ['Programador', media_clt_pro]
         , ['Analista programador', media_clt_anpro], ['Analista de sistemas', media_clt_ansis]]
tb_clt = pd.DataFrame(data=dados, index=line, columns=column) 
print(tb_clt)


app =dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])


fig = go.Figure()

fig.add_trace(go.Funnel(name='Terceiro', y=tb_terceiro['Cargo'], x=tb_terceiro['Terceiro']))

fig.add_trace(go.Funnel(name='CLT', orientation='h', y=tb_clt['Cargo'], x=tb_clt['CLT']))


fig.update_layout(

template='plotly_dark',
autosize=True,
margin=go.Margin(l=0, r=0, t=0, b=0),

)

#============================================
# Layout
app.layout = dbc.Container(
  dbc.Row([
    dbc.Col([
      html.Div([
        html.Img(id='logo', src=app.get_asset_url("logo.png"), height=50),
        html.H5("Salário em R$ Terceirizados e CLT"),
        dbc.Button("MERCADO DE TI", color='primary', id='cargos_botoes', size='lg'),
      ], style={}),
      html.P('Informe qual cargo deseja visualizar', style={'margin-top': '40px'}),

      html.Div(id='test_div', children=[
        dcc.Dropdown(
          # passar uma lista somente com os 4 nomes
          df['Cargo'].unique(),
          'Cargos',
          id='test_botao'
        )
      ]),

      dbc.Row([
          dbc.Col([
              dbc.Card([
                dbc.CardBody([
                  html.Span('Maior salário CLT'),
                  html.H3(style={'color': '#04bf3c'}, id='maior_salario_clt'),
                  html.Span('Menor salário CLT'),
                  html.H5(id='menor_clt'),
                ])
              ], color='light', outline=True, style={'margin-top': '10px', 'box-shadow': '0 4px 4px 0 rgba(0,0,0,0.15), 0 4px 20px 0 rgba(0,0,0,0.19)', 'color': '#FFFFFF'})
          ], md=6),
          dbc.Col([
              dbc.Card([
                dbc.CardBody([
                  html.Span('Maior salário Terceiro'),
                  html.H3(style={'color': '#0413bf'}, id='maior_salario_terceiro'),
                  html.Span('Menor salário Terceiro'),
                  html.H5(id='menor_terceiro'),
                ])
              ], color='light', outline=True, style={'margin-top': '10px', 'box-shadow': '0 4px 4px 0 rgba(0,0,0,0.15), 0 4px 20px 0 rgba(0,0,0,0.19)', 'color': '#FFFFFF'})
          ], md=6),

      ]),
          
    ], md=5, style={'padding': '25px', 'background-color': '#242424'}),
    dbc.Col([
        dcc.Loading(id='loading_1', type='default'
        ,children=[
             dcc.Graph(id='Funil', figure=fig, style={'height' : '100vh', 'margin-right' : '10px'}) 
        ])
        
    ]),
  ])
, fluid=True)

#=================================
# Interatividade

if __name__ == '__main__':
    app.run_server(debug=True)