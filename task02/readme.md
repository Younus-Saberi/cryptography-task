# Task 2 Writeup

## Algorithm Used

The encryption scheme used for this task is the **XOR cipher** (a type of stream cipher).

## How the Keys Were Obtained

The XOR cipher's encryption and decryption functions are based on the XOR operation:

* `Ciphertext = Plaintext  ⊕  Key`
* `Plaintext = Ciphertext  ⊕  Key`

The task provided the ciphertext ($C$) and both possible plaintexts ($P_1$ and $P_2$). To find the two keys ($k_1$ and $k_2$), the decryption formula was rearranged to solve for the key:

* `Key = Ciphertext  ⊕  Plaintext`

My script (`cipher_keys.py`) implements this logic:

1.  **To find k1:** It performed a byte-by-byte XOR between `cipher.crypt` and `plaintext1.txt`. The result was saved as `k1.key`.
2.  **To find k2:** It performed a byte-by-byte XOR between `cipher.crypt` and `plaintext2.txt`. The result was saved as `k2.key`.

This demonstrates that a single ciphertext can be "decrypted" to any arbitrary plaintext, as long as one has the corresponding key.