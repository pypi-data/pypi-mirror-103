// @dart=2.9
import 'package:sprintf/sprintf.dart';


List<int> comb_sort(List<int> seq) {
var gap = seq.length;
bool swap = true;
while (gap > 1||swap) {
gap = max(1, floor((gap/1.25)));
swap = false;
for (final i in ([for(var i = 0; i < (seq.length - gap); i += 1) i])) {


if(seq[i] > seq[(i + gap)]) {


({
['__tmp1', '__tmp2'] = (seq[(i + gap)], seq[i]);
seq[i] = __tmp1;
seq[(i + gap)] = __tmp2;
;
})
swap = true;
}
}
}
return seq;}


 main() {
var unsorted = [14, 11, 19, 5, 16, 10, 19, 12, 5, 12];
var expected = [5, 5, 10, 11, 12, 12, 14, 16, 19, 19];
assert(comb_sort(unsorted) == expected);
print(sprintf("%s", ["OK"]));}


