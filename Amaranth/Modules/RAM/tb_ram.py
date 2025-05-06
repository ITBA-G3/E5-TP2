from amaranth import *
from amaranth.sim import *
from amaranth_boards import arty_a7
from ram import RAM

ram = RAM()

test_data = [
    (0x00000000, 0x00000000),
    (0x11111111, 0x00000002),
    (0x22222222, 0x00000004),
    (0x33333333, 0x00000006),
    (0x44444444, 0x00000008),
    (0x55555555, 0x0000000A),
    (0x66666666, 0x0000000C),
    (0x77777777, 0x0000000E),
    (0x88888888, 0x00000010),
    (0x99999999, 0x00000012),
    (0xAAAAAAAA, 0x00000014),
    (0xBBBBBBBB, 0x00000016),
    (0xCCCCCCCC, 0x00000018),
    (0xDDDDDDDD, 0x0000001A),
    (0xEEEEEEEE, 0x0000001C),
    (0xFFFFFFFF, 0x0000001E)
]

async def ram_tb(ctx):
    # Initialize the RAM
    ctx.set(ram.addr_reg, 0x00)
    ctx.set(ram.data_in_reg, 0x00)
    ctx.set(ram.write_en, 1)
    ctx.set(ram.read_en, 0)
    
    # Write test data to RAM
    for data, addr in test_data:
        ctx.set(ram.addr_reg, addr)
        ctx.set(ram.data_in_reg, data)
        ctx.set(ram.write_en, 1)
        ctx.set(ram.read_en, 0)
    
        await ctx.tick().repeat(2)   # Wait 2 clock cycles for stable data
    
    # Read back the data
    for _, addr in test_data:
        ctx.set(ram.addr_reg, addr)
        ctx.set(ram.write_en, 0)
        ctx.set(ram.read_en, 1)
    
        await ctx.tick().repeat(2)
    
        data = ctx.get(ram.data_out_reg)
        addr = ctx.get(ram.addr_reg)
        print(f"Read data: {data:#010x} from address: {addr:#010x}")
    
sim = Simulator(ram)
sim.add_clock(1e-6)  # 1 MHz clock
sim.add_testbench(ram_tb)

with sim.write_vcd("ram.vcd"):
    sim.run()