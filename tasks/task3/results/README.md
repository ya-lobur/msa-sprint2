# Task 3 Results

Этот каталог содержит результаты выполнения Task 3: Federated GraphQL API implementation.

## Содержание

1. **REPORT.md** - Отчёт о внесённых изменениях
    - Описание изменений в каждом сервисе
    - Архитектура решения
    - Реализованные функции
    - Технологический стек

2. **docker-ps.txt** - Результат команды `docker ps`
    - Список запущенных контейнеров
    - Статусы и порты

3. **successful-request.txt** - Пример успешного GraphQL запроса
    - Команда curl с правильным userid header
    - Полный JSON ответ
    - Подтверждение работы ACL

4. **acl-deny.txt** - Примеры отказа в доступе
    - Сценарий 1: Пользователь пытается получить чужие бронирования
    - Сценарий 2: Запрос без заголовка userid
    - Логи из booking-subgraph

5. **booking-subgraph-logs.txt** - Логи booking-subgraph после тестовых запросов
    - Все попытки доступа
    - ACL проверки
    - Результаты gRPC вызовов

6. **TESTING.md** - Полная инструкция по тестированию
    - Запуск окружения
    - Создание тестовых данных
    - Примеры всех типов запросов
    - Команды для просмотра логов

## Краткое резюме

### Что реализовано

✅ **Booking Subgraph**

- gRPC клиент для подключения к booking-service
- ACL на уровне резолвера (проверка userid header)
- Федеративная связь с hotel-subgraph

✅ **Hotel Subgraph**

- REST клиент для подключения к monolith
- __resolveReference для федерации
- Корректная схема, соответствующая API монолита

✅ **Apollo Gateway**

- Агрегация subgraph'ов
- Передача заголовков в subgraph'ы
- Единая точка входа на порту 4000

✅ **Docker & Networking**

- Общая сеть hotelio-net для всех сервисов
- Правильные environment переменные
- Связность между task2 и task3 сервисами

### Как проверить

1. Запустить сервисы:
   ```bash
   cd tasks/task2 && docker compose up -d
   cd ../task3 && docker compose up -d --build
   ```

2. Выполнить успешный запрос:
   ```bash
   curl -X POST http://localhost:4000/ \
     -H "Content-Type: application/json" \
     -H "userid: test-user-2" \
     -d '{"query":"query { bookingsByUser(userId: \"test-user-2\") { id hotel { city } discountPercent } }"}'
   ```

3. Проверить ACL (должен вернуть пустой массив):
   ```bash
   curl -X POST http://localhost:4000/ \
     -H "Content-Type: application/json" \
     -H "userid: test-user-3" \
     -d '{"query":"query { bookingsByUser(userId: \"test-user-2\") { id } }"}'
   ```

4. Посмотреть логи:
   ```bash
   docker compose logs booking-subgraph
   ```

## Технические детали

- **Node.js**: 18
- **Apollo Server**: 4.x
- **gRPC**: @grpc/grpc-js, @grpc/proto-loader
- **HTTP Client**: node-fetch
- **Ports**:
    - Gateway: 4000
    - Booking Subgraph: 4001
    - Hotel Subgraph: 4002
    - Booking Service (gRPC): 50051
    - Monolith (REST): 8084

## ACL Security

Реализована простая, но эффективная проверка доступа:

- Проверяется HTTP заголовок `userid`
- Пользователь видит только свои бронирования
- Попытки доступа к чужим данным логируются
- Отсутствие заголовка = отказ в доступе

## Архитектура

```
Client → Gateway (4000) → Booking Subgraph (4001) → gRPC → Booking Service (50051)
                       ↘ Hotel Subgraph (4002) → REST → Monolith (8084)
```

Все компоненты работают в единой Docker сети `hotelio-net`.
