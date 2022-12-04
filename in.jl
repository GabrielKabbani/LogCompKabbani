fn soma(x: i32, y: i32) -> i32 { var a: i32;
a = x + y;
Print(a);
return a; }
fn Main() { var a: i32; var b: i32; a = 3;
  b = soma(a, 4);
  Print(a);
  Print(b);
}