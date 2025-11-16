# break_monoalphabetic.py
import random
import string
# This import now points to your new file
import ngram_score
from collections import Counter

# --- Constants ---

# Standard English letter frequencies, from most to least common
ENGLISH_FREQUENCIES_ORDER = 'ETAOINSHRDLCUMWFGYPBVKJXQZ'
ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

# --- 1. Initialization Function (No changes needed) ---

def init_key(ciphertext: str) -> str:
    """
    Initializes a key based on frequency analysis, as required
    by the lab sheet.
    
    Returns the key in the format "VFT...", where plaintext 'A'
    is mapped to 'V', 'B' to 'F', etc..
    """
    print("Initializing key using frequency analysis...")
    
    # 1. Clean text and get its letter frequencies
    cleaned_text = "".join(filter(str.isalpha, ciphertext)).upper()
    cipher_freq = Counter(cleaned_text)
    
    # 2. Sort ciphertext letters by their frequency
    # e.g., ['X', 'G', 'Q', ...]
    cipher_freq_sorted = [item[0] for item in cipher_freq.most_common()]
    
    # 3. Create a decryption map
    # Map most frequent cipher letter ('X') to most frequent
    # English letter ('E'), and so on.
    decryption_map = {}
    for i, cipher_char in enumerate(cipher_freq_sorted):
        # Handle cases where ciphertext has fewer than 26 letters
        if i < len(ENGLISH_FREQUENCIES_ORDER):
            decryption_map[cipher_char] = ENGLISH_FREQUENCIES_ORDER[i]
    
    # Fill in any missing letters (that weren't in the ciphertext)
    unused_cipher_chars = [c for c in ALPHABET if c not in decryption_map]
    unused_plain_chars = [c for c in ENGLISH_FREQUENCIES_ORDER if c not in decryption_map.values()]
    
    for i, cipher_char in enumerate(unused_cipher_chars):
        if i < len(unused_plain_chars):
            decryption_map[cipher_char] = unused_plain_chars[i]

    # 4. Create the ENCRYPTION key (format for subst.key)
    # The lab format is: Key[0] = what 'A' maps to
    #                   Key[1] = what 'B' maps to ...
    #
    # We must invert our decryption_map.
    # decryption_map {'X': 'E'}  ->  encryption_map {'E': 'X'}
    encryption_map = {v: k for k, v in decryption_map.items()}
    
    # 5. Build the final key string
    initial_key = ""
    for plain_char in ALPHABET:
        initial_key += encryption_map.get(plain_char, '?') # '?' as a fallback

    print(f"Initial key guess: {initial_key}")
    return initial_key

# --- Helper Function (No changes needed) ---

def decrypt(ciphertext: str, key_string: str) -> str:
    """
    Decrypts the ciphertext using a key in the "VFT..." format.
    """
    # Create decryption map from the key string
    # "VFT..." means V->A, F->B, T->C
    decryption_map = {key_string[i]: ALPHABET[i] for i in range(len(ALPHABET))}
    
    decrypted_text = ""
    for char in ciphertext:
        if char.upper() in decryption_map:
            # Preserve original case (e.g., lowercase 'v' -> 'a')
            if char.islower():
                decrypted_text += decryption_map[char.upper()].lower()
            else:
                decrypted_text += decryption_map[char.upper()]
        else:
            # Keep non-alphabetic chars (spaces, punctuation)
            decrypted_text += char
            
    return decrypted_text

# --- 2 & 3. Hill-Climbing Algorithm (Refactored) ---

def main():
    print("Starting Task 1.2: Hill-Climbing Attack")
    
    # Load the ciphertext from Task 1.1
    try:
        with open('Subst.txt', 'r', encoding='latin-1') as f:
            ciphertext = f.read()
    except FileNotFoundError:
        print("Error: Subst.txt not found. Please run Task 1.1 first.")
        return

    # --- REFACTORED LINE ---
    # Load the n-gram scorer using your new lowercase class name
    scorer = ngram_score.ngram_score('english_quadgrams.txt')

    # 1. Get initial key
    parent_key = init_key(ciphertext)
    parent_decrypted = decrypt(ciphertext, parent_key)
    
    # --- REFACTORED LINES ---
    # Your new scorer doesn't clean for non-alphabetic chars.
    # We must do it here so that n-grams like "THE " aren't scored.
    cleaned_for_scoring = "".join(filter(str.isalpha, parent_decrypted))
    parent_score = scorer.score(cleaned_for_scoring)
    
    best_key = parent_key
    best_score = parent_score
    print(f"Initial Score: {best_score:.2f}")

    # 2. Start the hill-climbing loop
    # More iterations give a better chance of finding the true key
    iterations = 5000 
    print(f"Running {iterations} iterations of hill-climbing...")
    
    for i in range(iterations):
        # Create a new key by swapping two letters
        child_key_list = list(best_key)
        a, b = random.sample(range(26), 2) # Pick 2 random indices
        child_key_list[a], child_key_list[b] = child_key_list[b], child_key_list[a]
        child_key = "".join(child_key_list)
        
        # 3. Measure the quality of the new key
        child_decrypted = decrypt(ciphertext, child_key)
        
        # --- REFACTORED LINES ---
        # We must clean this text too before scoring.
        cleaned_for_scoring = "".join(filter(str.isalpha, child_decrypted))
        child_score = scorer.score(cleaned_for_scoring)
        
        # If it's an improvement, "climb the hill"
        if child_score > best_score:
            best_score = child_score
            best_key = child_key
            
            # Print progress so you know it's working
            if i % 100 == 0:
                print(f"  Iter {i}: New best score: {best_score:.2f}")

    # 4. Finished. Save the final key.
    print("\nAttack finished.")
    print(f"Final Score: {best_score:.2f}")
    print(f"Final Key: {best_key}")
    
    # Save the key to subst.key
    with open('subst.key', 'w', encoding='utf-8') as f:
        f.write(best_key)
    print("Discovered substitution key saved to subst.key")

    # Also save the final plaintext so you can read it
    final_plaintext = decrypt(ciphertext, best_key)
    with open('plaintext_final.txt', 'w', encoding='latin-1') as f:
        f.write(final_plaintext)
    print("Final decrypted text saved to plaintext_final.txt")

if __name__ == "__main__":
    main()