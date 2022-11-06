
  {
    // v2.2 testing
    var x_1: i32;
    
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
    while ((x_1 > 1) || (x_1 == 1)) {x_1 = x_1 - 1; Print(x_1);}
}