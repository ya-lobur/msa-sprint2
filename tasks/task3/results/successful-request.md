# Успешный вызов с правильным userid

## Команда:
```bash
curl -X POST http://localhost:4000/ \
  -H "Content-Type: application/json" \
  -H "userid: test-user-2" \
  -d '{"query":"query { bookingsByUser(userId: \"test-user-2\") { id hotel { city rating description } discountPercent } }"}'
```

## Ответ:
```json
{
  "data": {
    "bookingsByUser": [
      {
        "id": "22",
        "hotel": {
          "city": "Seoul",
          "rating": 4.7,
          "description": "Modern hotel in Seoul downtown with spa and skybar."
        },
        "discountPercent": 10
      },
      {
        "id": "23",
        "hotel": {
          "city": "Seoul",
          "rating": 4.7,
          "description": "Modern hotel in Seoul downtown with spa and skybar."
        },
        "discountPercent": 10
      },
      {
        "id": "25",
        "hotel": {
          "city": "Seoul",
          "rating": 4.7,
          "description": "Modern hotel in Seoul downtown with spa and skybar."
        },
        "discountPercent": 10
      },
      {
        "id": "26",
        "hotel": {
          "city": "Seoul",
          "rating": 4.7,
          "description": "Modern hotel in Seoul downtown with spa and skybar."
        },
        "discountPercent": 0
      },
      {
        "id": "27",
        "hotel": {
          "city": "Seoul",
          "rating": 4.7,
          "description": "Modern hotel in Seoul downtown with spa and skybar."
        },
        "discountPercent": 0
      },
      {
        "id": "28",
        "hotel": {
          "city": "Seoul",
          "rating": 4.7,
          "description": "Modern hotel in Seoul downtown with spa and skybar."
        },
        "discountPercent": 10
      }
    ]
  }
}
```

## Статус: ✅ Успешно
- Пользователь test-user-2 получил свои бронирования
- Данные об отелях загружены корректно
- ACL проверка пройдена
