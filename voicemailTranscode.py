import boto3
from pprint import pprint

def utc_string(epoch_ms):
    from datetime import datetime as dt, timezone as tz

    # Create a datetime object in UTC
    utc_datetime = dt.fromtimestamp(epoch_ms / 1000, tz.utc)

    return utc_datetime.isoformat()


def lambda_handler(event, context):
    # Replace 'your-stream-name' and 'your-s3-bucket' with the actual names of your Kinesis Video Stream and S3 bucket
    stream_name = 'customconfigure-connect-customconfigure-contact-a925f374-8ab9-45bf-8b1d-7dabb97948e8'
    s3_bucket = 'your-s3-bucket'

    # Create a Kinesis Video client
    kvs_client = boto3.client('kinesisvideo')

    # Get the data endpoint for the stream
    endpoint = kvs_client.get_data_endpoint(
        StreamName=stream_name,
        APIName='LIST_FRAGMENTS'
    )['DataEndpoint']

    # Create a Kinesis Video archiver client
    kvs_archiver_client = boto3.client('kinesis-video-archived-media', endpoint_url=endpoint)

    # Specify the start and end timestamps for the desired time range
#    start_timestamp = utc_string(1707607329466)
    start_timestamp = utc_string(1707607330_466)
    end_timestamp =   utc_string(1707607345169)
    print(start_timestamp, end_timestamp)

    # Create a fragment selector for the specified time range
    fragment_selector = {
        'FragmentSelectorType': 'PRODUCER_TIMESTAMP',
        'TimestampRange': {
            'StartTimestamp': start_timestamp,
            'EndTimestamp': end_timestamp
        }
    }

    # Get the list of fragments within the specified time range
    list_fragments_response = kvs_archiver_client.list_fragments(
        StreamName=stream_name,
        FragmentSelector=fragment_selector
    )

    # Combine fragments into a single file
    combined_data = b''
    pprint(list_fragments_response)
    for fragment_info in list_fragments_response['Fragments']:
        fragment_number = fragment_info['FragmentNumber']

        # Get the fragment URL
        get_media_response = kvs_archiver_client.get_media(
            StreamName=stream_name,
            FragmentNumber=fragment_number
        )

        # Read the fragment data and append to the combined data
        fragment_data = get_media_response['Payload'].read()
        combined_data += fragment_data

    # Create an S3 client
    s3_client = boto3.client('s3')

    # Upload the combined data to S3
    s3_key = 'combined/combined.aac'
    s3_client.put_object(Body=combined_data, Bucket=s3_bucket, Key=s3_key)

    print("Combined fragments uploaded to S3")

    return {
        'statusCode': 200,
        'body': 'Fragments downloaded, combined, and uploaded to S3 successfully!'
    }
