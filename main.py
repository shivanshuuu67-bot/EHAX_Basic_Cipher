import argparse
from io_handler import get_input
from classical import vigenere_encrypt, vigenere_decrypt
from modes import ecb_encrypt, ecb_decrypt, cbc_encrypt, cbc_decrypt
from padding import pkcs7_pad, pkcs7_unpad
from encoding import bytes_to_hex, hex_to_bytes, bytes_to_base64, base64_to_bytes


def main():

    parser = argparse.ArgumentParser(description="AES and Classical Cipher Tool")
    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument("-e","--encrypt",action="store_true",help="Encrypt the input")
    group.add_argument("-d","--decrypt",action="store_true",help="Decrypt the input")
    parser.add_argument("-c","--cipher",choices=["aes", "vigenere"],required=True,help="Choose the cipher")
    parser.add_argument("-m", "--mode",choices=["ecb", "cbc"],default="ecb",help="Choose AES mode")
    parser.add_argument("-i","--input",required=True,help="Input text or path to a .txt file")
    parser.add_argument("-k","--key",required=True,help="Encryption/decryption key")
    parser.add_argument("--iv",help="Initialization Vector for CBC mode")
    parser.add_argument("-f", "--format",choices=["hex", "base64"],default="hex",help="Ciphertext encoding format")

    args = parser.parse_args()
    data = get_input(args.input)

    if args.cipher == "vigenere":
        if args.encrypt:
            result = vigenere_encrypt(data, args.key)
        else:
            result = vigenere_decrypt(data, args.key)

        print("Result:", result)

    if args.cipher == "aes":

        key = list(args.key.encode("utf-8"))

        if len(key) != 16:
            raise ValueError("AES-128 key must be exactly 16 bytes")

        data = data.encode("utf-8")

        if args.mode == "cbc":

            if args.iv is None:
                raise ValueError("CBC mode requires an IV")

            iv = list(args.iv.encode("utf-8"))

            if len(iv) != 16:
                raise ValueError("CBC IV must be exactly 16 bytes")

        if args.encrypt:

            if args.mode == "ecb":
                ciphertext = ecb_encrypt(data, key)
                if args.format == "hex":
                    print("Ciphertext:", bytes_to_hex(ciphertext))
                elif args.format == "base64":
                    print("Ciphertext:", bytes_to_base64(ciphertext))


            elif args.mode == "cbc":

                padded_data = pkcs7_pad(data)
                ciphertext = cbc_encrypt(padded_data, key, iv)
                ciphertext = bytes(ciphertext)

                if args.format == "hex":
                    print("Ciphertext:", bytes_to_hex(ciphertext))
                elif args.format == "base64":
                    print("Ciphertext:", bytes_to_base64(ciphertext))


        else:

            if args.mode == "ecb":
                if args.format == "hex":
                    ciphertext = hex_to_bytes(data)
                else:
                    ciphertext = base64_to_bytes(data)
                plaintext = ecb_decrypt(ciphertext, key)
                print("Plaintext:", plaintext.decode("utf-8"))

            elif args.mode == "cbc":
                if args.format == "hex":
                    ciphertext = hex_to_bytes(data)
                else:
                    ciphertext = base64_to_bytes(data)
                decrypted = cbc_decrypt(list(ciphertext),key,iv)
                plaintext = pkcs7_unpad(bytes(decrypted))

                print("Plaintext:", plaintext.decode("utf-8"))



if __name__ == "__main__":
    try:
        main()
    except ValueError as e:
        print("Error:", e)