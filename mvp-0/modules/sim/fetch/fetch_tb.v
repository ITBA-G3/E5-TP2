`timescale 1ns/1ps

module fetch_tb;
    wire [31:0] instr;
    wire [31:0] pc;

    reg clk;
    reg resetn = 0;


    initial begin
        clk = 0;   // Initialize clock signal
        resetn = 0;
    end

    always begin 
        #10
        clk = ~clk;
    end

    fetch dut(
        .clk(clk),
        .resetn(resetn),
        .instr(instr),
        .pc(pc)
    );
    
    initial begin
        $dumpfile("tb_fetch.vcd");
        $dumpvars(0, fetch_tb);

    // Verify that when resetn = 0 the PC stays in 0 and the instr stays NOP.
        #10;
        $display("PC=%d, Instruction =%h, resetn=%d, clk =%d",pc,instr,resetn,clk);
        
        #10;
        $display("PC=%d, Instruction =%h, resetn=%d, clk =%d",pc,instr,resetn,clk);
        
    // Resetn = 1 so now the PC should increase with every clk posedge.
        resetn = 1;

        #10;
        $display("PC=%d, Instruction =%h, resetn=%d, clk =%d",pc,instr,resetn,clk);
        
        #10;
        $display("PC=%d, Instruction = %h, resetn=%d",pc,instr,resetn);

        #10;
        $display("PC=%d, Instruction = %h, resetn=%d",pc,instr,resetn);
        
        #10;
        $display("PC=%d, Instruction =%h, resetn=%d, clk =%d",pc,instr,resetn,clk);
        
        #10;
        $display("PC=%d, Instruction = %h, resetn=%d",pc,instr,resetn);

        #10;
        $display("PC=%d, Instruction = %h, resetn=%d",pc,instr,resetn);
        
        $finish;
    end

endmodule