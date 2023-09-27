## Stack for generating public and private keys

# Encrypted Private Key SSM : /APP/ENCRYPTED_PRIVATE_KEY


# Pycryptodome required to generate RSA key (pip install pycryptodome)

Stack will generate a private_key.pem and upload the private_key.pem to SSM as well as the public key bucket

set generate_new_keys to True in deploy_keys.py to generate new keys (you will need to generate new keys in the first time). Else, it will always use private_key.pem file for the stack