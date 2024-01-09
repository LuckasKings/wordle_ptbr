# Import libraries
import pandas as pd
import os
import plotly.express as px
from dash import Dash

# Load data
base = pd.read_excel('Termo\dicionariousp.xlsx', names=['dic'])

# Preprocess data
base = base[base['dic'].str.len() == 5]
base['dic'] = base['dic'].str.lower()

# Split words into letters
columns = ['1P', '2P', '3P', '4P', '5P']
numbers = list(range(5))
for column, number in zip(columns, numbers):
    base[column] = base['dic'].str[number]

# Count letter occurrences
letras = ['a', 'b', ..., 'z']
for letra in letras:
    base[letra] = base['dic'].str.contains(letra, regex=False)
    base[letra] = sum(base[letra])

# Prepare data for analysis
posicao = pd.DataFrame()
new_columns = []
for column in columns:
    new_columns.append(column + 'Letra')
    posicao[column] = pd.Series(base[column].value_counts().index.tolist())

# Create analysis DataFrame
del base['dic']
base.drop(columns, inplace=True, axis=1)
base = base.head(1)
pivot = {'pivot':['pivot']}
analise = pd.DataFrame(pivot)
analise = pd.concat([base, analise])
analise = analise.melt(id_vars='pivot')
del analise['pivot']
analise.dropna(inplace=True)
analise = analise.sort_values('value', ascending=False)

# Visualization
colorscales = px.colors.named_colorscales()
app = Dash(__name__)
fig = px.bar(analise.sort_values(by="value", ascending=False),
             x="variable",
             y="value",
             color="variable",
             color_discrete_sequence=px.colors.qualitative.Vivid_r,
             text="value")

fig.update_traces(texttemplate='%{text:.2s}', textposition='inside')

fig.update_layout(
    title="Análise",
    xaxis_title="Variável",
    yaxis_title="Valor",
    font=dict(
        family="Courier New, monospace",
        size=14,
        color="black"
    )
)

fig.show()
