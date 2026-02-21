# Implement booking-history-service

## Task Description

In the `booking-service` `/Users/yalobur/projects/courses/yandex/mswa/msa-sprint2/tasks/task2/results/booking-service`
we publish `BookingCreated` event at `app/transport/grpc/handlers/booking_handler.py:58` after booking is created.
Example of the event:

```json
{
  "event_type": "BookingCreated",
  "data": {
    "id": "13",
    "user_id": "test-user-2",
    "hotel_id": "test-hotel-1",
    "price": 90.0,
    "promo_code": "TESTCODE1",
    "discount_percent": 10.0,
    "created_at": "2026-02-15T14:37:34.859067+00:00"
  }
}
```

Implement booking-history-service which consumes `BookingCreated` event and stores it in the database.

## Requirements

- Use the same project architechture/structure as in `booking-service` located in
  `/Users/yalobur/projects/courses/yandex/mswa/msa-sprint2/tasks/task2/results/booking-service`.
- Reuse what's implemented in `common` and `infrastructure` modules (and any other modules you think it is necessary).
