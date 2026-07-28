package main

import (
	"net/http"

	"github.com/gin-gonic/gin"
)

type userInfo struct {
	Name string `json:"name"`
	Age  int    `json:"age"`
}

func hello(c *gin.Context) {
	u := userInfo{
		Name: "Alice",
		Age:  30,
	}
	c.JSON(http.StatusOK, u)
}
func posthello(c *gin.Context) {
	var u userInfo
	if err := c.ShouldBindJSON(&u); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}
	c.JSON(http.StatusOK, u)
}
func main() {
	//定义路由
	r := gin.Default()
	//注册路由
	r.GET("/hello", hello)
	r.POST("/hello", posthello)
	//启动服务
	r.Run(":8080")
}
