
fun bubble_sort(seq: Array<Int>): Array<Int> {
val L = seq.size
for (_ in (0..L-1)) {
for (n in (1..L-1)) {
if(seq[n] < seq[(n - 1)]) {
if(true) {
__tmp1, __tmp2 = (seq[n], seq[(n - 1)])
seq[(n - 1)] = __tmp1
seq[n] = __tmp2
}
}
}
}
return seq}


fun main() {
var unsorted = arrayOf(14, 11, 19, 5, 16, 10, 19, 12, 5, 12)
val expected = arrayOf(5, 5, 10, 11, 12, 12, 14, 16, 19, 19)
assert(bubble_sort(unsorted) == expected)
println("OK")}


