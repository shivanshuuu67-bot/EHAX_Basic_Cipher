import argparse
from html import parser
from io_handler import get_input
from classical import vigenere_encrypt, vigenere_decrypt


def main():

    parser = argparse.ArgumentParser(description="AES and Classical Cipher Tool")
    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument("-e","--encrypt",action="store_true",help="Encrypt the input")
    group.add_argument("-d","--decrypt",action="store_true",help="Decrypt the input")
    parser.add_argument("-c","--cipher",choices=["aes", "vigenere"],required=True,help="Choose the cipher")
    parser.add_argument("-i","--input",required=True,help="Input text or path to a .txt file")
    parser.add_argument("-k","--key",required=True,help="Encryption/decryption key")

    args = parser.parse_args()
    data = get_input(args.input)
    
    if args.cipher == "vigenere":
        if args.encrypt:
            result = vigenere_encrypt(data, args.key)
        else:
            result = vigenere_decrypt(data, args.key)

    print("Result:", result)

    print("Encrypt:", args.encrypt)
    print("Decrypt:", args.decrypt)
    print("Cipher:", args.cipher)
    print("Input:", data)
    print("Key:", args.key)

if __name__ == "__main__":
    main()