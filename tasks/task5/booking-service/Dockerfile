# Используем официальный минимальный образ Go
FROM golang:1.21-alpine

# Добавить необходимые пакеты (например, curl)
RUN apk add --no-cache curl

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем Go-файл
COPY main.go .

# Собрать бинарник из main.go
RUN go build -o booking-service main.go

# Задать команду запуска
CMD ["./booking-service"]
