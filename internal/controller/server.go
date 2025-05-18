package main

import (
	"log"

	"github.com/stmcginnis/gofish"
	"github.com/stmcginnis/gofish/redfish"
)

type LOM struct {
	gofish.ClientConfig
	gofish.APIClient
}

func NewLOM(clientConfig *gofish.ClientConfig) (*LOM, error) {
	apiClient, err := gofish.Connect(*clientConfig)
	if err != nil {
		return nil, err
	}

	return &LOM{
		ClientConfig: *clientConfig,
		APIClient:    *apiClient,
	}, nil
}

func (lom *LOM) ServerPowerOn() {
	system := lom.GetSystem()
	err := system.Reset(redfish.OnResetType)
	if err != nil {
		return
	}
}

func (lom *LOM) ServerPowerOff() {
	system := lom.GetSystem()
	err := system.Reset(redfish.ForceOffResetType)
	if err != nil {
		return
	}
}

func (lom *LOM) ServerPowerToggle() {
	if lom.serverIsPoweredOn() {
		lom.ServerPowerOff()
	} else {
		lom.ServerPowerOn()
	}
}

func (lom *LOM) ServerRestart() error {
	system := lom.GetSystem()
	err := system.Reset(redfish.ForceRestartResetType)
	if err != nil {
		log.Fatal(err)
	}
	return nil
}

func (lom *LOM) GetSystem() *redfish.ComputerSystem {
	systems, err := lom.Service.Systems()
	if err != nil {
		panic(err)
	}

	return systems[0]
}
func (lom *LOM) getServerPowerState() string {
	return string(lom.GetSystem().PowerState)
}

func (lom *LOM) serverIsPoweredOn() bool {
	return lom.getServerPowerState() == "On"
}

func (lom *LOM) serverIsPoweredOff() bool {
	return lom.getServerPowerState() == "Off"
}

func (lom *LOM) Destroy() {
	lom.APIClient.Logout()
}
