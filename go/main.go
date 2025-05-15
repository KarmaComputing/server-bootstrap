// SPDX-License-Identifier: BSD-3-Clause
package main

import (
	"fmt"
	"net/http"
	// "time"

	"github.com/stmcginnis/gofish"
	"github.com/stmcginnis/gofish/redfish"
)

func main() {
	// Create a new instance of gofish client, ignoring self-signed certs
	config := gofish.ClientConfig{
		Endpoint: "https://192.168.0.230",
		Username: "Administrator",
		Password: "A0F7HKUU",
		Insecure: true,
	}
	
	c, err := gofish.Connect(config)
	if err != nil {
		panic(err)
	}
	defer c.Logout()

	// Attached the client to service root
	service := c.Service

	// Query the computer systems
	systems, err := service.Systems()
	if err != nil {
		panic(err)
	}
	system := systems[0]
	
	// Creates a boot override to pxe once
	// bootOverride := redfish.Boot{
	// 	BootSourceOverrideTarget:  redfish.PxeBootSourceOverrideTarget,
	// 	BootSourceOverrideEnabled: redfish.OnceBootSourceOverrideEnabled,
	// }

	// HTTP server to trigger power reset
	http.HandleFunc("/power/restart", func(w http.ResponseWriter, r *http.Request) {
		if r.Method == "POST" {
			err := restartPower(getSystem(config))
			if err != nil {
				http.Error(w, err.Error(), http.StatusInternalServerError)
				return
			}
			fmt.Fprintf(w, "Power reset initiated")
		} else {
			http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		}
	})

	http.HandleFunc("/power/off", func(w http.ResponseWriter, r *http.Request) {
		if r.Method == "POST" {
			err := powerOff(getSystem(config))
			if err != nil {
				http.Error(w, err.Error(), http.StatusInternalServerError)
				return
			}
			fmt.Fprintf(w, "Power off initiated")
		} else {
			http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		}
	})

	http.HandleFunc("/power/on", func(w http.ResponseWriter, r *http.Request) {
		if r.Method == "POST" {
			err := powerOn(getSystem(config))
			if err != nil {
				http.Error(w, err.Error(), http.StatusInternalServerError)
				return
			}
			fmt.Fprintf(w, "Power on initiated")
		} else {
			http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		}
	})

	http.HandleFunc("/power/status", func(w http.ResponseWriter, r *http.Request) {
		if r.Method == "GET" {
			fmt.Fprintf(w, getPower(getSystem(config)))
		} else {
			http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		}
	})
	
	// go func() {
	// 	for true {
	// 		fmt.Println("Toggling power")
	// 		currentState := getPower(getSystem(config))
	// 		togglePower(getSystem(config))
			
	// 		for currentState == getPower(getSystem(config)) {
	// 			time.Sleep(1 * time.Second)
	// 			fmt.Println("Waiting for power state to change...")
	// 		}
			
	// 		fmt.Println("Waiting for 10 seconds")
	// 		time.Sleep(10 * time.Second)
	// 	}
	// }()
	
	fmt.Println("Starting HTTP server on :8080")
	if err := http.ListenAndServe("0.0.0.0:8080", nil); err != nil {
		panic(err)
	}
}

func getSystem(config gofish.ClientConfig) (*redfish.ComputerSystem)  {
	c, err := gofish.Connect(config)
	if err != nil {
		panic(err)
	}
	defer c.Logout()

	// Attached the client to service root
	service := c.Service

	// Query the computer systems
	systems, err := service.Systems()
	if err != nil {
		panic(err)
	}
	system := systems[0]
	fmt.Println(system)
	return system
}

func restartPower(system *redfish.ComputerSystem) error {
	fmt.Println("restartPower")
	err := system.Reset(redfish.ForceRestartResetType)
	if err != nil {
		return err
	}
	return nil
}

func powerOff(system *redfish.ComputerSystem) error {
	fmt.Println("powerOff")
	err := system.Reset(redfish.ForceOffResetType)
	if err != nil {
		return err
	}
	return nil
}

func powerOn(system *redfish.ComputerSystem) error {
	fmt.Println("powerOn")
	err := system.Reset(redfish.OnResetType)
	if err != nil {
		return err
	}
	return nil
}

func togglePower(system *redfish.ComputerSystem) {
	if isPowerOff(system) {
		powerOn(system)
	} else {
		powerOff(system)
	}
}

func getPower(system *redfish.ComputerSystem) string {
	return string(system.PowerState)
}

func isPowerOn(system *redfish.ComputerSystem) bool {
	if getPower(system) == "On" {
		return true
	} else {
		return false
	}
}

func isPowerOff(system *redfish.ComputerSystem) bool {
	if getPower(system) == "Off" {
		return true
	} else {
		return false
	}
}