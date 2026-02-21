# Publish events when a booking is created

- here is the handler for booking creation
  `app.transport.grpc.handlers.booking_handler.BookingServiceHandler.CreateBooking`
- we need to publish an event when a booking is created
- event name should be `BookingCreated`
- add containers for kafka and zookeeper in docker-compose.yml
  example:

```yaml
  kafka:
    image: confluentinc/cp-kafka:7.2.1
    ports:
      - "9092:9092"
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka:9092
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
  zookeeper:
    image: confluentinc/cp-zookeeper:7.2.1
    ports:
      - "2181:2181"
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181
      ZOOKEEPER_TICK_TIME: 2000

```

- add new settings for kafka and zookeeper url and kafka topic name in `app.settings.py`
- take entity `app.domain.entities.booking.Booking` as a base and create a pydantic model for validation before publishing an event 
- use aiokafka package 