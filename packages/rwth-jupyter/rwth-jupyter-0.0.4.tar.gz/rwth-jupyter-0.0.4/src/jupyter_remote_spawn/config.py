import site
import socket
import pathlib
import argparse
import platform


from jupyter_remote_spawn.util import str2bool

PLATFORM = platform.system().lower()
MACHINE = platform.machine()

if MACHINE == 'x86_64':
    ARCH = 'amd64'
elif MACHINE == 'i386':
    ARCH='386'
elif MACHINE == 'aarch64':
    ARCH='arm64'

JUPYTERHUB_URL = 'https://jupyter.rwth-aachen.de'
CHISEL_URL = f'https://github.com/jpillora/chisel/releases/download/v1.7.6/chisel_1.7.6_{PLATFORM}_{ARCH}.gz'
SSHFS_URL = 'https://download-ib01.fedoraproject.org/pub/epel/7/x86_64/Packages/f/fuse-sshfs-2.10-1.el7.x86_64.rpm'

HOME_PATH = str(pathlib.Path.home())

LOCAL_BIN_PATH = f'{site.USER_BASE}/bin'

CHISEL_PATH = f'{LOCAL_BIN_PATH}/chisel'
JUPYTER_PATH = f'{LOCAL_BIN_PATH}/jupyterhub-singleuser'
SSHFS_PATH = f'{LOCAL_BIN_PATH}/sshfs'

USER_MOUNT_PATH = f'{HOME_PATH}/jupyter-home'
MOUNT_PATH = f'{HOME_PATH}/jupyter-home'

def get_config():
    is_rwth = socket.gethostname().endswith('hpc.itc.rwth-aachen.de')

    parser = argparse.ArgumentParser('rwth-jupyter')

    parser.add_argument('--rwth', '-r', type=str2bool, default=is_rwth)

    parser.add_argument('--token', '-t')
    parser.add_argument('--token-path', '-T', default=f'{HOME_PATH}/.jupyter/token')

    parser.add_argument('--mount', '-m', type=str2bool, default=True)
    parser.add_argument('--mount-point', '-M', default=MOUNT_PATH)

    parser.add_argument('--jupyterhub-url', '-J', default=JUPYTERHUB_URL)
    parser.add_argument('--sshfs-url', '-S', default=SSHFS_URL)
    parser.add_argument('--chisel-url', '-C', default=CHISEL_URL)

    return parser.parse_args()
