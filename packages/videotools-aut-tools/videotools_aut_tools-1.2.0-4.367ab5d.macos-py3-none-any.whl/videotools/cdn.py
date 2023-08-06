"""
Module with convenience methods to perform operations on cdn infrastructure
"""
import json
import logging
import os
import re
from collections import namedtuple
from json import JSONDecodeError

import yaml
from bs4 import BeautifulSoup
from stringcolor import cs
from tqdm import tqdm

from videotools import APP_CDN_DIR
from videotools.model import ColoredException, COLOR_RED, COLOR_YELLOW, COLOR_BLUE, MissingArgumentException, \
    WrongFileTypeException
from videotools.net import CouldNotLoadFileFromUrl, get_httpfile_content, get_ip_location, CouldNotGetIpInfoException
from videotools.settings import ST2SVC_PROD_USER, ST2SVC_PROD_PEM_FILE
from videotools.utils import FileNotExistsError, check_file, DateTimeHelper, build_csv_filter, filter_dict, \
    WrongCsvFormatException

CDN_VERSION_PATTERN = re.compile(r'\d+\.\d+\.\d+')

# -- html

_CDN_ENV_NAMES = {
    'PRO': {
        'html': 'http://cdn-deploy-manager.cdn.hi.inet/cdn/apps/docviewer/VERSION/docs/view/environment/ips/production.html',
        'yaml': 'http://cdn-deploy-manager.cdn.hi.inet/cdn/repositories/VERSION/docs/environment/production.yaml',
        'local': 'cdn_pro_VERSION.json',
        'gps': 'cdn_pro_gps_VERSION.json'},
    'PRE': {'html': '',
            'yaml': 'http://cdn-deploy-manager.cdn.hi.inet/cdn/repositories/VERSION/docs/environment/prepro.yaml',
            'local': 'cdn_pre_VERSION.json',
            'gps': 'cdn_pre_gps_VERSION.json'},
    'OPT': {'html': '',
            'yaml': 'http://cdn-deploy-manager.cdn.hi.inet/cdn/repositories/VERSION/docs/environment/opt.yaml',
            'local': 'cdn_opt_VERSION.json',
            'gps': 'cdn_opt_gps_VERSION.json'},
    'CERT': {
        'html': 'http://cdn-deploy-manager.cdn.hi.inet/cdn/apps/docviewer/VERSION/docs/view/environment/ips/cert.html',
        'yaml': '',
        'local': '',
        'gps': ''},
    'DEV': {'html': '',
            'yaml': '',
            'local': '',
            'gps': ''},
    'QA': {'html': '',
           'yaml': '',
           'local': '',
           'gps': ''}}

CDN_ENV = namedtuple('CdnEnvInventory', _CDN_ENV_NAMES.keys())(**_CDN_ENV_NAMES)

_CDN_HTML_COLUMN_NAMES = {'SITE_ID': 'Site-Id',
                          'ROLE': 'Role', 'NAME': 'Name', 'REGION': 'Region', 'MANAGEMENT': 'Management',
                          'IPV4': 'IPv4',
                          'IPV6': 'IPv6', 'SERVICE': 'Service', 'SERVICE_IPTV': 'Service_IPTV',
                          'INTERNODE': 'Internode',
                          'STORAGE': 'Storage', 'BACKUP': 'Backup', 'ILO': 'Ilo', 'VIP': 'Vip',
                          'CLUSTER_ID': 'Cluster-id'}
CDN_HTML_COLUMN = namedtuple('CdnInventoryColumNames', _CDN_HTML_COLUMN_NAMES.keys())(**_CDN_HTML_COLUMN_NAMES)

_CDN_INVENTORY_HTML_COLUMNS = {0: CDN_HTML_COLUMN.SITE_ID, 1: CDN_HTML_COLUMN.ROLE, 2: CDN_HTML_COLUMN.NAME,
                               3: CDN_HTML_COLUMN.REGION,
                               4: CDN_HTML_COLUMN.MANAGEMENT, 5: CDN_HTML_COLUMN.IPV4, 6: CDN_HTML_COLUMN.IPV6,
                               7: CDN_HTML_COLUMN.SERVICE, 8: CDN_HTML_COLUMN.IPV4, 9: CDN_HTML_COLUMN.IPV6,
                               10: CDN_HTML_COLUMN.SERVICE_IPTV, 11: CDN_HTML_COLUMN.IPV4, 12: CDN_HTML_COLUMN.IPV6,
                               13: CDN_HTML_COLUMN.INTERNODE, 14: CDN_HTML_COLUMN.IPV4,
                               15: CDN_HTML_COLUMN.STORAGE, 16: CDN_HTML_COLUMN.IPV4,
                               17: CDN_HTML_COLUMN.BACKUP, 18: CDN_HTML_COLUMN.IPV4,
                               19: CDN_HTML_COLUMN.ILO, 20: CDN_HTML_COLUMN.VIP, 21: CDN_HTML_COLUMN.CLUSTER_ID}

_CDN_INVENTORY_HTML_COLUMNS_INTERFACES = (4, 7, 10, 13, 15, 17)

# -- yaml
_CDN_YAML_KEY_NAMES = {'NAME': 'name', 'FQDN': 'fqdn', 'HOSTNAME': 'hostname', 'SITE_ID': 'site_id',
                       'REGION_NAME': 'region_name', 'OB': 'ob', 'COUNTRY': 'country', 'CITY': 'city',
                       'ROLE': 'role', 'IPADDRESS_MANAGEMENT': 'ipaddress_management',
                       'IPADDRESS_SERVICE': 'ipaddress_service', 'IPADDRESS_SERVICE_IPTV': 'ipaddress_service_iptv'}
CDN_YAML_KEY = namedtuple('CdnYamlKey', _CDN_YAML_KEY_NAMES.keys())(**_CDN_YAML_KEY_NAMES)

_CDN_YAML_INTERFACE_NAMES = [CDN_YAML_KEY.IPADDRESS_MANAGEMENT, CDN_YAML_KEY.IPADDRESS_SERVICE,
                             CDN_YAML_KEY.IPADDRESS_SERVICE_IPTV]

_CDN_YAML_HEADER_SIZE = {CDN_YAML_KEY.FQDN: 35, CDN_YAML_KEY.HOSTNAME: 28, CDN_YAML_KEY.SITE_ID: 30,
                         CDN_YAML_KEY.SITE_ID: 30, CDN_YAML_KEY.REGION_NAME: 14, CDN_YAML_KEY.OB: 14,
                         CDN_YAML_KEY.COUNTRY: 10, CDN_YAML_KEY.CITY: 30, CDN_YAML_KEY.ROLE: 15,
                         CDN_YAML_KEY.IPADDRESS_MANAGEMENT: 16, CDN_YAML_KEY.IPADDRESS_SERVICE: 16,
                         CDN_YAML_KEY.IPADDRESS_SERVICE_IPTV: 16}

# our created inventory
INVENTORY_REQUIRED_KEYS = ['date', 'hosts']

# -- gpsdata fields
_GPSDATA_NAMES = {'LATITUDE': 'latitude', 'LONGITUDE': 'longitude'}
GPSDATA_NAME = namedtuple('GpsDataName', _GPSDATA_NAMES.keys())(**_GPSDATA_NAMES)

# exclusive gpsdata
GPSDATA_FIELDS = [GPSDATA_NAME.LATITUDE, GPSDATA_NAME.LONGITUDE]

# gps data fields from cdn inventory
GPSDATA_INVENTORY_FIELDS = [CDN_YAML_KEY.HOSTNAME, CDN_YAML_KEY.COUNTRY, CDN_YAML_KEY.CITY,
                            CDN_YAML_KEY.IPADDRESS_SERVICE]

# mapping between ipinfo values and flink fields
# INTERFAZ|HOSTNAME|ROLE|deliveryRegion|Country|City|latitud|longitud
UD_NODE_INVENTORY_FIELDS_SERVICE = [CDN_YAML_KEY.IPADDRESS_SERVICE, CDN_YAML_KEY.HOSTNAME, CDN_YAML_KEY.ROLE,
                                    CDN_YAML_KEY.REGION_NAME, CDN_YAML_KEY.COUNTRY, CDN_YAML_KEY.CITY]
UD_NODE_INVENTORY_FIELDS_SERVICE_IPTV = [CDN_YAML_KEY.IPADDRESS_SERVICE_IPTV, CDN_YAML_KEY.HOSTNAME, CDN_YAML_KEY.ROLE,
                                         CDN_YAML_KEY.REGION_NAME, CDN_YAML_KEY.COUNTRY, CDN_YAML_KEY.CITY]
UD_NODE_GPS_FIELDS = [GPSDATA_NAME.LATITUDE, GPSDATA_NAME.LONGITUDE]

# -----------

_logger = logging.getLogger('cdn')


class CouldNotGetHttpInventoryException(ColoredException):
    """
    Exception launched when inventory can not be obtained form url
    """


class CouldNotReadInventoryException(ColoredException):
    """
    Exception launched when inventory can not be red
    """


class CouldNotFindHtmlTableException(ColoredException):
    """
    Exception launched when a table can not be found in html content
    """


class CouldNotParseHtmlTableException(ColoredException):
    """
    Exception launched when a table can not be parse for some reason, maybe there is an error in a row, a column...
    """


class CouldNotFindHtmlColumnException(ColoredException):
    """
    Exception launched when supplied column name is not found in inventory table
    """


class MissingEnvArgumentException(ColoredException):
    """
    Exception launched when required environment namedptuple value is not supplied
    """

    def __init__(self):
        super().__init__('env argument must be supplied when inventory is a file')


class WrongEnvironmentException(ColoredException):
    """
    Exception launched when supplied environment is not a supported one
    """

    def __init__(self, env_name):
        super().__init__('Supplied environment is not supported', env_name=env_name)


class SkipNodeFilterException(Exception):
    """
    Used to escape inner loop during inventory's table parsing
    """


class CouldNotBuildInventoryException(ColoredException):
    """
    Exception launched when inventory can not be build with supplied content
    """


class WrongInventoryException(ColoredException):
    """
    Exception launched when supplied inventory has not correct keys
    """

    def __init__(self, inventory_keys):
        super().__init__('Supplied inventory has not required format', keys=inventory_keys,
                         required_keys=INVENTORY_REQUIRED_KEYS)


class CouldNotFilterInventoryException(ColoredException):
    """
    Exception launched when inventory can not be filtered with supplied filter
    """


class CouldNotFindYamlKeyException(ColoredException):
    """
    Exception launched when supplied yaml key name is not found in inventory
    """


class MissingGpsDataFile(ColoredException):
    """
    Exception launched when gps data file can not be found
    """

    def __init__(self, _gpsdatafile):
        super().__init__('Missing gps data file', _file=_gpsdatafile)


class CouldNotLoadGpsDataFile(ColoredException):
    """
    Exception launched when gps data file can not be loaded for some reason
    """


class NodeNotFoundError(ColoredException):
    """
    Exception launched when certain searched node is not found
    """

# -- logic

def node_info(inventory, ipaddress, **kwargs):
    """
    Searches for supplied ipaddress in supplied inventory
    :param inventory: A given inventory as a dictionary
    :param ipaddress: Any ipaddress to look into nodes interfaces. It doesn't have to be complete, it'll be searched
       forward from left to right
    :param kwargs: Any extra arguments
    :return: Found node info as dict,  if any
    """
    _logger.debug('searching node info with ipaddress [ %s ]', ipaddress)
    try:
        return next(filter(lambda h: ipaddress in h[CDN_YAML_KEY.IPADDRESS_MANAGEMENT] or
                              ipaddress in h[CDN_YAML_KEY.IPADDRESS_SERVICE] or
                              ipaddress in h[CDN_YAML_KEY.IPADDRESS_SERVICE_IPTV], inventory['hosts']))
    except StopIteration:
        _logger.debug('\t no host found with ippaddress [ %s ]', ipaddress)
        raise NodeNotFoundError('Could not found node with supplied data', ipaddress=ipaddress)


def load_gpsdata_file(filepath, **kwargs):
    """
    Loads supplied gpsdata file. If none is given, then it's loaded from supplied environment
    :param filepath: File to load gpsdata from
    :pram kwargs: Extra arguments
            version: CDN inventory version
                env: CDN environment. A valid value from namedtuple
    """

    version = check_version(kwargs.get('version'))
    env = check_environment(kwargs.get('env'))

    try:
        if filepath:
            return check_gpsdata_file(filepath, load=True)
    except FileNotExistsError:
        _logger.info('\t filepath supplied not found [ %s ]', filepath)

    # load from environment
    try:
        filepath = os.path.join(APP_CDN_DIR, env['gps'].replace('VERSION', version))
        _logger.info('\t trying to load default file from environment [ %s ]', filepath)
        return check_gpsdata_file(filepath, load=True)
    except FileNotExistsError:
        _logger.debug('\t\t default environment file not found', filepath)
        raise CouldNotLoadGpsDataFile('GPS data file could not be loaded')


def check_gpsdata_file(filepath, **kwargs):
    """
    Checks that supplied filepath contains a gps data file, and that is valid.
    :param filepath: Gps data file location
    :param kwargs: Extra arguments
             load: If correct, teturn loadad content instead of file
    :return: The gpsdata file
    """
    filepath = check_file(filepath, extensions=['json'])

    try:
        with open(filepath, 'r') as _fpath:
            content = json.loads(_fpath.read())
        for _key in INVENTORY_REQUIRED_KEYS:
            if _key not in content.keys():
                raise

        # all required keys must be in host key
        if set(content['hosts'][0].keys()).difference([*GPSDATA_INVENTORY_FIELDS, *GPSDATA_FIELDS]):
            raise WrongFileTypeException('Wrong gps data format', filepath=filepath,
                                         main_keys=INVENTORY_REQUIRED_KEYS,
                                         host_keys=[*GPSDATA_INVENTORY_FIELDS, *GPSDATA_FIELDS])

        if kwargs.get('load', False):
            return content
        else:
            return filepath
    except (JSONDecodeError, KeyError, IndexError) as err:
        raise WrongFileTypeException('A gps data file was expected', filepath=filepath,
                                     main_keys=INVENTORY_REQUIRED_KEYS,
                                     host_keys=[*GPSDATA_INVENTORY_FIELDS, *GPSDATA_FIELDS])  from err


def check_version(*args, **kwargs):
    """
    Method that checks that version exists in kwargs, and format is correct
    :param kwargs: Dictionary with argument version to check
    """
    if args:
        _version = args[0]
    else:
        _version = kwargs.get('version')
    if not _version:
        raise MissingArgumentException('Version is required for any inventory operation', version='None')
    elif not CDN_VERSION_PATTERN.match(_version):
        raise MissingArgumentException('Version format is wrong. Expected: '
                                       '"a.b.c" where a,b and c are integers',
                                       version=_version)
    return _version


def check_csvfilter(csvfilter, **kwargs):
    """
    Checks if supplied filter has correct key names for inventory
    :param csvfilter: A csv formatted string, a list or dictionary
    :param kwargs: Extra arguments
        :html: If given, keys will be checked against html key names. Else, keys will be matched against yaml keynames
    :return: The csvfilter as a list or dictionary
    """
    # check if filter is list or dict, and if not, build it
    csvfilter = build_csv_filter(csvfilter)

    if not csvfilter:
        return ''

    # if it's a list
    if isinstance(csvfilter, list):
        for item in csvfilter:
            if kwargs.get('html'):
                csvfilter[csvfilter.index(item)] = is_html_column_valid(item)
            csvfilter[csvfilter.index(item)] = is_yaml_key_valid(item)
        return csvfilter

    # then, it has to be a dict
    _csvfilter = {}
    for _key, _value in csvfilter.items():
        if kwargs.get('html'):
            _csvfilter[is_html_column_valid(_key)] = _value
        _csvfilter[is_yaml_key_valid(_key)] = _value
    return _csvfilter


def is_yaml_key_valid(keyname):
    """
    Checks that supplied yaml key exits in cdn yaml inventory.
    :param keyname: Name of the yaml key to check
    :return: True if valid. A CouldNotFindYamlKeyException is thrown otherwise
    """
    try:
        # helper for simple ipaddress expressions:
        if keyname.lower() in ['management', 'service', 'service_iptv']:
            keyname = f'ipaddress_{keyname.lower()}'

        if keyname in _CDN_YAML_KEY_NAMES.values():
            return keyname
        return _CDN_YAML_KEY_NAMES[keyname.upper()]
    except KeyError:
        raise CouldNotFindHtmlColumnException('supplied yaml keyname is not valid', keyname=keyname,
                                              valid_keys=str(_CDN_YAML_KEY_NAMES.keys()),
                                              valid_values=str(_CDN_YAML_KEY_NAMES.values()))


# deprecated
def is_html_column_valid(column_name):
    """
    Checks that supplied column exits in cdn inventory.
    :param column_name: Name of the column to check in inventory
    :return: True if valid. A CouldNotFindColumnException is thrown otherwise
    """
    try:
        if column_name in _CDN_HTML_COLUMN_NAMES.values():
            return column_name
        return _CDN_HTML_COLUMN_NAMES[column_name.upper()]
    except KeyError:
        raise CouldNotFindHtmlColumnException('supplied column is not a valid', col_name=column_name,
                                              valid_keys=str(_CDN_HTML_COLUMN_NAMES.keys()),
                                              valid_values=str(_CDN_HTML_COLUMN_NAMES.values()))


def check_environment(env_name):
    """
    Checkes supplied inventory named, and provide the namedtuple value
    """
    assert env_name, cs('Supplied env name is None')

    _logger.debug('checking supplied environment [ %s ]', env_name)
    if isinstance(env_name, dict) and env_name in _CDN_ENV_NAMES.values():
        _logger.debug("\t it's a valid dictionary, returning content")
        return env_name
    elif isinstance(env_name, str):
        env_name = env_name.upper()
        _logger.debug("\t it's a string [ %s ], checking if valid", env_name)
        if env_name in _CDN_ENV_NAMES.keys():
            _logger.debug('\t Yes, returning env values')
            return _CDN_ENV_NAMES[env_name]
    raise WrongEnvironmentException(env_name)


# deprecated
def find_html_table(html_content, **kwargs):
    # extra attributes
    attrs = kwargs.get('attrs', {})

    assert isinstance(attrs, dict), 'attrs must be a dictionary'

    _logger.debug('Searching for table with attrs: [%s]\n\t into html:\n\t [%s]', str(kwargs), html_content)
    try:
        if os.path.isfile(html_content):
            _logger.debug('supplied content is a file, loading...')
            with open(html_content) as _file:
                html_content = _file.read()

        soup = BeautifulSoup(html_content, features='html.parser')
        table = soup.find('table', attrs=attrs)
        if not table:
            raise CouldNotFindHtmlTableException(f'table not found', table_attrs=attrs)
        _logger.debug('\t table found\n\t %s', repr(table))
        return table
    except Exception as ex:
        raise CouldNotFindHtmlTableException('Error parsing html content') from ex


# deprecated
def _htmltable2inventory(htmltable, **kwargs):
    """
    Builds inventory from supplied html content
    :param kwargs:
            columns: List of column names to retrieve from inventory, skipping the rest of them
            cfilter: A dictionary with column name values to filter. Column must be either one of supplied columns in
                 former argument, or any column in inventory in no columns arguments must supplied. Natural search
                 is done, matching text in clumn value. i.e '{"Role": "endpoint", "Name": "madpe"}.
                 Multiple values can be provided for filtering, ie: '{"Role": ["endpoint", "ldap"],...}'
    """
    columns = kwargs.get('columns', [])
    _cfilter = kwargs.get('cfilter', '{}')

    # parse table body
    _inventory = {'nodes': []}
    for _row in htmltable.find('tbody').find_all('tr'):
        _columns = [ele.text.strip() for ele in _row.find_all('td')]
        _row_dict = {}

        try:
            for i in range(0, len(_columns)):
                try:
                    _name = _CDN_INVENTORY_HTML_COLUMNS[i]
                    if _name == CDN_HTML_COLUMN.IPV4 or _name == CDN_HTML_COLUMN.IPV6:  # skip ips, they're added to interfaces
                        continue
                    elif columns and _name not in columns:  # if columns supplied, get only those columns
                        _logger.debug('\t column filtering enabled -> skipping column [%s]', _name)
                        continue

                    # check if column has an ipv4 interface
                    if i in _CDN_INVENTORY_HTML_COLUMNS_INTERFACES:
                        _value = {_CDN_INVENTORY_HTML_COLUMNS[i + 1]: _columns[i + 1]}
                    else:
                        _value = _columns[i]

                    # check if filter applies (if no filter exits, a keyError will be raised)
                    try:
                        # create values list, either with single value or all given
                        _fvalues = [i for i in _cfilter[_name] if isinstance(_cfilter[_name], list)] \
                                   or [_cfilter[_name]]

                        skipRow = True
                        for _fval in _fvalues:
                            # if no filter value is in current column value, skip it
                            if _fval in _value:
                                skipRow = False
                                break

                        if skipRow:
                            _logger.debug('\t skipping node, [ %s ] does not match filter  %s -> %s ', _value, _name,
                                          _fvalues)
                            raise SkipNodeFilterException()
                    except KeyError:
                        pass

                    # if no filter exists, add row
                    _row_dict[_name] = _value
                except KeyError as err:
                    raise CouldNotParseHtmlTableException('Error parsing row', row=_row) from err
            _logger.debug('\t new column %s', _row_dict)
            _inventory['nodes'].append(_row_dict)
        except SkipNodeFilterException:
            continue
        except Exception as ex:
            raise CouldNotParseHtmlTableException('unknown exception parsing table') from ex
        return _inventory


def _check_inventory(inventory, **kwargs):
    """
    Checks if supplied inventory has correct format
    :param content: Inventory as a dictionary
    :param kwargs: Extra arguments
    """
    assert isinstance(inventory, dict), cs('Inventory must be a dictionary', COLOR_RED)

    _inv_keys = inventory.keys()
    _logger.debug('checking inventory keys %s ...', _inv_keys)

    for _key in INVENTORY_REQUIRED_KEYS:
        if _key not in _inv_keys:
            raise WrongInventoryException(_inv_keys)
    return inventory


def _build_inventory(content, **kwargs):
    """
    Build dictionary inventory from supplied content.
    :param content: Content as a string
    :param kwargs: Extra arguments
        html: build html content. If not supplied, yaml content will be built
    :return: The inventory as a dictionary
    """
    html = kwargs.get('html', False)

    _logger.debug('\t building inventory...')

    try:
        # if content is html
        if html:
            _logger.debug('\t\t building html inventory...')
            return _htmltable2inventory(find_html_table(content, **kwargs), **kwargs)

        # if content is yaml, then load it and create our inventory
        _logger.debug('\t\t  building yaml inventory...')
        content = yaml.load(content, Loader=yaml.CLoader)
        inventory = {'date': DateTimeHelper.short_date()}
        inventory['hosts'] = [{CDN_YAML_KEY.FQDN: nd['facts'][CDN_YAML_KEY.FQDN],
                               CDN_YAML_KEY.HOSTNAME: nd['facts'][CDN_YAML_KEY.HOSTNAME],
                               CDN_YAML_KEY.SITE_ID: nd['facts'][CDN_YAML_KEY.SITE_ID],
                               CDN_YAML_KEY.REGION_NAME: nd['facts'][CDN_YAML_KEY.REGION_NAME],
                               CDN_YAML_KEY.OB: nd['facts'][CDN_YAML_KEY.OB],
                               CDN_YAML_KEY.COUNTRY: nd['facts'][CDN_YAML_KEY.COUNTRY],
                               CDN_YAML_KEY.CITY: nd['facts'][CDN_YAML_KEY.CITY],
                               CDN_YAML_KEY.ROLE: nd['facts'][CDN_YAML_KEY.ROLE],
                               CDN_YAML_KEY.IPADDRESS_MANAGEMENT: nd['facts'][CDN_YAML_KEY.IPADDRESS_MANAGEMENT],
                               CDN_YAML_KEY.IPADDRESS_SERVICE: nd['facts'][CDN_YAML_KEY.IPADDRESS_SERVICE],
                               CDN_YAML_KEY.IPADDRESS_SERVICE_IPTV: nd['facts'].get(CDN_YAML_KEY.IPADDRESS_SERVICE_IPTV,
                                                                                    "")}
                              for nd in content['hosts']]

        # fix region_name based on service_iptv
        for _hst in inventory['hosts']:
            ob = _hst[CDN_YAML_KEY.OB].split('_IPTV')
            _hst[CDN_YAML_KEY.REGION_NAME] = ob[0]
            if _hst.get(CDN_YAML_KEY.IPADDRESS_SERVICE_IPTV):
                _hst[CDN_YAML_KEY.REGION_NAME] += f'_IPTV'

        return inventory
    except (TypeError, CouldNotFindHtmlTableException, CouldNotParseHtmlTableException) as ex:
        raise CouldNotBuildInventoryException('could not build inventory') from ex


def _load_content_from_cdn_environment(env, **kwargs):
    """
    Loads inventory content from url associated to supplied cdn environment
    :param env: Cdn environment. One from namedtuple CDN_ENVIRONMENT
    :param kwargs: Extra arguments
        html: load html content. If not supplied, yaml content will be loaded
     version: Cdn version to use
    :return: Content of supplied env, either as a string (from html) or a dictionary (from yaml)
    """
    html = kwargs.get('html', False)
    version = kwargs.get('version')

    # it was checked in main method, it must exists
    assert version, cs('Review method invocation, version should be checked previously')

    # supplied inventory must be a valid value from namedtuple
    env = check_environment(env)

    if html:
        _url = env['html'].replace('VERSION', version)
        _logger.info('\t loading content from [ %s ]', _url)
        try:
            return get_httpfile_content(_url)
        except CouldNotLoadFileFromUrl as err:
            raise CouldNotGetHttpInventoryException('could not load inventory') from err

    # --yaml: check if local file exists, and if not, download content from web, build inventory and save it
    _filepath = os.path.join(APP_CDN_DIR, env['local'].replace('VERSION', version))

    try:
        _file = check_file(_filepath)
        _content = yaml.load(open(_file), Loader=yaml.CLoader)

        _check_inventory(_content)

        # update file if older than 24h
        if DateTimeHelper.days_between(_content['date'], DateTimeHelper.short_date()) < 1:
            return _content
        _logger.debug('\t expired inventory building new one...')
        raise
    except FileNotExistsError:
        # 1. download new content
        _logger.info('\t local file does not exists [ %s ] or has expired\n\t loading content from [ %s ]...',
                     _filepath, env['yaml'])
        _content = get_httpfile_content(env['yaml'].replace('VERSION', version))

        # 2. build inventory
        _inventory = _build_inventory(_content, **kwargs)

        # 3. persist it
        with open(_filepath, 'w') as _f:
            _f.write(json.dumps(_inventory, indent=4))
            _f.flush()

        _logger.info('\t new inventory saved to [ %s ]', _filepath)
        return _inventory


def load_inventory(env, **kwargs):
    """
    Loads supplied inventory environment. If not found, a new one is generated from yaml (default). However
    a yaml file (or html) file can be provided if necessary.
    :param env: One of the possible values of CDN_ENV_INVENTORY namedtuple (PRO, PRE,...) or a file
    :param kwargs: Any extra arguments
                version: Cdn version to use
                   html: load html content
    :return: Inventory as a dictionary
    """
    # supplied inventory must be a valid value from namedtuple or a file, else an Exception is thrown

    _version = check_version(**kwargs)
    html = kwargs.get('html', False)

    # If a file was supplied, check it and use it
    try:
        if not isinstance(env, str):
            raise FileNotExistsError('')
        _file = check_file(env.replace('VERSION', _version), extensions=['html', 'yaml'])
        _logger.debug('loading content from [ %s ]', _file)
        with open(env, 'r') as _f:
            _content = _f.read()

        if _file.endswith('html'):
            _logger.debug('\t building html inventory ...')
            return _build_inventory(_content, **kwargs)

        _logger.debug('\t loading yaml...')
        inventory = yaml.load(open(_file), Loader=yaml.CLoader)
        return _check_inventory(inventory)
    except FileNotExistsError:
        _content = _load_content_from_cdn_environment(env, **kwargs)
        if html:
            # if html, inventory must be built
            return _build_inventory(_content, **kwargs)
        else:
            # if yaml, inventory is already built
            return _content


def filter_inventory(inventory, **kwargs):
    """
    :param inventory: Inventory to be filtered as a dict
    :param kwargs: Extra arguments
            html: Supplied inventory is from html
       csvfilter: A CSV formatted line with key:value pairs to match in inventory. If key:value pairs
                  are found, a dictionary is returned. If only key values are provided (separated by
                  semicolon too), an array is returned, for example:  role:endpoint;site_id:Madrid...
                  or ROLE;CITY;HOSTNAME ... Multiple values can be provided for filtering as
                     key1:value1,value2;key2:value1;key3:value1 ...
                  If a dict or list is provided,  it'll be used, else, a filtering dict will be built
        columns:  If given, inventory will be filtered again to removed all columns not given in this list.
                  Powerful when combined with csvfilter. It can be used alone too
           case:  If given, inventory will be filtered using case sensitive matching
    :return: The filtered dict if a filter is given
    """
    csvfilter = kwargs.get('csvfilter', '')
    columns = kwargs.get('columns', None)

    # make sure that service and management fields are added
    if columns and not kwargs.get('html'):
        for _key in (CDN_YAML_KEY.HOSTNAME, CDN_YAML_KEY.IPADDRESS_MANAGEMENT, CDN_YAML_KEY.IPADDRESS_SERVICE,
                     CDN_YAML_KEY.IPADDRESS_SERVICE_IPTV):
            if _key not in [_col.lower() for _col in columns]:
                columns.append(_key)
        columns = check_csvfilter(columns)

    if not csvfilter and not columns:
        _logger.debug('\t No filter supplied, exit filtering')
        return inventory
    elif columns:
        _logger.debug('\t only filtering columns')
        csvfilter = columns.copy()
        columns = None

    try:
        # check supplied csvfilter
        csvfilter = check_csvfilter(csvfilter)

        # check inventory
        inventory = _check_inventory(inventory, **kwargs)

        _logger.debug('\t filtering with supplied filter %s', str(csvfilter))
        _hosts = inventory['hosts']

        _finventory = {'date': inventory['date']}
        _finventory['hosts'] = []
        for _hst in _hosts:
            _hst = filter_dict(_hst, csvfilter, **kwargs)
            if not _hst:
                continue
            elif columns:
                _hst = filter_dict(_hst, columns, **kwargs)
            _finventory['hosts'].append(_hst)
        return _finventory
    except WrongInventoryException as ex:
        raise CouldNotFilterInventoryException('wrong inventory format', csvfilter=str(csvfilter)) from ex
    except WrongCsvFormatException as ex:
        raise CouldNotFilterInventoryException('wrong filter format', csvfilter=str(csvfilter)) from ex


# TODO: reformat html output
def print_inventory(inventory, **kwargs):
    """
    Outputs inventory to console as formatted text
    :param inventory: Inventory to output
    :param kwargs:
            html: Supplied inventory is from html
          sort: Name of key to sort the inventory, default hostname (Always ascending). If key does not exists
          in inventory, a warning is printed and any kind of sorting is done
    """

    _html = kwargs.get('html', False)
    _sort = is_yaml_key_valid(kwargs.get('sort', 'hostname'))

    _logger.debug('building table with inventory results...')
    if isinstance(inventory, str):
        try:
            inventory = json.loads(inventory)
        except TypeError:
            _logger.error('supplied inventory is a string, but not in json format')

    # get nodes
    date = inventory['date']
    hosts = inventory['hosts']
    # sort it
    hosts = sorted(hosts, key=lambda h: h[_sort])

    if len(hosts) == 0:
        print(cs('No results found', COLOR_YELLOW))
        return

    # get column names from first element
    headers = hosts[0].keys()

    total_length = 0
    for _h in headers:
        total_length += _CDN_YAML_HEADER_SIZE[_h]

    # print headers
    print('-' * total_length)
    print(cs(f'\t Inventory  ', COLOR_BLUE) + cs(f'{kwargs["version"]}', COLOR_YELLOW) + cs('  from:   ', COLOR_BLUE)
          + cs(f'{date}', COLOR_YELLOW))
    print('-' * total_length)
    _headers = ''
    for _hdr in headers:
        _txt = _hdr
        if _hdr.startswith('ipaddress_'):
            _txt = _hdr.split('ipaddress_')[1]
        _headers += '{:^{width}}'.format(_txt, width=_CDN_YAML_HEADER_SIZE[_hdr])
    print(_headers)
    print('-' * total_length)

    for _hst in hosts:
        _logger.debug('\t processing host [ %s ]', _hst)
        _line = ''
        for _hdr in headers:
            _line += '{:^{width}}'.format(_hst[_hdr], width=_CDN_YAML_HEADER_SIZE[_hdr])
        print(_line)
    print('-' * total_length)


def gen_gpsdata(inventory, **kwargs):
    """
    Generates a new file with gps data from supplied inventory, as a dict. Gps data file will have fields:'
        name, latitude, longitude, country, city
    :param inventory: Inventory as a dictionary
    :param kwargs: Any extra arguments
         filepath: If given, content will be saved in supplied filepath
    :return: a new file with gps data is generated with inventory fields:
             hostname, latitude, longitude, country, city from supplied environment or inventory file
    """

    _date = DateTimeHelper.short_date()
    _filename = kwargs.get('filepath', f'gpsdata_{_date}.json')

    _logger.info('\t generating gpsdata file...')

    # create new gps_data file
    _gpsinv = {'date': _date}
    _gpsinv['hosts'] = []

    progress = tqdm(total=len(inventory['hosts']), desc='Nodes', position=0, colour='blue')
    for _hst in inventory['hosts']:
        _logger.debug('\t processing host [ %s ]', _hst[CDN_YAML_KEY.HOSTNAME])
        _ipservice = _hst[CDN_YAML_KEY.IPADDRESS_SERVICE]
        try:
            location = get_ip_location(_ipservice)
        except CouldNotGetIpInfoException:
            _logger.info('\t\t could not get ip information for [ %s ][ %s ]',
                         _hst[CDN_YAML_KEY.HOSTNAME], _ipservice)
            location = '0,0'

        # add new entry
        _ghst = {key: _hst[key] for key in GPSDATA_INVENTORY_FIELDS}

        _logger.debug('\t adding location info [ %s ]', location)
        location = location.split(',')
        _ghst[GPSDATA_NAME.LATITUDE] = location[0]
        _ghst[GPSDATA_NAME.LONGITUDE] = location[1]

        _logger.debug('\t\t %s added ', _hst[CDN_YAML_KEY.HOSTNAME])
        _gpsinv['hosts'].append(_ghst)
        progress.update(1)

    progress.close()

    # persist file
    _logger.info('\t saving file %s', _filename)
    with open(_filename, 'w') as _f:
        _f.write(json.dumps(_gpsinv, indent=4))
        _f.flush()
    _logger.info('\t done')

    return _gpsinv


def gen_udnodes(inventory, **kwargs):
    """
    Generates a new file from supplied inventory dictionary, with format:
        Service IP|HOSTNAME|ROLE|deliveryRegion|Country|latitude|longitud
    :param inventory:  Inventory as a dictionary
    :param kwargs: Any extra arguments
            version: CDN inventory version
                env: CDN environment. A valid value from namedtuple
           filepath: If given, file is written to given path
    :return: a new file with ud_nodes format from supplied environment or inventory file
    """
    gpsdata = kwargs.get('gpsdata')
    version = kwargs['version']
    env = kwargs['env']
    filepath = kwargs.get('filepath', f'cdn_udnodes_{DateTimeHelper.short_date()}.csv')

    _logger.info('generating udnodes file...')

    # check inventory data
    inventory = _check_inventory(inventory)

    if not gpsdata:
        # If no gpsdata was supplied, then we need to load it from default environment file
        try:
            gpsdata = load_gpsdata_file(None, **kwargs)
        except CouldNotLoadGpsDataFile:
            # environment file not found. Ask if a new one should be created, else, load gpsdata fails
            create = ''
            while not create.upper() in ['Y', 'N']:
                create = input(cs('Environment GPS data file not found. Create on takes about 2-3min. Y/N?',
                                  COLOR_YELLOW))
            if create.upper() == 'N':
                _logger.info('\t rejecting gps file creation. Can not proceed with udnodes creation. Exit')
                return
            # proceed with gpsdata creation
            _filepath = os.path.join(APP_CDN_DIR, env['gps'].replace('VERSION', version))
            gpsdata = gen_gpsdata(inventory, filepath=_filepath, **kwargs)

    _logger.info('\t writing udnodes file... ')
    progress = tqdm(total=len(inventory['hosts']), desc='Nodes', position=0, colour='green')
    with open(filepath, 'w') as _f:
        for _hst in inventory['hosts']:
            _service_ipv = _hst.get(CDN_YAML_KEY.IPADDRESS_SERVICE_IPTV)

            # get host from gps data with same hostname
            gpshost = next(filter(lambda node: node['hostname'] == _hst['hostname'], gpsdata['hosts']))

            # fields from main inventory for service interface
            line = '|'.join([_hst[_key] for _key in UD_NODE_INVENTORY_FIELDS_SERVICE])
            line += f'|{"|".join([gpshost[_key] for _key in UD_NODE_GPS_FIELDS])}'
            _f.write(f'{line}\n')

            # add a second line if service iptv exists in host
            if _service_ipv:
                line = '|'.join([_hst[_key] for _key in UD_NODE_INVENTORY_FIELDS_SERVICE_IPTV])
                line += f'|{"|".join([gpshost[_key] for _key in UD_NODE_GPS_FIELDS])}'
                _f.write(f'{line}\n')
            _f.flush()
            progress.update(1)
    _logger.info(f'\t Udnodes file written to: [ %s ]', filepath)
    progress.close()


def gen_st2ssh(inventory, **kwargs):
    """
    Generates a new file from supplied inventory dictionary, with format:
    hostname;host;port;timeout;username;password/keyfile;description 1#command1;description 2 #command2:...
    :param inventory: Inventory as a dictionary
    :param kwargs: Any extra arguments
        st2ssh: Param that generates a csv formatted file to be used in batch ssh operations as 'ssh csv <filecsvlines>'
    :return: A new file with ssh2 batch execution format
    """

    st2ssh = kwargs.get('st2ssh', '')

    if not st2ssh:
        _logger.info('No common csv line supplied. Exiting...')

    # format --> 'description 1#command1;description 2 #command2:...'
    st2ssh = st2ssh.split(';')

    _logger.info('generating csv file for ssh batch operations...')

    # check inventory data
    inventory = _check_inventory(inventory)

    _filename = f'cdn_st2ssh_{DateTimeHelper.short_date()}.csv'
    with open(_filename, 'w') as _f:
        for _hst in inventory['hosts']:
            _logger.debug('\t building st2ssh for [ %s ]', _hst[CDN_YAML_KEY.HOSTNAME])
            # user default port and timeout
            _line = f'{_hst[CDN_YAML_KEY.HOSTNAME]}'
            _line += f';{_hst[CDN_YAML_KEY.IPADDRESS_MANAGEMENT]}'
            _line += f';;;{ST2SVC_PROD_USER};{ST2SVC_PROD_PEM_FILE}'
            for _cmd in st2ssh:
                _logger.debug('\t\t command: [ %s ]', _cmd)
                _line += f';{_cmd}'
            _logger.debug('\t writing line [ %s ]', _line)
            _f.write(f'{_line}\n')
        _f.flush()

    _logger.info('\t new ssh batch file for st2 operations created as %s', _filename)
