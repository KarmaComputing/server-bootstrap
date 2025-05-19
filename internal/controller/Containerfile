# Builder stage
FROM docker.io/library/golang:latest as builder
WORKDIR /src
COPY . .
RUN go build -o /app/main

# Final stage
FROM docker.io/library/debian:latest
WORKDIR /app
COPY --from=builder /app .
ENTRYPOINT ["/app/main"]  # Entry point
