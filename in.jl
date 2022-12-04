
fn soma(x: i32, y: i32) -> i32
{
    return x + y;
}

fn Main()
{
// v2.3 testing
var x_1: i32;
x_1 = 2;
x_1 = soma(1, x_1);

x_1 = Read();
if ((x_1 > 1) && !(x_1 < 1)) {
    x_1 = 3;
}
else {
    {
    x_1 = (-20+30)*4*3/40;;;;; // teste de comentario
    }
}
Print(x_1);
x_1 = Read();
if ((x_1 > 1) && !(x_1 < 1))
    x_1 = 3;
else
    x_1 = (-20+30)*12/40;;;;;

Print(x_1);
while ((x_1 > 1) || (x_1 == 1)) {x_1 = x_1 - 1;Print(x_1);}}