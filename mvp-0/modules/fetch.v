module fetch (
    input  clk,
    input  resetn,          // active-low reset
    output reg [31:0] instr,
    output reg [31:0] pc
);
   // Instruction memory (256 words)
   reg [31:0] MEM [0:255];
   
   // Initialize PC and memory with sample instructions
   initial begin
      pc = 0;
      // Initialize with a NOP instruction: add x0, x0, x0
      MEM[0] = 32'b0000000_00000_00000_000_00000_0110011;
      
      // Example instructions:
      // add x1, x0, x0
      MEM[1] = 32'b0000000_00000_00000_000_00001_0110011;
      // addi x1, x1, 1
      MEM[2] = 32'b000000000001_00001_000_00001_0010011;
   end

   always @(posedge clk) begin
      if (!resetn) begin
         pc    <= 0;
         instr <= 32'b0000000_00000_00000_000_00000_0110011; // NOP on reset
      end else begin
         instr <= MEM[pc];
         pc    <= pc + 1;
      end
   end
endmodule

