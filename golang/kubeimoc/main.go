package main

import (
	"kubeimoc.com/global"
	"kubeimoc.com/initialize"
)

func main() {
	r := initialize.Route() // Initialize routes
	initialize.InitViper()  // Initialize configuration
	initialize.K8s()
	r.Run(global.CONF.System.Addr) // Start the server on port 8081
}
