"""
Module with logic to create, edit and convert inventory files
"""
import json
import logging
import os
from argparse import ArgumentTypeError
from collections import namedtuple

from stringcolor import cs
from tqdm import tqdm

import videotools.cdn as cdn_plat
from videotools import COMMANDS
from videotools.model import COLOR_RED, COLOR_BLUE, COLOR_GREEN, COLOR_GRAY, COLOR_YELLOW
from videotools.net import CouldNotGetIpInfoException, get_ip_location
from videotools.utils import DateTimeHelper

_logger = logging.getLogger('cdn_cmd')

ENV_NAMES = {'PRO': 'PRO', 'PRE': 'PRE', 'OPT': 'OPT', 'CERT': 'CERT', 'DEV': 'DEV', 'QA': 'QA'}
ENV_NAME = namedtuple('EnvName', ENV_NAMES.keys())(**ENV_NAMES)


class WrongColumnFormatError(ArgumentTypeError):
    """
    Exception launched when supplied column names are not correct
    """

    def __init__(self, col_names):
        super().__init__(cs(f'Supplied column names [ {col_names} ] is not a string of names separated by colon',
                            COLOR_RED))


class WrongFilterFormatError(ArgumentTypeError):
    """
    Exception launched when supplied string filter is not correct
    """

    def __init__(self, _fstring):
        super().__init__(cs(f'Supplied filter [ {_fstring} ] is not correct', COLOR_RED))


class MissingColumnFilterException(ArgumentTypeError):
    """
    Exception launched when string filter is required in a command
    """

    def __init__(self):
        super().__init__(cs(f'Missing required filter', COLOR_RED))


# -- methods

def _search_inventory(env, **kwargs):
    """
    Searches into a given inventory with supplied filter values,a nd always provides Management and Service IP addresses
    :param env: Name of the environment for the inventory or file to search into
    :param kwargs: Any extra arguments
           csvfilter: A CSV formatted line with key:value pairs to match in inventory. If key:value pairs
                      are found, a dictionary is returned. If only key values are provided (separated by semicolon too),
                      an array is returned, for example:  role:endpoint;site_id:Madrid... or ROLE;CITY;HOSTNAME ...
                      Multiple values can be provided for filtering as  key1:value1,value2;key2:value1;key3:value1 ...
    :param columns: If given, inventory will be filtered again to removed all columns not given in this list. Powerful
                    when combined with csvfilter
    :return: A dictionary with found inventory content
    """
    csvfilter = kwargs.get('csvfilter', '')

    _logger.info('searching in inventory...')

    # load inventory
    inventory = cdn_plat.load_inventory(env, **kwargs)

    # filter environment if needed
    if not csvfilter and not kwargs.get('columns'):
        return inventory

    # filter inventory
    return cdn_plat.filter_inventory(inventory, **kwargs)


def _convert_inventory(env, **kwargs):
    """
    Converts a given inventory into another format for processing
    :param env: A given inventory, either as filepath, a dictionary or a string in json format
    :param kwargs: Any given extra args
        gpsdata: If given, a new file with gps data is generated with inventory fields:
                 hostname, latitude, longitude, country, city from supplied environment or file
    :return: Creates a file with new format
    """
    gps = kwargs.get('gps', False)
    udnodes = kwargs.get('udnodes', False)
    st2ssh = kwargs.get('st2ssh', False)

    _logger.debug('processing inventory environment %s ...', env)

    # load inventory
    inventory = cdn_plat.load_inventory(env, **kwargs)

    # proceed with transformations
    if gps:
        _logger.debug('\t converting inventory to gpsdata format...')
        cdn_plat.gen_gpsdata(inventory, **kwargs)

    if udnodes:
        _logger.debug('\t converting inventory to ud_nodes format...')
        cdn_plat.gen_udnodes(inventory, env=env, **kwargs)

    if st2ssh:
        _logger.debug('\t converting inventory to st2ssh format...')
        cdn_plat.gen_st2ssh(inventory, **kwargs)


def _show_info(env, ipaddress, **kwargs):
    """
    Shows node information, if found, with given data. Current implementation searches in the fields of
    ipaddress management, service and service_iptv
    :param env: A given inventory, either as filepath, a dictionary or a string in json format
    :param ipaddress: Any ipaddress to look into nodes interfaces. It doesn't have to be complete, it'll be searched
       forward from left to right
    :return: Node information
    """
    _logger.info('searching for node with ipaddress [ %s ] ...', ipaddress)

    # load inventory
    inventory = cdn_plat.load_inventory(env, **kwargs)

    try:
        # search for node with supplied ipaddress
        _node = cdn_plat.node_info(inventory, ipaddress, **kwargs)

        if not _node:
            raise cdn_plat.NodeNotFoundError()

        print('-'*80)
        print(cs('Node info:', COLOR_YELLOW))
        print()
        for _key, _value in _node.items():
            _line = cs(f'{_key:>30}:', COLOR_BLUE)
            if ipaddress in _value:
                _line += cs(f'\t{_value:<40}', COLOR_GREEN)
            else:
                _line += cs(f'\t{_value:<40}', COLOR_GRAY)
            print(_line)
        print('-'*80)
    except cdn_plat.NodeNotFoundError:
        print(cs('No results fond', COLOR_BLUE))



def init_parser(parent_parser):
    cdn_parser = parent_parser.add_parser(COMMANDS.CDN,
                                          help='Used to create, edit or convert any file with cdn nodes inventory')
    common_grp = cdn_parser.add_argument_group('Common args')
    common_grp.add_argument('--version', type=lambda v: cdn_plat.check_version(version=v),
                            help='Use this CDN version when loading inventory files', required=False, default='8.2.0')
    #
    # -- subparsers
    cdn_subparsers = cdn_parser.add_subparsers()
    cdn_subparsers.required = True

    # -- new inventory
    cmd_search = cdn_subparsers.add_parser('find', help='Search cdn inventory file')
    cmd_search.set_defaults(func=_search_inventory)
    cmd_search.add_argument('env', nargs='?', help='Name of the environment for the inventory, or a file '
                                                   'to load the inventory from', default=ENV_NAME.PRO)
    cmd_search.add_argument('csvfilter', nargs='?', type=lambda csvfilter: cdn_plat.check_csvfilter(csvfilter),
                            help='A CSV formatted line with key:value pairs to match in inventory. If key:value pairs '
                                 'are found, a dictionary is returned. If only key values are provided (separated by '
                                 'semicolon too), an array is returned, for example:  role:endpoint;site_id:Madrid... '
                                 'or ROLE;CITY;HOSTNAME ... Multiple values can be provided for filtering as '
                                 ' key1:value1,value2;key2:value1;key3:value1 ...', default='')
    cmd_search.add_argument('--columns', required=False, help='If given, inventory will be filtered again '
                                                              'to removed all columns not given in this list. Powerful '
                                                              'when combined with csvfilter',
                            type=lambda columns: cdn_plat.check_csvfilter(columns), default='')
    cmd_search.add_argument('--case', required=False, action='store_true',
                            help='If given, inventory will be filtered using case sensitive matching', default=False)
    cmd_search.add_argument('--sort', required=False, help='If given, inventory will be sorted ascending by given '
                                                           'column name, if exists', default='hostname')
    cmd_search.add_argument('--json', required=False, action='store_true',
                            help='If given, inventory will be save in a json file', default=False)

    # convert content to another formats or file types
    cmd_conv = cdn_subparsers.add_parser('conv', help='Uses inventory content to create other types of files')
    cmd_conv.set_defaults(func=_convert_inventory)
    cmd_conv.add_argument('env', nargs='?', help='Name of the environment to load the inventory: pro, pre, opt',
                          type=lambda env: cdn_plat.check_environment(env), default=ENV_NAME.PRO)
    cmd_conv.add_argument('--gps', required=False, action='store_true',
                          help='If given, a new file with gps information is generated with inventory fields: '
                               'hostname, latitude, longitude, country, city from supplied environment name',
                          default=False)
    cmd_conv.add_argument('--udnodes', required=False, action='store_true',
                          help='If given, a new file with ud_nodes format is generated with inventory fields: '
                               'Service IP|HOSTNAME|ROLE|deliveryRegion|Country|latitude|longitud from supplied '
                               'environment. Gps data file must exists, either supplied with '
                               '--gpsdata option, or from default environment location',
                          default=False)

    cmd_conv.add_argument('--gpsdata', required=False, help='If given, this file will be used to get location '
                                                            'information, instead of default one, which may be created '
                                                            'if does not exists',
                          type=lambda _filepath: cdn_plat.check_gpsdata_file(_filepath, load=True), default=None)

    cmd_conv.add_argument('--st2ssh', required=False,
                          help="If given, a new csv formatted file with commands for ssh batch execution is created,"
                               "from given environment name. User and password/keyfile is used from appconfig file, "
                               "and default port and timeout options are got from ssh module. "
                               "then, a csv string is expected with this format:"
                               "description 1#command1;description 2 #command2:...", default=''
                          )

    # convert content to another formats or file types
    cmd_info = cdn_subparsers.add_parser('info', help='Prints a specific node information based on supplied ipaddress')
    cmd_info.set_defaults(func=_show_info)
    cmd_info.add_argument('env', nargs='?', help='Name of the environment to load the inventory: pro, pre, opt',
                          type=lambda env: cdn_plat.check_environment(env), default=ENV_NAME.PRO)
    cmd_info.add_argument('ipaddress', nargs='?', help='Any ipaddress of the node, management, service or iptv',
                          type=str, default=None)

    return cdn_parser


def command(args):
    """
    Process the call in a script with supplied args
    """
    # copy of arguments for function
    cmd_args = vars(args).copy()

    # remove function from copied args
    func = cmd_args.pop('func')

    # execute func and print output if str or int
    _result = args.func(**cmd_args)

    if func.__name__ in (_search_inventory.__name__,):
        if cmd_args.get('json'):
            _filename = f'cdn_search_results_{DateTimeHelper.short_date()}.json'
            with open(_filename, 'w') as _file:
                _file.write(json.dumps(_result, indent=4))
                _file.flush()
                _logger.info(f'new inventory in file [ %s ]', _filename)
        else:
            cmd_args['html'] = os.path.isfile(cmd_args['env']) and cmd_args['env'].endswith('html')
            cdn_plat.print_inventory(_result, **cmd_args)
