package initialize

import (
	"github.com/spf13/viper"
	"kubeimoc.com/global"
)

func InitViper() {
	v := viper.New()
	v.SetConfigFile("config.yaml") // Name of the configuration file (without extension)
	v.SetConfigType("yaml")
	err := v.ReadInConfig() // Read the configuration file
	if err != nil {
		panic(err.Error())
	}
	err = v.Unmarshal(&global.CONF) // Unmarshal the configuration into the global variable
	if err != nil {
		panic(err.Error())
	}
}
