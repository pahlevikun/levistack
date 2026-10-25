# Event streams and queues

For async failures: a consumer that fell behind, a message that kept failing, an event that was never sent.

## Where it lives

Kafka (and Redpanda, Confluent), RabbitMQ, Google Pub/Sub, AWS SQS and SNS, NATS, and background job queues (Sidekiq, Oban, Celery, BullMQ).

## How to search it

Read-only. Never produce, purge, reset offsets or move messages.

```bash
# Kafka: consumer lag per partition
kafka-consumer-groups --bootstrap-server <host> --describe --group <group>

# Kafka: read a few messages around an offset without committing (kcat)
kcat -b <host> -t <topic> -C -o <offset> -c 5 -e

# RabbitMQ: queue depth and consumers
rabbitmqctl list_queues name messages consumers

# SQS: queue depth and the dead-letter queue
aws sqs get-queue-attributes --queue-url <url> --attribute-names All
```

1. **Lag and depth** around the incident window: a growing lag means the consumer is slow or stuck.
2. **The dead-letter queue**: messages that failed too often. Read a few, and group them by error.
3. **One message end to end**: find it by key or id, then follow it to the consumer's logs.
4. **The schema**: a changed event schema (in a schema registry or the producer's code) can break consumers silently.

## What good evidence looks like

- Lag that starts growing at a deploy of the consumer
- A dead-letter queue full of one error type
- A producer change that renamed a field the consumer reads

## Pitfalls

- **Reading can commit.** Some consumers commit offsets when they read. Use a tool or a flag that does not join the real consumer group.
- **Retention.** Old messages are gone. Note the retention time.
- **Personal data** in payloads. Quote only the fields that matter, masked.

## What to return

Topic or queue, group or consumer, the command, lag or depth over time, dead-letter counts by error, and any message keys you followed (masked).
