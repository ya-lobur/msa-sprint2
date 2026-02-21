package main

import (
	"fmt"
	"log"
	"net/http"
	"os"
)

func main() {
	version := os.Getenv("VERSION")
	if version == "" {
		version = "v1"
	}

	enableFeatureX := os.Getenv("ENABLE_FEATURE_X") == "true"

	// Health check endpoint
	http.HandleFunc("/health", func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusOK)
		fmt.Fprintf(w, "healthy")
	})

	// Ready endpoint
	http.HandleFunc("/ready", func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusOK)
		fmt.Fprintf(w, "ready")
	})

	// Ping endpoint
	http.HandleFunc("/ping", func(w http.ResponseWriter, r *http.Request) {
		fmt.Fprintf(w, "pong from %s", version)
	})

	// Main booking endpoint
	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		// Check for feature flag header
		featureEnabled := r.Header.Get("X-Feature-Enabled") == "true"

		if version == "v2" && (featureEnabled || enableFeatureX) {
			fmt.Fprintf(w, "Response from booking-service %s with new features!", version)
		} else {
			fmt.Fprintf(w, "Response from booking-service %s", version)
		}
	})

	// Feature flag route
	if enableFeatureX {
		http.HandleFunc("/feature", func(w http.ResponseWriter, r *http.Request) {
			fmt.Fprintf(w, "Feature X is enabled in %s!", version)
		})
		log.Printf("Feature X is ENABLED in %s", version)
	} else {
		log.Printf("Feature X is DISABLED in %s", version)
	}

	log.Printf("Server %s running on :8080", version)
	log.Fatal(http.ListenAndServe(":8080", nil))
}
