package main

import (
	"log"

	"github.com/stmcginnis/gofish"
	"github.com/stmcginnis/gofish/redfish"
)

type Server struct {
	gofish.ClientConfig
	gofish.APIClient
}

func NewServer(endpoint, username, password string, secure bool) (*Server, error) {
	clientConfig := gofish.ClientConfig{
		Endpoint: endpoint,
		Username: username,
		Password: password,
		Insecure: !secure,
	}

	apiClient, err := gofish.Connect(clientConfig)
	if err != nil {
		return nil, err
	}

	system := Server{
		ClientConfig: clientConfig,
		APIClient:    *apiClient,
	}

	return &system, nil
}

func (server *Server) PowerOn() {
	system := server.GetSystem()
	err := system.Reset(redfish.OnResetType)
	if err != nil {
		return
	}
}

func (server *Server) PowerOff() {
	system := server.GetSystem()
	err := system.Reset(redfish.ForceOffResetType)
	if err != nil {
		return
	}
}

func (server *Server) PowerToggle() {
	if server.isPoweredOn() {
		server.PowerOff()
	} else {
		server.PowerOn()
	}
}

func (server *Server) Restart() error {
	system := server.GetSystem()
	err := system.Reset(redfish.ForceRestartResetType)
	if err != nil {
		log.Fatal(err)
	}
	return nil
}

func (server *Server) GetSystem() *redfish.ComputerSystem {
	systems, err := server.Service.Systems()
	if err != nil {
		panic(err)
	}

	return systems[0]
}
func (server *Server) getPowerState() string {
	return string(server.GetSystem().PowerState)
}

func (server *Server) isPoweredOn() bool {
	if server.getPowerState() == "On" {
		return true
	} else {
		return false
	}
}

func (server *Server) isPoweredOff() bool {
	if server.getPowerState() == "Off" {
		return true
	} else {
		return false
	}
}

func (server *Server) Destroy() {
	server.APIClient.Logout()
}
