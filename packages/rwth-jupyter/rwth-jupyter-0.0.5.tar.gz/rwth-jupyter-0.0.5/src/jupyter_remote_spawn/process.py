import threading
import subprocess
import logging
import sys
import os

class Process(threading.Thread):

    def __init__(self, name, command, env=None):
        super().__init__()

        self.name = name
        self.command = command
        self.env = env

        self.start()

    def stop(self):
        self.process.kill()
        self.process.wait()

        self.join()

    def process_line(self, line):
        pass

    def run(self):
        logging.info('Starting %s process in background: %s', self.name, ' '.join(self.command))

        self.process = subprocess.Popen(self.command,
                             env=self.env or os.environ,
                             shell=False,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT)

        for line in iter(self.process.stdout.readline, ''):
            sys.stdout.buffer.write(line)
            sys.stdout.flush()

            self.process_line(line)

            rc = self.process.poll()
            if rc is not None:
                break

        logging.info('Process %s has stopped: rc=%d', self.name, rc)


def run(command):
    logging.info('Running command: %s', ' '.join(command))

    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in iter(process.stdout.readline, ''):
        sys.stdout.buffer.write(line)
        sys.stdout.flush()

        rc = process.poll()
        if rc is not None:
            break

    return rc
