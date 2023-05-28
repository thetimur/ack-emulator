from module import *
import time

CLIENT_SEND_FILE = 'csend'
CLIENT_RECEIVE_FILE = 'crecv'

SERVER_IP = '127.0.0.1'
SERVER_PORT = 12345
ENCODING = 'utf-8'

MODE_GEN = 'gen'
MODE_SEND = 'send'
MODE_RECEIVE = 'recv'

def log(message):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

user_input = input(
    'Insert:\n \n send - you want to send file\n recv - you want to receive file\n')

if user_input == MODE_GEN:
    size = int(input('Insert requred size of file:\n\n\n'))
    file_data = '#' * size
    open(CLIENT_SEND_FILE, 'wt', encoding=ENCODING).write(file_data)
elif user_input == MODE_SEND:
    file_data = open(CLIENT_SEND_FILE, 'rt', encoding=ENCODING).read()
    send_to(file_data, SERVER_IP, SERVER_PORT, 1)

    log('Data has been sent')
elif user_input == MODE_RECEIVE:
    size = input('Insert requred size of file you inserted before:\n\n\n')
    data = recieve_from(size, SERVER_IP, SERVER_PORT, 1)

    log(f'Data has been received, size: {len(data)}')
    open(CLIENT_RECEIVE_FILE, 'wt', encoding=ENCODING).write(data)
