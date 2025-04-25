# app.py
import os
import csv
from flask import Flask, render_template, request, flash

app = Flask(__name__)
# Required for flashing messages
app.secret_key = 'your_very_secret_key_2' # Change this

# Define the directory where your CSV files are stored
# Assuming they are in the same directory as app.py
CSV_DIRECTORY = os.path.dirname(os.path.abspath(__file__))

# --- Helper function to get available CSV files ---
def get_csv_files():
    """Returns a sorted list of .csv files in the CSV_DIRECTORY."""
    try:
        files = [f for f in os.listdir(CSV_DIRECTORY) if f.endswith('.csv')]
        files.sort() # Sort alphabetically
        return files
    except FileNotFoundError:
        return [] # Return empty list if directory doesn't exist

# --- Helper function to check if a row should be filtered ---
def should_display_row(row):
    """
    Checks if a row contains 'No product info found' in relevant columns.
    Returns True if the row should be displayed, False otherwise.
    Assumes row has at least 6 elements.
    """
    if len(row) < 6:
        return False # Don't display malformed rows

    # Check columns: Price (index 2), Rating (3), Review Title (4), Review Content (5)
    columns_to_check = [row[2], row[3], row[4], row[5]]

    # Check if the exact string "No product info found" is present in any of these columns
    if "No product info found" in columns_to_check:
        return False # Filter out this row

    return True # Keep this row

# --- Main route ---
@app.route('/', methods=['GET', 'POST'])
def index():
    data = None
    selected_filename = None
    error_message = None
    available_csv_files = get_csv_files() # Get list of CSVs for the dropdown

    if request.method == 'POST':
        selected_filename = request.form.get('selected_csv') # Get filename from dropdown

        if not selected_filename:
            flash('Please select a data file from the dropdown.', 'error')
        elif selected_filename not in available_csv_files:
             flash('Invalid file selected.', 'error') # Security check
        else:
            # Construct the full path to the selected file
            csv_filepath = os.path.join(CSV_DIRECTORY, selected_filename)

            try:
                raw_data = []
                with open(csv_filepath, mode='r', newline='', encoding='utf-8') as file:
                    reader = csv.reader(file)
                    # Optional: Skip header row if your CSVs have one
                    # try:
                    #     next(reader, None)
                    # except StopIteration:
                    #     pass # Handle empty file
                    
                    for row in reader:
                        # Basic validation: Ensure row has expected number of columns (6)
                        if len(row) == 6:
                            raw_data.append(row)
                        else:
                            print(f"Skipping malformed row in {selected_filename}: {row}")

                # --- Filtering step ---
                filtered_data = []
                for row in raw_data:
                    if should_display_row(row): # Use the helper function
                        filtered_data.append(row)
                # --- End filtering step ---

                if not filtered_data:
                    if raw_data:
                         error_message = f"All displayable entries in '{selected_filename}' contained 'No product info found' in key fields and were filtered out."
                    else:
                         error_message = f"CSV file '{selected_filename}' is empty or contains only malformed rows."
                    flash(error_message, 'warning')
                else:
                     data = filtered_data # Assign FILTERED data

            except FileNotFoundError: # Should not happen if selected from list, but good practice
                 error_message = f"Selected data file '{selected_filename}' not found. This should not happen."
                 flash(error_message, 'error')
            except Exception as e:
                 error_message = f"An error occurred reading {selected_filename}: {str(e)}"
                 flash(error_message, 'error')
                 print(f"Error reading {selected_filename}: {e}")

    # Pass available files, selected file, and data to the template
    return render_template('index.html',
                           csv_files=available_csv_files,
                           selected_file_display_name=selected_filename, # Pass the name for display
                           data=data)

if __name__ == '__main__':
    # Check if any CSV files were found on startup
    if not get_csv_files():
        print("\nWARNING: No .csv files found in the application directory.")
        print(f"Please ensure your scraper has run and CSV files are located in: {CSV_DIRECTORY}\n")
    app.run(debug=True)