# EHAX Basic Cipher

A command-line cryptography tool implemented in Python as part of the **EHAX Basic Cipher Implementation Project**.

This project implements a classical cipher along with **AES-128 from scratch**, including AES key expansion, encryption/decryption, ECB and CBC modes, PKCS#7 padding, and hexadecimal/Base64 encoding.


---

## Features

### Classical Cipher
- Vigenère Cipher
- Encryption and decryption
- Alphabetic key-based substitution

### AES-128
- AES-128 encryption implemented from scratch
- AES-128 decryption implemented from scratch
- 128-bit (16-byte) keys
- AES key expansion
- 10 AES rounds
- SubBytes
- ShiftRows
- MixColumns
- AddRoundKey
- Inverse transformations for decryption
- Galois Field arithmetic
- AES S-Box and inverse S-Box

### Block Cipher Modes
- ECB (Electronic Codebook)
- CBC (Cipher Block Chaining)

### Padding
- PKCS#7 padding
- PKCS#7 unpadding

### Input / Output
- Direct string input
- `.txt` file input
- Hexadecimal ciphertext output
- Base64 ciphertext output
- Command-line interface using `argparse`

---

## Project Structure

```text
EHAX_Basic_Cipher/
│
├── aes.py
├── classical.py
├── encoding.py
├── io_handler.py
├── key_expansion.py
├── main.py
├── modes.py
├── padding.py
├── message.txt
├── README.md
└── .gitignore
```

### File Description

| File | Purpose |
|---|---|
| `main.py` | Main command-line interface and integration of all components |
| `aes.py` | AES-128 block encryption and decryption implementation |
| `key_expansion.py` | AES-128 key expansion and round-key generation |
| `modes.py` | ECB and CBC mode implementations |
| `padding.py` | PKCS#7 padding and unpadding |
| `classical.py` | Vigenère cipher encryption and decryption |
| `encoding.py` | Hexadecimal and Base64 encoding/decoding |
| `io_handler.py` | Handles direct input and `.txt` file input |
| `message.txt` | Example text input file |
| `.gitignore` | Git ignore configuration |

---

# How the Project Works

The project is divided into multiple modules so that each part of the encryption process can be implemented and tested independently.

The main program is controlled through `main.py`.

```text
                    ┌──────────────┐
                    │    main.py   │
                    └──────┬───────┘
                           │
             ┌─────────────┴─────────────┐
             │                           │
      ┌──────▼──────┐             ┌──────▼──────┐
      │  Vigenère   │             │    AES-128  │
      │   Cipher    │             │             │
      └─────────────┘             └──────┬──────┘
                                         │
                              ┌──────────┼──────────┐
                              │          │          │
                         ┌────▼───┐ ┌────▼────┐ ┌───▼────┐
                         │  AES   │ │   Key   │ │ Modes  │
                         │ Core   │ │Expansion│ │        │
                         └────────┘ └─────────┘ └───┬────┘
                                                    │
                                               ┌────▼────┐
                                               │ ECB/CBC │
                                               └─────────┘
```

---

# AES-128 Implementation

AES (Advanced Encryption Standard) is a symmetric block cipher.

This project implements **AES-128**, which means:

- Block size: **128 bits**
- Key size: **128 bits**
- Key size in bytes: **16 bytes**
- Number of rounds: **10**

AES operates on a 128-bit block represented internally as a **4 × 4 byte state matrix**.

## AES Encryption Flow

The AES-128 encryption process implemented in this project follows:

```text
Plaintext Block
      │
      ▼
Initial AddRoundKey
      │
      ▼
┌───────────────────────┐
│       Rounds 1–9       │
│                       │
│       SubBytes        │
│          ↓            │
│       ShiftRows       │
│          ↓            │
│      MixColumns       │
│          ↓            │
│      AddRoundKey      │
└───────────────────────┘
      │
      ▼
     Round 10
      │
      ├── SubBytes
      ├── ShiftRows
      └── AddRoundKey
      │
      ▼
Ciphertext Block
```

The final AES round does **not** perform MixColumns.

---

# AES Components

## 1. SubBytes

Each byte in the AES state is replaced using the AES S-Box.

The S-Box provides a nonlinear substitution that contributes to the security of AES.

For decryption, the inverse S-Box is used.

---

## 2. ShiftRows

The rows of the AES state matrix are cyclically shifted.

```text
Row 0 → no shift
Row 1 → shift left by 1
Row 2 → shift left by 2
Row 3 → shift left by 3
```

The inverse operation is used during decryption.

---

## 3. MixColumns

Each column of the state is transformed using matrix multiplication over the finite field GF(2⁸).

This operation provides diffusion by mixing the bytes within each column.

The implementation includes finite-field multiplication required for AES.

---

## 4. AddRoundKey

The current AES state is combined with the corresponding round key using XOR.

```text
State XOR Round Key
```

This operation is performed at the beginning of AES and during every AES round.

---

# AES Key Expansion

AES-128 does not use the original 16-byte key directly for every round.

Instead, the original key is expanded into:

```text
11 round keys
```

Each round key contains:

```text
16 bytes
```

The implementation includes:

- Word representation
- RotWord
- SubWord
- Rcon
- XOR operations
- Generation of all AES-128 round keys

The generated keys are then used by the AES encryption and decryption routines.

---

# Galois Field Arithmetic

AES performs several operations over the finite field:

```text
GF(2⁸)
```

The implementation therefore includes finite-field multiplication rather than relying on a cryptographic library.

This arithmetic is required for operations such as MixColumns.

---

# Block Cipher Modes

The project supports two AES modes.

## ECB

Electronic Codebook mode independently encrypts each 16-byte block.

```text
Plaintext Block 1 ──► AES ──► Ciphertext Block 1
Plaintext Block 2 ──► AES ──► Ciphertext Block 2
Plaintext Block 3 ──► AES ──► Ciphertext Block 3
```

PKCS#7 padding is applied before encryption and removed after decryption.

---

## CBC

Cipher Block Chaining mode XORs each plaintext block with the previous ciphertext block before AES encryption.

For the first block, an Initialization Vector (IV) is used.

```text
                 ┌─────────┐
Plaintext ──XOR──►   AES   ├──► Ciphertext
             ▲   └─────────┘
             │
        IV / Previous
        Ciphertext
```

For CBC:

- Key must be 16 bytes
- IV must be 16 bytes
- PKCS#7 padding is used
- The IV is required as a command-line argument

---

# PKCS#7 Padding

AES operates on fixed-size blocks of **16 bytes**.

When the plaintext is not exactly a multiple of 16 bytes, PKCS#7 padding is added.

For example, if 13 bytes of data are present:

```text
13 bytes of data + 03 03 03
```

If the plaintext is already exactly one block long, a complete block of padding is added:

```text
16 bytes of data + 10 10 10 ... 10
```

During decryption, the padding is validated and removed.

---

# Vigenère Cipher

The project also implements the classical **Vigenère cipher**.

Vigenère encryption uses a repeating key and operates on alphabetic characters.

For each character:

```text
C = (P + K) mod 26
```

For decryption:

```text
P = (C - K) mod 26
```

This demonstrates the difference between a classical substitution cipher and a modern block cipher such as AES.

---

# Encoding

AES ciphertext is binary data, so the project provides two ways of representing the ciphertext as text:

### Hexadecimal

Example:

```text
32 43 f6 a8 ...
```

### Base64

Example:

```text
MkP2qIhaMI0xMZii4Dc=
```

The corresponding decoding functions convert the encoded ciphertext back into bytes before AES decryption.

---

# Command-Line Interface

The program uses Python's `argparse` module.

General syntax:

```bash
python3 main.py [options]
```

The main options are:

| Option | Description |
|---|---|
| `-e`, `--encrypt` | Encrypt the input |
| `-d`, `--decrypt` | Decrypt the input |
| `-c`, `--cipher` | Select `aes` or `vigenere` |
| `-m`, `--mode` | Select AES `ecb` or `cbc` |
| `-i`, `--input` | Input text or `.txt` file path |
| `-k`, `--key` | Encryption/decryption key |
| `--iv` | Initialization Vector for CBC |
| `-f`, `--format` | Select `hex` or `base64` |

Encryption and decryption are mutually exclusive command-line options.

---

# Usage Examples

## Vigenère Encryption

```bash
python3 main.py -e -c vigenere -i HELLO -k KEY
```

## Vigenère Decryption

```bash
python3 main.py -d -c vigenere -i RIJVS -k KEY
```

---

# AES-128 ECB Encryption

AES-128 requires a key of exactly 16 bytes.

Example:

```bash
python3 main.py -e -c aes -m ecb -i "Hello AES" -k "1234567890abcdef"
```

Using Base64 output:

```bash
python3 main.py -e -c aes -m ecb -i "Hello AES" -k "1234567890abcdef" -f base64
```

---

# AES-128 ECB Decryption

For hexadecimal ciphertext:

```bash
python3 main.py -d -c aes -m ecb -i "<ciphertext>" -k "1234567890abcdef" -f hex
```

For Base64 ciphertext:

```bash
python3 main.py -d -c aes -m ecb -i "<ciphertext>" -k "1234567890abcdef" -f base64
```

---

# AES-128 CBC Encryption

CBC mode requires a 16-byte IV.

Example:

```bash
python3 main.py -e -c aes -m cbc -i "Hello AES" -k "1234567890abcdef" --iv "abcdef1234567890"
```

Using Base64 output:

```bash
python3 main.py -e -c aes -m cbc -i "Hello AES" -k "1234567890abcdef" --iv "abcdef1234567890" -f base64
```

---

# AES-128 CBC Decryption

```bash
python3 main.py -d -c aes -m cbc -i "<ciphertext>" -k "1234567890abcdef" --iv "abcdef1234567890" -f hex
```

---

# Using a Text File as Input

The input argument can also point to a `.txt` file.

For example:

```bash
python3 main.py -e -c aes -m ecb -i message.txt -k "1234567890abcdef"
```

The input handler determines whether the supplied input is direct text or a file path and loads the appropriate data.

---

# Error Handling

The project performs validation for important inputs.

Examples include:

- AES key must be exactly 16 bytes
- CBC IV must be exactly 16 bytes
- CBC mode requires an IV
- Invalid PKCS#7 padding is rejected
- Invalid command-line combinations are handled by `argparse`
- Unsupported cipher, mode, or encoding choices are rejected

---

# Author

**Shivanshu**
