"""
A simple TCP socket client.

Challenge that combine `sys.stdin.read()` with `socat` will hang
many clients. This script calls `socket.shutdown(socket.SHUT_WR)`
to let the server know that it's done sending input.
"""
import socket
import sys


# The size of recv() reads
READ_SIZE = 512


def communicate(host, port):
    """ Read from stdin till EOF, send, then return the results of recv().
    """
    s = socket.socket()
    s.connect((host, port))
    payload = sys.stdin.read().encode()
    s.sendall(payload)
    s.shutdown(socket.SHUT_WR)

    output = []
    while True:
        read = s.recv(READ_SIZE)
        if read:
            output.append(read.decode())
        else:
            break
    return ''.join(output)


def main():
    # A host to which the socket should connect
    host = sys.argv[1]

    # A port to which the socket should connect
    port = int(sys.argv[2])

    result = communicate(host, port)
    print(result)


if __name__ == '__main__':
    main()
