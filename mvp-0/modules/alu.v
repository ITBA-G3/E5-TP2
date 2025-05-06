module alu(
    input wire [31:0] A, B,
    input wire [2:0] func3,
    input wire [6:0] func7,
    input wire [4:0] shamt,

    input wire isALUreg,
    input wire isALUimm,
    input wire isBranch,
    input wire isJALR,
    input wire isJAL,
    input wire isAUIPC,
    input wire isLUI,
    input wire isLoad,
    input wire isStore,

    output reg EQ, EQM, EQM_U,
    output reg [31:0] Q

    
);

always @(*) 
begin
        Q = 32'b0;

        if (isALUreg || isALUimm) 
        begin
            case (func3)
                3'b000: 
                begin
                    if (func7[5] && isALUreg)
                        Q = A - B;
                    else 
                        Q = A + B;
                end
                3'b111: Q = A & B;
                3'b110: Q = A | B;
                3'b100: Q = A ^ B;
                3'b001: Q = A << shamt;
                3'b101: Q = (func7[5]) ? (A >>> shamt) : (A >> shamt);
                3'b010: Q = ($signed(A) < $signed(B)) ? 32'b1 : 32'b0;
                3'b011: Q = (A < B) ? 32'b1 : 32'b0;
                default: Q = 32'b0;
            endcase
        end
        else if (isAUIPC) 
        begin
            Q = A + B;
        end
        else if (isLUI) 
        begin
            Q = B;
        end
        else if (isJAL || isJALR) 
        begin
            Q = A + 4;
        end
        else if (isLoad || isStore) 
        begin
            Q = A + B;
        end
        else 
        begin
            Q = 32'b0;
        end
    end

endmodule