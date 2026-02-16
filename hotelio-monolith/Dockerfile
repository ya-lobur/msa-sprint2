# Build stage
FROM gradle:8.7-jdk17 AS build
WORKDIR /app

# Copy gradle files
COPY build.gradle settings.gradle gradlew ./
COPY gradle gradle/
COPY libs libs/

# Make gradlew executable
RUN chmod +x gradlew

# Copy source code
COPY src src/

# Build application
RUN ./gradlew build --no-daemon -x test

# Runtime stage
FROM openjdk:17-ea-3-jdk-slim
WORKDIR /app

# Copy the built jar from build stage
COPY --from=build /app/build/libs/*.jar app.jar

# Expose application port
EXPOSE 8080

# Run the application
ENTRYPOINT ["java", "-jar", "app.jar"]
