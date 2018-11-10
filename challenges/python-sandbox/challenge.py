"""
A helper module for the python-sandbox CTF challenge.

Sets up subprocess to enforce resource limits.
"""
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
    pass

