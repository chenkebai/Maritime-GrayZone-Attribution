import zipfile
import csv
import io

ZIP_PATH = 'data/raw_ais/AIS_2024_01_19.zip'

try:
    with zipfile.ZipFile(ZIP_PATH, 'r') as z:
        csv_name = z.namelist()[0]
        print(f"Reading file: {csv_name}")
        
        with z.open(csv_name) as f:
            # Wrap the binary stream in a text wrapper
            wrapper = io.TextIOWrapper(f, encoding='utf-8')
            reader = csv.reader(wrapper)
            
            # Get the headers
            headers = next(reader)
            # Get the first data row
            first_row = next(reader)
            
        print("\n--- Column Headers Found ---")
        print(headers)
        print("\n--- First Row Sample ---")
        print(dict(zip(headers, first_row)))

except Exception as e:
    print(f"Error: {e}")