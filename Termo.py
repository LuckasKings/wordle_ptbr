import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

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

#The dataframe will have '1PLetra' for the index(letter) and the '1P' containing the corresponding value.

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

#############################################################################################

# analise.sort_values('value', ascending=False, inplace=True)
# analise = analise.head(12)
# x = analise['variable']
# y = analise['value']
#
#
# plt.style.use('seaborn-pastel')
# plt.bar(x, y)
# plt.show()

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


# writer = pd.ExcelWriter('termo.xlsx', engine='xlsxwriter')
# posicao.to_excel(writer, sheet_name='Analise', index=False, header=True, startrow=0)
# analise.to_excel(writer, index=False, sheet_name='Base', header=True, startrow=0)
# writer.save()
# os.startfile('termo.xlsx')