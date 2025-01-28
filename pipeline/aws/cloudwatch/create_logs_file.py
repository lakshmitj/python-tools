import csv
import logging
import os

logger = logging.getLogger(__name__)

BASE_DIR = os.getcwd()

def save_to_csv(parsed_events, filename="output.csv"):
    """
    Save parsed log events to a CSV file.

    Args:
        parsed_events (list): List of dictionaries containing parsed log events.
        filename (str): Name of the CSV file to save the events to.
    """
    if not parsed_events:
        logger.error("No data to write to CSV.")
        return

    # Get the header from the first event (keys of the dictionary)
    fieldnames = parsed_events[0].keys()
    filepath = os.path.join(BASE_DIR, filename)

    try:
        # Open the CSV file in write mode
        with open(filepath, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            # Write the header (column names)
            writer.writeheader()

            # Write the rows (log events)
            writer.writerows(parsed_events)

        logger.info(f"Data successfully written to {filename}")
    except FileNotFoundError as e:
        logger.info(f"Could not find the {filename} file.\n")
    except Exception as e:
        logger.info(f"An error occurred while saving to CSV: {e}")

