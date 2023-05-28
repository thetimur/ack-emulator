import time
from module import *
from checksum import *

SERVER_SEND_FILE = 'send'
SERVER_RECEIVE_FILE = 'recv'

SERVER_IP = '127.0.0.1'
SERVER_PORT = 12345
ENCODING = 'utf-8'

MODE_GENERATE = 'gen'
MODE_TEST = 'test'
MODE_SEND = 'send'
MODE_RECEIVE = 'recv'


def log(message):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")


user_input = input(
    'Insert:\n test - you want to test checksum\n send - you want to send file\n recv - you want to receive file\n')

if user_input == MODE_GENERATE:
    file = open(SERVER_SEND_FILE, 'wt', encoding=ENCODING)

    size = int(input('Insert requred size of file:\n\n\n'))
    file.write('*' * size)
elif user_input == MODE_SEND:
    send_to(open(SERVER_SEND_FILE, 'rt', encoding=ENCODING).read(),
           SERVER_IP, SERVER_PORT, 1)
    log('Data has been sent')
elif user_input == MODE_RECEIVE:
    size = int(input('Insert requred size of file you inserted before:\n\n\n'))
    received_client_data = recieve_from(size, SERVER_IP, SERVER_PORT, 1)
    print(
        f'Data has been recieved: {len(received_client_data)}')
    file = open(SERVER_RECEIVE_FILE, 'wt', encoding=ENCODING).write(
        received_client_data)
elif user_input == MODE_TEST:
    test_data = b'[jadsfl;nmasdkfnasldfnskafm]'
    assert check(bytes([count(test_data)]) + test_data)
    log('test 1 OK')

    assert not check(bytes([count(test_data) + 1]) + test_data)
    log('test 2 OK')

