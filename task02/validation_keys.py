# validate_keys.py

def xor_data(data1: bytes, data2: bytes) -> bytearray:
    """
    XORs two byte streams together.
    """
    result = bytearray()
    for b1, b2 in zip(data1, data2):
        result.append(b1 ^ b2)
    return result

def main():
    print("Validating generated keys...")
    
    try:
        # Load all the files
        with open('cipher.crypt', 'rb') as f:
            cipher_data = f.read()
        with open('plaintext1.txt', 'rb') as f:
            plain1_data = f.read()
        with open('plaintext2.txt', 'rb') as f:
            plain2_data = f.read()
        with open('k1.key', 'rb') as f:
            key1_data = f.read()
        with open('k2.key', 'rb') as f:
            key2_data = f.read()

    except FileNotFoundError as e:
        print(f"Error: Missing file! {e.filename}")
        print("Run cipher_keys.py first.")
        return

    # --- Test 1 ---
    # Decrypt the ciphertext with k1
    decrypted_with_k1 = xor_data(cipher_data, key1_data)
    
    # Check if the result matches plaintext1
    if decrypted_with_k1 == plain1_data:
        print("✅ Validation for k1: SUCCESSFUL")
        print("   (Ciphertext ⊕ k1.key) == plaintext1.txt")
    else:
        print("❌ Validation for k1: FAILED")

    # --- Test 2 ---
    # Decrypt the ciphertext with k2
    decrypted_with_k2 = xor_data(cipher_data, key2_data)
    
    # Check if the result matches plaintext2
    if decrypted_with_k2 == plain2_data:
        print("✅ Validation for k2: SUCCESSFUL")
        print("   (Ciphertext ⊕ k2.key) == plaintext2.txt")
    else:
        print("❌ Validation for k2: FAILED")

if __name__ == "__main__":
    main()