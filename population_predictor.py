
import pandas as pd
import os

# Get the directory of the script
SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))

# Load the datasets
population_df = pd.read_csv(os.path.join(SCRIPT_DIR, 'population_data', 'ourworldindata_population_data.csv'))
tfr_df = pd.read_csv(os.path.join(SCRIPT_DIR, 'population_data', 'tfr_countries.csv'))

# Get the most recent population data
population_2023 = population_df[population_df['year'] == 2023]

# Get the TFR data for 2022 and 2023
tfr_2022 = tfr_df[tfr_df['year'] == 2022]
tfr_2023 = tfr_df[tfr_df['year'] == 2023]

# Merge the TFR data to calculate the rate of change
tfr_change = pd.merge(tfr_2022, tfr_2023, on='geo', suffixes=('_2022', '_2023'))
tfr_change['tfr_change_rate'] = tfr_change['Babies per women_2023'] - tfr_change['Babies per women_2022']

# Predict the TFR for the next 10 years
predicted_tfr = []
for index, row in tfr_change.iterrows():
    for year_offset in range(1, 11):
        predicted_tfr.append({
            'geo': row['geo'],
            'year': 2023 + year_offset,
            'predicted_tfr': row['Babies per women_2023'] + (row['tfr_change_rate'] * year_offset)
        })

predicted_tfr_df = pd.DataFrame(predicted_tfr)

# Predict the population for the next 10 years iteratively
predicted_population = []
for index, row in population_2023.iterrows():
    country_code_lower = str(row['country_code']).lower()
    country_tfr = predicted_tfr_df[predicted_tfr_df['geo'].str.lower() == country_code_lower]
    
    if not country_tfr.empty:
        current_population = row['population']
        for i, tfr_row in country_tfr.iterrows():
            # A more realistic, but still simple, growth model
            growth_rate = (tfr_row['predicted_tfr'] - 2.1) / 100.0
            future_population = current_population * (1 + growth_rate)
            
            predicted_population.append({
                'country': row['country'],
                'country_code': row['country_code'],
                'year': tfr_row['year'],
                'predicted_population': future_population
            })
            current_population = future_population # Update for next iteration

predicted_population_df = pd.DataFrame(predicted_population)

# Save the results to a CSV file
predicted_population_df.to_csv(os.path.join(SCRIPT_DIR, 'predicted_population.csv'), index=False)

print("Predicted population data saved to predicted_population.csv")
