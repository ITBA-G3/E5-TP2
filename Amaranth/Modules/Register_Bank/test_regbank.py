from amaranth import *
from amaranth.sim import Simulator
from regbank import RegBank

regbank = RegBank()

i = 0
j = 0

async def proc(ctx):
    global i
    global j
    ctx.set(regbank.we, 1)
    #this anidated "for" loop tests all 32 registers, one by one 
    #the first iteration should print all zeros, bc register 0 isn't writable.
    for i in range(32):
        ctx.set(regbank.rs1_addr,i)
        ctx.set(regbank.rd_addr,i)
        print("rs1_addr: {:05b}".format(i))
        for j in range(0xA): #funny way to say ten
            ctx.set(regbank.rd_data, 1 << 22+j)
            await ctx.tick()
            salida = ctx.get(regbank.rs1_data)
            print("rs1_data: {:032b}".format(salida)) 
    #this part tests the "write enable" function
    ctx.set(regbank.we, 0) 
    #this should print the same values 
    #as before, without changes in the 2 lsb
    for i in range(4):      
        ctx.set(regbank.rs1_addr,i)
        ctx.set(regbank.rd_addr,i)
        ctx.set(regbank.rd_data, 1)
        await ctx.tick()
        salida = ctx.get(regbank.rs1_data)
        print("rs1_data: {:032b}".format(salida)) 

sim = Simulator(regbank)
sim.add_clock(1e-6)  # 1 MHz clock
sim.add_testbench(proc)

with sim.write_vcd('regbank_test.vcd'):
    sim.run_until(36 * 10 * 1e-6)  # Run for 20 ms

