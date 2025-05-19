package main

import (
	"fmt"
	"log"
	"os"
	"server_bootstrap/lom"
	"strconv"
	"strings"
	"time"

	"github.com/stmcginnis/gofish"
	"github.com/stmcginnis/gofish/redfish"
	"golang.org/x/crypto/ssh"
)

type Config struct {
	gofish.ClientConfig
	wipeInterval int
}

func main() {
	config := tryGetConfigFromEnvironment()

	lom, err := lom.NewFromConfig(&config.ClientConfig)
	if err != nil {
		log.Fatal(err)
	}
	defer lom.Logout()

	err = bootstrap(lom)
	if err != nil {
		log.Fatal(err)
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

	var validCertOnly bool
	{
		env := os.Getenv("VALIDCERT")
		if env == "" {
			log.Fatal("VALIDCERT is not set, expects boolean")
		}
		switch strings.ToLower(env) {
		case "true":
			validCertOnly = true
		case "false":
			validCertOnly = false
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
			Insecure: !validCertOnly},
		wipeInterval: wipeInterval,
	}
}

func bootstrap(lom *lom.LOM) error {
	systems := *lom.AllSystems()

	bootOverride := redfish.Boot{
		BootSourceOverrideTarget:  redfish.CdBootSourceOverrideTarget,
		BootSourceOverrideEnabled: redfish.OnceBootSourceOverrideEnabled,
	}

	for _, system := range systems {
		fmt.Printf("Setting boot option of system: %s\n", system.HostName)
		err := system.SetBoot(bootOverride)
		if err != nil {
			return err
		}

		fmt.Printf("Setting virtual media for system: %s\n", system.HostName)
		_, err = lom.APIClient.Patch("/redfish/v1/managers/1/virtualmedia/2", map[string]string{"Image": "http://192.168.0.170/iso/alpine-netboot/ipxe.iso"})
		if err != nil {
			return err
		}

		// Reboot
		fmt.Printf("Restarting system: %s\n", system.HostName)
		err = system.Reset(redfish.OnResetType)
		if err != nil {
			return err
		}
	}

	// Await Alpine SSH access
	// Run ansible playbook
	// Wait for real OS SSH access
	// Ansible playbook 2: electric boogaloo?

	return nil
}

func canSSH(host, port, username string) bool {
	config := &ssh.ClientConfig{
		User:            username,
		HostKeyCallback: ssh.InsecureIgnoreHostKey(),
		Timeout:         5 * time.Second,
	}

	addr := fmt.Sprintf("%s:%s", host, port)
	client, err := ssh.Dial("tcp", addr, config)
	if err != nil {
		return false
	}
	client.Close()

	return true
}
