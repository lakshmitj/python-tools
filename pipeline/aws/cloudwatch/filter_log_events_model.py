import boto3
import botocore 
import re
from urllib.parse import urlparse
import logging

# Set up basic logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# your function to parse the event.
def parse_event(event):
    pass

parsed_events = []

def parse_log_entry(log_message):
    # Define regex pattern
    pattern = (r'\[(?P<timestamp>[^\]]+)]\s+'       # Timestamp in brackets
           r'(?P<remote_addr>[\d\.]+)\s+-\s+'    # Remote address
           r'[\S]+\s+[\S]+\s+'                   # Hostname (ignored)
           r'upstream_name:\s[\S]+\s+'           # Upstream name (ignored)
           r'(?P<server_ip>[\d\.]+):\d+:\s+'     # Server IP (ignored)
           r'(?P<request_type>GET|POST|PUT|DELETE|PATCH)\s+'  # HTTP method
           r'(?P<location>/[^\s]+)\s+'           # URL path
           r'(?P<protocol>HTTP/\d\.\d)\s+'       # Protocol
           r'(?P<response_code>\d+)\s+'          # Response code
           r'(?P<body_bytes_sent>\d+)\s+'        # Bytes sent
           r'(?P<referrer>https?://[^\s]+)\s+'   # Referrer URL
           r'(?P<user_agent>.*)')                # User agent (remaining text)

    # Match the pattern
    match = re.search(pattern, log_message)
    if match:
        log_data = match.groupdict()
        return log_data
    else:
        return None


# my solution:
def grab_data(log_group_name,
              list_log_stream,
              start_time,
              end_time,
              filter_pattern):
    """
    Fetch log events from AWS CloudWatch Logs.

    Args
    ----
        aws_region (str): AWS region.
        aws_access_key_id (str): AWS access key ID.
        aws_secret_access_key (str): AWS secret access key.
        log_group_name (str): Name of the log group.
        list_log_stream (list): List of log stream names.
        start_time (int): Start time for log event retrieval in milliseconds.
        end_time (int): End time for log event retrieval in milliseconds.
        filter_pattern (str): Pattern to filter log events.

    Returns
    -------
        list: List of strings representing parsed log events.
    """
    session = boto3.Session(profile_name='illumina-basespace-prod')    
    client = boto3.client(service_name='logs', 
        region_name=session.region_name, 
        aws_access_key_id=session.get_credentials().access_key, 
        aws_secret_access_key=session.get_credentials().secret_key, 
        aws_session_token=session.get_credentials().token)
   
    rows = []
    next_token = {}
    
     # Convert start_time and end_time to milliseconds if provided
    if start_time:
        start_time = int(start_time * 1000)
    if end_time:
        end_time = int(end_time * 1000)
        
    while True:
        try:
            response = client.filter_log_events(
                logGroupName=log_group_name,
                logStreamNames=list_log_stream,
                startTime=start_time,
                endTime=end_time,
                filterPattern=filter_pattern,
                **next_token
            )
        except botocore.exceptions.ClientError as ex:
            logger.error(f"ClientError occurred: {ex}")
            return []  # Returning empty list on error
        except botocore.exceptions.UnauthorizedSSOTokenError:
            logger.error(f"UnauthorizedSSOTokenError occurred: {ex}")
            return []  # Returning empty list on error
        except Exception as ex:
            # Catching any other exceptions (network, value errors, etc.)
            logger.error(f"An unexpected error occurred: {ex}")
            return []  # Return empty list or handle accordingly
        
        try:
            # Parse each event's message
            for event in response['events']:
                log_message = event['message']
                parsed_event = parse_log_entry(log_message)
                if parsed_event:
                    rows.append(parsed_event)
        except KeyError as ex:
            logger.error(f"KeyError: Missing expected field {ex} in the response.")
        except Exception as ex:
            logger.error(f"Error parsing log event: {ex}")
        
        # Handle pagination
        if 'nextToken' not in response:
            break
        next_token = {'nextToken': response['nextToken']}
        
    return rows