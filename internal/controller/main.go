// SPDX-License-Identifier: BSD-3-Clause
package main

import (
	"fmt"
	"log"
	"time"
)

func main() {
	server, err := NewServer("https://192.168.0.230", "Administrator", "A0F7HKUU", false)
	if err != nil {
		log.Fatal(err)
	}
	defer server.Destroy()

	for {
		fmt.Println("Toggling power from")
		currentState := server.getPower()
		server.PowerToggle()

		for currentState == server.getPower() {
			time.Sleep(1 * time.Second)
			fmt.Println("Waiting for power state to change...")
		}

		fmt.Println("Waiting for 10 minutes...")
		time.Sleep(10 * time.Minute)
	}
}
