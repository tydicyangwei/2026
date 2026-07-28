package main

import (
	"fmt"
	"sort"
)

func test() {
	var list = make([]string, 0)
	fmt.Println(list, len(list), cap(list))
	fmt.Printf("%v\n", "你好")
	var a1 []int
	a1 = []int{2, 1, 3}
	fmt.Printf("变量 'a1' 的内存地址是: %p\n", &a1)
	//	sort.Ints(a1)
	fmt.Println(a1)
	fmt.Printf("变量 'a1' 的内存地址是: %p\n", &a1)
	sort.Sort(sort.Reverse(sort.IntSlice(a1)))

	fmt.Println(a1)
}

func main() {
	test()
	//aa := "1"
	//a := []byte(aa)
	//fmt.Println(a)
}
