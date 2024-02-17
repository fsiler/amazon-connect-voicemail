# Voicemail for Amazon Connect
This seems like a pretty major oversight, and AWS discontinued a codebase that did support this feature.
This is super duper alpha, not recommended, just a pet project.

## Components
- Amazon Connect
- SQS
- Lambda
- S3
- Kinesis Video Stream

## Architecture
```mermaid
graph LR
  c [Amazon Connect]
  cq [Monitored Connect Queue]
  el [Enqueue Lambda]
  pl [Processing Lambda]
  sq [SQS Queue]
  v  [Kinesis Video Stream]
```
