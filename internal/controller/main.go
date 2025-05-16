package main

import (
	"fmt"
	"log"
	"os"
	"strconv"
	"strings"
	"time"
)

func main() {
	urlAddress := os.Getenv("URL")
	if urlAddress == "" {
		log.Fatal("URL is not set, expects format e.g. 'https://192.168.0.230'")
	}
	username := os.Getenv("USERNAME")
	if username == "" {
		log.Fatal("USERNAME is not set, expects string")
	}
	password := os.Getenv("PASSWORD")
	if password == "" {
		log.Fatal("PASSWORD is not set, expects string")
	}
	validCert := os.Getenv("VALIDCERT")
	if validCert == "" {
		log.Fatal("VALIDCERT is not set, expects boolean")
	}
	var isValidCert bool
	switch strings.ToLower(validCert) {
	case "true":
		isValidCert = true
	case "false":
		isValidCert = false
	default:
		log.Fatal("validCert is not <true|false>")
	}
	wipeInterval := os.Getenv("WIPEINTERVAL")
	if wipeInterval == "" {
		log.Fatal("WIPEINTERVAL is not set, expects seconds in an integer")
	}
	wipeIntervalInt, err := strconv.Atoi(wipeInterval)
	if err != nil {
		log.Fatal("WIPEINTERVAL is not an integer")
	}

	server, err := NewServer(urlAddress, username, password, isValidCert)
	if err != nil {
		log.Fatal(err)
	}

	defer server.Destroy()

	for {
		fmt.Println("Toggling power from")
		currentState := server.getPowerState()
		server.PowerToggle()

		for currentState == server.getPowerState() {
			time.Sleep(1 * time.Second)
			fmt.Println("Waiting for power state to change...")
		}
		fmt.Printf("Waiting for %d seconds\n", wipeIntervalInt)
		time.Sleep(time.Duration(wipeIntervalInt))
	}
}
