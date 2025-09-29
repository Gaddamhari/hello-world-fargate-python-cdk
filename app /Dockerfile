# Build stage
FROM golang:1.22-alpine AS build
WORKDIR /src
COPY main.go .
RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -o app main.go

# Runtime stage
FROM gcr.io/distroless/base-debian12
WORKDIR /app
COPY --from=build /src/app /app/app
EXPOSE 8080
USER 65532:65532
ENTRYPOINT ["/app/app"]
