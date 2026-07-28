package api

import (
	"kubeimoc.com/api/example"
)

type ApiGroup struct {
	ExampleGroup example.ExampleGroup
}

var (
	ExampleApiGroup = new(ApiGroup)
)
