from flask import Flask, render_template, send_from_directory
import pandas as pd
from supabase_client import supabase

app = Flask(__name__)

# Define the path to the plot file
PLOT_FILE = 'newplot.png'

@app.route('/')
def index():
    # Fetch all countries
    countries_response = supabase.table('ourworldindata_population').select('country').execute()
    countries_df = pd.DataFrame(countries_response.data)
    countries = sorted(countries_df['country'].unique().tolist())

    # Fetch all data
    response = supabase.table('ourworldindata_population').select('*').execute()
    df = pd.DataFrame(response.data)
    data = df.to_html(classes='table table-striped', index=False)
    
    return render_template('index.html', data=data, countries=countries)

@app.route('/country/<country>')
def country_data(country):
    # Fetch all data from the table
    response = supabase.table('ourworldindata_population').select('*').execute()
    df = pd.DataFrame(response.data)

    # Get the list of all unique countries for the dropdown
    countries = sorted(df['country'].unique().tolist())

    # Filter the DataFrame to get data for the selected country
    country_df = df[df['country'] == country]
    data = country_df.to_html(classes='table table-striped', index=False)
    
    return render_template('index.html', data=data, countries=countries, selected_country=country)

@app.route('/plot')
def plot():
    return send_from_directory('.', PLOT_FILE)

if __name__ == '__main__':
    app.run(debug=True)