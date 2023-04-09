import sys
from binascii import hexlify
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

if len(sys.argv) < 3:
    print('Usage: hex_to_verilog.py <input_bin_file> <output_v_file>')
    sys.exit(1)

with open(sys.argv[1], 'rb') as f:
    f_data = hexlify(f.read()).decode('utf-8')
cells = parse_hex(f_data, DEFAULT_CELL_SIZE, DEFAULT_ENDIANNESS)
with open(sys.argv[2], 'w') as f:
    write_data(cells, DEFAULT_ADDRESS_SIZE, DEFAULT_CELL_SIZE, f)