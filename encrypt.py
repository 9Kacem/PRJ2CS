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



def run(source, destination, AES_KEY="./AES_KEY"):
    """ Encrypts the source file and outputs to the destination folder.

        Arguments:
            source          The folder to be encrypted
            destination     The folder where the encrypted files will end up
            AES_KEY         The private key to be used for the encryption
    """
    # # Make sure that the source and destination folders finish with separator
    # if source[-1] != os.sep:
    #     source += os.sep
    # if destination[-1] != os.sep:
    #     destination += os.sep


    # Check to see if there is actually an AES secret file
    if not os.path.isfile(AES_KEY):
        print("Secret Key not found: " + AES_KEY)
        sys.exit(1)
    
    # Get the decrypted AES key
    with open(AES_KEY, "rb") as aes_secret_file:
        aes_secret = aes_secret_file.read()

    #dirnames
    file_path = source
    filename = os.path.basename(file_path)    

    # todo: Encrypt the file name
    encrypted_filename = str("encrypted_"+filename)

    # get the encryption key

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
                        default="plain_data/data_example_1")

    parser.add_argument("--destination",
                        required=False,
                        help="Path to the directory where the encrypted files will be exported.",
                        default="./encrypted_data/")

    parser.add_argument("--key", 
                    required=False,
                    help="The AES Key to be used to encrypt data with.",
                    default="./AES_KEY")

    args = parser.parse_args()

    run(args.source, args.destination, args.key)


if __name__ == "__main__":
    main()
