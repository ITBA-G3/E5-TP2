module decoder (
    input  [31:0] instr,
    
    // Instruction type flags
    output        isALUreg,  // rd <- rs1 OP rs2
    output        isALUimm,  // rd <- rs1 OP Iimm
    output        isBranch,  // if(rs1 OP rs2) PC<-PC+Bimm
    output        isJALR,    // rd <- PC+4; PC<-rs1+Iimm
    output        isJAL,     // rd <- PC+4; PC<-PC+Jimm
    output        isAUIPC,   // rd <- PC + Uimm
    output        isLUI,     // rd <- Uimm
    output        isLoad,    // rd <- mem[rs1+Iimm]
    output        isStore,   // mem[rs1+Simm] <- rs2
    output        isSYSTEM,  // SYSTEM (e.g., ebreak)
    
    // Immediate values in different formats
    output [31:0] Uimm,
    output [31:0] Iimm,
    output [31:0] Simm,
    output [31:0] Bimm,
    output [31:0] Jimm,
    
    // Register identifiers and function codes
    output [4:0]  rs1Id,
    output [4:0]  rs2Id,
    output [4:0]  rdId,
    output [2:0]  funct3,
    output [6:0]  funct7
);

   // Determine instruction type by opcode (bits [6:0])
   assign isALUreg = (instr[6:0] == 7'b0110011);
   assign isALUimm = (instr[6:0] == 7'b0010011);
   assign isBranch = (instr[6:0] == 7'b1100011);
   assign isJALR   = (instr[6:0] == 7'b1100111);
   assign isJAL    = (instr[6:0] == 7'b1101111);
   assign isAUIPC  = (instr[6:0] == 7'b0010111);
   assign isLUI    = (instr[6:0] == 7'b0110111);
   assign isLoad   = (instr[6:0] == 7'b0000011);
   assign isStore  = (instr[6:0] == 7'b0100011);
   assign isSYSTEM = (instr[6:0] == 7'b1110011);

   // Immediate formats
   assign Uimm = {instr[31], instr[30:12], 12'b0};
   assign Iimm = {{21{instr[31]}}, instr[30:20]};
   assign Simm = {{21{instr[31]}}, instr[30:25], instr[11:7]};
   assign Bimm = {{20{instr[31]}}, instr[7], instr[30:25], instr[11:8], 1'b0};
   assign Jimm = {{12{instr[31]}}, instr[19:12], instr[20], instr[30:21], 1'b0};

   // Register fields
   assign rs1Id = instr[19:15];
   assign rs2Id = instr[24:20];
   assign rdId  = instr[11:7];

   // Function codes
   assign funct3 = instr[14:12];
   assign funct7 = instr[31:25];
   
endmodule

