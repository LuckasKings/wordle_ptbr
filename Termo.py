import pandas as pd
import plotly.express as px
import dash
import plotly.graph_objects as go
from dash import html
from dash import dcc

base = pd.read_excel('Termo\dicionariousp.xlsx', names=['dic'])  # Loading the database (dictionary)

base = base[base['dic'].str.len() == 5]  # Filtering to only select the words with 5 letter lenght
base['dic'] = base['dic'].str.lower()  # Transforming all letters to be lowercase

columns = ['1P', '2P', '3P', '4P', '5P']  # Listing the new columns.
numbers = list(range(5))  # Listing the positions of the letter, so "0" is the First position, "1" is the second, and so on.

for column, number in zip(columns, numbers):
    base[column] = base['dic'].str[number]  #This loop essentially will create the 5 columns listed in 'columns' and split the word in 5 letters, so 1P column will have the letter of the word in the first position.

letras = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
          'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'] #Listing all the letters of the alphabet

for letra in letras:
    base[letra] = base['dic'].str.contains(letra, regex=False)  #This loop will create a column with the corresponding letter, and return a True or False if the word contains the same letter.
    base[letra] = sum(base[letra])  #Will sum all the values in the column. True = 1 False = 0. This will repeat the sum value for every row.

posicao = pd.DataFrame()  #Creating a new dataframe to extract the count on every position of the word.

new_columns = []  #Creating a empty list for the loop
for column in columns:
    new_columns.append(column + 'Letra')  #Will just create the same 5 columns in 'columns', but with 'Letter' together. This will be used to store the index of 'value_counts' function.

for n_column, column in zip(new_columns, columns):
    posicao[n_column] = pd.Series(base[column].value_counts().index.tolist())  # This loop will create the 5 new columns listed in 'new_columns' and store the index previoulsy commented.

for coluna in columns:
    posicao[coluna] = pd.Series(base[coluna].value_counts().tolist())  # This loop will create the columns with the count from 'value_counts'.

first = pd.DataFrame()
second = pd.DataFrame()
third = pd.DataFrame()
fourth = pd.DataFrame()
fiveth = pd.DataFrame()


list_df = [first, second, third, fourth, fiveth]

# Lista de DataFrames que você quer processar
dataframes = [first, second, third, fourth, fiveth]

# Loop para processar cada DataFrame
for i, df in enumerate(dataframes, start=1):
    coluna_letra = f'{i}PLetra'
    coluna_posicao = f'{i}P'
    
    # Adiciona a coluna de letras
    df[coluna_letra] = letras
    
    # Faz o merge com o DataFrame posicao
    df = pd.merge(df, posicao[[coluna_letra, coluna_posicao]], on=coluna_letra, how='left')
    
    # Preenche os valores nulos com 0
    df = df.fillna(0)
    
    # Atualiza o DataFrame original
    dataframes[i-1] = df

# Desempacota os DataFrames atualizados
first, second, third, fourth, fiveth = dataframes


posicao_new = pd.DataFrame()
posicao_new = pd.concat([first, second, third, fourth, fiveth], axis=1)

columns_to_drop = ['2PLetra', '3PLetra', '4PLetra', '5PLetra']
posicao_new = posicao_new.drop(columns_to_drop, axis=1)

posicao_new = posicao_new.rename(columns={'1PLetra': 'Letra'})
posicao_new = posicao_new.sort_values(by='Letra', ascending=False)
posicao_new['Letra'] = posicao_new['Letra'].str.upper()

del base['dic']
base.drop(columns,inplace=True, axis=1)
base = base.head(1)

pivot = {'pivot':['pivot']}
analise = pd.DataFrame(pivot)
analise = pd.concat([base, analise])
analise = analise.melt(id_vars='pivot')
del analise['pivot']
analise.dropna(inplace=True)
analise = analise.sort_values('value', ascending=False)


#################################################

colorscales = px.colors.named_colorscales()
app = dash.Dash(__name__)

fig = px.bar(analise.sort_values(by="value", ascending=False),
             x="variable",
             y="value",
             color="variable",
             color_discrete_sequence=px.colors.qualitative.Vivid_r,
             text='value',
             text_auto=False)

fig.update_traces(texttemplate='%{text:.2s}', textposition='inside')

fig.update_layout(
    title="Análise",
    xaxis_title="Letra",
    yaxis_title="Soma",
    
)

# Creating the heatmap
fig2 = go.Figure(go.Heatmap(
    z=posicao_new.iloc[:, 1:],
    x=posicao_new.columns[1:],
    y=posicao_new['Letra'],
    colorscale="Viridis",
    colorbar=dict(title='Frequência')
))

# Adjusting the layout
fig2.update_layout(title='Mapa de Calor',
                   xaxis=dict(title='Posição', showgrid=True),
                   yaxis=dict(title='Letra', showgrid=True),
                   height=800,
                   width=800,                    
                   margin=dict(l=50, r=50, b=100, t=100)
                   )

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Graph(figure=fig),
    dcc.Graph(figure=fig2)
])

if __name__ == "__main__":
    app.run_server(debug=True)
