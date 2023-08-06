import requests
import logging
import secrets
import string
import urllib
import json
import os
import threading

from jupyter_remote_spawn.process import Process
from jupyter_remote_spawn.config import HOME_PATH
from jupyter_remote_spawn.util import open_link


class JupyterSingleuser(Process):

    def __init__(self, username, token, notebook_port, hub_port):
        hub_api_url = f'http://localhost:{hub_port}/hub/api'
        env={
            **os.environ,
            'JUPYTERHUB_API_TOKEN': token,
            'JUPYTERHUB_CLIENT_ID': f'jupyterhub-user-{username}',
            'JUPYTERHUB_API_URL': hub_api_url,
            'JUPYTERHUB_ACTIVITY_URL': f'{hub_api_url}/users/{username}/activity',
            'JUPYTERHUB_OAUTH_CALLBACK_URL': f'/user/{username}/oauth_callback',
            'JUPYTERHUB_USER': username
        }

        options = {
            'SingleUserNotebookApp.base_url': f'/user/{username}',
            'SingleUserNotebookApp.port': notebook_port,
            'SingleUserNotebookApp.allow_origin': '*',
        }

        command = ['jupyterhub-singleuser']

        for k, v in options.items():
            command += [f'--{k}', str(v)]

        command.append(HOME_PATH)

        self.ready = threading.Event()

        super().__init__('jupyter', command, env=env)

    def process_line(self, line):
        if line.find(b'Updating Hub with activity every') >= 0:
            logging.info('Jupyter singleuser server started...')
            self.ready.set()


class JupyterHub:

    def __init__(self, url, token_path):
        self.url = url
        self.token_path = token_path

    def get_username(self, token):
        r = requests.get(self.url+'/hub/api/user',
            headers={
                'Authorization': f'token {token}'
            })
        r.raise_for_status()

        return r.json().get('name')

    def get_token(self, next=None):
        # Generate random reflection token
        reflect_token = ''.join(secrets.choice(string.ascii_letters + string.digits) for i in range(32))

        url = f'{self.url}/services/reflector/api/request/{reflect_token}'
        if next:
            url += '?next=' + urllib.parse.quote_plus(next)
            
        # Direct user to token reflector
        open_link(url, 'Please visit the following link to generate an API token for RWTHjupyter:')
        logging.info('Waiting for token...')

        r = requests.get(f'{self.url}/services/reflector/api/retrieve/{reflect_token}',
            timeout=60)
        r.raise_for_status()

        return r.json()

    @property
    def api_token(self):
        return self.token.get('token')

    def login(self, api_token, next=None):

        # Check if privided token is valid
        if api_token:
            self.token = {
                'token': api_token
            }
            try:
                self.username = self.get_username(self.api_token)
            except requests.RequestException as e:
                raise Exception('Invalid command line token: ' + str(e))
        else:
            try:
                with open(self.token_path, 'r') as tf:
                    logging.info('Found existing API token for JupyterHub')
                    self.token = json.load(tf)
            except (OSError, KeyError, json.JSONDecodeError):
                logging.error('Existing token is invalid. Requesting a new one...')

                try:
                    self.token = self.get_token(next)
                except requests.RequestException as e:
                    logging.error('Failed to get token via reflector: %s', e)
                    logging.error('')

                    self.token = {
                        'token': input('Please provide a token by hand: ')
                    }

            try:
                self.username = self.get_username(self.api_token)
            except requests.RequestException as e:
                raise Exception('Invalid command line token: ' + str(e))

        logging.info('Got RWTHjupyter token: %s', self.api_token)
        logging.info('Got RWTHjupyter username: %s', self.username)
        logging.info('Saving token to: %s', self.token_path)

        with open(self.token_path, 'w+') as tf:
            json.dump(self.token, tf)

    def spawn(self, slug='remote-spawn'):
        logging.info('Spawning JupyterHub session...')

        r = requests.post(f'{self.url}/hub/api/users/{self.username}/server',
            headers={
                'Authorization': f'token {self.api_token}'
            },
            json={
                'profile': slug
            })
        r.raise_for_status()

        # Observe progress
        r = requests.get(f'{self.url}/hub/api/users/{self.username}/server/progress',
            headers={
                'Authorization': f'token {self.api_token}'
            },
            stream=True,
            timeout=60)

        for raw_line in r.iter_lines():
            if raw_line:
                line = raw_line.decode('utf-8')

                if line.startswith('data: '):
                    payload_raw = line[6:]
                    payload = json.loads(payload_raw)

                    raw = payload.get('raw_event')
                    if raw:
                        type = raw.get('type')
                        if type in ['Warning']:
                            log = logging.warn
                        elif type in ['Normal']:
                            log = logging.info
                        else:
                            log = logging.info

                        log('  %d%% - %s',
                            payload.get('progress'),
                            raw.get('message')
                        )
                    else:
                        logging.info('  %d%% - %s',
                            payload.get('progress'),
                            payload.get('message')
                        )


    def get_server(self):
        r = requests.get(f'{self.url}/hub/api/user',
            headers={
                'Authorization': f'token {self.api_token}'
            })
        r.raise_for_status()

        j = r.json()

        return j.get('server')
