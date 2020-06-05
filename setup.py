def generateAESKey(destination, public_key="./key.public"):
    """ Generate our private encryption key.
        Arguments:
            destination     The folder where the encrypted files will end up
            public_key      The public key to be used for the encryption
    """
    
    # Generate a random secret that will encrypt the files as AES-256
    aes_secret = os.urandom(32)

    # Check to see if there is actually a public key file
    if not os.path.isfile(public_key):
        print("Public key not found: " + public_key)
        sys.exit(1)

    # Create the directory "keys" that will store our encryption keys
    keys_path = './keys'
    try: 
        os.mkdir(keys_path) 
    except FileExistsError: 
        os.rmdir(keys_path)
        os.mkdir(keys_path)

    # Encrypt and save our AES secret using the public key for the holder of
    # the private key to be able to decrypt the files.
    secret_path = destination + "AES_KEY"
	
    with open(secret_path, "wb") as secret_file:
        secret_file.write(encrypt_string(aes_secret, public_key))
