import socket


IP_ADDRESS  = '127.0.0.1'
PORT        = 5678

print('Creating socket...')
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((IP_ADDRESS, PORT))
    print('Running server...')
    print('\n')
    while True:
        s.listen(1)
        conn, addr = s.accept()
        print(f'Connection from {addr} established!')
        with conn:
            while True:
                request = conn.recv(1024).decode()
                if request == 'public_key required!':
                    with open('public_key.pem', 'r') as public_key_file: 
                        public_key = public_key_file.read()
                        conn.send(f'{public_key}'.encode())
                        print('Done Sending: public_key.pem')
                    break 
                if request == 'private_key required!':
                    with open('private_key.pem', 'r') as private_key_file: 
                        private_key = private_key_file.read()
                        conn.send(f'{private_key}'.encode())
                        print('Done Sending: private_key.pem')
                    break
            print(f'Connection from {addr} closed!')
            print('\n')