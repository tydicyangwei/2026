package initialize

import (
	"kubeimoc.com/router"

	"github.com/gin-gonic/gin"
)

func Route() *gin.Engine {
	// Create a Gin router with default middleware (logger and recovery)
	r := gin.Default()
	Examplegroup := router.RouterGroupApp.ExampleRouter
	Examplegroup.InitExampleRouter(r) // Initialize the example router
	return r
	//r.Run(":8080")                    // Start the server on port 8080
}
