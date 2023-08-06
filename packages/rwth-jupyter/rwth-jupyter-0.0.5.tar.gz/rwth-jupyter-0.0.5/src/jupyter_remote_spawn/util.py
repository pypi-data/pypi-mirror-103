import webbrowser
import socket
import random
import logging

def open_link(url, message):
    ctl = webbrowser.get()

    if hasattr(ctl, 'name') and ctl.name in ['lynx']:
        logging.info('')
        logging.info(message)
        logging.info('')
        logging.info('       %s', url)
        logging.info('')
    else:
        logging.info('Opening webbrowser: %s', url)
        ctl.open(url)

def get_free_port():
    for _ in range(5):
        port = random.randint(1024, 65535)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            r = sock.connect_ex(('127.0.0.1', port))
            if r != 0:
                return port

def str2bool(v):
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')
