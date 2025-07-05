
from flask import Flask, render_template, redirect, url_for, send_from_directory
import pandas as pd
import os

# Import the analysis functions from your existing scripts
from population_predictor import main as predict_population
from population_comparison import main as compare_population

app = Flask(__name__)

# Define the path to the CSV file and the plot
CSV_FILE = 'population_comparison.csv'
PLOT_FILE = 'newplot.png'

@app.route('/')
def index():
    # Read the CSV data
    if os.path.exists(CSV_FILE):
        df = pd.read_csv(CSV_FILE)
        countries = df['country'].unique().tolist()
        data = df.to_html(classes='table table-striped', index=False)
    else:
        data = "No data available. Please run the analysis."
        countries = []
        
    return render_template('index.html', data=data, countries=countries)

@app.route('/country/<country>')
def country_data(country):
    # Read the CSV data
    if os.path.exists(CSV_FILE):
        df = pd.read_csv(CSV_FILE)
        countries = df['country'].unique().tolist()
        
        # Filter by country
        df_country = df[df['country'] == country]
        data = df_country.to_html(classes='table table-striped', index=False)
    else:
        data = "No data available. Please run the analysis."
        countries = []
        
    return render_template('index.html', data=data, countries=countries)

@app.route('/run-analysis')
def run_analysis():
    # Run the data fetching, prediction, and comparison scripts
    predict_population()
    compare_population()
    return redirect(url_for('index'))

@app.route('/plot')
def plot():
    return send_from_directory('.', PLOT_FILE)

if __name__ == '__main__':
    app.run(debug=True)
