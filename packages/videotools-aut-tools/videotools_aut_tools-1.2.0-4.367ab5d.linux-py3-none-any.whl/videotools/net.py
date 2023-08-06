"""
Module with network utilities
"""

# - csv formatted file columns
import errno
import json
import logging
import os
import socket
from argparse import ArgumentTypeError
from urllib.parse import urlparse

import ipinfo
import paramiko
import requests
from stringcolor import cs
from tqdm import tqdm

from videotools import APP_LOGLEVEL
from videotools.model import COLOR_RED, COLOR_GREEN, ColoredException, MissingTokenException
from videotools.settings import IPINFO_TOKEN
from videotools.utils import check_file, FileNotExistsError, Stats, DateTimeHelper

DEFAULT_TIMEOUT = 10
DEFAULT_SSH_PORT = 22

# -- csv format for ssh batch executions
CSV_COL_HOSTNAME = 0
CSV_COL_HOST = 1
CSV_COL_PORT = 2
CSV_COL_TIMEOUT = 3
CSV_COL_USERNAME = 4
CSV_COL_PASS_OR_KEYFILE = 5

CSV_COLS_DICT = {0: 'hostname', 1: 'host', 2: 'port', 3: 'timeout', 4: 'username', 5: 'password'}

# map for connections
BOOL2STR_DICT = {True: 'OK', False: 'KO'}

# ipinfo details field names
IPINFO_FIELDS = {'IP': 'ip', 'HOSTNAME': 'hostname', 'CITY': 'city', 'REGION': 'region', 'COUNTRY': 'country',
                 'LOC': 'loc', 'ORG': 'org', 'POSTAL': 'postal', 'TIMEZONE': 'timezone', 'COUNTRY_NAME': 'country_name',
                 'LATITUDE': 'latitude', 'LONGITUDE': 'longitude'}

_logger = logging.getLogger('net')

# configure paramiko loglevel.
# handlers config in main appp's json config file
logging.getLogger("paramiko").setLevel(APP_LOGLEVEL)


# ---------------
#    EXCEPTIONS
# ---------------


class ServerNotAvailableException(ColoredException):
    """
    Exception launched when ip/hostname can not be reached
    """


class NoActiveSshConnException(ColoredException):
    """
    Exception launched when ssh connection is missing, or not active
    """

    def __init__(self, msg='ssh connection is not active', **kwargs):
        super().__init__(msg, **kwargs)


class CouldNotGetSshConnException(ColoredException):
    """
    Exception launched when a ssh connection can not be established
    """

    def __init__(self, msg='Could no create a ssh connection', **kwargs):
        super().__init__(msg, **kwargs)


class CouldNotExecuteSshCommandException(ColoredException):
    """
    Exception launched when there is an exception in a ssh command remote invocation
    """


class RemoteCommandExecutionError(ColoredException):
    """
    Exception launched when there is an error in remote host during command execution
    """

    def __init__(self, stderr, **kwargs):
        super().__init__(f'Remote error occurred:\n\n\t {stderr}', **kwargs)
        self.stderr = stderr


class WrongSshCsvLineFormatError(ArgumentTypeError):
    """
    Exception launched when supplied csv line is not correct
    """
    LINE_FORMAT = 'hostname;host;port;timeout;username;password/keyfile;name1#command1;name2#command2...'

    def __init__(self, line):
        msg = cs(f'Wrong format for:\n\n{line}\n', COLOR_RED)
        msg += cs(f'\n\t -> {self.LINE_FORMAT}\n', COLOR_GREEN)
        super().__init__(msg)
        self.line = line


class WrongIpInfoFieldNameException(ColoredException):
    """
    Exception launched when supplied ipinfo field name is not correct
    """

    def __init__(self, fieldname):
        super().__init__("Supplied field name is not valid. Note: it's case unsensitive", fieldname=fieldname,
                         valid_names=str(IPINFO_FIELDS.values()))


class CouldNotGetIpInfoException(ColoredException):
    """
    Exception launched when can not get ip information from supplied ip address
    """

    def __init__(self, ipaddress):
        super().__init__("Could not get ipinfo from adress", ipaddress=ipaddress)


class CouldNotLoadFileFromUrl(ColoredException):
    """
    Exception when file can not be loaded from supplied url
    """


# -----------
#    LOGIC
# -----------

# -- net


def is_available(host, **kwargs):
    """
    Check port access to an ip
    :param host: Ip or fqdn of the node to check
    :param kwargs: optional arguments
            hostname: Name of the host
            port: SSH port number
            timeout: Timeout of the connection
            loginfo: Log result  at info level
          as_string: Instead of True/False, return OK/KO
    :return: A boolean wih the status of the check
    """
    hostname = kwargs.get('hostname', 'N/A')
    port = int(kwargs.get('port', DEFAULT_SSH_PORT))
    timeout = int(kwargs.get('timeout', DEFAULT_TIMEOUT))
    loginfo = kwargs.get('loginfo', True)

    assert host, 'Ip or fqdn is required'

    _logger.debug('checking access to port [%s] on ip [%s]...', port, host)

    try:
        sck = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sck.settimeout(timeout)
        sck.connect((host, port))
        if loginfo:
            _logger.info('checking hostname [%s] with ip [%s] and port [%s] : OK', hostname, host, port)
        return True
    except socket.timeout:
        _logger.debug('\t connection timeout. Port [%s] is CLOSED at [%s]', port, host)
        _logger.error('checking [%s] with ip [%s] and port [%s] : KO', hostname, host, port)
        return False
    except socket.error as e:
        if e.errno == errno.ECONNREFUSED:
            _logger.debug('\t connection refused. Port [%s] is CLOSED at [%s]', port, host)
            _logger.error('checking [%s] with ip [%s] and port [%s] : KO', hostname, host, port)
        return False
    except Exception as e:
        _logger.debug(
            '\t exception opening socket in port [%s] at address [%s]: \n\t\t *** %s ***', port, host, str(e))
        _logger.error('checking [%s] with ip [%s] and port [%s] : KO', hostname, host, port)
        return False
    finally:
        sck.close()


def get_httpfile_content(url):
    """
    Loads a file content from supplied url
    :param url: Url to load file from
    """
    _logger.debug('getting file content from [ %s ]', url)
    try:
        netloc = urlparse(url).netloc
        hostname_port = netloc.split(':')
        if len(hostname_port) > 1:
            host = hostname_port[0]
            port = int(hostname_port[1])
        else:
            host = hostname_port[0]
            port = 80
    except Exception as ex:
        raise CouldNotLoadFileFromUrl('Error parsing url', url=url)

    if not is_available(host, port=port):
        raise CouldNotLoadFileFromUrl('Url is not available', url=url)

    _response = requests.get(url)
    if not _response.ok:
        raise CouldNotLoadFileFromUrl(_response.content, url=url, status_code=_response.status_code)
    return _response.content


def _check_ipinfo_field(fieldname):
    """
    Checks if supplied fieldname is a valid
    """
    _logger.debug('checking ipinfo field [ %s ]', fieldname)
    if not fieldname in IPINFO_FIELDS.values():
        try:
            fieldname = IPINFO_FIELDS[fieldname.upper()]
        except (KeyError, TypeError) as err:
            raise WrongIpInfoFieldNameException(fieldname) from err
    return fieldname


def get_ipinfo(ip_address, **kwargs):
    """
    Gets information from supplied ip. The information can be retrieved as a dict, or as a json formatted string
    :param ip_address: IP to get information about
    :param fields: It's used as a fitler to get only information of supplied field names
    :return: A dictionary with full ip information,or only the information of supplied field names.
    """
    if not IPINFO_TOKEN:
        raise MissingTokenException('Missing token for ipinfo. Check with tools admin')

    # check fields and build correct list
    fields = list(map(_check_ipinfo_field, kwargs.get('fields', [])))

    try:
        handler = ipinfo.getHandler(IPINFO_TOKEN)
        details = handler.getDetails(ip_address).details

        # filter details if needed
        if fields:
            details = {key: value for key, value in details.items() if key in fields}
        return details
    except Exception as ex:
        raise CouldNotGetIpInfoException(ip_address) from ex


def get_ip_location(ip_adress):
    """
    Provides location of given ipaddress as latitude, longitude
    :param ip_address: IP to get information about
    :return: Return location as (latitude, longitude)
    """
    details = get_ipinfo(ip_adress, fields=['loc'])
    try:
        location = details['loc']
    except KeyError:
        location = '0,0'
    return location


def get_ip_countryname(ip_adress):
    """
    Provides country name of given ipaddress
    :param ip_address: IP to get information about
    """
    details = get_ipinfo(ip_adress, fields=['country_name'])
    return details['country_name']


# -- ssh

def new_ssh_connection(host, username, **kwargs):
    """
    Connects via SSH to the host using username/password or ssh key
    :param host: Ip or fqdn of the node to connect to
    :param username: Remote host username to login with
    :param kwargs: optional arguments
          password: User's password
           keyfile: File location that contains the ssh key
              port: ssh port
           timeout: Timeout of the connection
    """
    password = kwargs.get('password')
    keyfile = kwargs.get('keyfile')
    port = int(kwargs.get('port', DEFAULT_SSH_PORT))
    timeout = int(kwargs.get('timeout', DEFAULT_TIMEOUT))

    assert host and username and (password or keyfile), 'A host, username and password (or keyfile) is required'

    try:
        if not is_available(host, loginfo=False, **kwargs):
            raise ServerNotAvailableException(f'{host}:{port} can not be reached')

        # New ssh conn
        _logger.debug('\t creating new ssh connection:\n\t host: %s\n\t user: %s\n\t opts: %s', host, username,
                      str(kwargs))
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        if password:
            _logger.debug('\t using password...')
            ssh_client.connect(host, username=username, password=password, timeout=timeout, port=port)
        else:
            _logger.debug('\t using pem key...')
            ssh_client.connect(host, username=username, key_filename=keyfile, timeout=timeout, port=port)
        return ssh_client
    except Exception as ex:
        raise CouldNotGetSshConnException() from ex


def is_ssh_conn_active(ssh_conn):
    if not ssh_conn or ssh_conn.get_transport() is None or not ssh_conn.get_transport().is_active():
        raise NoActiveSshConnException()
    return True


# todo: add --dry-run logger output (option exists in main parent parser)
def ssh_exec(expression, **kwargs):
    """
    Runs an expression in a remote host using a SSH connection
    :param expression: Command/s to be executed in remote host
    :param kwargs: Optional arguments
        ssh_conn: Active ssh connection to use to perform remote expression execution
            host: IP to connect
        username: User's name
        password: User's password
         keyfile: File location that contains the ssh key
            port: ssh port
         timeout: Timeout of the connection
           close: If True, the connection is closed after execution (default). It's left opened otherwise
        no_output: The return will be OK or KO. Data will be logged but return will be simple, as OK, KO
    :return: The stdout of the remote expression if no err occurs, otherwise, a CouldNotExecuteSshCommandException is
             raised
    """
    debug_args = {'cmd': expression}
    debug_args.update(kwargs)

    _logger.debug('executing ssh_exec:\n\t %s', debug_args)

    try:
        no_output = kwargs.get('no_output', False)

        # get an active ssh connection or create a new one
        ssh_conn = kwargs.get('ssh_conn')
        if not ssh_conn:
            kargs = kwargs.copy()
            ssh_conn = new_ssh_connection(kargs.pop('host'), kargs.pop('username'), **kargs)

        # check ssh connection is active (in case the connection was supplied as an optional arg)
        is_ssh_conn_active(ssh_conn)

        _logger.debug('\t executing command and waiting for end signal...')
        _, stdout, stderr = ssh_conn.exec_command(expression)

        # Wait until the command has finished. It'll return exec code result as an integer
        exec_status = stdout.channel.recv_exit_status()
        stdout = stdout.read().strip().decode("utf-8")
        stderr = stderr.read().strip().decode("utf-8")

        # any int value that is not 0 indicates an err in command execution
        if exec_status:
            if no_output:
                stderr = '**'
            raise RemoteCommandExecutionError(stderr)

        if kwargs.get('close', True):
            _logger.debug('closing ssh connection...')
            ssh_conn.close()
            _logger.debug('\t Sucess')

        _logger.debug(f'\t stdout: {stdout}')
        if no_output:
            stdout = 'OK'
        return stdout

    except NoActiveSshConnException as ex:
        raise CouldNotExecuteSshCommandException('ssh conn is not active or is null', debug_args=debug_args) from ex
    except CouldNotGetSshConnException as ex:
        raise CouldNotExecuteSshCommandException('could not create ssh connection', debug_args=debug_args) from ex
    except paramiko.BadHostKeyException as ex:
        raise CouldNotExecuteSshCommandException("SSH server's key did not match what we were expecting",
                                                 debug_args=debug_args) from ex
    except paramiko.AuthenticationException as ex:
        raise CouldNotExecuteSshCommandException('authentication failed', debug_args=debug_args) from ex
    except paramiko.SSHException as ex:
        raise CouldNotExecuteSshCommandException('failures in SSH2 protocol negotiation', debug_args=debug_args) from ex
    except socket.error as err:
        if ssh_conn:
            ssh_conn.close()
        raise CouldNotExecuteSshCommandException('socket IO error', debug_args=debug_args) from err
    except Exception as ex:
        # if an error ocurred during remote invocation, just raise the exceptio and handle it above
        if isinstance(ex, RemoteCommandExecutionError):
            if kwargs.get('close', True):
                _logger.debug('closing ssh connection...')
                ssh_conn.close()
                _logger.debug('\t Success')
            raise ex
        if ssh_conn:
            ssh_conn.close()
        raise CouldNotExecuteSshCommandException('Unchecked exception', **debug_args) from ex


# -- ssh csv batch operations

# todo: extend csv format verification
def check_csvssh_lineformat(csvline, **kwargs):
    """
    Checks that supplied csvline matches expected format for ssh batch execution
    :param csvline: CSV line to check format
    :param kwargs: Extra arguments
        minargs: minimum number of arguments in line
    """
    assert isinstance(csvline, str), cs('Supplied csvline is not a string', COLOR_RED)

    try:
        _minargs = kwargs.get('minargs', 6)
    except TypeError:
        raise ArgumentTypeError('Supplied arg is not an integer', minargs=_minargs)

    _logger.debug('checking csv format of line [ %s ]', csvline)

    if len(csvline.split(';')) < int(_minargs):
        raise WrongSshCsvLineFormatError(csvline)
    return True


def check_csv_fileformat2lines(csvfilepath):
    # checks it's a file first and expand user path if needed
    csvfilepath = check_file(csvfilepath)

    # check for csv format
    errors = ''
    with open(csvfilepath) as _file:
        _logger.debug('checking csv format of file [%s]', csvfilepath)
        lines = [_line.strip('\n') for _line in list(map(lambda x: x.strip('\n') or None, _file.readlines()))
                 if _line and not _line.startswith('#')]
        for _ln in lines:
            try:
                check_csvssh_lineformat(_ln)
            except WrongSshCsvLineFormatError:
                errors += f'\t{_ln}\n'
    if errors:
        raise WrongSshCsvLineFormatError(errors)
    return lines


def _get_kwargs_from_csvline(line, **kwargs):
    """
    Provides kwargs from supplied csv formatted line, and a list of tuples as (cmd_name, cmd_exec) if exists
    """
    _logger.debug('building new ssh connection args from line [ %s ]', line)
    args = list(map(lambda x: x or None, line.split(';')))
    _kwargs = {}
    for _col, _name in CSV_COLS_DICT.items():
        _kwargs[_name] = args[_col]

    # If no username is supplied, use global option
    _logger.debug('\t setting up username...')
    _kwargs['username'] = _kwargs.get('username') or kwargs.get('username')
    assert _kwargs['username'], cs(f'not username in global opt or line:\n\n\t {line}', COLOR_RED)
    _logger.debug('\t\t found [%s]', _kwargs['username'])

    _logger.debug('\t setting up authentication (password or keyfile...')
    # if global password is supplied, use it if none was provided in line
    password = _kwargs.get('password') or kwargs.get('password')
    keyfile = kwargs.get('keyfile')

    # password exists, either in line or global option
    if password:
        _logger.debug('\t\t password found...')

        # check if password is path to keyfile, in case it comes from line in file and not global,
        # in such case, change kwarg value to keyfile
        try:
            _logger.debug('\t\t checking if it is a path to a keyfile')
            _kwargs['keyfile'] = check_file(password)
            # remove password since we'll be using keyfile
            if _kwargs.get('password'):
                _kwargs.pop('password')
        except FileNotExistsError:
            _logger.debg('\t\t supplied password is not a keyfile')
            _kwargs['password'] = password
    elif keyfile:
        _logger.debug('\t\t found keyfile [%s]', keyfile)
        _kwargs['keyfile'] = keyfile
    else:
        raise WrongSshCsvLineFormatError(f'missing password or keyfile in args:\n\t {kwargs} or\n\t {line}')

    # -- port
    _kwargs['port'] = _kwargs.get('port') or DEFAULT_SSH_PORT

    # -- timeout
    _kwargs['timeout'] = _kwargs.get('timeout') or DEFAULT_TIMEOUT

    _logger.debug('csv line args -> %s', str(_kwargs))

    # -- get commands
    _logger.debug('\t looking for commands in line...')
    _cmds = args[(CSV_COL_PASS_OR_KEYFILE + 1):]
    for _cmd in _cmds:
        _cmd_list = _cmd.split('#')
        if len(_cmd_list) > 2:
            raise WrongSshCsvLineFormatError(f'command has more than one # for name [{line}]')
        elif len(_cmd_list) < 2:
            _logger.warning('no name supplied for command [%s]', _cmd)
            _cmds[_cmds.index(_cmd)] = (_cmd, _cmd)
        else:
            _logger.debug('\t\t found name [%s] and command [%s]', _cmd_list[0], _cmd_list[1])
            _cmds[_cmds.index(_cmd)] = (_cmd_list[0], _cmd_list[1])
    return _kwargs, _cmds


def csvfile2command(filewithlines, **kwargs):
    """
    Checks connectivity or run command/s using a csv file format
    :param filewithlines: File location with the csv formatted lines, or a list with csv formmated lines
                     -> hostname;host;port;timeout;username;password/keyfile;command1;command2...
                     where commands can include a short description as: ;any short description#command1;
    :param kwargs: Extra arguments
           json: Persist stats as a json file
    :return: A dictioanry with results and an instance of StatsDict with calculated stats or methods
    """
    try:
        if os.path.isfile(filewithlines):
            _logger.debug('using a file with csv formatted lines')
            filewithlines = check_csv_fileformat2lines(filewithlines)
    except TypeError:
        _logger.debug('using a list of csv formatted lines')

    _logger.debug('\t supplied lines:\n\n%s\n', '\n'.join(filewithlines))

    ssh_conn = None
    results = {}
    error_lines = []
    stats = Stats()

    progress_hosts = tqdm(total=len(filewithlines), desc='Host', position=0, colour='blue')
    # iterate over connections
    for _line in filewithlines:
        try:
            _kwargs, _cmds = _get_kwargs_from_csvline(_line, **kwargs)
        except WrongSshCsvLineFormatError:
            _logger.error('Format error in line: [%s]', _line)
            error_lines.append(_line)
            continue

        _hostname = _kwargs.get('hostname') or _kwargs.get('host')
        _host = _kwargs.pop('host')
        _username = _kwargs.pop('username')

        results[_hostname] = dict()

        # -- connectivity
        _logger.info('checking connectivity to [%s]...', _hostname)
        _rst = is_available(_host, loginfo=True, **_kwargs)

        results[_hostname]['conn'] = BOOL2STR_DICT[_rst]
        if _rst:
            stats.successUp('conn')
        else:
            stats.failureUp('conn')
            stats.failureUp('ssh')
            for _cmd in _cmds:
                _cmd_name = _cmd[0]
                _cmd_exec = _cmd[1]
                results[_hostname][_cmd_name] = 'KO'
                stats.failureUp(_cmd_name)
            continue

        if not _cmds:
            _logger.debug('\t skipping remote execution, not command given')
            continue
        elif len(_cmds) > 1:
            try:
                # create ssh connection to reuse in all commands for same host
                _logger.debug(str(_kwargs))
                ssh_conn = new_ssh_connection(_host, _username, close=False, **_kwargs)
                stats.successUp('ssh')
            except CouldNotGetSshConnException:
                _logger.error('could not get connection with line [ %s ]', _line)
                error_lines.append(_line)
                stats.failureUp('ssh')
                for _cmd in _cmds:
                    _cmd_name = _cmd[0]
                    _cmd_exec = _cmd[1]
                    results[_hostname][_cmd_name] = 'KO'
                    stats.failureUp(_cmd_name)
                if ssh_conn:
                    _logger.debug('closing active conn...')
                    ssh_conn.close()
                progress_hosts.update(1)
                continue

        # -- command execution
        progress_cmds = tqdm(total=len(_cmds), desc='Command', position=0, colour='green')
        for _cmd in _cmds:
            _cmd_name = _cmd[0]
            _cmd_exec = _cmd[1]
            _logger.info('executing __%s__...', _cmd_name)
            try:
                try:
                    is_ssh_conn_active(ssh_conn)
                    _rst = ssh_exec(_cmd_exec, ssh_conn=ssh_conn, no_output=True, **_kwargs)
                except NoActiveSshConnException:
                    _rst = ssh_exec(_cmd_exec, host=_host, username=_username, no_output=True, **_kwargs)

                results[_hostname][_cmd_name] = _rst
                # increase success counter
                stats.successUp(_cmd_name)

            except CouldNotExecuteSshCommandException:
                _logger.error('could not execute [ %s ]\n\t on line [ %s ]', _cmd_name, _line)
                results[_hostname][_cmd_name] = 'KO'
                stats.failureUp(_cmd_name)
            except RemoteCommandExecutionError as err:
                _logger.debug('remote error in command [ %s ]\n\t on line [ %s ]', _cmd_name, _line)
                results[_hostname][_cmd_name] = err.stderr
                stats.failureUp(_cmd_name)
            except Exception as ex:
                _logger.exception('Unchecked exception')
                results[_hostname][_cmd_name] = str(ex)
                stats.failureUp(_cmd_name)
            finally:
                progress_cmds.update(1)
        progress_cmds.close()
        progress_hosts.update(1)
    progress_hosts.close()
    if ssh_conn:
        _logger.debug('closing active conn...')
        ssh_conn.close()

    _logger.debug(str(_rst))

    results['stats'] = stats.as_dict()

    # saving stats
    if kwargs.get('json'):
        _logger.debug('\t saving stats...')
        with open(f'csvfile2command_results_{DateTimeHelper.short_date()}.json', 'w') as _f:
            _f.write(json.dumps(results, indent=4))
            _f.flush()

    return results, stats
