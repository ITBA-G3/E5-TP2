module top (
    input  CLK,
    input  RESET,         // Assume an external active-high reset; invert as needed
    output [4:0] LEDS     // Just for showing something on the board
);
   wire clk;
   wire resetn = ~RESET;  // Assuming the external RESET is active active-high
   wire [31:0] instr;
   wire [31:0] pc;
   
   // Instantiate fetch module
   fetch fetch_inst (
       .clk(clk),
       .resetn(resetn),
       .instr(instr),
       .pc(pc)
   );
   
   // Instantiate Decoder module
   wire isALUreg, isALUimm, isBranch, isJALR, isJAL, isAUIPC, isLUI, isLoad, isStore, isSYSTEM;
   wire [31:0] Uimm, Iimm, Simm, Bimm, Jimm;
   wire [4:0] rs1Id, rs2Id, rdId;
   wire [2:0] funct3;
   wire [6:0] funct7;
   
   decoder decoder_inst (
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

   // Clock generation or division can be added here.
   assign clk = CLK;  // Direct connection for now

   assign LEDS = { isSYSTEM, isALUreg, isALUimm, isStore, isLoad };
   
endmodule

