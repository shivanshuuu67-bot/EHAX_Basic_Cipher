import base64

def bytes_to_hex(data):
    return data.hex()


def hex_to_bytes(data):
    return bytes.fromhex(data)


def bytes_to_base64(data):

    return base64.b64encode(data).decode("utf-8")


def base64_to_bytes(data):
    return base64.b64decode(data)

# Test data: 16-byte AES block
data = bytes([
    0x32, 0x43, 0xF6, 0xA8,
    0x88, 0x5A, 0x30, 0x8D,
    0x31, 0x31, 0x98, 0xA2,
    0xE0, 0x37, 0x07, 0x34
])

print("Original:")
print(data)
print(list(data))


# HEX round trip
hex_data = bytes_to_hex(data)
decoded_hex = hex_to_bytes(hex_data)

print("\nHex:")
print(hex_data)

print("Hex decoded:")
print(list(decoded_hex))

print("Hex correct:", data == decoded_hex)


# BASE64 round trip
base64_data = bytes_to_base64(data)
decoded_base64 = base64_to_bytes(base64_data)

print("\nBase64:")
print(base64_data)

print("Base64 decoded:")
print(list(decoded_base64))

print("Base64 correct:", data == decoded_base64)