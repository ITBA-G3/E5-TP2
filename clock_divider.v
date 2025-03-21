module clock_divider
(
  input CLK,      // Board CLK pin
  input RESET,    // Board RESET pin

  output clk,
);

parameter SLOW = 0;

generate

  if (SLOW != 0) begin
    localparam slow_bit = SLOW;
    reg [slow_bit:0] slow_CLK = 0;
    
    always @(posedge CLK) begin
      slow_CLK <= slow_CLK + 1;
    end

    assign clk = slow_CLK[slow_bit];

  end

  // I may be missing some ifdefs for bench contexts
  // gh/BrunoLevy/learn-fpga/FemtoRV/TUTORIALS/FROM_BLINKER_TO_RICSV/clockworks.v
