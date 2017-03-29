import socket
import time


s = socket.socket()
for i in range(10):
    try:
        s.connect(('database', 5432))
    except (ConnectionError, socket.error):
        print('Connection failed. Sleeping briefly.')
        time.sleep(2)
    else:
        print('Connected!')
        break

