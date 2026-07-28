package example

import (
	"github.com/gin-gonic/gin"
	"kubeimoc.com/api"
)

type ExampleRouter struct {
}

func (er *ExampleRouter) InitExampleRouter(r *gin.Engine) {
	group := r.Group("/example")
	ExampleApiGroup := api.ExampleApiGroup.ExampleGroup
	group.GET("/ping", ExampleApiGroup.ExampleApp.ExampleTest)
}
