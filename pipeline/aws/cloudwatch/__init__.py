import logging
from logging_config import setup_logging
import datetime
from get_latest_log_streams import get_latest_log_streams
from filter_log_events_model import get_log_event_data
from create_logs_file import save_to_csv
from get_log_streams_by_day import get_log_streams_by_day
from datetime import datetime, timezone, timedelta
from unique_path import generate_unique_paths


setup_logging()
logger = logging.getLogger(__name__)  # Create a logger for this module


def get_start_and_end_time(date_str):
    """Returns the start and end time of a given date in UTC."""

    # Convert the date string to a datetime object
    date = datetime.strptime(date_str, "%Y-%m-%d").date()
    # Get the start time in UTC
    start_time = datetime.combine(date, datetime.min.time()).replace(tzinfo=timezone.utc)
    # Get the end time in UTC
    end_time = datetime.combine(date, datetime.max.time()).replace(tzinfo=timezone.utc)
    
     # Convert to timestamps in milliseconds
    start_timestamp_ms = int(start_time.timestamp() * 1000)
    end_timestamp_ms = int(end_time.timestamp() * 1000)

    logger.info(f"Start of day (UTC) in milliseconds:{start_timestamp_ms}")
    logger.info(f"End of day (UTC) in milliseconds:{end_timestamp_ms}")

    return start_timestamp_ms, end_timestamp_ms

def get_Filtered_Event_logs_per_day():
    date_str = input("Enter target date (YYYY/MM/DD)):")
    start_timestamp_ms, end_timestamp_ms = get_start_and_end_time(date_str)

    log_group_name = '/use1-prd-bssh-cluster/shwebproxy'
    filter_pattern='"use1-prd-bssh-cluster-shweb" -"HTTP/1.1 404"'
    
    # Set file name
    # Convert string to datetime
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")  
    file_name = f"parsed_event_logs_info_{date_obj.strftime('%Y-%m-%d')}.csv"
    logger.info(f"Parsed event logs file name:{file_name}")

    log_stream_names = get_log_streams_by_day(log_group_name, start_timestamp_ms, end_timestamp_ms)
    parsed_events = get_log_event_data(log_group_name, log_stream_names, start_timestamp_ms, end_timestamp_ms, filter_pattern)
    save_to_csv(parsed_events, file_name)
    

def display_menu():
    print("COMMAND MENU")
    print("1. Generate Filtered Event log files per Day")
    print("2. Parse url path")
    print("3. Exit program")
    print()

def main():
    logger.info("\nProgram started...\n")
    display_menu()
    while(True):
        command = int(input("Enter command:"))
        if command == 1:
            get_Filtered_Event_logs_per_day()
        if command == 2:
            generate_unique_paths()
        elif command == 3:
            logger.info("Exit program.\n Bye!")
            break
        else:
            logger.info("This is not a valid command. Please try again.")
   

if __name__ == '__main__':
    main()