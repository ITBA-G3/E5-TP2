# How to simulate

## Writing a simulation file

Start by setting the timescale at the top of the file and defining the testbench signals.

```verilog
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
    ...
endmodule
```

Instantiate your device under testing

```verilog
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
```

Next write some test cases inside an `initial begin` block. Remember to dump the waveforms to a `.vcd` file so you can analyze them in GTKWave later.

```verilog
$dumpfile("tb_decoder.vcd");
$dumpvars(0, tb_decoder);

// Test 1: ALU register instruction (R-type, opcode 0110011)
// Example instruction: 0x00A50533 (funct7=0, rs2=10, rs1=5, funct3=0, rd=10, opcode=0110011)
instr = 32'h00A50533;
#10;
$display("Time %0t: R-type -> instr = %h, isALUreg = %b", $time, instr, isALUreg);

$finish;

```

Make sure to write some clean test cases for your friends' sake.

## Running the simulation

The quickest and easiest way to run the simulation is to use `iverilog`. Make a folder for your simulation output files. I named mine `decoder`.

Then run
```
iverilog -o decoder_sim ../../decoder.v tb_decoder.v
```

Then executhe the simulation

```
vvp decoder_sim
```

And finally, check it out in GTKWave with

```
gtkwave tb_decoder.vcd
```