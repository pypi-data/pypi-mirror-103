// @dart=2.9
import 'package:sprintf/sprintf.dart';

class Colors {
  ST0 RED;
  ST1 GREEN;
  ST2 BLUE;

  String RED = "red";
  String GREEN = "green";
  String BLUE = "blue";
}

show() {
  var color_map = {Colors.RED: "1", Colors.GREEN: "2", Colors.BLUE: "3"};
  var a = Colors.GREEN;

  if (a == Colors.GREEN) {
    print(sprintf("%s", ["green"]));
  } else {
    print(sprintf("%s", ["Not green"]));
  }
}

main() {
  show();
}
