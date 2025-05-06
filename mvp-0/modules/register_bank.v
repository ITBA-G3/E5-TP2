//Falta la parte de la comunicación con la memoria

module reg_bank(input wire clk,             // clock signal
                input wire [4:0] rs1Id,     // 5-bit register address for rs1
                input wire [4:0] rs2Id,     // 5-bit register address for rs2
                input wire [4:0] rdId,      // 5-bit register address for rd
                input wire wr_en,           // write enable for storing rd_data
                input wire [31:0] rd_data,      
                output reg [31:0] rs1_data, 
                output reg [31:0] rs2_data);

    reg [31:0] regBank [0:31];
    // the writing process is done with a clk-syncronous block
    // 
    always @(posedge clk) begin
        if(wr_en && rdId != 0) begin
            regBank[rdId] <= rd_data;
        end
    end

    // the reading process is done with a combinational block
    // whenever an input changes, the output is updated
    always @(*) begin
        rs1_data = regBank[rs1Id];
        rs2_data = regBank[rs2Id];
    end

endmodule
