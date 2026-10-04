def gf_multiply(a, b):

    result = 0

    for i in range(8):

        if b & 1:
            result ^= a

        if a & 0x80:
            a = (a << 1) ^ 0x1B
        else:
            a <<= 1

        a &= 0xFF
        b >>= 1

    return result


def multiplicative_inverse(a):

    if a == 0:
        return 0

    for b in range(1, 256):

        if gf_multiply(a, b) == 1:
            return b

def rotate_left(byte, n):
    return ((byte << n) | (byte >> (8 - n))) & 0xFF

def affine_transform(x):

    result = x

    result ^= rotate_left(x, 1)
    result ^= rotate_left(x, 2)
    result ^= rotate_left(x, 3)
    result ^= rotate_left(x, 4)

    result ^= 0x63

    return result

def sbox(byte):

    inverse = multiplicative_inverse(byte)

    result = affine_transform(inverse)

    return result

def rot_word(word):

    return word[1:] + word[:1]

def sub_word(word):

    result = []

    for byte in word:
        result.append(sbox(byte))

    return result


rcon = [0x01,0x02,0x04,0x08,0x10,0x20,0x40,0x80,0x1B,0x36]

def g(word, round_number):

    word = rot_word(word)

    word = sub_word(word)

    word[0] ^= rcon[round_number - 1]

    return word

def key_expansion(key):

    words = []

    # Split original 16-byte key into 4 words
    for i in range(0, 16, 4):
        words.append(key[i:i+4])

    # Generate remaining 40 words
    for round_number in range(1, 11):

        w0 = words[-4]
        w1 = words[-3]
        w2 = words[-2]
        w3 = words[-1]

        w4 = [a ^ b for a, b in zip(w0, g(w3, round_number))]
        w5 = [a ^ b for a, b in zip(w1, w4)]
        w6 = [a ^ b for a, b in zip(w2, w5)]
        w7 = [a ^ b for a, b in zip(w3, w6)]

        words.extend([w4, w5, w6, w7])

    return words

if __name__ == "__main__":

    key = [
        0x2b, 0x7e, 0x15, 0x16,
        0x28, 0xae, 0xd2, 0xa6,
        0xab, 0xf7, 0x15, 0x88,
        0x09, 0xcf, 0x4f, 0x3c
    ]

    words = key_expansion(key)

    for i, word in enumerate(words):
        print(f"w{i}: {[hex(x) for x in word]}")