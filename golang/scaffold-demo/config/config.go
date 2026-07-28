package config

import (
	"github.com/sirupsen/logrus"
	"github.com/spf13/viper"
)

const (
	TimeFormat = "2006-01-02 15:04:05"
)

func initLogConfig(logLevel string) {
	switch logLevel {
	case "debug":
		logrus.SetLevel(logrus.DebugLevel)
	case "info":
		logrus.SetLevel(logrus.InfoLevel)
	case "warn":
		logrus.SetLevel(logrus.WarnLevel)
	case "error":
		logrus.SetLevel(logrus.ErrorLevel)
	}
	logrus.SetReportCaller(true) // Enable reporting of the calling method
	logrus.SetFormatter(&logrus.TextFormatter{
		TimestampFormat: TimeFormat,
	})
}
func init() {
	// Set the log level to DebugLevel
	viper.SetDefault("USERNAME", "杨威")
	viper.SetDefault("LOG_LEVEL", "info")
	viper.AutomaticEnv() // Automatically read environment variables
	logLevel := viper.GetString("LOG_LEVEL")
	initLogConfig(logLevel)
}
