import time
from get_latest_log_streams import get_latest_log_streams
from filter_log_events_model import grab_data
from create_logs_file import save_to_csv

def main():
    log_group_name = '/use1-prd-bssh-cluster/shwebproxy'
    log_stream_names = get_latest_log_streams(log_group_name, 1)
    print(f"Latest log streams:{log_stream_names}")
    
    filter_pattern='"use1-prd-bssh-cluster-shweb" "HTTP/1.1 404"'

    # Get logs from the last 24 hours
    end_time = int(time.time())  # Current time
    start_time = end_time - 86400  # 24 hours ago

    parsed_events = grab_data(log_group_name, log_stream_names, start_time, end_time, filter_pattern)
    save_to_csv(parsed_events, "parsed_event_logs_info.csv")

if __name__ == '__main__':
    main()