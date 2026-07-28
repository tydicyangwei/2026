package router

import (
	"kubeimoc.com/router/example"
)

type RouterGroup struct {
	ExampleRouter example.ExampleRouter
}

var (
	RouterGroupApp = new(RouterGroup)
)
