package main

import (
	"net/http"

	"github.com/gin-gonic/gin"
)

func hello(c *gin.Context) {
	c.String(http.StatusOK, "hello world")
}
func main() {
	//定义路由
	r := gin.Default()
	//注册路由
	r.GET("/hello", hello)
	//启动服务
	r.Run(":8080")
}
