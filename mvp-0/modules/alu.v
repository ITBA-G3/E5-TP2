module alu(
    input wire [31:0] A, B,
    input wire [2:0] func3,
    input wire [6:0] func7,
    input wire [6:0] opcode,
    input wire [4:0] shamt,
    output reg EQ, EQM, EQM_U,
    output reg [31:0] Q
);

always @(*) 
begin
    case(opcode)
    /* Immediate Instructions and Record Upload */
        7'b0110111: //LUI
            Q = B;
        7'b0010111: //AUIPC
            Q = A + B;
        7'b1101111: //JAL
            Q = 0;
        7'b1100111: //JALR
            Q = A + B;

        /* Jumping Instructions */
        7'b1100011: //JUMP
            case(func3)
                3'b000: //BEQ
                    Q = A == B;
                3'b001: //BNQ
                    Q = A != B;
                3'b100: //BLT
                    Q = $signed(A) < $signed(B);
                3'b101: //BGE
                    Q = $signed(A) >= $signed(B);
                3'b110: //BLTU
                    Q = A < B;
                default: //BGEU
                    Q = A >= B;
            endcase

        /* Load and Store Instructions */
        7'b0000011:     //LOAD
            Q = A + B;

        7'b0100011:     //STORE
            Q = A + B;

        /* Immediate Instructions */
        7'b0010011:
            case(func3)
                3'b000: //ADDI
                    Q = A + B;
                3'b010: //SLTI, Q = 1 if A<B
                    Q = $signed(A) < $signed(B);
                3'b011: //SLTI Unsigned, Q = 1 if A<B
                    Q = A < B;
                3'b100: //XORI
                    Q = A ^ B;
                3'b110: //ORI
                    Q = A | B;
                3'b111: //ANDI
                    Q = A & B;
                3'b001: //SHIFT LEFT LOGICAL IMMEDIATE (SLLI)
                    Q = A << shamt;
                default:
                    Q = (func7[5]) ? (A >>> shamt) : (A >> shamt); //SRA or SRL
            endcase

        /* Operations */
        7'b0110011:
            case(func3)
                3'b000:
                    Q = (func7[5]) ? (A - B) : (A + B); //SUB or ADD
                3'b010: //SLT, Q = 1 if A<B
                    Q = A < B;
                3'b011: //SLT Unsigned, Q = 1 if A<B
                    Q = $signed(A) < $signed(B);
                3'b100: //XOR
                    Q = A ^ B;
                3'b001: //SHIFT LEFT LOGICAL
                    Q = A << shamt;
                3'b101:
                    Q = (func7[5]) ? (A >>> shamt) : (A >> shamt); //SRA or SRL
                3'b110: //OR
                    Q = A | B;
                default: //AND
                    Q = A & B;
            endcase
        default: //NOP
            Q = 0;
    endcase

    EQ = A == B;
    EQM = A > B;
    EQM_U = A < B;
end
endmodule