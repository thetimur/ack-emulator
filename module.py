import socket
from random import randint
from checksum import *
import time

PADDING = 2 + 1000


def log(message):
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    print(f'[{timestamp}] {message}')


def is_package_lost():
    return randint(1, 3) != 1


def send_to(data, host, port, timeout):
    log('Setup socket...')
    s = socket.socket(
        socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    setup_socket(timeout, s)

    log('Socker ready!')

    ACK_state = 1
    for i in range(0, len(data), 1000):
        package = data[i:i + 1000]
        ACK_state ^= 1

        encoded_package = package.encode(encoding='utf-8')
        count_value = count(bytes([ACK_state]) + encoded_package)
        modified_package = bytes([count_value]) + \
            bytes([ACK_state]) + encoded_package

        while True:
            s.sendto(modified_package, (host, port))
            try:
                log(f'Package with state: {ACK_state} sent.')
                package_lost = is_package_lost()
                if package_lost:
                    r_data = s.recvfrom(5)[0]
                    e_data = bytes([count_value]) + bytes([ACK_state]) + b'ACK'

                    if r_data == e_data:
                        log(f'Pacage ACK with state: {ACK_state} received.')
                        break
                else:
                    raise socket.timeout()
            except socket.timeout:
                log('Timeout passed')
                continue


def recieve_from(len_s, _host, _port, timeout):
    log('Setup socket...')
    s = socket.socket(
        socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    setup_socket(timeout, s)
    s.bind((_host, _port))

    log('Socker ready!')

    ACK_state = 0
    result = []

    while len_s > 0:
        try:
            response = s.recvfrom(PADDING)
            r_ACK_state, r_data = response[0][1], response[0][2:].decode(
            )

            package_lost = is_package_lost()
            if package_lost:
                if r_ACK_state == ACK_state:
                    if not check(response[0]):
                        log('Invalid checksum')
                        continue

                    ACK_state ^= 1

                    len_s -= len(r_data)
                    result.append(r_data)

                    log(
                        f'Got ackage ACK with state: {r_ACK_state}\n')

                s.sendto(bytes(
                    [count(bytes([r_ACK_state]) + b'ACK')]) + bytes([r_ACK_state]) + b'ACK', response[1])
                log(f'Package ACK with state: {ACK_state} sent')
            else:
                raise socket.timeout()
        except socket.timeout:
            log('Timeout passed')
            continue

    return ''.join(result)


def setup_socket(timeout, s):
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.settimeout(timeout)
