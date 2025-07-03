
import pandas as pd
import os

# Get the directory of the script
SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))

# Load the datasets
predicted_population_df = pd.read_csv(os.path.join(SCRIPT_DIR, 'predicted_population.csv'))
ourworldindata_population_df = pd.read_csv(os.path.join(SCRIPT_DIR, 'population_data', 'ourworldindata_population_data.csv'))

# Get the historical data for the last 10 years (2014-2023)
historical_df = ourworldindata_population_df[ourworldindata_population_df['year'].between(2014, 2023)]

# Rename columns for consistency
historical_df = historical_df.rename(columns={'population': 'actual_population'})
predicted_population_df = predicted_population_df.rename(columns={'predicted_population': 'population'})

# Combine the historical and predicted data
# We need to make sure the columns align for a clean concatenation

# Reformat historical data to match the structure of the predicted data for concatenation
historical_to_concat = historical_df[['country', 'year', 'actual_population']].rename(columns={'actual_population': 'population'})

# Reformat predicted data
predicted_to_concat = predicted_population_df[['country', 'year', 'population']]

# Concatenate the two dataframes
combined_df = pd.concat([historical_to_concat, predicted_to_concat], ignore_index=True)

# Sort by country and year
combined_df = combined_df.sort_values(by=['country', 'year'])

# Save the results to a new CSV file
combined_df.to_csv(os.path.join(SCRIPT_DIR, 'population_comparison.csv'), index=False)

print("Population comparison data saved to population_comparison.csv")
