"""
This module is the canonical way to share global information across modules
"""
import json
import logging.config
import os
from argparse import ArgumentParser
from collections import namedtuple

import coloredlogs
import urllib3

from videotools import APP_KEY_FILE, APP_CONFIG_FILENAME, get_resource_path, \
    APP_LOGGING_FILENAME, APP_LOGLEVEL, ResourceNotFoundException
from videotools.commands.cipher import decrypt

# -- disable verify=False warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# -- github token
GITHUB_TOKEN = None

# -- appconfig

_CONFIG_NAMES = {'ROLE': 'role', 'ADMIN_ROLE': 'admin_role', 'GITHUB': 'github', 'TOKEN': 'token', 'ST2': 'st2',
                 'PRO': 'pro', 'USER': 'user', 'PEMFILE': 'pemfile', 'IPINFO': 'ipinfo'}
CONFIG_FIELDS = namedtuple('ConfigFields', _CONFIG_NAMES.keys())(**_CONFIG_NAMES)

# -- ROLE
# - this role is used to check what actions a user can perform with the tools
ADMIN_ROLE = None

# -- ST2 pem file
ST2SVC_PROD_USER = None
ST2SVC_PROD_PEM_FILE = None


# -- IPinfo Token
IPINFO_TOKEN = None


def get_common_parser():
    """
    Provides the common argument parser to be used in any args parser for our scripts
    :return: An instance of Argument parser with common args to any script
    """
    parser = ArgumentParser()
    group = parser.add_argument_group('Common args')
    group.add_argument('--keyfile', '-KF',
                        help='Optional key file for cypher',
                        dest='keyfile',
                        action='store',
                        required=False)
    group.add_argument('--dry-run', '-DR',
                        help='Do not perform any final action, just inform. (IN PROGRESS)',
                        dest='dryrun',
                        action='store_true',
                        default=False,
                        required=False)
    return parser


# -- load config
class AppConfigNotFoundException(Exception):
    """
    Exception launched when application config is not found
    """


class NotGithubTokenException(Exception):
    """
    Exception launched when github token is missing from configuration
    """


class MissingSt2ConfigException(Exception):
    """
    Exception launched when some part of Stackstorm configuration is missing
    """


# -- init logging
_log_config_file = get_resource_path(APP_LOGGING_FILENAME)
with open(_log_config_file, 'r') as file_:
    logging.config.dictConfig(json.loads(file_.read()))
    logging.root.setLevel(APP_LOGLEVEL)
coloredlogs.install(level=APP_LOGLEVEL)


# -- conf methods

def load_config():
    """
    Loads the content of application appconfig.json file as a dictionary
    """
    global ADMIN_ROLE, GITHUB_TOKEN, ST2SVC_PROD_USER, ST2SVC_PROD_PEM_FILE, IPINFO_TOKEN

    _logger = logging.getLogger('settings')

    # -- create paths and save config files if not exists

    _logger.debug('checking if supplied file [%s] exists...', APP_CONFIG_FILENAME)
    _cfg_file = get_resource_path(APP_CONFIG_FILENAME)
    if not os.path.exists(_cfg_file):
        raise AppConfigNotFoundException(f'Configuration file not found: __{_cfg_file}__')

    # load de file
    _logger.debug('loading config...')
    with open(_cfg_file, 'r') as f:
        data = json.loads(f.read())
        _logger.debug('\t json config [%s]', data)

    # - stackstorm config

    try:
        _logger.debug('loading stackstorm prod configuration...')
        _st2_pro_cfg = data.get(CONFIG_FIELDS.ST2)[CONFIG_FIELDS.PRO]
        try:
            ST2SVC_PROD_USER = _st2_pro_cfg[CONFIG_FIELDS.USER]
            ST2SVC_PROD_PEM_FILE = _st2_pro_cfg[CONFIG_FIELDS.PEMFILE]
        except KeyError as err:
            raise MissingSt2ConfigException('Wrong st2 pro configuration, missing user or pemfile') from err
    except KeyError:
        _logger.debug('\t skipping st2 prod configuration, not found')

    # ------ ENCRYPTED CONFIG BELOW

    # Key file is used to encrypt any tokens or sensitive info, if it does not exists, just return
    try:
        get_resource_path(APP_KEY_FILE)
    except ResourceNotFoundException:
        _logger.debug('\t pass file not found, not decrypting any data from config')
        return

    # -- admin
    try:
        _logger.debug('checking admin role...')
        ADMIN_ROLE = decrypt(text_to_decrypt=data[CONFIG_FIELDS.ADMIN_ROLE])
        _logger.debug('\t OK')
    except KeyError:
        _logger.debug('\t skipping admin config not found')

    # -- github
    try:
        _logger.debug('\t checking if github token exists...')
        GITHUB_TOKEN = decrypt(text_to_decrypt=data[CONFIG_FIELDS.GITHUB][CONFIG_FIELDS.TOKEN])
        _logger.debug('\t\t sucess')
    except KeyError as err:
        _logger.debug('\t skipping token, not found')

    # -- ipinfo
    try:
        _logger.debug('\t checking if ipinfo token exists...')
        IPINFO_TOKEN = decrypt(text_to_decrypt=data[CONFIG_FIELDS.IPINFO][CONFIG_FIELDS.TOKEN])
        _logger.debug('\t\t sucess')
    except KeyError as err:
        _logger.debug('\t skipping token, not found')


load_config()
