from amaranth import *
from amaranth_boards import arty_a7
from amaranth.lib import wiring
from amaranth.lib.wiring import In, Out

class RAM(wiring.Component):
    read_en: In(1)
    write_en: In(1)
    
    addr_reg: In(32)
    data_in_reg: In(32)
    data_out_reg: Out(32)
        
    # If wiring.Component is not used, the following lines should be uncommented
    # def __init__(self):    
    #     # Define the RAM size and address width
    
    # self.read_en = Signal(1)
    # self.write_en = Signal(1)
    # self.addr_reg = Signal(32)
    # self.data_in_reg = Signal(32)
    # self.data_out_reg = Signal(32)
        
    def elaborate(self, platform):
        ram_size = 256
        word_size = 32   # 4 byte words
        
        self.ram = Memory(width=word_size, depth=ram_size)
        
        self.read_port = self.ram.read_port()
        self.write_port = self.ram.write_port()
        
        m = Module()
        
        # Link the ports to the module
        m.submodules.ram = self.ram
        
        with m.If(self.write_en):
            m.d.comb += [
                self.write_port.addr.eq(self.addr_reg),
                self.write_port.en.eq(self.write_en),
                self.write_port.data.eq(self.data_in_reg)
            ]
        with m.Elif(self.read_en):      # Can i r/w simultaneously? for now, no
            m.d.comb += [
                self.read_port.addr.eq(self.addr_reg),
                self.read_port.en.eq(self.read_en),
                self.data_out_reg.eq(self.read_port.data)
            ]
        
        return m