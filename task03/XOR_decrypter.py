# XOR_decrypter.py
import sys

def xor_with_key(data: bytes, key: bytes) -> bytearray:
    """
    XORs a stream of data with a repeating key.
    """
    result = bytearray()
    key_len = len(key)
    
    for i in range(len(data)):
        key_byte = key[i % key_len] # The repeating key part
        result.append(data[i] ^ key_byte)
        
    return result

def main():
    try:
        with open('XOR.zip.crypt', 'rb') as f:
            cipher_data = f.read()
    except FileNotFoundError:
        print("Error: XOR.zip.crypt not found.")
        return

    # -----------------------------------------------------------------
    # STEP 1: Define known plaintext (10 bytes)
    # -----------------------------------------------------------------
    # 50 4B 03 04 (Signature)
    # 14 00       (Version 2.0)
    # 00 00       (Bit flag)
    # 08 00       (DEFLATE)
    known_plaintext = b'\x50\x4B\x03\x04\x14\x00\x00\x00\x08\x00'

    # -----------------------------------------------------------------
    # STEP 2: Find first 10 bytes of the 12-byte key
    # -----------------------------------------------------------------
    partial_key_10 = xor_with_key(cipher_data[:10], known_plaintext)
    
    # Create the 12-byte partial key (as per Hint 5)
    key_guess_1 = bytearray(partial_key_10)
    key_guess_1.append(0x00) # K[10] = unknown
    key_guess_1.append(0x00) # K[11] = unknown

    print(f"Partial key guess (first 10 bytes): {key_guess_1[:10].hex()}0000")

    # -----------------------------------------------------------------
    # STEP 3: Decrypt with partial key to find missing bytes
    # -----------------------------------------------------------------
    partial_decryption = xor_with_key(cipher_data, key_guess_1)
    
    # Save for manual analysis in a hex editor (good practice)
    with open('partial.zip', 'wb') as f:
        f.write(partial_decryption)
    print("Saved partial.zip for analysis.")

    # -----------------------------------------------------------------
    # STEP 4: Analyze byte 30+ to find filename and guess missing bytes
    # -----------------------------------------------------------------
    # The filename starts at byte 30.
    # The key repeats every 12 bytes.
    # P[34] is XORed with K[10] (34 % 12 = 10)
    # P[35] is XORed with K[11] (35 % 12 = 11)
    
    # We can see the partial filename from the hex dump or just by
    # decoding here (bytes 30-38).
    
    # P[30-33] are correct. P[34-35] are garbage. P[36-37] are correct.
    partial_filename = partial_decryption[30:38]
    print(f"Partial filename (raw): {partial_filename}")
    
    # By observing the partial filename (e.g., "secr??t."), we can
    # guess the missing plaintext characters.
    #
    # *** YOU MUST EDIT THESE TWO BYTES BASED ON YOUR ANALYSIS ***
    #
    # Example: If you see 'secr' (garbage) (garbage) 't.txt'
    # you can guess the two missing bytes are 'e' and 't'.
    #
    # For this example, let's assume the filename is "task3.txt"
    # We would see: 'task' (garbage) (garbage) 'txt'
    # So we guess P[34] ('3') and P[35] ('.')
    
    try:
        P_34 = '3'.encode('ascii')[0] # P[34]
        P_35 = '.'.encode('ascii')[0] # P[35]
    except Exception as e:
        print(f"Error in guess: {e}. Please manually edit the script.")
        return

    print(f"Guessing plaintext bytes P[34]='{chr(P_34)}' and P[35]='{chr(P_35)}'")

    # Now find the last 2 key bytes
    C_34 = cipher_data[34]
    C_35 = cipher_data[35]
    
    K_10 = C_34 ^ P_34
    K_11 = C_35 ^ P_35

    # -----------------------------------------------------------------
    # STEP 5: Build final key and decrypt
    # -----------------------------------------------------------------
    final_key = bytearray(partial_key_10)
    final_key.append(K_10)
    final_key.append(K_11)
    
    print(f"\nDiscovered full 96-bit key:\n{final_key.hex()}")

    # Save the key as a hex string
    with open('XOR.key', 'w') as f:
        f.write(final_key.hex())
    print("Saved key to XOR.key")

    # Do the final decryption
    final_decryption = xor_with_key(cipher_data, final_key)
    with open('XOR_decrypted_final.zip', 'wb') as f:
        f.write(final_decryption)
        
    print("Saved final decrypted file to XOR_decrypted_final.zip")
    print("\nTask complete. Try to open XOR_decrypted_final.zip")

if __name__ == "__main__":
    main()