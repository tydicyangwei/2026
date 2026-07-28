package logs

import (
	logrus "github.com/sirupsen/logrus"
)

func Debug(fields map[string]interface{}, message string) {
	logrus.WithFields(fields).Debug(message)
}

func Info(fields map[string]interface{}, message string) {
	logrus.WithFields(fields).Info(message)
}

func Warn(fields map[string]interface{}, message string) {
	logrus.WithFields(fields).Warn(message)
}

func Error(fields map[string]interface{}, message string) {
	logrus.WithFields(fields).Error(message)
}
