package main

import (
	"fmt"
	// "github.com/stmcginnis/gofish"
	"github.com/stmcginnis/gofish/redfish"
)

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