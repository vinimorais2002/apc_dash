import pandas as pd # importando a biblioteca pandas para leitura de dados
import plotly.graph_objects as go
import plotly.express as px
from dash import html, Dash, dcc
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc

# definindo um dataframe a partir do arquivo 
# definindo um dataframe a partir do arquivo 
url = 'https://raw.githubusercontent.com/TrabalhoAPC2021-02/Trabalho_Final/main/arquivos/02.1_salarios_CLT_Terceirizado.xlsx'
df = pd.read_excel(url)

#df = pd.read_excel(io.BytesIO(uploaded['sala.xlsx'])) 
df

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

fig = go.Figure()

fig.add_trace(go.Funnel(name='Terceiro', y=tb_terceiro['Cargo'], x=tb_terceiro['Terceiro']))

fig.add_trace(go.Funnel(name='CLT', orientation='h', y=tb_clt['Cargo'], x=tb_clt['CLT']))


fig.update_layout(title='Comparação entre salários de contratados pela CLT e salários de terceirizados', template='plotly_dark')


#-------------------------------------Layout--------------------------

app = Dash(__name__, external_stylesheets=[dbc.themes.SUPERHERO])

fig = go.Figure()

fig.add_trace(go.Funnel(name='Terceiro', y=tb_terceiro['Cargo'], x=tb_terceiro['Terceiro']))

fig.add_trace(go.Funnel(name='CLT', orientation='h', y=tb_clt['Cargo'], x=tb_clt['CLT']))


fig.update_layout(title='Comparação entre salários de contratados pela CLT e salários de terceirizados', template='plotly_dark')

opcoes = ['Programador', 'Analista Programador', 'Analista de Suporte', 'Analista de sistemas']
opcoes.append('Gráfico original')

app.layout = html.Div(children=[
    html.H1(children='Mercado de Ti', style={'text-align': 'center'}),
    html.Div(id='texto'),
    dcc.Dropdown(
        id='teste_button',
        options=opcoes,
        value='Gráfico original',
        style={'color': '#6134eb'}
    ),
    dcc.Graph(id='test_graph'),
])

#-----------------------Interação---------------------------

@app.callback(
    Output('texto', 'children'),
    Input('teste_button', 'value'),
)

def update_text(value):
    return f'Você selecionou {value}'

@app.callback(
    Output('test_graph', 'figure'),
    Input('teste_button', 'value')
)

def update_graph(value):
    if value == 'Gráfico original':
        fig = go.Figure()
        fig.add_trace(go.Funnel(name='Terceiro', y=tb_terceiro['Cargo'], x=tb_terceiro['Terceiro']))
        fig.add_trace(go.Funnel(name='CLT', orientation='h', y=tb_clt['Cargo'], x=tb_clt['CLT']))
        fig.update_layout(title='Comparação entre salários de contratados pela CLT e salários de terceirizados', template='plotly_dark')
    elif value == 'Programador':
        programador = df[df['Cargo'] == 'Programador']
        fig = px.bar(programador, x='Especialidade', y='Terceiro', color='Cargo')
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
