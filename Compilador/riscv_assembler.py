# riscv_assembler_full.py

REGISTER_MAP = {f"x{i}": i for i in range(32)}

ISA = {
    # R-type
    'add':  {'type': 'R', 'opcode': '0110011', 'funct3': '000', 'funct7': '0000000'},
    'sub':  {'type': 'R', 'opcode': '0110011', 'funct3': '000', 'funct7': '0100000'},
    'and':  {'type': 'R', 'opcode': '0110011', 'funct3': '111', 'funct7': '0000000'},
    'or':   {'type': 'R', 'opcode': '0110011', 'funct3': '110', 'funct7': '0000000'},

    # I-type
    'addi': {'type': 'I', 'opcode': '0010011', 'funct3': '000'},
    'lw':   {'type': 'I', 'opcode': '0000011', 'funct3': '010'},
    'jalr': {'type': 'I', 'opcode': '1100111', 'funct3': '000'},

    # S-type
    'sw':   {'type': 'S', 'opcode': '0100011', 'funct3': '010'},

    # B-type
    'beq':  {'type': 'B', 'opcode': '1100011', 'funct3': '000'},
    'bne':  {'type': 'B', 'opcode': '1100011', 'funct3': '001'},

    # U-type
    'lui':  {'type': 'U', 'opcode': '0110111'},
    'auipc':{'type': 'U', 'opcode': '0010111'},

    # J-type
    'jal':  {'type': 'J', 'opcode': '1101111'},
}

def reg_bin(reg): return format(REGISTER_MAP[reg], '05b')
def imm_bin(imm, bits): return format(int(imm) & ((1 << bits) - 1), f'0{bits}b')

def encode_r(inst, args):
    rd, rs1, rs2 = map(reg_bin, args)
    f = ISA[inst]
    return f['funct7'] + rs2 + rs1 + f['funct3'] + rd + f['opcode']

def encode_i(inst, args):
    rd, rs1, imm = args
    rd, rs1 = map(reg_bin, [rd, rs1])
    imm = imm_bin(imm, 12)
    f = ISA[inst]
    return imm + rs1 + f['funct3'] + rd + f['opcode']

def encode_s(inst, args):
    rs2, offset_reg = args
    offset, rs1 = offset_reg.strip(')').split('(')
    rs1 = reg_bin(rs1)
    rs2 = reg_bin(rs2)
    imm = imm_bin(offset, 12)
    f = ISA[inst]
    return imm[:7] + rs2 + rs1 + f['funct3'] + imm[7:] + f['opcode']

def encode_b(inst, args):
    rs1, rs2, imm = args
    rs1, rs2 = map(reg_bin, [rs1, rs2])
    imm = imm_bin(imm, 13)  # 13 bits to include sign
    return imm[0] + imm[2:8] + rs2 + rs1 + ISA[inst]['funct3'] + imm[8:12] + imm[1] + ISA[inst]['opcode']

def encode_u(inst, args):
    rd, imm = args
    rd = reg_bin(rd)
    imm = imm_bin(imm, 32)[:20]
    return imm + rd + ISA[inst]['opcode']

def encode_j(inst, args):
    rd, imm = args
    rd = reg_bin(rd)
    imm = imm_bin(imm, 21)  # 21 bits to include sign
    return imm[0] + imm[10:20] + imm[9] + imm[1:9] + rd + ISA[inst]['opcode']

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

    tokens = [tok.strip() for tok in line.replace(',', ' ').split()]
    inst = tokens[0]
    args = tokens[1:]

    if inst not in ISA:
        raise ValueError(f"Instrucción no soportada: {inst}")

    itype = ISA[inst]['type']
    binary = ENCODERS[itype](inst, args)
    hex_out = format(int(binary, 2), '08x')
    return hex_out

def assemble_program(lines):
    result = []
    for line in lines:
        try:
            hexcode = assemble_line(line)
            if hexcode:
                result.append(hexcode)
        except Exception as e:
            print(f"Error en línea '{line}': {e}")
    return result

# === Ejemplo de uso ===
if __name__ == "__main__":
    lines = [
        "addi x3,x0,13",   #// n
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
        "bne x5,x3,-5",
        "beq x5,x3,3",     #//DEVOLVER RESULTADO

        "add x7,x2,x0",    #//ACÁ DEVUELVO 1
        "jal x0,10",

        "add x7,x4,x0",    #//ACÁ DEVUELVO EL RESULTADO
        "jal x0,10"
    ]

    hexes = assemble_program(lines)
    for i, h in enumerate(hexes):
        print(f"0x{h},")
