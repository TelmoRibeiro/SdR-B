import socket

IP_ADDRESS = '127.0.0.1'
PORT = 5678

print('Creating socket...')
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((IP_ADDRESS, PORT))
    print('The server is running...')
    while True:
        s.listen(1)
        conn, addr = s.accept()
        print(f'Connection from {addr} established!')
        with conn:
            while True:
                request = conn.recv(1024).decode()
                if request == 'public_key required!':
                    with open('public_key.pem', 'r') as f: 
                        public_key = f.read()
                        conn.send(f'{public_key}'.encode())
                        print('public_key.pem sent!')
                    break
                if request == 'private_key required!':
                    with open('private_key.pem', 'r') as f: 
                        private_key = f.read()
                        conn.send(f'{private_key}'.encode())
                        print('private_key.pem sent!')
                    break
            print('Connection closed!')