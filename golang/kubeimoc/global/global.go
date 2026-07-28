package global

import (
	"k8s.io/client-go/kubernetes"
	"kubeimoc.com/config"
)

var (
	CONF          config.Server
	KubeConfigSet *kubernetes.Clientset
)
