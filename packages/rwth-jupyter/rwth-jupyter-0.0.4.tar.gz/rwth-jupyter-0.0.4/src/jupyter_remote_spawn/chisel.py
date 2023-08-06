import threading
import shutil
import tempfile
import os
import requests
import logging
import gzip

from jupyter_remote_spawn.process import Process
from jupyter_remote_spawn.config import CHISEL_PATH


class Chisel(Process):

    def __init__(self, host, remotes, auth=None, fingerprint=None):
        command = ['chisel', 'client']

        if auth:
            username = auth.get('username')
            password = auth.get('password')

            command += ['--auth', f'{username}:{password}']

        if fingerprint:
            command += ['--fingerprint', fingerprint]

        command += [host] + remotes

        super().__init__('chisel', command)

        self.connected = threading.Event()

    def process_line(self, line):
        if line.find(b'Connected') >= 0:
            self.connected.set()

    @staticmethod
    def install(url):
        # Abort if executable already exists
        if shutil.which('chisel'):
            logging.info('Tool chisel already exists. Skipping installation')
            return

        logging.info('Installing Chisel...')

        # Download an unzip Chisel
        r = requests.get(url)
        with tempfile.TemporaryFile() as tf:
            tf.write(r.content)
            tf.seek(0)

            with gzip.open(tf) as sf:
                with open(CHISEL_PATH, '+wb') as df:
                    df.write(sf.read())

        os.chmod(CHISEL_PATH, 0o744)
