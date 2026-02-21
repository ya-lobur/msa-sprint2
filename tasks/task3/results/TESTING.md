# Инструкция по тестированию

## Запуск окружения

### 1. Создать сеть Docker (если еще не создана)
```bash
docker network create hotelio-net
```

### 2. Запустить сервисы из Task 2 (monolith, booking-service, и др.)
```bash
cd tasks/task2
docker compose up -d
```

### 3. Запустить GraphQL сервисы (gateway и subgraphs)
```bash
cd tasks/task3
docker compose up -d --build
```

### 4. Проверить, что все контейнеры запущены
```bash
docker ps
```

Должны быть запущены:
- `task3-apollo-gateway-1` (порт 4000)
- `task3-booking-subgraph-1` (порт 4001)
- `task3-hotel-subgraph-1` (порт 4002)
- `hotelio-monolith` (порт 8084)
- `task2-booking-service-1` (порт 50051)

## Создание тестовых данных

### Создать бронирование через gRPC
```bash
cd tasks/task3/booking-subgraph
grpcurl -plaintext -proto booking.proto \
  -d '{"user_id": "test-user-2", "hotel_id": "test-hotel-1"}' \
  localhost:50051 booking.BookingService/CreateBooking
```

### Создать бронирование с промокодом
```bash
grpcurl -plaintext -proto booking.proto \
  -d '{"user_id": "test-user-2", "hotel_id": "test-hotel-1", "promo_code": "TESTCODE1"}' \
  localhost:50051 booking.BookingService/CreateBooking
```

## Тестирование GraphQL API

### 1. Успешный запрос с правильным userid

```bash
curl -X POST http://localhost:4000/ \
  -H "Content-Type: application/json" \
  -H "userid: test-user-2" \
  -d '{
    "query": "query { bookingsByUser(userId: \"test-user-2\") { id hotel { city rating description } discountPercent } }"
  }'
```

**Ожидаемый результат**: Возвращается список бронирований пользователя test-user-2

**Лог в booking-subgraph**:
```
✅ ACL passed: user test-user-2 accessing own bookings
✅ Retrieved X bookings for user test-user-2
```

### 2. ACL Deny: Попытка получить чужие бронирования

```bash
curl -X POST http://localhost:4000/ \
  -H "Content-Type: application/json" \
  -H "userid: test-user-3" \
  -d '{
    "query": "query { bookingsByUser(userId: \"test-user-2\") { id userId hotelId } }"
  }'
```

**Ожидаемый результат**: Возвращается пустой массив `[]`

**Лог в booking-subgraph**:
```
❌ ACL denied: user test-user-3 tried to access bookings of test-user-2
```

### 3. ACL Deny: Запрос без userid header

```bash
curl -X POST http://localhost:4000/ \
  -H "Content-Type: application/json" \
  -d '{
    "query": "query { bookingsByUser(userId: \"test-user-2\") { id userId hotelId } }"
  }'
```

**Ожидаемый результат**: Возвращается пустой массив `[]`

**Лог в booking-subgraph**:
```
❌ No userid header provided
```

## Тестирование через GraphQL Playground

1. Открыть в браузере: http://localhost:4000/
2. В секции "HTTP HEADERS" добавить:
```json
{
  "userid": "test-user-2"
}
```

3. Выполнить запрос:
```graphql
query {
  bookingsByUser(userId: "test-user-2") {
    id
    hotel {
      city
      rating
      description
    }
    discountPercent
  }
}
```

## Просмотр логов

### Логи booking-subgraph
```bash
docker compose logs booking-subgraph -f
```

### Логи hotel-subgraph
```bash
docker compose logs hotel-subgraph -f
```

### Логи gateway
```bash
docker compose logs apollo-gateway -f
```

### Логи всех сервисов
```bash
docker compose logs -f
```

## Остановка сервисов

```bash
# Остановить GraphQL сервисы
cd tasks/task3
docker compose down

# Остановить сервисы Task 2
cd ../task2
docker compose down
```

## Проверка работоспособности отдельных компонентов

### gRPC Booking Service
```bash
grpcurl -plaintext -proto booking.proto \
  -d '{"user_id": "test-user-2"}' \
  localhost:50051 booking.BookingService/ListBookings
```

### REST Monolith (Hotel API)
```bash
curl http://localhost:8084/api/hotels/test-hotel-1
```

### Booking Subgraph
```bash
curl -X POST http://localhost:4001/ \
  -H "Content-Type: application/json" \
  -H "userid: test-user-2" \
  -d '{"query":"query { bookingsByUser(userId: \"test-user-2\") { id userId } }"}'
```

### Hotel Subgraph
```bash
curl -X POST http://localhost:4002/ \
  -H "Content-Type: application/json" \
  -d '{"query":"query { hotelsByIds(ids: [\"test-hotel-1\"]) { id city rating } }"}'
```
