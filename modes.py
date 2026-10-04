from aes import aes_encrypt_block, aes_decrypt_block
from padding import pkcs7_pad, pkcs7_unpad


def ecb_encrypt(data, key):

    data = pkcs7_pad(data)

    ciphertext = b""

    for i in range(0, len(data), 16):

        block = data[i:i + 16]

        encrypted_block = aes_encrypt_block(list(block), key)

        ciphertext += bytes(encrypted_block)

    return ciphertext

def ecb_decrypt(data, key):

    plaintext = b""

    for i in range(0, len(data), 16):

        block = data[i:i + 16]

        decrypted_block = aes_decrypt_block(list(block), key)

        plaintext += bytes(decrypted_block)

    plaintext = pkcs7_unpad(plaintext)

    return plaintext



def xor_blocks(block1, block2):

    result = []

    for i in range(16):
        result.append(block1[i] ^ block2[i])

    return result

def cbc_encrypt(plaintext, key, iv):

    if len(key) != 16:
        raise ValueError("AES-128 key must be exactly 16 bytes")

    if len(iv) != 16:
        raise ValueError("IV must be exactly 16 bytes")

    if len(plaintext) % 16 != 0:
        raise ValueError("Plaintext must be padded to a multiple of 16 bytes")

    ciphertext = []

    for i in range(0, len(plaintext), 16):

        block = plaintext[i:i+16]

        xored = xor_blocks(block, iv)

        encrypted = aes_encrypt_block(xored, key)

        ciphertext.extend(encrypted)

        iv = encrypted

    return ciphertext

def cbc_decrypt(ciphertext, key, iv):

    if len(key) != 16:
        raise ValueError("AES-128 key must be exactly 16 bytes")

    if len(iv) != 16:
        raise ValueError("IV must be exactly 16 bytes")

    if len(ciphertext) == 0 or len(ciphertext) % 16 != 0:
        raise ValueError("Ciphertext must be a multiple of 16 bytes")

    plaintext = []

    for i in range(0, len(ciphertext), 16):

        block = ciphertext[i:i+16]

        decrypted = aes_decrypt_block(block, key)

        xored = xor_blocks(decrypted, iv)

        plaintext.extend(xored)

        iv = block

    return plaintext


if __name__ == "__main__":

    key = [
        0x2b, 0x7e, 0x15, 0x16,
        0x28, 0xae, 0xd2, 0xa6,
        0xab, 0xf7, 0x15, 0x88,
        0x09, 0xcf, 0x4f, 0x3c
    ]

    iv = [
        0x00, 0x01, 0x02, 0x03,
        0x04, 0x05, 0x06, 0x07,
        0x08, 0x09, 0x0a, 0x0b,
        0x0c, 0x0d, 0x0e, 0x0f
    ]

    plaintext = b"Hello AES CBC!"

    # Padding
    padded = pkcs7_pad(plaintext)

    # CBC Encryption
    ciphertext = cbc_encrypt(
        list(padded),
        key,
        iv
    )

    print("CBC Ciphertext:")
    print([hex(x) for x in ciphertext])

    # CBC Decryption
    decrypted_padded = cbc_decrypt(
        ciphertext,
        key,
        iv
    )

    # Remove padding
    decrypted = pkcs7_unpad(bytes(decrypted_padded))

    print("CBC Decrypted:")
    print(decrypted)