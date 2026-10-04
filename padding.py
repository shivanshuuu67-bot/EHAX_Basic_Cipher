BLOCK_SIZE = 16


def pkcs7_pad(data):
    padding_length = BLOCK_SIZE - (len(data) % BLOCK_SIZE)

    padding = bytes([padding_length]) * padding_length

    return data + padding


def pkcs7_unpad(data):
    if len(data) == 0 or len(data) % BLOCK_SIZE != 0:
        raise ValueError("Invalid padding")

    padding_length = data[-1]

    if padding_length < 1 or padding_length > BLOCK_SIZE:
        raise ValueError("Invalid padding")

    if data[-padding_length:] != bytes([padding_length]) * padding_length:
        raise ValueError("Invalid padding")

    return data[:-padding_length]


if __name__ == "__main__":

    plaintext = b"HELLO"

    padded = pkcs7_pad(plaintext)

    print("Original:")
    print(plaintext)

    print("Padded:")
    print(padded)
    print([hex(x) for x in padded])

    unpadded = pkcs7_unpad(padded)

    print("Unpadded:")
    print(unpadded)