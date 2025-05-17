package main

import (
	"fmt"
	"log"
	"os"
	"strconv"
	"strings"
	"time"

	"github.com/stmcginnis/gofish"
)

type Config struct {
	gofish.ClientConfig
	wipeInterval int
}

func main() {
	config := tryGetConfigFromEnvironment()

	server, err := NewServer(&config.ClientConfig)
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
		fmt.Printf("Waiting for %d seconds\n", config.wipeInterval)
		time.Sleep(time.Second * time.Duration(config.wipeInterval))
	}
}

func tryGetConfigFromEnvironment() *Config {
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

	var allowValidCert bool
	{
		env := os.Getenv("VALIDCERT")
		if env == "" {
			log.Fatal("VALIDCERT is not set, expects boolean")
		}
		switch strings.ToLower(env) {
		case "true":
			allowValidCert = true
		case "false":
			allowValidCert = false
		default:
			log.Fatal("validCert is not <true|false>")
		}
	}

	var wipeInterval int
	{
		env := os.Getenv("WIPEINTERVAL")
		if env == "" {
			log.Fatal("WIPEINTERVAL is not set, expects seconds in an integer")
		}
		value, err := strconv.Atoi(env)
		if err != nil {
			log.Fatal("WIPEINTERVAL is not an integer")
		}
		wipeInterval = value
	}

	return &Config{
		ClientConfig: gofish.ClientConfig{Endpoint: urlAddress,
			Username: username,
			Password: password,
			Insecure: !allowValidCert},
		wipeInterval: wipeInterval,
	}
}
