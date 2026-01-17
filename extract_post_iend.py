import os

files = [
    'challenges/swimmer2026/rain/images/tobu_line.png',
    'challenges/swimmer2026/rain/images/suigun.png',
    'challenges/swimmer2026/rain/images/sannnomiya-1.png'
]

# IEND chunk including length(0), type(IEND), and CRC
iend_marker = b'\x00\x00\x00\x00\x49\x45\x4E\x44\xAE\x42\x60\x82'

for filepath in files:
    filename = os.path.basename(filepath)
    print(f"--- Processing {filename} ---")
    try:
        with open(filepath, 'rb') as f:
            data = f.read()
            
        index = data.find(iend_marker)
        if index == -1:
            print("IEND marker not found!")
            continue
            
        # The actual data ends after the 12-byte IEND chunk (4 len + 4 type + 4 crc)
        # But wait, the marker above is 12 bytes. 
        # index points to the start of '00 00 00 00...'
        
        split_point = index + len(iend_marker)
        extra_data = data[split_point:]
        
        if not extra_data:
            print("No data after IEND.")
            continue
            
        print(f"Found {len(extra_data)} bytes of extra data.")
        
        output_filename = filename + ".extracted"
        with open(output_filename, 'wb') as out_f:
            out_f.write(extra_data)
        print(f"Saved to {output_filename}")
        
    except Exception as e:
        print(f"Error: {e}")
