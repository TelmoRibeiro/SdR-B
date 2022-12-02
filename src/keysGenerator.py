from Crypto.PublicKey import RSA



key = RSA.generate(2048)
privateKey  = key.export_key()
publicKey   = key.publickey().export_key()

with open('private_key.pem', 'wb') as f:
    f.write(privateKey)
print('Done Generating: private_key.pem')

with open('public_key.pem', 'wb') as f:
    f.write(publicKey)
print('Done Generating: public_key.pem')