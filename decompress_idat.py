import struct
import glob
import zlib
import sys
import re

def extract_strings(data, min_len=4):
    result = ""
    for b in data:
        if 32 <= b <= 126:
            result += chr(b)
        else:
            if len(result) >= min_len:
                yield result
            result = ""
    if len(result) >= min_len:
        yield result

def process_png(filepath):
    print(f"--- Processing {filepath} ---")
    idat_data = b""
    try:
        with open(filepath, 'rb') as f:
            f.read(8) # Signature
            while True:
                len_bytes = f.read(4)
                if not len_bytes: break
                chunk_len = struct.unpack('>I', len_bytes)[0]
                chunk_type = f.read(4)
                if chunk_type == b'IDAT':
                    idat_data += f.read(chunk_len)
                else:
                    f.seek(chunk_len, 1)
                f.read(4) # CRC
                if chunk_type == b'IEND': break
        
        if not idat_data:
            print("No IDAT found")
            return

        try:
            decompressed = zlib.decompress(idat_data)
            print(f"Decompressed size: {len(decompressed)}")
            
            # Look for specific keywords
            found_keywords = False
            for s in extract_strings(decompressed):
                if "swimmer" in s.lower() or "flag" in s.lower() or "ctf" in s.lower() or "rain" in s.lower():
                    print(f"Found keyword match: {s}")
                    found_keywords = True
            
            if not found_keywords:
                # print first 10 strings just in case
                count = 0
                for s in extract_strings(decompressed):
                    print(f"String: {s}")
                    count += 1
                    if count > 10: break

        except Exception as e:
            print(f"Decompression failed: {e}")

    except Exception as e:
        print(f"Error reading file: {e}")

files = [
    'challenges/swimmer2026/rain/images/tobu_line.png',
    'challenges/swimmer2026/rain/images/suigun.png', 
    'challenges/swimmer2026/rain/images/sannnomiya-1.png',
    'challenges/swimmer2026/rain/images/old-photo.png',
    'challenges/swimmer2026/rain/images/hokkaido.png'
]

for f in files:
    process_png(f)
