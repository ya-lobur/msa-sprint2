# Отчёт по Заданию 5: Настройка управления трафиком с Istio

## Описание изменений

### 1. Установка и настройка Istio

- Установлен Istio с профилем demo: `istioctl install --set profile=demo -y`
- Включена автоматическая инъекция Envoy sidecar в namespace `default`
- Все поды booking-service получили Istio sidecar контейнеры (istio-proxy)
- Включить injection `kubectl label namespace default istio-injection=enabled --overwrite`

### 2. Создание двух версий сервиса

#### Изменения в коде (booking-service/main.go):
- Добавлена поддержка переменной окружения `VERSION` (v1/v2)
- Реализована логика обработки заголовка `X-Feature-Enabled: true`
- Версия v2 при включенном фича-флаге возвращает расширенный ответ с новыми возможностями
- Эндпоинт `/ping` теперь возвращает версию сервиса для тестирования

#### Helm конфигурация:
- **values-v1.yaml**: Основная версия с 2 репликами, VERSION=v1, ENABLE_FEATURE_X=false
- **values-v2.yaml**: Новая версия с 1 репликой, VERSION=v2, ENABLE_FEATURE_X=true
- Обновлены Helm templates для поддержки version labels (необходимо для Istio субсетов)
- Создан общий сервис `booking-service.yaml` для обеих версий

### 3. Настройка Istio маршрутизации

#### VirtualService (virtual-service.yaml):
- **Канареечный Release**: 90% трафика на v1, 10% на v2
- **Feature Flag маршрут**: При заголовке `X-Feature-Enabled: true` весь трафик направляется на v2 (приоритет выше канареечного)
- **Retry политика**: 3 попытки с таймаутом 2s на каждую, повтор при 5xx ошибках
- **Mirror трафика**: Копирование трафика на v2 для тестирования

#### DestinationRule (destination-rule.yaml):
- **Circuit Breaking**:
  - Максимум 100 TCP соединений
  - 50 ожидающих HTTP/1.1 запросов
  - 100 одновременных HTTP/2 запросов
- **Outlier Detection**:
  - 3 последовательные ошибки для изоляции
  - Интервал проверки 30s
  - Время изоляции 30s
  - Максимум 50% подов могут быть изолированы
- Настроены субсеты для v1 и v2 на основе version labels

#### EnvoyFilter (envoy-filter.yaml):
- Добавлен Lua фильтр для обработки заголовка `X-Feature-Enabled`
- Логирование запросов с включенным фича-флагом

### 4. CI/CD конфигурация

Обновлён `.gitlab-ci.yml` для поддержки Istio:
- Деплой общего сервиса booking-service
- Установка обеих версий через Helm с разными values файлами
- Применение всех Istio конфигураций (DestinationRule, VirtualService, EnvoyFilter)
- Проверка статуса развертывания обеих версий

### 5. Тестирование

Созданы скрипты для проверки:
- `check-istio.sh` - проверка установки Istio и инъекции sidecar
- `check-canary.sh` - тестирование распределения трафика (90/10)
- `check-fallback.sh` - тестирование отказоустойчивости при падении v1
- `check-feature-flag.sh` - проверка маршрутизации через фича-флаг

## Результаты тестирования

### Канареечное развертывание:
- При 100 запросах: 87% на v1, 13% на v2 ✓
- Распределение близко к заданному 90/10

### Feature Flag маршрутизация:
- При заголовке `X-Feature-Enabled: true`: 100% запросов на v2 ✓
- Без заголовка: используется канареечное распределение

### Istio компоненты:
- Версия Istio: 1.29.0
- Количество прокси в data plane: 5 (2x v1 + 1x v2)
- Все поды имеют 2 контейнера: приложение + istio-proxy

## Структура результатов

```
task5/results/
├── report.md                    # Данный отчет
├── values-v1.yaml              # Helm values для v1
├── values-v2.yaml              # Helm values для v2
├── booking-service.yaml        # Общий Service для обеих версий
├── virtual-service.yaml        # Istio VirtualService (канареечный + feature flag)
├── destination-rule.yaml       # Istio DestinationRule (retry + circuit breaking)
├── envoy-filter.yaml           # EnvoyFilter для фича-флагов
└── test-logs.txt               # Логи тестирования
```

## Команды для развертывания

```bash
# Установка Istio
istioctl install --set profile=demo -y
kubectl label namespace default istio-injection=enabled --overwrite

# Развертывание через CI/CD
make ci

# Проверка установки
./check-istio.sh

# Тестирование
kubectl exec deploy/booking-service-v1 -c booking-service -- sh -c 'for i in $(seq 1 100); do curl -s http://booking-service/ping; echo ""; done' | sort | uniq -c

# Тест фича-флага
kubectl exec deploy/booking-service-v1 -c booking-service -- curl -s -H "X-Feature-Enabled: true" http://booking-service/
```

## Выводы

1. Istio успешно установлен и настроен в Kubernetes кластере
2. Реализовано канареечное развертывание с распределением трафика 90/10
3. Настроена маршрутизация на основе заголовков (фича-флаги)
4. Добавлены Circuit Breaking и Retry механизмы для отказоустойчивости
5. CI/CD пайплайн автоматизирует развертывание обеих версий с Istio конфигурацией
6. Все проверочные скрипты подтверждают корректную работу Service Mesh
