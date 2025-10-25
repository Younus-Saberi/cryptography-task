# Introduction to Cyber Security - cryptography-task

This repository contains the solution files for the first lab program from the "Introduction to Cyber Security" course. The assignments focus on the practical cryptanalysis of historical and modern secret-key ciphers.

The tasks in this lab include:
* **Task 1:** A multi-stage attack to break a file encrypted with both AES and a mono-alphabetic substitution. This involves a brute-force attack on a weak AES key and a hill-climbing algorithm to crack the substitution cipher.
* **Task 2:** A demonstration of the properties of the XOR cipher, showing how one ciphertext can decrypt to two different plaintexts.
* **Task 3:** A partial known-plaintext attack on a `.zip` file encrypted with a repeating XOR key.

## 🧠 Core Concepts & Tools

Before diving into the code, it's helpful to understand the core concepts. This lab assumes some basic knowledge of cryptography.

**Key Concepts:**
* **Mono-alphabetic vs. Poly-alphabetic Ciphers:** Understanding the difference between a simple substitution (like Caesar) and a multi-alphabet cipher (like Vigenère).
* **Frequency Analysis:** The core technique used to break classic ciphers. It relies on the fact that letters in a language (like 'E' in English) appear with a predictable frequency.
* **Known-Plaintext Attack:** An attack model where the attacker has access to both a ciphertext and its corresponding plaintext.
* **XOR Operation:** The `^` (Exclusive OR) bitwise operation, which is fundamental to many stream ciphers.
* **Shannon Entropy:** A measure of randomness or unpredictability in a set of data. This is used in Task 1 to distinguish correct decryptions (low entropy) from random garbage (high entropy).

**E-Learning with CrypTool**
For a quick, hands-on understanding of these ciphers without writing any code, the [CrypTool](https://www.cryptool.org/en/) project is an excellent resource.

I highly recommend the online version, **CrypTool Online (CTO)**, for fast experiments directly in your browser.
* **CTO Website:** `https://www.cryptool.org/en/cto/`

## 🚀 Getting Started

These scripts were developed and tested on **Windows 11** using **Python 3.x**.

### Prerequisites
* [Python 3.x](https://www.python.org/downloads/)
* [Git](https://git-scm.com/downloads)
* A terminal (like PowerShell, CMD, or Windows Terminal)

### Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git)
    cd your-repo-name
    ```

2.  **Set up a virtual environment (recommended):**
    ```bash
    # Create a virtual environment
    python -m venv venv
    
    # Activate it (Windows PowerShell)
    .\venv\Scripts\Activate
    ```

3.  **Install dependencies:**
    This project requires the `pycryptodome` library for the AES decryption in Task 1.
    ```bash
    pip install -r requirements.txt
    ```

4.  **Download the N-gram Data File (Crucial for Task 1):**
    The hill-climbing algorithm in `task01` requires a data file of letter-sequence frequencies (`english_quadgrams.txt`) to function. This file is not included in the repository.

    * You must download this file separately. A common version can be found at [practicalcryptography.com](http://practicalcryptography.com/cryptanalysis/stochastic-searching/cryptanalysis-vigenere-cipher/) (look for `english_quadgrams.txt`).
    * Place the downloaded `english_quadgrams.txt` file inside the `task01` folder.

## 📁 Project Structure & Task Explanations

Here is a breakdown of what each file in this repository does.

---

### Task 1: Ciphertext-Only & Hill-Climbing Attack

**Goal:** Decrypt `Subst-Rijndael.crypt`, a file encrypted first by a substitution cipher and then by AES in CBC mode with a weak key.

#### `task01/bruteforce_aes.py`
* **Role:** Solves Task 1.1.
* **Importance:** This script breaks the "outer" AES encryption layer. Since the 128-bit key was weak (only the first 16 bits were unknown), this script brute-forces all $2^{16}$ (65,536) possible keys.
* **Method:** It finds the correct key by calculating the **Shannon entropy** of every possible decryption. The correct key is the one that produces an output with the *lowest* entropy (i.e., looks the least random).
* **Output:** Generates `aes.key` (the discovered AES key) and `Subst.txt` (the decrypted text, which is still encrypted with the substitution cipher).

#### `task01/ngram_score.py`
* **Role:** A "given" module that acts as the "scorer" for the hill-climbing algorithm.
* **Importance:** This file contains the "measurement function". It scores a piece of text based on the frequency of its 4-letter sequences (quadgrams). Text that looks like real English (e.g., has many "TION", "THER" sequences) gets a high score.

#### `task01/break_monoalphabetic.py`
* **Role:** Solves Task 1.2.
* **Importance:** This script breaks the "inner" substitution cipher from `Subst.txt`. It uses a **hill-climbing algorithm** to find the key. A brute-force attack is impossible ($26!$ combinations).
* **Method:**
    1.  **Initialization:** It starts with a "good guess" key generated via **frequency analysis**.
    2.  **Climbing:** It iteratively makes thousands of small, random changes (key swaps).
    3.  **Scoring:** It uses `ngram_score.py` to score the result of each change. It only keeps a change if the new score is higher than the previous one.
* **Output:** Generates `subst.key` (the final 26-letter substitution key) and `plaintext_final.txt`.

---

### Task 2: Find the Right Algorithm

**Goal:** Solve the paradox of how one ciphertext (`cipher.crypt`) can be decrypted into two *different* plaintexts (`plaintext1.txt`, `plaintext2.txt`) using two different keys.

#### `task02/cipher_keys.py`
* **Role:** The main script for Task 2.
* **Importance:** This script demonstrates that the only common algorithm fitting the criteria is the **XOR cipher**. It uses the properties of XOR (`Key = Ciphertext ⊕ Plaintext`) to instantly find both keys.
* **Method:**
    * `k1.key = cipher.crypt ⊕ plaintext1.txt`
    * `k2.key = cipher.crypt ⊕ plaintext2.txt`
* **Output:** Generates `k1.key` and `k2.key` as binary files.

#### `task02/validate_keys.py`
* **Role:** (Helper script) A validation script to prove the solution.
* **Importance:** It confirms the keys are correct by reversing the process (`Plaintext = Ciphertext ⊕ Key`). It proves the mathematical identity of XOR (`A ⊕ (A ⊕ B) = B`).

#### `task02/Writeup.md`
* **Role:** The mandatory writeup file explaining the XOR cipher's properties and how the keys were found.

---

### Task 3: Partial Known-Plaintext Attack

**Goal:** Decrypt `XOR.zip.crypt`, a `.zip` file encrypted with a 96-bit (12-byte) repeating XOR key.

#### `task03/XOR_decrypter.py`
* **Role:** The full cryptanalysis script for Task 3.
* **Importance:** This script performs a **partial known-plaintext attack**. The "known plaintext" is the standard file header (magic number `PK...`) that all `.zip` files begin with.
* **Method:**
    1.  **Phase 1:** It XORs the first 10 known header bytes (e.g., `\x50\x4B\x03\x04...`) with the first 10 bytes of the ciphertext to find the *first 10 bytes* of the 12-byte key.
    2.  **Phase 2:** It performs an iterative analysis (as suggested in Hint 5) by decrypting the file with a partial key (e.g., `key_bytes_1-10 + \x00\x00`).
    3.  **Phase 3:** By inspecting the (now partially readable) filename in the decrypted data, the script can deduce the two missing plaintext bytes, which in turn reveals the last two bytes of the key.
* **Output:** Generates `XOR.key` (the full 96-bit key as a hex string) and `XOR_decrypted_final.zip` (the successfully decrypted file).

#### `task03/Writeup.md`
* **Role:** The mandatory writeup file explaining the step-by-step known-plaintext attack methodology.