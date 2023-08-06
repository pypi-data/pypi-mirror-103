"""
Module with logic to integrate with SSH's videotoools operations

With this module, we can:

 - check connectivity to a remote host:port
 - execute commands on remote host
 - perform a batch of remote commands given a file with csv format as:

   hostname;host;port;timeout;username;password/keyfile;command1;command2
   where commands can include a short description as:
   ;any short description#command1;another description for other command#command2;...

"""

import getpass
import logging

from stringcolor import cs

from videotools import COMMANDS
from videotools.net import DEFAULT_SSH_PORT, DEFAULT_TIMEOUT, csvfile2command, ssh_exec, is_available, \
    check_csv_fileformat2lines
from videotools.utils import check_file

_logger = logging.getLogger('ssh_cmd')


def init_parser(parent_parser):
    ssh_parser = parent_parser.add_parser(COMMANDS.SSH, help='Actions to manage ssh commands')
    ssh_subparser = ssh_parser.add_subparsers()
    ssh_subparser.required = True

    # --- Check connectivity
    cmd_check = ssh_subparser.add_parser('check', help='Check connectivity with host via port')
    cmd_check.set_defaults(func=is_available)
    cmd_check.add_argument('host', nargs='?', type=str, help='Host to be checked')
    cmd_check.add_argument('port', nargs='?', type=int, help='Port to be checked in host', default=DEFAULT_SSH_PORT)
    cmd_check.add_argument('--timeout', type=int, required=False, default=DEFAULT_TIMEOUT,
                           help='SSH Timeout (Default 10 seg)')

    # --- Run command/s in a specified host
    cmd_run = ssh_subparser.add_parser('run', help='Run a command in a remote host')
    cmd_run.set_defaults(func=ssh_exec)
    cmd_run.add_argument('host', nargs='?', type=str, help='Host ip')
    cmd_run.add_argument('expression', nargs='?', help='Expression to be executed in remote host')

    # # Require either password or keyfile
    auth_group = cmd_run.add_mutually_exclusive_group(required=True)
    auth_group.add_argument('--password', required=False, help='User password')
    auth_group.add_argument('--keyfile', required=False, type=lambda _path: check_file(_path),
                            help='Private key file location')
    #
    cmd_run.add_argument('--username', nargs='?', type=str, help='Username to connect to the host',
                         default=getpass.getuser())
    cmd_run.add_argument('--port', type=int, required=False, default=DEFAULT_SSH_PORT,
                         help='Host ssh port (Default port DEFAULT_SSH_PORT)')
    cmd_run.add_argument('--timeout', type=int, required=False, default=DEFAULT_TIMEOUT, help='SSH Timeout')

    # -- Check connectivity or run command/s using a csv formatted file
    cmd_csv = ssh_subparser.add_parser('csv', help='run remote commands specified in file with format: '
                                                   'hostname;host;port;username;password;command1;command2...')
    cmd_csv.set_defaults(func=csvfile2command)
    cmd_csv.add_argument('filewithlines', nargs='?', type=lambda _path: check_csv_fileformat2lines(_path),
                         help='Csv file location with csv formatted lines.\n'
                              'hostname;host;port;timeout;username;password/keyfile;command1;command2..\n'
                              'The lambda will return a list with file lines')
    cmd_csv.add_argument('--username', required=False, default=getpass.getuser(),
                         help='Common username for all hosts in file')
    auth_group = cmd_csv.add_mutually_exclusive_group(required=False)
    auth_group.add_argument('--password', required=False, help='Common user password for all hosts in file')
    auth_group.add_argument('--keyfile', required=False, type=lambda _path: check_file(_path),
                            help='Common private key file location for all hosts in file')
    cmd_csv.add_argument('--json', required=False, action='store_true',
                         help='If given, save calculated stats as a json file',
                         default=False)
    cmd_csv.add_argument('--short', required=False, action='store_true',
                         help='Only final stats are printed, no further detail information will be presented. It is '
                              'crucial to persist data with --json if data is important and it was a long time '
                              'consuming operation', default=False)

    return ssh_parser


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
    if isinstance(_result, str) or isinstance(_result, int) and not isinstance(_result, bool):
        _logger.info(_result)

    if func.__name__ == 'csvfile2command':
        _rst_info = _result[0]
        _stats = _result[1]

        if not cmd_args.get('short'):
            print('-' * 100)
            print(f'{"HOSTNAME":^25}{"COMMAND":^50}{"RESULT":^30}')
            print('-' * 100)
            for _hostname, _rsts in _rst_info.items():
                if _hostname == 'stats':
                    continue
                print(f'\t{cs(_hostname, "yellow2"):<25}')
                for _name, value in _rsts.items():
                    print(f'{"" * 25:<25}{_name:>50}{value:^30}')
            print('-' * 100)
            print()

        _stats.print()
