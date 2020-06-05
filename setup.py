import os

def generateAESKey():
    """ Generate an AES encryption key.
        Arguments:
    
    """
    
	# Generate a random secret that will encrypt the files as AES-256
    aes_secret = os.urandom(32)
    aes_secret_path = "./AES_KEY"

    with open(aes_secret_path, "wb") as aes_secret_file:
        aes_secret_file.write(aes_secret)


def main():
    # Generate an AES key and store it in the root folder
    generateAESKey()

    # Create a folder to contain encrypted data
    # todo: specify proper permissions instead of default (777)
    os.mkdir("./encrypted_data")

if __name__ == "__main__":
    main()
