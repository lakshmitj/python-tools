import boto3

def get_latest_log_streams(log_group_name, log_stream_limit=10):
   # Create a CloudWatch Logs client
    session = boto3.Session(profile_name='illumina-basespace-prod')    
    client = boto3.client(service_name='logs', 
            region_name=session.region_name, 
            aws_access_key_id=session.get_credentials().access_key, 
            aws_secret_access_key=session.get_credentials().secret_key, 
            aws_session_token=session.get_credentials().token)

    # Fetch log streams sorted by last event time (latest first)
    response = client.describe_log_streams(
        logGroupName=log_group_name,
        orderBy='LastEventTime',
        descending=True,
        limit=log_stream_limit  # Fetch a few 
    )

    latest_log_stream = []
    for stream in response.get('logStreams', []):
        if stream:
            latest_log_stream.append(stream['logStreamName'])

    # return None  # No matching log stream found
    return latest_log_stream
