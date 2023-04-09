import sys
from binascii import hexlify
import argparse
LITTLE = True
BIG = False
DEFAULT_ADDRESS_SIZE = 16
DEFAULT_CELL_SIZE = 32
DEFAULT_ENDIANNESS = LITTLE

def default(cell_size): return 0xdeadbeef % (1 << cell_size)

def parse_hex(f_data, cell_size, endian):
    hex_bytes = [f_data[i:i+2] for i in range(0, len(f_data), 2)]
    byte_width = cell_size // 8
    cells = [hex_bytes[i:i+byte_width] for i in range(0, len(hex_bytes), byte_width)]
    if endian == LITTLE:
        [cell.reverse() for cell in cells]
    cells = ["".join(cell) for cell in cells]
    cells = [int(cell, 16) for cell in cells]
    return cells

def write_data(cells, address_size, cell_size, f):
    f.write(f"always_comb begin\n")
    f.write(f"  case(addr)\n")
    for idx, cell in enumerate(cells):
        f.write(f"    {address_size}'h{idx:0{address_size // 4}x}: data <= ")
        f.write(f"{cell_size}'h{cell:0{cell_size // 4}x};\n")
    f.write(f"    default: data <= {cell_size}'h{default(cell_size):0{cell_size // 4}x};\n")
    f.write(f"  endcase\n")
    f.write(f"end")

parser = argparse.ArgumentParser(description='Hex to Verilog Translator')
parser.add_argument('infile', help='Input .bin file')
parser.add_argument('outfile', help='Output .v file')
parser.add_argument('-c', '--cell', type=int, action='store', help='the size of individual memory cells in ram')
parser.add_argument('-a', '--address', type=int, action='store', help='the size of addresses in ram')
endian_group = parser.add_mutually_exclusive_group()
endian_group.add_argument('-l', '--little', action='store_true', help='Set to little endian')
endian_group.add_argument('-b', '--big', action='store_true', help='Set to big endian')
args = parser.parse_args()

cell_size = args.cell if args.cell else DEFAULT_CELL_SIZE
address_size = args.address if args.address else DEFAULT_ADDRESS_SIZE
endian = BIG if args.big else LITTLE if args.little else DEFAULT_ENDIANNESS

with open(args.infile, 'rb') as f:
    f_data = hexlify(f.read()).decode('utf-8')
cells = parse_hex(f_data, cell_size, endian)
with open(args.outfile, 'w') as f:
    write_data(cells, address_size, cell_size, f)