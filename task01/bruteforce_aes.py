import math
from collections import Counter
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

def calculate_entropy(data: bytes) -> float:
    """Calculates the Shannon entropy for a given block of data."""
    if not data:
        return 0
    
    # Count the frequency of each byte
    counter = Counter(data)
    data_len = len(data)
    entropy = 0.0
    
    # Calculate entropy
    for count in counter.values():
        probability = count / data_len
        entropy -= probability * math.log2(probability)
        
    return entropy

def find_aes_key():
    """
    Brute-forces the 16-bit weak AES key for Subst-Rijndael.crypt.
    """
    print("Starting AES key brute-force attack...")
    
    # 1. Read the encrypted file
    try:
        with open('Subst-Rijndael.crypt', 'rb') as f:
            full_data = f.read()
    except FileNotFoundError:
        print("Error: Subst-Rijndael.crypt not found.")
        print("Please place the file in the same directory as this script.")
        return

    # 2. Separate IV and Ciphertext
    # The IV is the first block (16 bytes) 
    iv = full_data[:16]
    ciphertext = full_data[16:]
    
    min_entropy = float('inf')
    best_key_bytes = None
    best_plaintext = None

    # 3. Brute-force loop (0 to 2^16 - 1)
    # 2^16 = 65,536
    for i in range(65536):
        # 4. Construct the weak key 
        # 16 bits = 2 bytes. Pad with 14 bytes of zeros.
        # We use 'big' endian to convert the int to 2 bytes.
        key_guess = i.to_bytes(2, 'big') + (b'\x00' * 14)
        
        try:
            # 5. Decrypt the data
            cipher = AES.new(key_guess, AES.MODE_CBC, iv)
            decrypted_data = cipher.decrypt(ciphertext)
            
            # 6. Check the entropy
            entropy = calculate_entropy(decrypted_data)
            
            # 7. Check if this key is the best one so far
            if entropy < min_entropy:
                min_entropy = entropy
                best_key_bytes = key_guess
                best_plaintext = decrypted_data
                print(f"  New best key found: {best_key_bytes.hex()}")
                print(f"  Entropy: {min_entropy:.4f}")

        except Exception as e:
            # This might happen with bad padding, etc.
            continue
            
    # 8. Unpad the best result
    # ... (Keep the rest of your script, just replace this final 'if' block)
    
    if best_plaintext:
        print("\nAttack successful!")
        print(f"Final Key: {best_key_bytes.hex()}")
        print(f"Final Entropy: {min_entropy:.4f}")

        unpadded_plaintext = None
        try:
            # Try to unpad, as this is the standard
            unpadded_plaintext = unpad(best_plaintext, AES.block_size)
            print("  - Padding unpadded successfully.")
        except ValueError as e:
            # If it fails, don't worry. Just use the raw data.
            # The next task is robust to a few junk bytes at the end.
            print(f"  - Warning: {e}. Using raw decrypted data (padding might be non-standard).")
            unpadded_plaintext = best_plaintext

        # 9. Save the outputs
        # Save the key as a hex text string
        with open('aes.key', 'w') as f_key:
            f_key.write(best_key_bytes.hex())
        print("  - Discovered AES key saved to aes.key")
        
        # Save the decrypted text for the next step
        with open('Subst.txt', 'w', encoding='latin-1') as f_plain:
            f_plain.write(unpadded_plaintext.decode('latin-1'))
        print("  - Decrypted plaintext saved to Subst.txt")
            
    else:
        print("\nAttack failed. No key was found.")

# --- Run the attack ---
if __name__ == "__main__":
    find_aes_key()
