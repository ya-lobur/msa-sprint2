# ACL Deny - Отказ в доступе

## Сценарий 1: Пользователь пытается получить чужие бронирования

### Команда:

```bash
curl -X POST http://localhost:4000/ \
  -H "Content-Type: application/json" \
  -H "userid: test-user-3" \
  -d '{"query":"query { bookingsByUser(userId: \"test-user-2\") { id userId hotelId promoCode discountPercent hotel { city rating } } }"}'
```

### Ответ:

```json
{
  "data": {
    "bookingsByUser": []
  }
}
```

### Лог в booking-subgraph:

```
❌ ACL denied: user test-user-3 tried to access bookings of test-user-2
```

### Статус: ❌ Доступ запрещён

- Пользователь test-user-3 попытался получить бронирования пользователя test-user-2
- ACL проверка не пройдена
- Возвращён пустой массив

---

## Сценарий 2: Запрос без заголовка userid

### Команда:

```bash
curl -X POST http://localhost:4000/ \
  -H "Content-Type: application/json" \
  -d '{"query":"query { bookingsByUser(userId: \"test-user-2\") { id userId hotelId } }"}'
```

### Ответ:

```json
{
  "data": {
    "bookingsByUser": []
  }
}
```

### Лог в booking-subgraph:

```
❌ No userid header provided
```

### Статус: ❌ Доступ запрещён

- Заголовок userid не предоставлен
- ACL проверка не пройдена
- Возвращён пустой массив
