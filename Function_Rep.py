# Define the function to find the most recent .csv file
def find_most_recent_csv_file(directory):
    # Create a pattern for .csv files
    pattern = os.path.join(directory, '*.csv')
    # Find all files in the directory that match the pattern
    csv_files = glob.glob(pattern)
    # If no files found, return None
    if not csv_files:
        return None
    # Find the most recent file based on last modification time
    most_recent_file = max(csv_files, key=os.path.getmtime)
    # Return the full path to the most recent file
    return most_recent_file