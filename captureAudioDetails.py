from json import dumps, loads
from time import time
from boto3 import client

QUEUE_URL = 'https://sqs.us-east-1.amazonaws.com/992382850243/customconfigure-connect-processvoicemail.fifo'

def lambda_handler(event, context):
#    print("Received event:", json.dumps(event))
#    print("Received context:", context)

    timestamp = int(time() * 1000)
    message_body = {
        'statusCode': 200,
        'timestamp': int(time() * 1000),
        'event': dumps(event)
    }

    # Create an SQS client
    sqs = client('sqs')

    # Send message to SQS queue
    response = sqs.send_message(
        QueueUrl=QUEUE_URL,
        MessageBody=dumps(message_body),
        MessageGroupId='my-group',  # Use a unique identifier for message grouping
        MessageDeduplicationId = str(timestamp)  # Use a unique identifier for deduplication
    )

    print(f"Message sent. MessageId: {response['MessageId']}")

    return message_body