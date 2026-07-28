package main

import (
	_ "scaffold-demo/config"
	"scaffold-demo/utils/logs"

	"github.com/gin-gonic/gin"
)

func main() {
	// Create a Gin router with default middleware (logger and recovery)
	r := gin.Default()
	r.GET("/ping", func(c *gin.Context) {
		// Return JSON response
		c.JSON(200, gin.H{
			"message": "pong",
		})
	})
	logs.Info(nil, "Server is starting...")
	r.Run(":8080") // Start the server on port 8080
}
