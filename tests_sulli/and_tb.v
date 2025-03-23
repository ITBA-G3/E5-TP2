`include "and.v"

module and_tb();
  reg a, b;
  wire y;

  and_t  and1 (a, b, y);


  initial begin
    $dumpfile("and_tb.vcd");
    $dumpvars(0, and_tb);
    
    a = 0; b = 0;
    #10 a = 1;
    #10 b = 1;
    #10 a = 0;
    #10 b = 0;
    #10 $finish;
  end
endmodule