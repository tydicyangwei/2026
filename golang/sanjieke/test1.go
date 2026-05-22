// package main

// import (
// 	"errors"
// 	"fmt"
// )

// // 可变参数函数，接受任意数量的字符串参数
// func Teststr(s ...string) string {
// 	fmt.Println(s)
// 	return ""
// }

// func Testtype(a string, b int) (string, error) {
// 	return a, errors.New("自定义错误")
// }

// func main() {
// 	Teststr("a", "b", "c")
// 	fmt.Println(Testtype("test", 123))
// }
