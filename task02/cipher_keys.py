# cipher_keys.py

def xor_data(data1: bytes, data2: bytes) -> bytearray:
    """
    XORs two byte streams together. Stops at the end of the
    shortest stream.
    """
    result = bytearray()
    # zip stops automatically when the shortest list/bytes ends
    for b1, b2 in zip(data1, data2):
        result.append(b1 ^ b2)
    return result

def main():
    print("Starting Task 2...")
    
    try:
        # 1. Read the binary data from all three files
        with open('cipher.crypt', 'rb') as f:
            cipher_data = f.read()
        
        with open('plaintext1.txt', 'rb') as f:
            plain1_data = f.read()
            
        with open('plaintext2.txt', 'rb') as f:
            plain2_data = f.read()

    except FileNotFoundError as e:
        print(f"Error: Missing file! {e.filename}")
        print("Please make sure cipher.crypt, plaintext1.txt, and plaintext2.txt are in the same directory.")
        return

    # 2. Calculate k1 (Ciphertext XOR Plaintext1)
    key1 = xor_data(cipher_data, plain1_data)
    
    # 3. Calculate k2 (Ciphertext XOR Plaintext2)
    key2 = xor_data(cipher_data, plain2_data)
    
    # 4. Save the keys as binary files
    with open('k1.key', 'wb') as f:
        f.write(key1)
        
    with open('k2.key', 'wb') as f:
        f.write(key2)
        
    print("Successfully generated k1.key and k2.key.")

if __name__ == "__main__":
    main()