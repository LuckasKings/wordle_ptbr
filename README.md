# "Termo" Analysis Project

This project was developed to analyze data from the game "Termo," the Portuguese version of the popular word-guessing game "Wordle." The provided code performs various data processing and visualization tasks to gain insights into the word dataset.

## Project Structure
The project consists of a Python script that uses several libraries, including Pandas, Plotly Express, Dash, and Plotly Graph Objects, to load, preprocess, and visualize data.

## Files
- dicionariousp.xlsx: This Excel file contains a list of Portuguese words.
## Code Explanation
1. Loading and Preprocessing Data:
- Reads the Excel file 'dicionariousp.xlsx' into a Pandas DataFrame, filtering words to have a length of 5 characters and converting all letters to lowercase.

2. Data Analysis:
- Creates five new columns ('1P' to '5P') to represent each position of the five-letter words.
- Creates columns for each letter of the alphabet, indicating whether the word contains that letter.
- Creates a new DataFrame (posicao) to store the count of each letter's position in the words.
- Merges and fills missing values for each position and letter in "posicao_new".

3. Visualization:

- Utilizes Plotly Express to create a bar chart (fig) displaying the frequency of each letter in the first position of the words.
- Uses Plotly Graph Objects to create a heatmap (fig2) representing the frequency of each letter in different positions of the words.

4. Dash Web Application:

- Initializes a Dash web application.
- Sets up two Dash graphs to display the previously created figures.

## How to Run

1. Ensure you have the required libraries installed by running:

``` pip install pandas openpyxl plotly dash ```


2. Execute the script using a Python interpreter:

``` python Termo.py ```
   
4. Open a web browser and go to http://127.0.0.1:8050/ to view the Dash web application.

## Additional Note:
The dictionary used in this project was provided by the Institute of Mathematics and Statistics (IME) at the University of São Paulo (USP).
