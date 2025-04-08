`timescale 1ns/1ps

module tb_alu;
    reg [31:0] A, B;
    reg [2:0] func3;
    reg [6:0] func7;
    reg [6:0] opcode;
    reg [4:0] shamt;

    wire EQ, EQM, EQM_U;
    wire [31:0] Q;

    alu dut(
        .A(A),
        .B(B),
        .func3(func3),
        .func7(func7),
        .opcode(opcode),
        .shamt(shamt),
        .EQ(EQ),
        .EQM(EQM),
        .EQM_U(EQM_U),
        .Q(Q)
    );

    initial begin
        $dumpfile("tb_alu.vcd");
        $dumpvars(0, tb_alu);

        // Test 1: ADD (opcode = 0110011, func3 = 000, func7 = 0000000)
        A = 32'h00000001;
        B = 32'h00000002;
        opcode = 7'b0110011;
        func3 = 3'b000;
        func7 = 7'b0000000;
        #10;
        $display("Test 1: ADD (opcode = 0110011, func3 = 000, func7 = 0000000)");
        $display("Time %0t: ADD -> A = %h, B = %h, Q = %h", $time, A, B, Q);

        #10;

        // Test 2: SUB (opcode = 0110011, func3 = 000, func7 = 0100000)
        func7 = 7'b0100000;
        #10;
        $display("Test 2: SUB (opcode = 0110011, func3 = 000, func7 = 0100000)");
        $display("Time %0t: SUB -> A = %h, B = %h, Q = %h", $time, A, B, Q);

        #10;

        // Test 3: AND (opcode = 0110011, func3 = 111, func7 = 0000000)
        func3 = 3'b111;
        func7 = 7'b0000000;
        #10;
        $display("Test 3: AND (opcode = 0110011, func3 = 111, func7 = 0000000)");
        $display("Time %0t: AND -> A = %h, B = %h, Q = %h", $time, A, B, Q);

        #10;

        // Test 4: OR (opcode = 0110011, func3 = 110, func7 = 0000000)
        func3 = 3'b110;
        #10;
        $display("Test 4: OR (opcode = 0110011, func3 = 110, func7 = 0000000)");
        $display("Time %0t: OR -> A = %h, B = %h, Q = %h", $time, A, B, Q);

        #10;

        // Test 5: XOR (opcode = 0110011, func3 = 100, func7 = 0000000)
        func3 = 3'b100;
        #10;
        $display("Test 5: XOR (opcode = 0110011, func3 = 100, func7 = 0000000)");
        $display("Time %0t: XOR -> A = %h, B = %h, Q = %h", $time, A, B, Q);

        #10;

        // Test 6: SLL (opcode = 0110011, func3 = 001, func7 = 0000000)
        func3 = 3'b001;
        shamt = 5'b00001;
        #10;
        $display("Test 6: SLL (opcode = 0110011, func3 = 001, func7 = 0000000)");
        $display("Time %0t: SLL -> A = %h, B = %h, Q = %h", $time, A, B, Q);

        #10;

        // Test 7: SRL (opcode = 0110011, func3 = 101, func7 = 0000000)
        func3 = 3'b101;
        #10;
        $display("Test 7: SRL (opcode = 0110011, func3 = 101, func7 = 0000000)");
        $display("Time %0t: SRL -> A = %h, B = %h, Q = %h", $time, A, B, Q);

        #10;

        // Test 8: SRA (opcode = 0110011, func3 = 101, func7 = 0100000)
        func7 = 7'b0100000;
        #10;
        $display("Test 8: SRA (opcode = 0110011, func3 = 101, func7 = 0100000)");
        $display("Time %0t: SRA -> A = %h, B = %h, Q = %h", $time, A, B, Q);

        #10;

        // Test 9: SLT (opcode = 0110011, func3 = 010, func7 = 0000000)
        func3 = 3'b010;
        A = -7;
        B = 6;
        #10;
        $display("Test 9: SLT (opcode = 0110011, func3 = 010, func7 = 0000000)");
        $display("Time %0t: SLT -> A = %h, B = %h, Q = %h", $time, A, B, Q);

        #10;

        // Test 10: SLTU (opcode = 0110011, func3 = 011, func7 = 0000000)
        func3 = 3'b011;
        A = 2;
        B = 3;
        #10;
        $display("Test 10: SLTU (opcode = 0110011, func3 = 011, func7 = 0000000)");
        $display("Time %0t: SLTU -> A = %h, B = %h, Q = %h", $time, A, B, Q);

        #10;

        $finish;
    end
endmodule
