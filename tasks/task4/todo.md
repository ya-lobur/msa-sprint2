# Задание 4. Автоматизация развёртывания и тестирования

## Цель задания

Ускорить доставку фич, уменьшить количество ошибок при выкладке и упростить масштабирование в Kubernetes.

## Что нужно сделать

Root директория задания `/Users/yalobur/projects/courses/yandex/mswa/msa-sprint2/tasks/task4`

### 1. Реализовать Docker-образ сервиса

В рабочей директории задания сделан простой Mock-сервис
`/Users/yalobur/projects/courses/yandex/mswa/msa-sprint2/tasks/task4/booking-service`для понимания работы фича-флагов.  
Для него сделан драфт Helm-чартов и тестов.

Mock-сервис заменён на вашу реализацию.

#### Дополнительно о реализации сервиса:

- собирается с помощью `docker build`;
- сделан `healthcheck` endpoint;
- сделан `ready` endpoint;
- поведение сервиса меняется при наличии переменной `ENABLE_FEATURE_X=true`.

> Обязательно сделайте два варианта values.yaml: для staging и prod.

### 2. Реализовать Helm-чарт

#### Deployment:

- с пробами:
    - `livenessProbe`
    - `readinessProbe` по `/ping`.

#### Service:

- тип `ClusterIP`;
- порт `80 → targetPort 8080`.

#### Значения из `values.yaml`:

- `replicaCount`;
- `image.name`, `image.tag`, `image.pullPolicy`;
- `env[]` — переменные окружения;
- `resources` — requests и limits;
- `ENABLE_FEATURE_X` — фича-флаг.

Обязательно сделайте **два варианта `values.yaml`**:

- для staging;
- для prod.

## 3. Реализовать CI/CD-пайплайн (`.gitlab-ci.yml`)

### Стадии:

- **build** — `docker build`
- **test** — `docker run`, проверка `/ping`, `docker rm`
- **deploy** — `minikube image load` и `helm upgrade`
- **tag** — создать git-тег с timestamp

Если есть unit-тесты, нужно добавить отдельный шаг для их запуска.

> Используйте: `gitlab-ci-local build test deploy tag`

## 4. Реализовать Service Discovery через DNS

Проверка:

`http://booking-service/ping` работает из другого пода внутри Minikube.

Ниже есть инструкция по установке Minikube.

Используйте скрипт `check-dns.sh`.

## Подсказки по проверке корректности

**Проверка сервисов:**

`./check-status`
**Пример вывода:**

```text
Checking booking-service deployment...
NAME                                     READY   STATUS    RESTARTS   AGE
booking-service-78d99d7dd5-abc           1/1     Running   0          1m 

Checking service...
NAME             TYPE        CLUSTER-IP     PORT(S)   AGE
booking-service  ClusterIP   10.96.170.171  80/TCP    1m 

Port-forward to test service locally: 
kubectl port-forward svc/booking-service 8080:80
Then: 
curl http://localhost:8080/ping
``` 

**Проверка DNS внутри кластера:**

`./check-dns.sh`
**Ожидаемый вывод:**

```text
[INFO] Running in-cluster DNS test...
[INFO] DNS Response: pong
[PASS] DNS test succeeded
```

Подсказки:

- imagePullPolicy: Never нужен для использования локального образа
- minikube image load копирует образ внутрь Minikube
- DNS имена booking-service работают только внутри кластера

**Для доступа снаружи используйте:**

```shell
kubectl port-forward svc/booking-service 8080:80
curl http://localhost:8080/ping 
```

## Образ результата

### Структура проекта:

```text
task4/ 
├── booking-service/ # REST-сервис (Go/Java/etc) 
├── helm/ 
│ └── booking-service/ # Helm-чарт сервиса (требуется доработка)
├── .gitlab-ci.yml # CI/CD-пайплайн (требуется доработка) 
├── check-dns.sh # Проверка DNS внутри кластера 
├── check-status # Статус деплоя и curl локально 
├── README.md 
```

**Dockerfile для каждого микросервиса**

- helm/-директория с чартами.
- .gitlab-ci.yml с пайплайном.
- README.md с инструкцией по разворачиванию в Minikube.
- Логика обнаружения сервисов (DNS).
- Пример успешного деплоя в Kubernetes (скриншот или вывод команды get pods + get services).

**Структура и содержание репозитория, в котором нужно сдать решение:**

```text
task4/results/ 
├── report.md # Описание изменений и решений 
├── values-staging.yaml 
├── values-prod.yaml 
├── .gitlab-ci.yml 
├── Скриншот успешного curl на /ping 
├── Скриншот ./check-dns.sh 
├── Скриншот ./check-status 
├── kubectl get pods + get services
├── Лог успешной сборки
└── docker image ls + minikube image list 
```

Загрузите результат в директорию task4/results/ вашего репозитория