import struct
import glob
import sys
import os

def parse_png(filepath):
    print(f"--- {os.path.basename(filepath)} ---")
    try:
        with open(filepath, 'rb') as f:
            signature = f.read(8)
            if signature != b'\x89PNG\r\n\x1a\n':
                print("Not a valid PNG signature")
                return

            while True:
                chunk_len_data = f.read(4)
                if not chunk_len_data:
                    break
                chunk_len = struct.unpack('>I', chunk_len_data)[0]
                chunk_type = f.read(4).decode('ascii', errors='ignore')
                
                print(f"Chunk: {chunk_type}, Length: {chunk_len}")
                
                if chunk_type == 'IHDR':
                    data = f.read(chunk_len)
                    width, height, bit_depth, color_type, compression, filter_method, interlace = struct.unpack('>IIBBBBB', data)
                    print(f"  IHDR: Width={width}, Height={height}, BitDepth={bit_depth}, ColorType={color_type}, Comp={compression}, Filter={filter_method}, Interlace={interlace}")
                elif chunk_type in ['tEXt', 'zTXt', 'iTXt']:
                    data = f.read(chunk_len)
                    print(f"  Data: {data}")
                else:
                    f.seek(chunk_len, 1) # Skip data
                
                f.read(4) # Skip CRC
                
                if chunk_type == 'IEND':
                    break
    except Exception as e:
        print(f"Error: {e}")

files = glob.glob('challenges/swimmer2026/rain/images/*.png')
for file in files:
    parse_png(file)

