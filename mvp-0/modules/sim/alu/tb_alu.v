`timescale 1ns/1ps

module tb_alu;
    reg [31:0] A, B;
    reg [2:0] func3;
    reg [6:0] func7;
    reg [4:0] shamt;
    
    reg isALUreg;
    reg isALUimm;
    reg isBranch;
    reg isJALR;
    reg isJAL;
    reg isAUIPC;
    reg isLUI;
    reg isLoad;
    reg isStore;

    wire EQ, EQM, EQM_U;
    wire [31:0] Q;

    alu dut(
        .A(A),
        .B(B),
        .func3(func3),
        .func7(func7),
        .shamt(shamt),
        .isALUreg(isALUreg),
        .isALUimm(isALUimm),
        .isBranch(isBranch),
        .isJALR(isJALR),
        .isJAL(isJAL),
        .isAUIPC(isAUIPC),
        .isLUI(isLUI),
        .isLoad(isLoad),
        .isStore(isStore),
        .EQ(EQ),
        .EQM(EQM),
        .EQM_U(EQM_U),
        .Q(Q)
    );

    initial begin
        $dumpfile("tb_alu.vcd");
        $dumpvars(0, tb_alu);

        isALUreg = 0; 
        isALUimm = 0; 
        isBranch = 0; 
        isJALR = 0; 
        isJAL = 0;
        isAUIPC = 0; 
        isLUI = 0; 
        isLoad = 0; 
        isStore = 0;

        // Test 1: ADD (func3 = 000, func7 = 0000000)
        A = 32'h00000001;
        B = 32'h00000002;
        func3 = 3'b000;
        func7 = 7'b0000000;
        shamt = 0;
        isALUreg = 1;
        #10;
        $display("ADD -> A = %h, B = %h, Q = %h", A, B, Q);

        // Test 2: SUB (func3 = 000, func7 = 0100000)
        func7 = 7'b0100000;
        #10;
        $display("SUB -> A = %h, B = %h, Q = %h", A, B, Q);

        // Test 3: AND (func3 = 111)
        func3 = 3'b111;
        func7 = 7'b0000000;
        #10;
        $display("AND -> A = %h, B = %h, Q = %h", A, B, Q);

        // Test 4: OR (func3 = 110)
        func3 = 3'b110;
        #10;
        $display("OR -> A = %h, B = %h, Q = %h", A, B, Q);

        // Test 5: XOR (func3 = 100)
        func3 = 3'b100;
        #10;
        $display("XOR -> A = %h, B = %h, Q = %h", A, B, Q);

        // Test 6: SLL (func3 = 001)
        func3 = 3'b001;
        shamt = 5'd1;
        #10;
        $display("SLL -> A = %h, shamt = %d, Q = %h", A, shamt, Q);

        // Test 7: SRL (func3 = 101, func7 = 0000000)
        func3 = 3'b101;
        func7 = 7'b0000000;
        #10;
        $display("SRL -> A = %h, shamt = %d, Q = %h", A, shamt, Q);

        // Test 8: SRA (func3 = 101, func7 = 0100000)
        func7 = 7'b0100000;
        A = 32'hFFFFFFF0;  // valor negativo
        #10;
        $display("SRA -> A = %h, shamt = %d, Q = %h", A, shamt, Q);

        // Test 9: SLT (signed comparison)
        func3 = 3'b010;
        func7 = 7'b0000000;
        A = -5;
        B = 3;
        #10;
        $display("SLT -> A = %h, B = %h, Q = %h", A, B, Q);

        // Test 10: SLTU (unsigned comparison)
        func3 = 3'b011;
        A = 2;
        B = 3;
        #10;
        $display("SLTU -> A = %h, B = %h, Q = %h", A, B, Q);

        $finish;
    end
endmodule