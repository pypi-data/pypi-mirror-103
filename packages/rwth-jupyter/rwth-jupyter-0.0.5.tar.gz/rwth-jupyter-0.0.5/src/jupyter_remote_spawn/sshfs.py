import shutil
import logging
import os
import pathlib
import requests
import tempfile
import rpmfile

from jupyter_remote_spawn.process import run
from jupyter_remote_spawn.config import SSHFS_PATH


class Sshfs:

    def __init__(self, mp, port):
        self.mount_point = mp
        self.port = port

    def mount(self):
        logging.info('Mounting RWTHjupyter home...')

        # Create mountpoint
        pathlib.Path(self.mount_point).mkdir(parents=True, exist_ok=True)

        if os.path.ismount(self.mount_point):
            logging.warn('Already mounted')
            return

        options = {
            'directport': self.port,
            'cache': True,
            'cache_max_size': 536870912, # 512 MiB
            'cache_timeout': 60,
            'compression': False,
            'kernel_cache': None,
            'auto_cache': None,
            'large_read': None
        }

        command = ['sshfs']

        for k, v in options.items():
            if v is None:
                command += ['-o', k]
            else:
                if v in [True, False]:
                    v = 'yes' if v else 'no'

                command += ['-o', f'{k}={v}']

        command += ['127.0.0.1:/home/jovyan', self.mount_point]

        rc = run(command)
        if rc != 0:
            raise Exception('Failed to mount remote dir: rc=' + rc)


    def sshfs_unmount():
        if os.path.ismount(self.mount_point):
            logging.info('Un-mounting RWTHjupyter home...')

            run(['fusermount', '-u', self.mount_point])

    @staticmethod
    def install(url):
        # Abort if executable already exists
        if shutil.which('sshfs'):
            logging.info('Tool sshfs already exists. Skipping installation')
            return

        logging.info('Install sshfs...')

        # Download an extract executable from RPM
        r = requests.get(url)
        with tempfile.TemporaryFile() as tf:
            tf.write(r.content)
            tf.seek(0)
        
            with rpmfile.open(fileobj=tf) as f:
                with f.extractfile('./usr/bin/sshfs') as sf:
                    with open(SSHFS_PATH, 'wb') as df:
                        df.write(sf.read())

        os.chmod(SSHFS_PATH, 0o744)
