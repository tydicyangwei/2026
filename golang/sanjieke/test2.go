package main

import (
	"fmt"
)

func main() {
	t1 := make(chan int)
	go func() {
		t1 <- 42
	}()
	r1 := <-t1
	fmt.Println("从通道接收到的值:", r1)
}
