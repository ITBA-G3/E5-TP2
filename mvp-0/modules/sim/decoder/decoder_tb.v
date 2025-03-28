`timescale 1ns/1ps

module tb_decoder;

    reg [31:0] instr;
    
    wire        isALUreg;
    wire        isALUimm;
    wire        isBranch;
    wire        isJALR;
    wire        isJAL;
    wire        isAUIPC;
    wire        isLUI;
    wire        isLoad;
    wire        isStore;
    wire        isSYSTEM;
    
    wire [31:0] Uimm, Iimm, Simm, Bimm, Jimm;
    wire [4:0]  rs1Id, rs2Id, rdId;
    wire [2:0]  funct3;
    wire [6:0]  funct7;
    
    decoder dut (
        .instr(instr),
        .isALUreg(isALUreg),
        .isALUimm(isALUimm),
        .isBranch(isBranch),
        .isJALR(isJALR),
        .isJAL(isJAL),
        .isAUIPC(isAUIPC),
        .isLUI(isLUI),
        .isLoad(isLoad),
        .isStore(isStore),
        .isSYSTEM(isSYSTEM),
        .Uimm(Uimm),
        .Iimm(Iimm),
        .Simm(Simm),
        .Bimm(Bimm),
        .Jimm(Jimm),
        .rs1Id(rs1Id),
        .rs2Id(rs2Id),
        .rdId(rdId),
        .funct3(funct3),
        .funct7(funct7)
    );
    
    initial begin
        // Optional: Dump waveforms to a VCD file for viewing with a waveform viewer
        $dumpfile("tb_decoder.vcd");
        $dumpvars(0, tb_decoder);
        
        // Test 1: ALU register instruction (R-type, opcode 0110011)
        // Example instruction: 0x00A50533 (funct7=0, rs2=10, rs1=5, funct3=0, rd=10, opcode=0110011)
        instr = 32'h00A50533;
        #10;
        $display("Time %0t: R-type -> instr = %h, isALUreg = %b", $time, instr, isALUreg);
        
        // Test 2: ALU immediate instruction (I-type, opcode 0010011)
        // Example: 0x00A58513 (ADDI with opcode 0010011)
        instr = 32'h00A58513;
        #10;
        $display("Time %0t: I-type -> instr = %h, isALUimm = %b", $time, instr, isALUimm);
        
        // Test 3: Branch instruction (B-type, opcode 1100011)
        // Example: 0xFE000EE3 (a branch instruction)
        instr = 32'hFE000EE3;
        #10;
        $display("Time %0t: B-type -> instr = %h, isBranch = %b", $time, instr, isBranch);
        
        // Test 4: JALR instruction (I-type, opcode 1100111)
        // Example: 0x00008067 (a JALR instruction)
        instr = 32'h00008067;
        #10;
        $display("Time %0t: JALR -> instr = %h, isJALR = %b", $time, instr, isJALR);
        
        // Test 5: JAL instruction (J-type, opcode 1101111)
        // Example: 0x0000006F (a minimal JAL instruction)
        instr = 32'h0000006F;
        #10;
        $display("Time %0t: JAL -> instr = %h, isJAL = %b", $time, instr, isJAL);
        
        // Test 6: AUIPC instruction (U-type, opcode 0010111)
        // Example: 0x00000517
        instr = 32'h00000517;
        #10;
        $display("Time %0t: AUIPC -> instr = %h, isAUIPC = %b", $time, instr, isAUIPC);
        
        // Test 7: LUI instruction (U-type, opcode 0110111)
        // Example: 0x12345037
        instr = 32'h12345037;
        #10;
        $display("Time %0t: LUI -> instr = %h, isLUI = %b", $time, instr, isLUI);
        
        $finish;
    end
endmodule