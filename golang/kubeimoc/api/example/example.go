package example

import (
	"net/http"

	"github.com/gin-gonic/gin"
)

type ExampleApp struct {
}

func (*ExampleApp) ExampleTest(c *gin.Context) {
	// Return JSON response
	c.JSON(http.StatusOK, gin.H{
		"message": "pong",
	})
}
