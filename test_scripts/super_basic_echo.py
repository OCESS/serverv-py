#!/usr/bin/env python3

# Shitty echo server for serverv-py
#
# Usage: shitty_serverv_echo.py
# and then start up serverv-py

from socket import *
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
        startup_message = msgpack.unpackb(b''.join(total_data))
        assert b'background_stars' in startup_message
        assert b'insignificant_pairs' in startup_message
        assert b'entities' in startup_message
        print('server received from %r of length %d' % (addr, len(startup_message)))
        break
    else:
        total_data.append(data)

# Status updates
udp_socket = socket(AF_INET, SOCK_DGRAM)
udp_socket.bind(('', ECHO_PORT))
while 1:
    status_update = msgpack.unpackb(udp_socket.recv(BUFSIZE))
    assert b'datetime' in status_update
    assert b'locations' in status_update
    print('server update of length %d' % len(status_update))
