# riscv_assembler_rv32i.py

REGISTER_MAP = {f"x{i}": i for i in range(32)}

ISA = {
    # R-type
    'add':  {'type': 'R', 'opcode': '0110011', 'funct3': '000', 'funct7': '0000000'},
    'sub':  {'type': 'R', 'opcode': '0110011', 'funct3': '000', 'funct7': '0100000'},
    'sll':  {'type': 'R', 'opcode': '0110011', 'funct3': '001', 'funct7': '0000000'},
    'slt':  {'type': 'R', 'opcode': '0110011', 'funct3': '010', 'funct7': '0000000'},
    'sltu': {'type': 'R', 'opcode': '0110011', 'funct3': '011', 'funct7': '0000000'},
    'xor':  {'type': 'R', 'opcode': '0110011', 'funct3': '100', 'funct7': '0000000'},
    'srl':  {'type': 'R', 'opcode': '0110011', 'funct3': '101', 'funct7': '0000000'},
    'sra':  {'type': 'R', 'opcode': '0110011', 'funct3': '101', 'funct7': '0100000'},
    'or':   {'type': 'R', 'opcode': '0110011', 'funct3': '110', 'funct7': '0000000'},
    'and':  {'type': 'R', 'opcode': '0110011', 'funct3': '111', 'funct7': '0000000'},

    # I-type (incluye shifts con shamt)
    'addi':  {'type': 'I', 'opcode': '0010011', 'funct3': '000'},
    'slti':  {'type': 'I', 'opcode': '0010011', 'funct3': '010'},
    'sltiu': {'type': 'I', 'opcode': '0010011', 'funct3': '011'},
    'xori':  {'type': 'I', 'opcode': '0010011', 'funct3': '100'},
    'ori':   {'type': 'I', 'opcode': '0010011', 'funct3': '110'},
    'andi':  {'type': 'I', 'opcode': '0010011', 'funct3': '111'},
    'slli':  {'type': 'I', 'opcode': '0010011', 'funct3': '001', 'funct7': '0000000'},
    'srli':  {'type': 'I', 'opcode': '0010011', 'funct3': '101', 'funct7': '0000000'},
    'srai':  {'type': 'I', 'opcode': '0010011', 'funct3': '101', 'funct7': '0100000'},
    'jalr':  {'type': 'I', 'opcode': '1100111', 'funct3': '000'},
    'lb':    {'type': 'I', 'opcode': '0000011', 'funct3': '000'},
    'lh':    {'type': 'I', 'opcode': '0000011', 'funct3': '001'},
    'lw':    {'type': 'I', 'opcode': '0000011', 'funct3': '010'},
    'lbu':   {'type': 'I', 'opcode': '0000011', 'funct3': '100'},
    'lhu':   {'type': 'I', 'opcode': '0000011', 'funct3': '101'},

    # S-type
    'sb':    {'type': 'S', 'opcode': '0100011', 'funct3': '000'},
    'sh':    {'type': 'S', 'opcode': '0100011', 'funct3': '001'},
    'sw':    {'type': 'S', 'opcode': '0100011', 'funct3': '010'},

    # B-type
    'beq':   {'type': 'B', 'opcode': '1100011', 'funct3': '000'},
    'bne':   {'type': 'B', 'opcode': '1100011', 'funct3': '001'},
    'blt':   {'type': 'B', 'opcode': '1100011', 'funct3': '100'},
    'bge':   {'type': 'B', 'opcode': '1100011', 'funct3': '101'},
    'bltu':  {'type': 'B', 'opcode': '1100011', 'funct3': '110'},
    'bgeu':  {'type': 'B', 'opcode': '1100011', 'funct3': '111'},

    # U-type
    'lui':   {'type': 'U', 'opcode': '0110111'},
    'auipc': {'type': 'U', 'opcode': '0010111'},

    # J-type
    'jal':   {'type': 'J', 'opcode': '1101111'},
}

def reg_bin(r): return format(REGISTER_MAP[r], '05b')
def imm_bin(val, bits): return format(int(val) & ((1 << bits) - 1), f'0{bits}b')

def encode_r(inst, args):
    rd, rs1, rs2 = map(reg_bin, args)
    f = ISA[inst]
    return f['funct7'] + rs2 + rs1 + f['funct3'] + rd + f['opcode']

def encode_i(inst, args):
    f = ISA[inst]
    if inst in ['slli', 'srli', 'srai']:
        rd, rs1, shamt = args
        rd = reg_bin(rd)
        rs1 = reg_bin(rs1)
        shamt = imm_bin(shamt, 5)
        return f['funct7'] + shamt + rs1 + f['funct3'] + rd + f['opcode']
    else:
        rd, rs1, imm = args
        return imm_bin(imm, 12) + reg_bin(rs1) + f['funct3'] + reg_bin(rd) + f['opcode']

def encode_s(inst, args):
    rs2, offset_base = args
    offset, rs1 = offset_base.strip(')').split('(')
    imm = imm_bin(offset, 12)
    return imm[:7] + reg_bin(rs2) + reg_bin(rs1) + ISA[inst]['funct3'] + imm[7:] + ISA[inst]['opcode']

def encode_b(inst, args):
    rs1, rs2, imm = args
    imm = imm_bin(imm, 13)
    return imm[0] + imm[2:8] + reg_bin(rs2) + reg_bin(rs1) + ISA[inst]['funct3'] + imm[8:12] + imm[1] + ISA[inst]['opcode']

def encode_u(inst, args):
    rd, imm = args
    imm = imm_bin(imm, 32)[:20]
    return imm + reg_bin(rd) + ISA[inst]['opcode']

def encode_j(inst, args):
    rd, imm = args
    imm = imm_bin(imm, 21)
    return imm[0] + imm[10:20] + imm[9] + imm[1:9] + reg_bin(rd) + ISA[inst]['opcode']

ENCODERS = {
    'R': encode_r,
    'I': encode_i,
    'S': encode_s,
    'B': encode_b,
    'U': encode_u,
    'J': encode_j,
}

def assemble_line(line):
    line = line.strip().lower()
    if not line or line.startswith('#'):
        return None
    tokens = [t.strip() for t in line.replace(',', ' ').split()]
    inst, args = tokens[0], tokens[1:]
    if inst not in ISA:
        raise ValueError(f"Instrucción no soportada: {inst}")
    itype = ISA[inst]['type']
    binstr = ENCODERS[itype](inst, args)
    return format(int(binstr, 2), '08x')

def assemble_program(lines):
    return [assemble_line(line) for line in lines if assemble_line(line)]

# === Ejemplo de uso ===
if __name__ == "__main__":
    asm = [
        "addi x3,x0,25",   #// n
        "addi x1,x0,2",    #//i0
        "addi x2,x0,1",    #//i1
        "addi x4,x0,2",    #//resultado
        "addi x5,x0,2",    #//counter

        "bge  x1,x3,6",    #//DEVOLVER 1

        #//Inicio While
        "add x4,x1,x2",
        "add x2,x1,x0",
        "add x1,x4,x0",
        "addi x5,x5,1",
        "beq x5,x3,4",     #//DEVOLVER RESULTADO
        "bne x5,x3,-6",

        "add x7,x2,x0",    #//ACÁ DEVUELVO 1
        "jal x0,10",

        "add x0,x0,x0",

        "add x7,x4,x0",    #//ACÁ DEVUELVO EL RESULTADO
        "jal x0,10"
    ]

    for i, hexcode in enumerate(assemble_program(asm)):
        if i != len(asm)-1:
            print(f"0x{hexcode},    #",asm[i], f"   {i+1}")
        else:
            print(f"0x{hexcode}     #",asm[i], f"   {i+1}")
