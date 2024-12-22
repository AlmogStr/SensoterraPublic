import struct
import csv

def float_to_float16(value):
    """Convert a float to a half-precision float (float16) and return it as bytes."""
    # Use struct to pack the float into 2 bytes (half-precision float)
    packed = struct.pack('e', value)
    
    # Reverse conversion: unpack back to float16 to check
    unpacked_value = struct.unpack('e', packed)[0]
    return packed, unpacked_value

def hex_to_float16(hex_value):
    """Convert hex to float16 (reverse conversion)."""
    byte_data = bytes.fromhex(hex_value)
    unpacked_value = struct.unpack('e', byte_data)[0]
    return unpacked_value

def generate_payload(a, b, c, sp):
    """Generate the payload for the given soil type and parameters."""
    # Convert a, b, c, and sp to float16 and get their packed byte values
    a_packed, a_reversed = float_to_float16(a)
    b_packed, b_reversed = float_to_float16(b)
    c_packed, c_reversed = float_to_float16(c)
    sp_packed, sp_reversed = float_to_float16(sp)
    
    # Explicitly add the missing byte to the beginning of the payload
    # Assuming that the first byte is 0x03 and second byte should be 0x01
    payload = b'\x03\x01' + a_packed + b_packed + c_packed + sp_packed
    
    # Return payload and the reversed values (which represent rounded values)
    return payload, a_reversed, b_reversed, c_reversed, sp_reversed

def process_csv(input_file, output_file):
    """Process the CSV file and generate payloads with rounded values."""
    with open(input_file, mode='r') as infile:
        csv_reader = csv.DictReader(infile)
        
        # Open the output file to write the results
        with open(output_file, mode='w', newline='') as outfile:
            fieldnames = ['Soil type', 'Payload', 'Rounded a', 'Rounded b', 'Rounded c', 'Rounded sp']
            csv_writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            csv_writer.writeheader()

            for row in csv_reader:
                soil_type = row['Soil type']
                a = float(row['a'])
                b = float(row['b'])
                c = float(row['c'])
                sp = float(row['sp'])

                # Generate the payload and retrieve the reversed (rounded) values
                payload, rounded_a, rounded_b, rounded_c, rounded_sp = generate_payload(a, b, c, sp)

                # Write the results to the output file
                csv_writer.writerow({
                    'Soil type': soil_type,
                    'Payload': payload.hex(),
                    'Rounded a': rounded_a,
                    'Rounded b': rounded_b,
                    'Rounded c': rounded_c,
                    'Rounded sp': rounded_sp
                })

# Example usage
process_csv('input.csv', 'output.csv')
