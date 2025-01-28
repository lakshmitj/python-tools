import logging
import boto3
from datetime import datetime, timedelta, timezone
from create_logs_file import save_to_csv

logger = logging.getLogger(__name__)

def get_log_streams_by_day(log_group_name, start_time, end_time):
    """
    Retrieves log streams for a specific date.
    
    :param log_group_name: CloudWatch Log Group name
    :param target_date: Date (YYYY-MM-DD) for which log streams are needed
    :return: List of log stream names
    """
    logger.info("Processing data started")

    # Create a CloudWatch Logs client
    session = boto3.Session(profile_name='illumina-basespace-prod')    
    client = boto3.client(service_name='logs', 
            region_name=session.region_name, 
            aws_access_key_id=session.get_credentials().access_key, 
            aws_secret_access_key=session.get_credentials().secret_key, 
            aws_session_token=session.get_credentials().token)

    log_stream_names = []
    next_token = None
    while True:
        
        params = {
            'logGroupName': log_group_name,
            'orderBy': 'LastEventTime',
            'descending': True,
        }
        if next_token:
            params['nextToken'] = next_token

        response = client.describe_log_streams(**params)

        for stream in response.get('logStreams', []):
            last_event_timestamp = stream.get('lastEventTimestamp')  # Timestamp in milliseconds
            if last_event_timestamp:
                if start_time <= last_event_timestamp and last_event_timestamp < end_time:
                    log_stream_names.append(stream['logStreamName'])

        # Handle pagination
        next_token = response.get('nextToken')
        if not next_token:
            break
        
    logger.info(f"Data processing complete. Total log streams:{len(log_stream_names)}")
    return log_stream_names