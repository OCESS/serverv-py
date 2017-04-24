#!/usr/bin/env python3

# Shitty echo server for serverv-py
#
# Usage: shitty_serverv_echo.py
# and then start up serverv-py

from socket import *  # I know, gross.
import msgpack

ECHO_PORT = 31415
BUFSIZE = 2048

# Startup message
tcp_socket = socket(AF_INET, SOCK_STREAM)
tcp_socket.bind(('', ECHO_PORT))
tcp_socket.listen(0)
tcp_conn, addr = tcp_socket.accept()
total_data = []
while 1:
    data = tcp_conn.recv(BUFSIZE)
    if not data:
        total_data_string = b''.join(total_data)
        startup_message = msgpack.unpackb(total_data_string)
        assert b'background_stars' in startup_message
        assert b'insignificant_pairs' in startup_message
        assert b'entities' in startup_message
        print('server received from %r of length %d' % (addr, len(total_data_string)))
        break
    else:
        total_data.append(data)

# Status updates
udp_socket = socket(AF_INET, SOCK_DGRAM)
udp_socket.bind(('', ECHO_PORT))
while 1:
    data = udp_socket.recv(BUFSIZE)
    status_update = msgpack.unpackb(data)
    assert b'datetime' in status_update
    assert b'locations' in status_update
    print('server update of length %d' % len(data))
