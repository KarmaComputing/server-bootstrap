package lom

import (
	"fmt"

	"github.com/stmcginnis/gofish"
	"github.com/stmcginnis/gofish/redfish"
)

type SystemPowerState string

const (
	PowerStateUnknown SystemPowerState = ""
	PowerStateOn      SystemPowerState = "On"
	PowerStateOff     SystemPowerState = "Off"
)

type LOM struct {
	gofish.APIClient
	systems []*redfish.ComputerSystem
}

func NewFromConfig(clientConfig *gofish.ClientConfig) (*LOM, error) {
	apiClient, err := gofish.Connect(*clientConfig)
	if err != nil {
		return nil, err
	}

	systems, err := apiClient.Service.Systems()
	if err != nil {
		return nil, err
	}

	return &LOM{
		APIClient: *apiClient,
		systems:   systems,
	}, nil
}

func (lom *LOM) AllSystems() *[]*redfish.ComputerSystem {
	return &lom.systems
}

func (lom *LOM) SystemsCount() int {
	return len(lom.systems)
}

func (lom *LOM) SystemPowerOn(systemNumber int) error {
	system, err := lom.GetSystem(systemNumber)
	if err != nil {
		return err
	}

	err = system.Reset(redfish.OnResetType)
	if err != nil {
		return err
	}

	return nil
}

func (lom *LOM) SystemPowerOff(systemNumber int) error {
	system, err := lom.GetSystem(systemNumber)
	if system != nil {
		return err
	}

	err = system.Reset(redfish.ForceOffResetType)
	if err != nil {
		return err
	}

	return nil
}

func (lom *LOM) SystemPowerToggle(systemNumber int) error {
	isPoweredOn, err := lom.IsSystemPoweredOn(systemNumber)
	if err != nil {
		return err
	}

	if isPoweredOn {
		return lom.SystemPowerOff(systemNumber)
	} else {
		return lom.SystemPowerOn(systemNumber)
	}
}

func (lom *LOM) SystemRestart(systemNumber int) error {
	system, err := lom.GetSystem(systemNumber)
	if system == nil {
		return err
	}

	err = system.Reset(redfish.ForceRestartResetType)
	if err != nil {
		return err
	}

	return nil
}

func (lom *LOM) GetSystem(systemNumber int) (*redfish.ComputerSystem, error) {
	if systemNumber < 0 || systemNumber >= lom.SystemsCount() {
		return nil, fmt.Errorf("This LOM does not have %d systems", systemNumber)
	}

	system := lom.systems[systemNumber]
	return system, nil
}

func (lom *LOM) SystemPowerState(systemNumber int) (SystemPowerState, error) {
	system, err := lom.GetSystem(systemNumber)
	if err != nil {
		return PowerStateUnknown, err
	}

	return SystemPowerState(system.PowerState), nil
}

func (lom *LOM) IsSystemPoweredOn(systemNumber int) (bool, error) {
	system, err := lom.GetSystem(systemNumber)
	if err != nil {
		return false, err
	}

	return SystemPowerState(system.PowerState) == PowerStateOn, nil
}

func (lom *LOM) IsSystemPoweredOff(systemNumber int) (bool, error) {
	system, err := lom.GetSystem(systemNumber)
	if err != nil {
		return false, err
	}

	return SystemPowerState(system.PowerState) == PowerStateOff, nil
}

func (lom *LOM) Logout() {
	lom.APIClient.Logout()
}
