import requests
import csv
import json
import os
import time
from urllib.parse import urljoin

class PopulationDataFetcher:
    def __init__(self, output_dir="./population_data/"):
        self.output_dir = output_dir
        # Create output directory if it doesn't exist
        os.makedirs(self.output_dir, exist_ok=True)
    
    def fetch_world_bank_data(self):
        """
        Fetch World Bank population data and save directly to CSV
        """
        print("Fetching World Bank population data...")
        try:
            # World Bank API for population data
            url = "https://api.worldbank.org/v2/country/all/indicator/SP.POP.TOTL"
            params = {
                'format': 'json',
                'date': '1960:2023',
                'per_page': 20000
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            if len(data) > 1:
                # Prepare CSV file
                csv_filename = os.path.join(self.output_dir, "world_bank_population_data.csv")
                
                with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
                    fieldnames = ['country_code', 'country_name', 'year', 'population']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    
                    records_count = 0
                    for item in data[1]:  # Skip metadata
                        if item['value'] is not None:
                            writer.writerow({
                                'country_code': item['country']['id'],
                                'country_name': item['country']['value'],
                                'year': int(item['date']),
                                'population': int(item['value'])
                            })
                            records_count += 1
                
                print(f"World Bank data saved to {csv_filename}: {records_count} records")
                return csv_filename
            else:
                print("No data received from World Bank API")
                return None
                
        except Exception as e:
            print(f"Error fetching World Bank data: {e}")
            return None
    
    def fetch_ourworldindata_population(self):
        """
        Fetch Our World in Data population dataset and save to CSV
        """
        print("Fetching Our World in Data population data...")
        try:
            url = "https://ourworldindata.org/grapher/population.csv?v=1&csvType=full&useColumnShortNames=true"
            
            response = requests.get(url)
            response.raise_for_status()
            
            # Save directly to CSV with processed content
            csv_filename = os.path.join(self.output_dir, "ourworldindata_population_data.csv")
            
            # Process the CSV content
            lines = response.text.strip().split('\n')
            
            with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                
                # Write header with standardized names
                writer.writerow(['country', 'country_code', 'year', 'population'])
                
                records_count = 0
                for line in lines[1:]:  # Skip original header
                    parts = line.split(',')
                    if len(parts) >= 4 and parts[3].strip():  # Check if population data exists
                        try:
                            population = int(float(parts[3]))
                            writer.writerow([
                                parts[0].strip('"'),  # country
                                parts[1].strip('"'),  # country_code
                                int(parts[2]),         # year
                                population             # population
                            ])
                            records_count += 1
                        except (ValueError, IndexError):
                            continue  # Skip invalid rows
            
            print(f"Our World in Data saved to {csv_filename}: {records_count} records")
            return csv_filename
            
        except Exception as e:
            print(f"Error fetching Our World in Data: {e}")
            return None
    """
    Gapminder data fetching is currently commented out due to API changes. So data is directly downloaded from the URL.
    
    def fetch_gapminder_population(self):
        Fetch Gapminder population data and save to CSV
        print("Fetching Gapminder population data...")
        try:
            url = "http://gapm.io/dpop"
            
            response = requests.get(url)
            response.raise_for_status()
            
            csv_filename = os.path.join(self.output_dir, "gapminder_population_data.csv")
            
            # Process the CSV content
            lines = response.text.strip().split('\n')
            
            with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                
                # Write standardized header
                writer.writerow(['country_code', 'year', 'population'])
                
                records_count = 0
                for line in lines[1:]:  # Skip original header
                    parts = line.split(',')
                    if len(parts) >= 3 and parts[2].strip():  # Check if population data exists
                        try:
                            population = int(float(parts[2]))
                            writer.writerow([
                                parts[0].strip('"'),  # country_code (geo)
                                int(parts[1]),        # year (time)
                                population            # population_total
                            ])
                            records_count += 1
                        except (ValueError, IndexError):
                            continue  # Skip invalid rows
            
            print(f"Gapminder data saved to {csv_filename}: {records_count} records")
            return csv_filename
            
        except Exception as e:
            print(f"Error fetching Gapminder data: {e}")
            return None
     """
    def fetch_un_population_data(self):
        """
        Fetch UN World Population Prospects data and save to CSV
        Note: This downloads a direct CSV file from UN data portal
        """
        print("Fetching UN Population data...")
        try:
            # UN Population estimates CSV (alternative source)
            url = "https://population.un.org/wpp/Download/Files/1_Indicators%20(Standard)/CSV_Files/WPP2022_TotalPopulationBySex.csv"
            
            response = requests.get(url)
            response.raise_for_status()
            
            csv_filename = os.path.join(self.output_dir, "un_population_data.csv")
            
            # Process the CSV content
            lines = response.text.strip().split('\n')
            
            with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                
                # Write standardized header
                writer.writerow(['country_code', 'country_name', 'year', 'population'])
                
                records_count = 0
                # Find header indices (UN CSV has many columns)
                header = lines[0].split(',')
                
                for line in lines[1:]:  # Skip header
                    parts = [p.strip('"') for p in line.split(',')]
                    
                    if len(parts) > 10:  # UN CSV has many columns
                        try:
                            # Extract relevant data (adjust indices based on actual UN CSV structure)
                            country_code = parts[1]  # LocID
                            country_name = parts[2]  # Location
                            year = int(parts[4])     # Time
                            population = float(parts[7]) * 1000  # PopTotal (in thousands)
                            
                            if population > 0:
                                writer.writerow([
                                    country_code,
                                    country_name,
                                    year,
                                    int(population)
                                ])
                                records_count += 1
                        except (ValueError, IndexError):
                            continue  # Skip invalid rows
            
            print(f"UN data saved to {csv_filename}: {records_count} records")
            return csv_filename
            
        except Exception as e:
            print(f"Error fetching UN data: {e}")
            print("Falling back to World Bank data (same source)")
            return self.fetch_world_bank_data()
    
    def download_csv_directly(self, url, filename, column_mapping=None):
        """
        Generic method to download CSV directly from URL
        """
        try:
            response = requests.get(url)
            response.raise_for_status()
            
            csv_filename = os.path.join(self.output_dir, filename)
            
            with open(csv_filename, 'wb') as f:
                f.write(response.content)
            
            print(f"Downloaded {filename} successfully")
            return csv_filename
            
        except Exception as e:
            print(f"Error downloading {filename}: {e}")
            return None

# Usage example
def main():
    # Initialize the fetcher
    fetcher = PopulationDataFetcher("./population_data/")
    
    print("Starting data collection and saving to CSV files...\n")
    
    downloaded_files = []
    
    # Fetch World Bank data (most reliable)
    wb_file = fetcher.fetch_world_bank_data()
    if wb_file:
        downloaded_files.append(wb_file)
    time.sleep(1)  # Be nice to APIs
    
    # Fetch Our World in Data
    owid_file = fetcher.fetch_ourworldindata_population()
    if owid_file:
        downloaded_files.append(owid_file)
    time.sleep(1)
    
    # Fetch Gapminder data
    gapminder_file = fetcher.fetch_gapminder_population()
    if gapminder_file:
        downloaded_files.append(gapminder_file)
    time.sleep(1)
    
    # Fetch UN data
    un_file = fetcher.fetch_un_population_data()
    if un_file:
        downloaded_files.append(un_file)
    
    # Print summary
    print(f"\n=== DOWNLOAD COMPLETE ===")
    print(f"Successfully downloaded {len(downloaded_files)} CSV files:")
    for file in downloaded_files:
        file_size = os.path.getsize(file) / 1024  # Size in KB
        print(f"- {os.path.basename(file)} ({file_size:.1f} KB)")
    
    print(f"\nAll files saved in: {fetcher.output_dir}")
    
    return downloaded_files

# Additional utility functions for direct downloads
def download_eurostat_data():
    """
    Download Eurostat population data directly
    """
    print("Downloading Eurostat population data...")
    url = "https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/demo_pjan?format=TSV&compressed=true"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        with open("./population_data/eurostat_population_data.tsv", 'wb') as f:
            f.write(response.content)
        
        print("Eurostat data downloaded as TSV file")
        return "./population_data/eurostat_population_data.tsv"
        
    except Exception as e:
        print(f"Error downloading Eurostat data: {e}")
        return None

def download_all_sources():
    """
    Download from all available sources
    """
    # Run main download function
    main_files = main()
    
    # Download additional sources
    eurostat_file = download_eurostat_data()
    
    print("\n=== ALL DOWNLOADS COMPLETE ===")
    print("Available CSV files for analysis:")
    
    # List all CSV files in the directory
    data_dir = "./population_data/"
    if os.path.exists(data_dir):
        for file in os.listdir(data_dir):
            if file.endswith(('.csv', '.tsv')):
                file_path = os.path.join(data_dir, file)
                file_size = os.path.getsize(file_path) / 1024
                print(f"- {file} ({file_size:.1f} KB)")

# Run the data collection
if __name__ == "__main__":
    # Simple download
    fetcher = main()
    
    # Or download from all sources
    # download_all_sources()