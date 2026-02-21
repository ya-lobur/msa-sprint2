# Task 3: Federated GraphQL API Implementation Report

## Описание внесённых изменений

### 1. Сервис booking-subgraph

**Файл:** `tasks/task3/booking-subgraph/index.js`

Изменения:

- Добавлены зависимости `@grpc/grpc-js` и `@grpc/proto-loader` для работы с gRPC
- Реализован gRPC клиент для подключения к booking-service (порт 50051)
- Добавлен proto файл `booking.proto` для определения gRPC интерфейса
- Реализован резолвер `bookingsByUser` с вызовом gRPC метода `ListBookings`
- **Реализован ACL (Access Control List):**
    - Проверяется заголовок `userid` из запроса
    - Пользователь может видеть только свои бронирования
    - Если `userid` не совпадает с запрашиваемым `userId`, возвращается пустой массив
    - Если заголовок отсутствует, доступ запрещён
- Добавлена связь с hotel-subgraph через поле `hotel` в типе `Booking`

**Файл:** `tasks/task3/booking-subgraph/package.json`

- Добавлены зависимости: `@grpc/grpc-js` и `@grpc/proto-loader`

### 2. Сервис hotel-subgraph

**Файл:** `tasks/task3/hotel-subgraph/index.js`

Изменения:

- Добавлена зависимость `node-fetch` для REST вызовов
- Реализован REST клиент для получения данных об отелях из monolith
- Обновлена GraphQL схема в соответствии с API монолита:
    - Убраны поля `name` и `stars` (отсутствуют в API)
    - Добавлены поля: `city`, `rating`, `description`, `operational`, `fullyBooked`
- Реализован метод `__resolveReference` для резолвинга ссылок на отели из booking-subgraph
- Реализован query `hotelsByIds` для получения нескольких отелей

**Файл:** `tasks/task3/hotel-subgraph/package.json`

- Добавлена зависимость: `node-fetch`

### 3. Сервис apollo-gateway

**Файл:** `tasks/task3/gateway/index.js`

Изменения:

- Добавлен класс `AuthenticatedDataSource`, расширяющий `RemoteGraphQLDataSource`
- Реализована передача всех HTTP заголовков из gateway в subgraph'ы
- Это обеспечивает передачу заголовка `userid` для работы ACL

### 4. Docker Compose конфигурация

**Файл:** `tasks/task3/docker-compose.yml`

Изменения:

- Добавлена внешняя сеть `hotelio-net` для всех сервисов
- Настроены environment переменные для каждого сервиса:
    - `booking-subgraph`: BOOKING_SERVICE_HOST и BOOKING_SERVICE_PORT
    - `hotel-subgraph`: HOTEL_SERVICE_URL
- Обеспечена связность с сервисами из task2 через общую сеть

## Архитектура решения

```
┌─────────────────┐
│  GraphQL Client │
└────────┬────────┘
         │ HTTP + userid header
         ▼
┌─────────────────┐
│ Apollo Gateway  │  (port 4000)
│  (Aggregates    │
│   subgraphs)    │
└────┬───────┬────┘
     │       │
     │       │ Forward headers
     ▼       ▼
┌─────────┐ ┌─────────────┐
│ Booking │ │   Hotel     │
│Subgraph │ │  Subgraph   │
│(4001)   │ │   (4002)    │
└────┬────┘ └──────┬──────┘
     │ gRPC        │ REST
     │             │
     ▼             ▼
┌─────────────┐ ┌──────────────┐
│  Booking    │ │   Hotelio    │
│  Service    │ │   Monolith   │
│  (50051)    │ │   (8080)     │
└─────────────┘ └──────────────┘
```

## Реализованные функции

### ACL (Access Control List)

- Реализована проверка на уровне booking-subgraph
- Используется заголовок HTTP `userid`
- Логирование всех попыток доступа:
    - ✅ ACL passed - успешная авторизация
    - ❌ ACL denied - отказ в доступе
    - ❌ No userid header - отсутствие заголовка

### Федеративный GraphQL

- Связь между Booking и Hotel через Federation
- Автоматическое резолвинг ссылок между subgraph'ами
- Единая точка входа через Gateway

## Технологии

- **Apollo Federation** - федеративная архитектура GraphQL
- **gRPC** - для связи booking-subgraph → booking-service
- **REST** - для связи hotel-subgraph → monolith
- **Docker & Docker Compose** - контейнеризация
- **Node.js 18** - runtime для всех GraphQL сервисов
