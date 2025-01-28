import logging
import re
import pandas as pd

logger = logging.getLogger(__name__)

def get_unique_location_from_parsed_events(column_name='location'):
        
    logger.info("Processing data started")

    # List of CSV file names
    csv_files = ["parsed_event_logs_info_2025-01-21.csv", 
                "parsed_event_logs_info_2025-01-22.csv",
                "parsed_event_logs_info_2025-01-23.csv",
                "parsed_event_logs_info_2025-01-24.csv",
                "parsed_event_logs_info_2025-01-25.csv",
                "parsed_event_logs_info_2025-01-26.csv",
                "parsed_event_logs_info_2025-01-27.csv"
                ]

    # Column name to extract unique values from
    # column_name = "location"

    # Set to store unique values across all files
    unique_values = set()

    # Read each file and collect unique values
    for file in csv_files:
        try:
            df = pd.read_csv(file)  # Read the file
            if column_name in df.columns:
                unique_values.update(df[column_name].dropna().unique())  # Add unique values, ignoring NaN
            else:
                logger.warning(f"Warning: Column '{column_name}' not found in {file}")
        except Exception as e:
            logger.error(f"Error reading {file}: {e}")
            logger.info("Exit program.\n Bye!")
            exit(1)

    logger.info("Processing Unique values across all files completed")
    return unique_values
    
    
# Function to extract leading number
def extract_and_remove_leading_number(value):
    match = re.match(r"\d+$", value)  # Match numbers at the start
    leading_number = match.group() if match else None  # Extract the leading number
    if leading_number:
        cleaned_value = value[len(leading_number):]  # Remove the leading number
    else:
        cleaned_value = value
    return leading_number, cleaned_value

def remove_ids_from_url(url):
    """
    Removes numeric IDs from the URL after the '/project' part and captures the removed IDs.
    
    Parameters:
    url (str): The URL to be cleaned.

    Returns:
    tuple: (cleaned_url, removed_ids)
            cleaned_url (str): The URL with IDs removed.
            removed_ids (list): A list of captured numeric IDs.
    """
    
    cleaned_url, removed_query_params = remove_and_capture_query_params(url)
    # Capture all numeric IDs in the URL
    removed_ids = re.findall(r"/\d+", cleaned_url)
    
    # Remove the captured numeric IDs from the URL
    cleaned_url = re.sub(r"/\d+", "", cleaned_url)
    
    # Return cleaned URL and list of removed IDs
    return cleaned_url, removed_query_params, removed_ids

def remove_query_params(url):
    """
    Removes the query parameters from the URL.

    Parameters:
    url (str): The URL from which query parameters need to be removed.

    Returns:
    str: The URL without query parameters.
    """
    cleaned_url = re.sub(r"\?.*", "", url)  # Remove the query parameters
    return cleaned_url

# Example usage
url = "/api/sample/file?limit=25&offset=0&sortBy=name&sortDir=desc"
cleaned_url = remove_query_params(url)



def remove_and_capture_query_params(url):
    """
    Removes query parameters from the URL and captures them.

    Parameters:
    url (str): The URL with query parameters.

    Returns:
    tuple: (cleaned_url, query_params)
           cleaned_url (str): The URL without query parameters.
           query_params (str or None): The removed query parameters (without '?').
    """
    match = re.search(r"\?(.*)", url)  # Find query parameters after '?'
    
    if match:
        query_params = match.group(1)  # Extract query parameters without '?'
        cleaned_url = re.sub(r"\?.*", "", url)  # Remove query parameters from URL
    else:
        query_params = None
        cleaned_url = url  # No change if there are no query parameters

    return cleaned_url, query_params

def generate_unique_paths():
    
    column_name = "location"
    file_name = "unique_location_values.csv"
    unique_values = get_unique_location_from_parsed_events(column_name)
    if unique_values:
        logger.info(f"Remove query params and leading numbers")
        # Convert the set to a DataFrame
        df = pd.DataFrame({"Original_Path": list(unique_values)})

        # Apply function to remove query params and leading numbers
        df[["Cleaned_Path", "Removed_Query_Params", "Removed_Leading_Numbers"]] = df["Original_Path"].apply(
            lambda x: pd.Series(remove_ids_from_url(x))
        )
    
        # Export to a CSV file
        logger.info(f"Export to {file_name} file")
        df.to_csv(file_name, index=False)
        logger.info(f"Unique values exported to {file_name} file")
  