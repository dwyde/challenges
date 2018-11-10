"""
A helper module for the python-sandbox CTF challenge.

Sets up subprocess to enforce resource limits.
"""
import resource
import subprocess


def main(user_input):
    proc = subprocess.Popen(
        ['python3', 'sandbox.py'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        universal_newlines=True,
        preexec_fn=setup
    )
    output, _ = proc.communicate(user_input)
    proc.stdin.close()
    proc.stdout.close()
    return output


def setup():
    resource.setrlimit(resource.RLIMIT_CPU, (1, 1))
    resource.setrlimit(resource.RLIMIT_RSS, (30000, 30000))
    resource.setrlimit(resource.RLIMIT_FSIZE, (1024, 1024))
    resource.setrlimit(resource.RLIMIT_NOFILE, (100, 100))
    resource.setrlimit(resource.RLIMIT_NPROC, (0, 0))

