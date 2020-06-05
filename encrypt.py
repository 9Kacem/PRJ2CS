"""
Script to encrypt the files.

Encrypts the given source folder and outputs the encrypted files in the given
destination folder. If the source and destination folders are the same then
the initial unencrypted files are removed after they are encrypted. Will work
on both Windows and Linux.
"""

import sys
import os
import struct
import argparse
import hashlib
import json
import tempfile
import shutil
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP


def encrypt_file(key, in_filename, out_filename=None, chunksize=64*1024):
    """ Encrypts a file using AES (CBC mode) with the
        given key.

        Adopted from Eli Bendersky's example:
        http://eli.thegreenplace.net/2010/06/25/aes-encryption-of-files-in-python-with-pycrypto/

        Arguments:
            key             The encryption key - a string that must be
                            either 16, 24 or 32 bytes long. Longer keys
                            are more secure.
            in_filename     Path to the file to be encrypted.
            out_filename    The name (and path) for the encrypted file to be
                            generated.
                            If no filename is supplied, the encrypted file name
                            will be the original plus the `.enc` suffix.
            chunksize       Sets the size of the chunk which the function
                            uses to read and encrypt the file. Larger chunk
                            sizes can be faster for some files and machines.
                            chunksize must be divisible by 16.
    """
    if not out_filename:
        out_filename = os.path.basename(in_filename) + '.enc'

    iv = os.urandom(16)
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    filesize = os.path.getsize(in_filename)

    with open(in_filename, 'rb') as infile:
        with open(out_filename, 'wb') as outfile:
            outfile.write(struct.pack('<Q', filesize))
            outfile.write(iv)

            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += ' '.encode("UTF-8") * (16 - len(chunk) % 16)

                outfile.write(encryptor.encrypt(chunk))


def encrypt_string(text_to_encrypt, public_key_file):
    """ Encrypt the supplied string using our public key.

        Arguments:
            text_to_encrypt     The plain text to encrypt
            public_key_file     The public key to be used for encryption

        Return:
            encrypted_text      The encrypted text using the public key
    """

    with open(public_key_file, 'r') as pub_file:
        pub_key = RSA.importKey(pub_file.read())

    cipher = PKCS1_OAEP.new(pub_key)
    encrypted_text = cipher.encrypt(text_to_encrypt)
    return encrypted_text


def run(source, destination, public_key="./key.public"):
    """ Encrypts the source folder and outputs to the destination folder.

        Arguments:
            source          The folder to be encrypted
            destination     The folder where the encrypted files will end up
            public_key      The public key to be used for the encryption
    """
    # # Make sure that the source and destination folders finish with separator
    # if source[-1] != os.sep:
    #     source += os.sep
    # if destination[-1] != os.sep:
    #     destination += os.sep

    # Check to see if there is actually a public key file
    if not os.path.isfile(public_key):
        print("Public key not found: " + public_key)
        sys.exit(1)

    # Generate a random secret that will encrypt the files as AES-256
    aes_secret = os.urandom(32)

    # Encrypt and save our AES secret using the public key for the holder of
    # the private key to be able to decrypt the files.
    secret_path = destination + "secret"
    with open(secret_path, "wb") as key_file:
        key_file.write(encrypt_string(aes_secret, public_key))

    ######## Encrypt the desired file

    #dirnames
    file_path = source
    filename = os.path.basename(file_path)    

    # Amelioration: Encrypt the file name
    encrypted_filename = str("encrypted_"+filename)

    
    # Encrypt the clear text file and give it an obscured name
    print("Encrypting: " + filename)
    encrypt_file(aes_secret, source, destination + encrypted_filename)
    print("Encryption completed")



def main():
    parser_description = "Encrypt a file"
    parser = argparse.ArgumentParser(description=parser_description)
    parser.add_argument("--source",
                        help="Path to the directory with the files to encrypt",
                        required=False,
                        default="plain_data/data_example_1"),
    destination_message = "Path to the directory where the encrypted files \
    will be exported. If it is the same as the source folder, then the \
    existing unencrypted files will be removed."
    parser.add_argument("--destination", help=destination_message,
                        required=False,
                        default="./encrypted_data/"),
    parser.add_argument("--public-key",
                        help="Path to the public key", default="./key.public")
    args = parser.parse_args()

    run(args.source, args.destination, args.public_key)


if __name__ == "__main__":
    main()
