package main

import (
	"fmt"
	"os"
)

func main() {
	byteData, err := os.ReadFile("./hello.txt")
	if err != nil {
		fmt.Println("Error reading file:", err)
		return
	}
	fmt.Println(string(byteData))
}
