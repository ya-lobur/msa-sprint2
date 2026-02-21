# Логи booking-subgraph после тестовых запросов

```
booking-subgraph-1  | Enabling inline tracing for this subgraph. To disable, use ApolloServerPluginInlineTraceDisabled.
booking-subgraph-1  | ✅ Booking subgraph ready at http://localhost:4001/

# Первый запрос: без userid header (попытка 1)
booking-subgraph-1  | ❌ No userid header provided

# Второй запрос: без userid header (попытка 2)
booking-subgraph-1  | ❌ No userid header provided

# Третий запрос: с правильным userid (test-user-2)
booking-subgraph-1  | ✅ ACL passed: user test-user-2 accessing own bookings
booking-subgraph-1  | ✅ Retrieved 6 bookings for user test-user-2

# Четвертый запрос: с правильным userid (test-user-2)
booking-subgraph-1  | ✅ ACL passed: user test-user-2 accessing own bookings
booking-subgraph-1  | ✅ Retrieved 6 bookings for user test-user-2

# Пятый запрос: с правильным userid (test-user-2)
booking-subgraph-1  | ✅ ACL passed: user test-user-2 accessing own bookings
booking-subgraph-1  | ✅ Retrieved 6 bookings for user test-user-2

# Шестой запрос: с правильным userid (test-user-2)
booking-subgraph-1  | ✅ ACL passed: user test-user-2 accessing own bookings
booking-subgraph-1  | ✅ Retrieved 6 bookings for user test-user-2

# Седьмой запрос: попытка test-user-3 получить данные test-user-2 (ACL Deny)
booking-subgraph-1  | ❌ ACL denied: user test-user-3 tried to access bookings of test-user-2

# Восьмой запрос: без userid header
booking-subgraph-1  | ❌ No userid header provided
```

## Интерпретация логов:

1. **Запуск сервиса**: Сервис успешно запущен на порту 4001
2. **ACL работает корректно**:
    - Запросы без заголовка `userid` отклонены
    - Запросы с неправильным `userid` отклонены
    - Запросы с правильным `userid` успешно обработаны
3. **gRPC интеграция работает**: Успешно получены 6 бронирований из booking-service
4. **Логирование**: Все попытки доступа логируются с понятными сообщениями
