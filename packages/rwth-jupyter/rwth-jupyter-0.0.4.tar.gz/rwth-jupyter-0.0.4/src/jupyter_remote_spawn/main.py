#!/bin/env python3

import atexit
import logging
import os
import pathlib
import requests
import getpass

from jupyter_remote_spawn.config import *
from jupyter_remote_spawn.jupyter import JupyterSingleuser, JupyterHub
from jupyter_remote_spawn.chisel import Chisel
from jupyter_remote_spawn.sshfs import Sshfs
from jupyter_remote_spawn.util import get_free_port, open_link
jupyter = None
chisel = None
sshfs = None


def stop():

    if jupyter is not None:
        jupyter.stop()

    if chisel is not None:
        chisel.stop()

    if sshfs is not None:
        sshfs.unmount()


def main():
    # Setup logging
    FORMAT = '%(asctime)-15s [%(levelname)s] %(message)s'
    logging.basicConfig(level=logging.INFO, format=FORMAT)

    # Register signals for catching Ctrl-C
    atexit.register(stop)

    # Command line arguments
    cfg = get_config()

    # Find free ports
    jupyter_notebook_port = get_free_port()
    jupyter_hub_port = get_free_port()
    sftp_port = get_free_port()

    if None in [jupyter_notebook_port, jupyter_hub_port, sftp_port]:
        raise Exception('Failed to find free ports')

    # Create directories
    pathlib.Path(os.path.dirname(cfg.token_path)).mkdir(parents=True, exist_ok=True)
    pathlib.Path(LOCAL_BIN_PATH).mkdir(parents=True, exist_ok=True)
    os.environ['PATH'] += os.pathsep + LOCAL_BIN_PATH

    if os.environ.get('PYTHONPATH'):
        os.environ['PYTHONPATH'] += os.pathsep + site.USER_BASE + '/lib/python3.6/site-packages'
    else:
        os.environ['PYTHONPATH'] = site.USER_BASE + '/lib/python3.6/site-packages'

    # Install tools
    if cfg.rwth:
        Sshfs.install(cfg.sshfs_url)
        Chisel.install(cfg.chisel_url)

    next = '/user-redirect/'

    hub = JupyterHub(cfg.jupyterhub_url, cfg.token_path)

    hub.login(cfg.token, next)

    # Check if proper server is running in JupyterHub
    server = hub.get_server()
    if server is None:
        hub.spawn()

    # Get tunnel connection details
    r = requests.post(JUPYTERHUB_URL+f'/user/{hub.username}/api/v1',
        headers={
            'Authorization': f'token {hub.api_token}'
        },
        data={
            'stop': 'true'
        })
    r.raise_for_status()

    j = r.json()

    chisel_username = j.get('chisel').get('username')
    chisel_password = j.get('chisel').get('password')
    chisel_fingerprint = j.get('chisel').get('fingerprint')
    jupyter_token = j.get('jupyter').get('token')

    # Establish chisel tunnel
    chisel = Chisel(cfg.jupyterhub_url+f'/user/{hub.username}/', [
            f'{sftp_port}:localhost:7777',
            f'{jupyter_hub_port}:hub.jhub:8081',
            f'R:8890:localhost:{jupyter_notebook_port}'
        ],
        auth={
            'username': chisel_username,
            'password': chisel_password
        },
        fingerprint=chisel_fingerprint)

    if not chisel.connected.wait(timeout=10):
        raise Exception('Failed to connect to chisel server')

    # Start jupyterhub-singleuser
    jupyter = JupyterSingleuser(hub.username, jupyter_token, jupyter_notebook_port, jupyter_hub_port)

    # Mount RWTHjupyter home directory
    if cfg.mount:
        if cfg.rwth:
            # For some reason we can not create an SSHFS mountpoint
            # within an existing NFS mount point which is the case for the RWTH compute cluster
            # As a workaround we mount it into /tmp and create a symlink
            orig_mount_point = cfg.mount_point
            cfg.mount_point = f'/tmp/' + getpass.getuser() + '/jupyter'

            if not os.path.islink(orig_mount_point):
                os.symlink(orig_mount_point, cfg.mount_point)

        sshfs = Sshfs(cfg.mount_point, sftp_port)
        sshfs.mount()

    jupyter.ready.wait()
    open_link(f'{hub.url}/user/{hub.username}/', 'You can now access your RWTHjupyter session here:')
