# Task 3 Writeup

## Analysis Approach

This task was a **partial known-plaintext attack** on a file encrypted with a 96-bit (12-byte) repeating XOR key.

The strategy relied on the fact that the encrypted file, `XOR.zip.crypt`, was a standard `.zip` file. All `.zip` files share a common file header structure, which can be used as the "known plaintext."

## Step-by-Step Decryption

1.  **Phase 1: Finding the Partial Key**
    * I identified the first 10 bytes of a standard `.zip` header as my known plaintext: `50 4B 03 04` (Signature), `14 00` (Version), `00 00` (Bit Flag), and `08 00` (Deflate Compression).
    * Using the formula `Key = Ciphertext  ⊕  Plaintext`, I XORed the first 10 bytes of `XOR.zip.crypt` with these 10 known bytes.
    * This revealed the first 10 bytes of the 12-byte repeating key.

2.  **Phase 2: Finding the Missing Key Bytes**
    * As per **Hint 5**, I created a 12-byte "partial key" using the 10 bytes I found, plus two `0x00` bytes as placeholders for the unknown key bytes (`K[10]` and `K[11]`).
    * I decrypted the entire ciphertext with this repeating partial key and saved the result as `partial.zip`.
    * Because the key repeats, this new file was *mostly* correct, but had garbage data at every 10th and 11th byte of every 12-byte chunk.
    * I inspected the file header of `partial.zip` (specifically the filename field, which starts at byte 30).
    * By observing the mostly-correct filename (e.g., `task??txt`), I was able to deduce the two missing plaintext characters (`P[34]` and `P[35]`).
    * With these two known plaintext bytes, I used the formula again (`K[10] = C[34]  ⊕  P[34]` and `K[11] = C[35]  ⊕  P[35]`) to find the last two bytes of the key.

3.  **Phase 3: Final Decryption**
    * With all 12 bytes of the key assembled, I ran the decryption script one final time.
    * The resulting file, `XOR_decrypted_final.zip`, is a valid zip archive, and the key was saved to `XOR.key`.