# Задание 5. Настройка управления трафиком с Istio

## Цель задания

Настроить маршрутизацию трафика с **Istio**.

После настройки CI/CD и развёртывания микросервисов в Kubernetes команда Hotelio столкнулась с новой задачей —
управление трафиком на продакшне.

Компания хочет:

- тестировать фичи без риска;
- быстрее находить проблемные сервисы;
- управлять отказами без изменений в бизнес-коде.

Было решено установить **Istio как Service Mesh** и начать использовать трафик-менеджмент:  
канареечный Release, Circuit Breaker и другие механики.

Начать необходимо с уже перенесённого в Kubernetes сервиса **booking-service**.

## Что нужно сделать

### 1. Подготовка (сделано)

Скопируйте выполненный `task4` в `task5`. (сделано)

Используйте тот же сервис `booking-service`, но теперь добавьте для него **Istio Service Mesh**.

### 2. Установите Istio 

- Установите Istio в Minikube, используя:

  `istioctl install --set profile=demo`

- Включите автоматическую инъекцию Istio в `default` namespace, чтобы каждый под автоматически
  получал sidecar-прокси **(Envoy)**.

### 3. Добавьте две версии сервиса

- **v1** — основная версия сервиса.
- **v2** — новая версия с возможностью включения фича-флагов через заголовок: `X-Feature-Enabled: true`

### 4. Настройте Istio-маршрутизацию

#### Канареечный Release

- 90% трафика направляется на `v1`
- 10% трафика направляется на `v2`

#### Fallback-маршрут

- Если `v1` возвращает ошибку, трафик перенаправляется на `v2`.

#### Retry и Circuit Breaking

- Используйте `DestinationRule` для настройки:
    - Retries
    - Circuit Breaking

### 5. Настройте фича-флаги через EnvoyFilter

Примените `EnvoyFilter`, чтобы включить маршрутизацию трафика на `v2`, если заголовок запроса:
`X-Feature-Enabled = true`

### 6. Проверьте настройки с помощью скриптов

Используйте проверочные скрипты (уже лежат в папке с заданием):

- `check-istio.sh` — проверка установки Istio и инъекции.
- `check-canary.sh` — тестирование разделения трафика (90% на v1, 10% на v2).
- `check-fallback.sh` — тестирование fallback-маршрута (предварительно погасите один из подов).
- `check-feature-flag.sh` — проверка маршрутизации через фича-флаг.

Скрипты можно модифицировать.

## Подсказки по подготовке окружения

Для выполнения задания нужно установить Istio в уже имеющийся кластер.

### 1. Запустите Istio в Minikube

`istioctl install --set profile=demo -y`

### 2. Включите инъекцию Istio в namespace

`kubectl label namespace default istio-injection=enabled --overwrite`

### 3. Проверьте установку

`kubectl get pods -n istio-system`  
`istioctl version`

---

Не забывайте, что Istio-конфигурации нужно применять вручную — «из коробки» они работать не будут.

Пример:

`kubectl apply -f istio/virtual-service.yaml`  
`kubectl get virtualservices`

Для удобства дебага можно использовать `access_log` — в demo он включён по умолчанию:

`kubectl logs -l app=booking-service -n default`

## Образ результата

### Структура и содержание репозитория

```text
task5/results/ 
├── report.md # Описание изменений и решений 
├── values-v1.yaml и values-v2.yaml с разными конфигурациями сервиса
├── virtual-service.yaml (canary + fallback + feature flag)
├── destination-rule.yaml (Retry + CircuitBreaking)
├── envoy-filter.yaml  (Feature flag через EnvoyFilter) 
└── Логи запуска проверочных скриптов (или Скриншоты)
```