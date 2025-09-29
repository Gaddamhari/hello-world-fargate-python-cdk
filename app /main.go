package main

import (
	"fmt"
	"log"
	"net/http"
	"os"
)

func root(w http.ResponseWriter, r *http.Request) {
	host, _ := os.Hostname()
	fmt.Fprintf(w, "Hello from ECS Fargate! Host: %s\n", host)
}

func health(w http.ResponseWriter, r *http.Request) {
	w.WriteHeader(http.StatusOK)
	w.Write([]byte("ok"))
}

func main() {
	http.HandleFunc("/", root)
	http.HandleFunc("/healthz", health)

	port := "8080"
	log.Printf("Listening on :%s ...", port)
	log.Fatal(http.ListenAndServe("0.0.0.0:"+port, nil))
}

