package main

import (
iter "github.com/hgfischer/go-iter"
"github.com/google/go-cmp/cmp"
"fmt")




func bubble_sort(seq []int) []int {
L := len(seq)
for _, _ := range iter.NewIntSeq(iter.Start(0), iter.Stop(L)).All() {
_ = _
for _, n := range iter.NewIntSeq(iter.Start(1), iter.Stop(L)).All() {
if(seq[n] < seq[(n - 1)]) {
({
__tmp1, __tmp2 := (seq[n], seq[(n - 1)])
seq[(n - 1)] := __tmp1
seq[n] := __tmp2
;
})
}
}
}
return seq}


func main() {
var unsorted []int = []int{14, 11, 19, 5, 16, 10, 19, 12, 5, 12}
var expected []int = []int{5, 5, 10, 11, 12, 12, 14, 16, 19, 19}
if !(cmp.Equal(bubble_sort(unsorted), expected)) { panic("assert") }
fmt.Printf("%v\n","OK")}


