from amaranth import *
from amaranth_boards import arty_a7

class RAM(Elaboratable):
    
    def __init__(self):
        self.read_en = Signal(1)
        self.write_en = Signal(1)
        self.addr_reg = Signal(32)
        self.data_in_reg = Signal(32)
        self.data_out_reg = Signal(32)
        
        # Define the RAM size and address width
        ram_size = 256
        word_size = 32   # 4 byte words
        
        self.ram = Memory(width=word_size, depth=ram_size)
        
        self.read_port = self.ram.read_port()
        self.write_port = self.ram.write_port()
        
    def elaborate(self, platform):
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