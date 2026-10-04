def vigenere_encrypt(text, key):

    encrypted = ""

    for i in range(len(text)):

        p = ord(text[i]) - ord('A')
        k = ord(key[i % len(key)]) - ord('A')

        c = (p + k) % 26

        encrypted += chr(c + ord('A'))

    return encrypted


def vigenere_decrypt(text, key):

    decrypted = ""

    for i in range(len(text)):

        c = ord(text[i]) - ord('A')
        k = ord(key[i % len(key)]) - ord('A')

        p = (c - k) % 26

        decrypted += chr(p + ord('A'))

    return decrypted
