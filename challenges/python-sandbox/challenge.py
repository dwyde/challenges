"""
A helper module for the python-sandbox CTF challenge.

Sets up subprocess to enforce resource limits.
"""
import resource
import sys

import tornado.process


async def main(user_input):
    """ Create a subprocess to run input in a sandbox.
    """
    proc = tornado.process.Subprocess(
        [sys.executable, 'sandbox.py'],
        stdin=tornado.process.Subprocess.STREAM,
        stdout=tornado.process.Subprocess.STREAM,
        preexec_fn=setup
    )

    proc.stdin.write(user_input.encode())
    proc.stdin.close()

    output = await proc.stdout.read_until_close()
    proc.stdout.close()
    return output.decode()


def setup():
    """ Impose resource limits on the worker process.
    """
    resource.setrlimit(resource.RLIMIT_CPU, (1, 1))
    resource.setrlimit(resource.RLIMIT_RSS, (30000, 30000))
    resource.setrlimit(resource.RLIMIT_FSIZE, (1024, 1024))
    resource.setrlimit(resource.RLIMIT_NOFILE, (100, 100))
    resource.setrlimit(resource.RLIMIT_NPROC, (0, 0))

