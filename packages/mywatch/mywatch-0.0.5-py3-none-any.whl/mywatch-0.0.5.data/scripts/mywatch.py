#!python
import os
import sys
import subprocess
import checksumdir
import signal
from time import sleep


_dir = sys.argv[1]
command = sys.argv[2]


def kill(pid):
    try:
        os.killpg(os.getpgid(pid), signal.SIGINT)
    except ProcessLookupError:
        pass


if __name__ == '__main__':
    try:
        process = subprocess.Popen(command, shell=True, start_new_session=True)
        dirhash = checksumdir.dirhash(_dir)
        while True:
            sleep(1)
            new_hash = checksumdir.dirhash(_dir)
            if new_hash != dirhash:
                print(f"Change detected, new hash: {new_hash}")
                kill(process.pid)
                dirhash = new_hash
                process = subprocess.Popen(command, shell=True, start_new_session=True)
    except KeyboardInterrupt:
        kill(process.pid)
