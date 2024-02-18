# Voicemail for Amazon Connect
This seems like a pretty major oversight, and AWS discontinued a codebase that did support this feature.
This is super duper alpha, not recommended, just a pet project.

## Components
- Amazon Connect
- Kinesis Video Stream
- SQS
- Lambda
- S3

## Architecture
```mermaid
sequenceDiagram
  actor c as Caller
  participant ac as Amazon Connect
  participant q as Amazon Connect Call Queue
  participant v as Kinesis Video Stream
  participant SQS
  participant S3
  c-)ac: incoming call
  ac->>q: Connect Flow:<br />transfer to Connect queue
  q->>v: Connect Flow:<br />begin media stream
  q->>c: Caller hangs up
  q->>SQS: Lambda:<br />record audio details
  par Lambda
    SQS->>S3: Receive SQS trigger
  and
      v->>S3: Fetch, transcode, deposit audio
  end
```

## Problem space
Amazon Connect is a pretty powerful system.
But it's designed for interactive sessions, and not really built as a generalized phone system.

The call recording feature records only when an agent is talking with a caller- so it can be used for outbound calling and for when someone picks up a queue.
However, in order to record voicemail, we have to abuse the media streaming features of Amazon Connect.
The media streaming features only function within queues, so you must first send the call to a queue and enable the Connect [start media streaming](https://docs.aws.amazon.com/connect/latest/adminguide/start-media-streaming.html).


## Required setup
1. Amazon Connect