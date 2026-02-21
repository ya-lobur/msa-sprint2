## Что нужно сделать

Ваша задача — завершить реализацию федеративного **GraphQL API** с тремя модулями.
Реализовать задания как можно проще

### 1. Сервис booking-subgraph

- Бронирования возвращаются по `userId`.
- Есть поля:
    - `id`
    - `userId`
    - `hotelId`
    - `promoCode`
    - `discountPercent`

Необходимо:

- заменить заглушки на реальные вызовы (например, к базе, REST, gRPC),
- реализовать **ACL**, чтобы пользователь мог видеть только свои бронирования.

### 2. Сервис hotel-subgraph

- Возвращает описание отелей.
- Используется для `hotel { ... }` внутри бронирования.
- Должен уметь обращаться к внешнему API или сервису.
- Должно быть разрешено `__resolveReference` через ID.

### 3. Сервис apollo-gateway

- Агрегирует схемы booking и hotel.
- Проксирует запросы к нужным подграфам.
- Если сервисы работают, менять это не надо.

## Подсказки по подготовке окружения

Ознакомьтесь с предложенной структурой.

Поднять сервис можно с помощью:

`docker compose up -d --build`

## Проверка корректности

Выполните следующий GraphQL-запрос через GraphQL Playground на:

`http://localhost:4000/`

```graphql
    query {
    bookingsByUser(userId: "user1") {
        id
        hotel {
            name
            city
        }
        discountPercent
    }
}
```

Можно запрашивать больше данных.

Перед этим добавьте заголовок:

`userid: user1`

Иначе данные не вернутся из-за ACL.

## Образ результата

### Структура проекта

```text
task3/
├── booking-subgraph/
│   ├── index.js               // TODO: заменить заглушки на вызовы
│   └── ...
├── hotel-subgraph/
│   ├── index.js               // TODO: заменить заглушки на вызовы
│   └── ...
├── apollo-gateway/
│   ├── index.js               // Gateway-конфигурация
│   └── ...
├── docker-compose.yml         // Запускает все 3 модуля
└── README.md                  
```

---

## Куда делать вызовы
Эти сервисы поднимаются тут `/Users/yalobur/projects/courses/yandex/mswa/msa-sprint2/tasks/task2/docker-compose.yml`
Обрати внимение на общую сеть, ее нужно будет также прописать в `/Users/yalobur/projects/courses/yandex/mswa/msa-sprint2/tasks/task3/docker-compose.yml`

### Для booking-subgraph

- grpc сервис для booking-subgraph
  `/Users/yalobur/projects/courses/yandex/mswa/msa-sprint2/tasks/task2/results/booking-service/app/transport/grpc/handlers/booking_handler.py`
- его README.md `/Users/yalobur/projects/courses/yandex/mswa/msa-sprint2/tasks/task2/results/booking-service/README.md`

### hotel-subgraph
- сами котнроллеры тут `/Users/yalobur/projects/courses/yandex/mswa/msa-sprint2/hotelio-monolith/src/main/java/com/hotelio/monolith/controller`
- еще примеры вызовов их тут `/Users/yalobur/projects/courses/yandex/mswa/msa-sprint2/test/regress.sh`


## Подсказки

- Все заголовки передаются из API Gateway в подграфы автоматически.
- Для реализации ACL проверяйте `req.headers['userid']` в резолверах.
- Если пользователь не авторизован, не возвращайте бронирование.
- При использовании реальных модулей не забудьте использовать одну и ту же сеть в Docker.

## Структура и содержание репозитория, в котором нужно сдать решение

находится тут `/Users/yalobur/projects/courses/yandex/mswa/msa-sprint2/tasks/task3/results/`
```text
task3/results/
├── Report с описанием внесённых изменений
├── Результат docker ps
├── Скриншот успешного вызова 
├── Скриншот Deny по ACL 
└── Логи booking-subgraph после двух запросов (или всех контейнеров через docker-compose up --build)
```