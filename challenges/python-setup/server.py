"""
Code heavily based on:
https://docs.python.org/3/library/asyncio-protocol.html#tcp-echo-server-protocol
"""
import asyncio

import challenge

# The host on which this server will listen.
HOST = '0.0.0.0'

# The port on which this server will listen.
PORT = 8888


class EchoServerClientProtocol(asyncio.Protocol):

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        message = data.decode().strip()

        try:
            result = challenge.main(message)
        except Exception as ex:
            result = str(ex)

        output = '{}\n'.format(result).encode()
        self.transport.write(output)
        self.transport.close()

def main():
    loop = asyncio.get_event_loop()
    # Each client connection will create a new protocol instance
    coro = loop.create_server(EchoServerClientProtocol, HOST, PORT)
    server = loop.run_until_complete(coro)

    # Serve requests until Ctrl+C is pressed
    print('Serving on {}'.format(server.sockets[0].getsockname()))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    # Close the server
    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


if __name__ == '__main__':
    main()
