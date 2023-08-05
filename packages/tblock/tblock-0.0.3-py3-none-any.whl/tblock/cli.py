# TBlock - An anticapitalist ad-blocker that uses the hosts file
# Copyright (C) 2021 Twann <twann@ctemplar.com>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

########################################################################################################################
# This module contains function needed to run TBlock inside a terminal emulator (CLI).                                 #
########################################################################################################################

# Standard libraries
import os.path
import sys
import sqlite3
import re

# External libraries
from colorama import Fore, Style

# Local libraries
from . import __version__, run_help, run_converter_help
from .rules import add_user_rule, delete_user_rule, list_rules
from .core import Policy, Filter, update_hosts, Rule, restore_hosts
from .utils import check_root
from .converter.detector import detect_syntax
from .converter.output import convert_filter
from .filters import update_all_filters, update_filter, update_remote_repo, subscribe_to_filter, unsubscribe_to_filter,\
    list_filters, show_filter_info, change_filter_permissions
from .config import database, remote_repo_version_db, default_ip, hosts, tmp_dir, remote_repo, \
    remote_repo_mirror, default_hosts


def print_status(db_path: str, default_hosts_file: str, version: str) -> None:
    """Print status of the ad-blocker

    Args:
        db_path (str): The path to the SQLite database
        default_hosts_file (str): The path to the file that indicates if TBlock is active or not
        version (str): The version of the program to show
    """
    db_path = os.path.realpath(db_path)
    if not os.path.isfile(db_path):
        print(f'Error: file not found: "{db_path}"')
        sys.exit(1)
    with open(remote_repo_version_db, 'rt') as fi:
        remote_repo_version = int(fi.read())
    db = sqlite3.connect(db_path)
    stats = Rule.rules_count(db)
    if os.path.isfile(default_hosts_file):
        status = f'{Fore.GREEN}blocking{Style.RESET_ALL}'
    else:
        status = f'{Fore.RED}not blocking{Style.RESET_ALL}'
    print(
        f'TBlock version {version} running on {sys.platform}\n\n'
        f'Status:                    {status}\n\n'
        f'Total rules:               {stats["total"]}\n'
        f'User rules:                {stats["user"]}\n'
        f'Allowing rules:            {stats["allow"]}\n'
        f'Blocking rules:            {stats["block"]}\n'
        f'Redirecting rules:         {stats["redirect"]}\n\n'
        f'Online repository version: {remote_repo_version}\n'
        f'Total active filters:      {len(Filter.get_all_subscribing_filter(db))}'
    )
    db.close()


def run() -> None:
    """Run the CLI ad-blocker
    """
    try:
        if '-f' in sys.argv or '--force' in sys.argv:
            force = True
        else:
            force = False
        if len(sys.argv) <= 1:
            sys.exit(run_help)
        elif '-h' in sys.argv or '--help' in sys.argv or re.findall(r"^-h", sys.argv[1]):
            print(run_help)
        elif '-s' in sys.argv or '--status' in sys.argv or re.findall(r"^-s", sys.argv[1]):
            print_status(database, default_hosts, __version__)
        elif '-v' in sys.argv or '--version' in sys.argv or re.findall(r"^-v", sys.argv[1]):
            print(version_info)
        else:
            count = 0
            if sys.argv[1] == '--allow':
                check_root()
                for arg in sys.argv[1:]:
                    if not re.findall(r"^-[0-9a-zA-Z\-]", arg):
                        add_user_rule(arg, Policy.allow, database, force=force)
                        count += 1
                if count == 0:
                    sys.exit('Error: please specify at least one domain')
                else:
                    with sqlite3.connect(database) as db:
                        update_hosts(hosts, db, default_hosts, default_ip, force=force)
            elif re.match(r"^-a", sys.argv[1]):
                check_root()
                if 'f' in sys.argv[1]:
                    force = True
                for arg in sys.argv[1:]:
                    if not re.findall(r"^-[0-9a-zA-Z\-]", arg):
                        add_user_rule(arg, Policy.allow, database, force=force)
                        count += 1
                if count == 0:
                    sys.exit('Error: please specify at least one domain')
                else:
                    with sqlite3.connect(database) as db:
                        update_hosts(hosts, db, default_hosts, default_ip, force=force)
            elif sys.argv[1] == '--block':
                check_root()
                for arg in sys.argv[1:]:
                    if not re.findall(r"^-[0-9a-zA-Z\-]", arg):
                        add_user_rule(arg, Policy.block, database, force=force)
                        count += 1
                if count == 0:
                    sys.exit('Error: please specify at least one domain')
                else:
                    with sqlite3.connect(database) as db:
                        update_hosts(hosts, db, default_hosts, default_ip, force=force)
            elif re.match(r"^-b", sys.argv[1]):
                check_root()
                if 'f' in sys.argv[1]:
                    force = True
                for arg in sys.argv[1:]:
                    if not re.findall(r"^-[0-9a-zA-Z\-]", arg):
                        add_user_rule(arg, Policy.block, database, force=force)
                        count += 1
                if count == 0:
                    sys.exit('Error: please specify at least one domain')
                else:
                    with sqlite3.connect(database) as db:
                        update_hosts(hosts, db, default_hosts, default_ip, force=force)
            elif sys.argv[1] == '--redirect':
                check_root()
                for arg in sys.argv[1:]:
                    ip = sys.argv[len(sys.argv) - 1]
                    if not re.findall(r"^-[0-9a-zA-Z\-]", arg) and not arg == ip:
                        add_user_rule(arg, Policy.redirect, database, ip, force=force)
                        count += 1
                if count == 0:
                    sys.exit('Error: please specify at least one domain')
                else:
                    with sqlite3.connect(database) as db:
                        update_hosts(hosts, db, default_hosts, default_ip, force=force)
            elif re.match(r"^-r", sys.argv[1]):
                check_root()
                if 'f' in sys.argv[1]:
                    force = True
                for arg in sys.argv[1:]:
                    ip = sys.argv[len(sys.argv) - 1]
                    if not re.findall(r"^-[0-9a-zA-Z\-]", arg) and not arg == ip:
                        add_user_rule(arg, Policy.redirect, database, ip, force=force)
                        count += 1
                if count == 0:
                    sys.exit('Error: please specify at least one domain')
                else:
                    with sqlite3.connect(database) as db:
                        update_hosts(hosts, db, default_hosts, default_ip, force=force)
            elif sys.argv[1] == '--delete-rule':
                check_root()
                for arg in sys.argv[1:]:
                    if not re.findall(r"^-[0-9a-zA-Z\-]", arg):
                        delete_user_rule(arg, database, force=force)
                        count += 1
                if count == 0:
                    sys.exit('Error: please specify at least one domain')
                else:
                    with sqlite3.connect(database) as db:
                        update_hosts(hosts, db, default_hosts, default_ip, force=force)
            elif re.match(r"^-d", sys.argv[1]):
                check_root()
                if 'f' in sys.argv[1]:
                    force = True
                for arg in sys.argv[1:]:
                    if not re.findall(r"^-[0-9a-zA-Z\-]", arg):
                        delete_user_rule(arg, database, force=force)
                        count += 1
                if count == 0:
                    sys.exit('Error: please specify at least one domain')
                else:
                    with sqlite3.connect(database) as db:
                        update_hosts(hosts, db, default_hosts, default_ip, force=force)
            elif sys.argv[1] == '--list-rules':
                if '-s' in sys.argv or '--standard' in sys.argv:
                    standard = True
                else:
                    standard = False
                if '-u' in sys.argv or '--user' in sys.argv:
                    user = True
                else:
                    user = False
                list_rules(database, standard=standard, user=user)
            elif re.match(r"^-l", sys.argv[1]):
                if '-s' in sys.argv or '--standard' in sys.argv or 's' in sys.argv[1]:
                    standard = True
                else:
                    standard = False
                if '-u' in sys.argv or '--user' in sys.argv or 'u' in sys.argv[1]:
                    user = True
                else:
                    user = False
                list_rules(database, standard=standard, user=user)
            elif sys.argv[1] == '--subscribe':
                check_root()
                permissions = 'b'
                source = None
                try:
                    if '-c' in sys.argv:
                        source = sys.argv[sys.argv.index('-c') + 1]
                    elif '--custom' in sys.argv:
                        source = sys.argv[sys.argv.index('--custom') + 1]
                    if '-m' in sys.argv:
                        permissions = sys.argv[sys.argv.index('-m') + 1]
                    elif '--mod' in sys.argv:
                        permissions = sys.argv[sys.argv.index('--mod') + 1]
                except IndexError:
                    sys.exit('Error: please specify at least one filter ID')
                for arg in sys.argv[1:]:
                    if not re.findall(r"^-[0-9a-zA-Z\-]", arg) and not arg == source and not arg == permissions:
                        if count >= 1 and source is not None:
                            sys.exit('Error: cannot add more than one custom filter at the same time')
                        else:
                            subscribe_to_filter(arg, database, tmp_dir, permissions, source, force=force)
                            count += 1
                if count == 0:
                    sys.exit('Error: please specify at least one filter ID')
                else:
                    with sqlite3.connect(database) as db:
                        update_hosts(hosts, db, default_hosts, default_ip, force=force)
                if '-y' in sys.argv or '--sync' in sys.argv:
                    update_remote_repo(remote_repo, remote_repo_mirror, remote_repo_version_db, database,
                                       tmp_dir, force=force)
            elif re.match(r"^-S", sys.argv[1]):
                check_root()
                if 'f' in sys.argv[1]:
                    force = True
                permissions = 'b'
                source = None
                try:
                    if '-c' in sys.argv:
                        source = sys.argv[sys.argv.index('-c') + 1]
                    elif '--custom' in sys.argv:
                        source = sys.argv[sys.argv.index('--custom') + 1]
                    if '-m' in sys.argv:
                        permissions = sys.argv[sys.argv.index('-m') + 1]
                    elif '--mod' in sys.argv:
                        permissions = sys.argv[sys.argv.index('--mod') + 1]
                    if 'c' in sys.argv[1] and 'm' in sys.argv[1]:
                        sys.exit(f'Error: argument required after: "{sys.argv[1][0:3]}"')
                    elif 'c' in sys.argv[1]:
                        source = sys.argv[2]
                    elif 'm' in sys.argv[1]:
                        permissions = sys.argv[2]
                except IndexError:
                    sys.exit('Error: please specify at least one filter ID')
                for arg in sys.argv[1:]:
                    if not re.findall(r"^-[0-9a-zA-Z\-]", arg) and not arg == source and not arg == permissions:
                        if count >= 1 and source is not None:
                            sys.exit('Error: cannot add more than one custom filter at the same time')
                        else:
                            subscribe_to_filter(arg, database, tmp_dir, permissions, source, force=force)
                            count += 1
                if count == 0:
                    sys.exit('Error: please specify at least one filter ID')
                else:
                    with sqlite3.connect(database) as db:
                        update_hosts(hosts, db, default_hosts, default_ip, force=force)
                if '-y' in sys.argv or '--sync' in sys.argv or 'y' in sys.argv[1]:
                    update_remote_repo(remote_repo, remote_repo_mirror, remote_repo_version_db, database,
                                       tmp_dir, force=force)
            elif sys.argv[1] == '--remove':
                check_root()
                for arg in sys.argv[1:]:
                    if not re.findall(r"^-[0-9a-zA-Z\-]", arg):
                        unsubscribe_to_filter(arg, database, force=force)
                        count += 1
                if count == 0:
                    sys.exit('Error: please specify at least one filter ID')
                else:
                    with sqlite3.connect(database) as db:
                        update_hosts(hosts, db, default_hosts, default_ip, force=force)
                if '-y' in sys.argv or '--sync' in sys.argv:
                    update_remote_repo(remote_repo, remote_repo_mirror, remote_repo_version_db, database,
                                       tmp_dir, force=force)
            elif re.match(r"^-R", sys.argv[1]):
                check_root()
                if 'f' in sys.argv[1]:
                    force = True
                for arg in sys.argv[1:]:
                    if not re.findall(r"^-[0-9a-zA-Z\-]", arg):
                        unsubscribe_to_filter(arg, database, force=force)
                        count += 1
                if count == 0:
                    sys.exit('Error: please specify at least one filter ID')
                else:
                    with sqlite3.connect(database) as db:
                        update_hosts(hosts, db, default_hosts, default_ip, force=force)
                if '-y' in sys.argv or '--sync' in sys.argv or 'y' in sys.argv[1]:
                    update_remote_repo(remote_repo, remote_repo_mirror, remote_repo_version_db, database,
                                       tmp_dir, force=force)
            elif sys.argv[1] == '--update':
                check_root()
                for arg in sys.argv[1:]:
                    if not re.findall(r"^-[0-9a-zA-Z\-]", arg):
                        update_filter(arg, database, tmp_dir, force=force)
                        count += 1
                if count == 0:
                    update_all_filters(database, tmp_dir, force=force)
                with sqlite3.connect(database) as db:
                    update_hosts(hosts, db, default_hosts, default_ip, force=force)
                if '-y' in sys.argv or '--sync' in sys.argv:
                    update_remote_repo(remote_repo, remote_repo_mirror, remote_repo_version_db, database,
                                       tmp_dir, force=force)
            elif re.match(r"^-U", sys.argv[1]):
                check_root()
                if 'f' in sys.argv[1]:
                    force = True
                for arg in sys.argv[1:]:
                    if not re.findall(r"^-[0-9a-zA-Z\-]", arg):
                        update_filter(arg, database, tmp_dir, force=force)
                        count += 1
                if count == 0:
                    update_all_filters(database, tmp_dir, force=force)
                with sqlite3.connect(database) as db:
                    update_hosts(hosts, db, default_hosts, default_ip, force=force)
                if '-y' in sys.argv or '--sync' in sys.argv or 'y' in sys.argv[1]:
                    update_remote_repo(remote_repo, remote_repo_mirror, remote_repo_version_db, database,
                                       tmp_dir, force=force)
            elif sys.argv[1] == '--mod':
                check_root()
                try:
                    with sqlite3.connect(database) as db:
                        if Filter(sys.argv[2], db).exists:
                            permissions = 'b'
                        else:
                            permissions = sys.argv[2]
                except IndexError:
                    permissions = 'b'
                for arg in sys.argv[1:]:
                    if not re.findall(r"^-[0-9a-zA-Z\-]", arg) and not arg == permissions:
                        change_filter_permissions(arg, database, tmp_dir, permissions, force=force)
                        count += 1
                if count == 0:
                    sys.exit('Error: please specify at least one filter ID')
                else:
                    with sqlite3.connect(database) as db:
                        update_hosts(hosts, db, default_hosts, default_ip, force=force)
                if '-y' in sys.argv or '--sync' in sys.argv:
                    update_remote_repo(remote_repo, remote_repo_mirror, remote_repo_version_db, database,
                                       tmp_dir, force=force)
            elif re.match(r"^-M", sys.argv[1]):
                check_root()
                if 'f' in sys.argv[1]:
                    force = True
                try:
                    with sqlite3.connect(database) as db:
                        if Filter(sys.argv[2], db).exists:
                            permissions = 'b'
                        else:
                            permissions = sys.argv[2]
                except IndexError:
                    permissions = 'b'
                for arg in sys.argv[1:]:
                    if not re.findall(r"^-[0-9a-zA-Z\-]", arg) and not arg == permissions:
                        change_filter_permissions(arg, database, tmp_dir, permissions, force=force)
                        count += 1
                if count == 0:
                    sys.exit('Error: please specify at least one filter ID')
                else:
                    with sqlite3.connect(database) as db:
                        update_hosts(hosts, db, default_hosts, default_ip, force=force)
                if '-y' in sys.argv or '--sync' in sys.argv or 'y' in sys.argv[1]:
                    update_remote_repo(remote_repo, remote_repo_mirror, remote_repo_version_db, database,
                                       tmp_dir, force=force)
            elif sys.argv[1] == '--info':
                for arg in sys.argv[1:]:
                    if not re.findall(r"^-[0-9a-zA-Z\-]", arg):
                        show_filter_info(arg, database)
                        count += 1
                if count == 0:
                    sys.exit('Error: please specify at least one filter ID')
            elif re.match(r"^-I", sys.argv[1]):
                for arg in sys.argv[1:]:
                    if not re.findall(r"^-[0-9a-zA-Z\-]", arg):
                        show_filter_info(arg, database)
                        count += 1
                if count == 0:
                    sys.exit('Error: please specify at least one filter ID')
            elif sys.argv[1] == '--list':
                if '--custom' in sys.argv or '-c' in sys.argv:
                    custom = True
                else:
                    custom = False
                if '--subscribed' in sys.argv or '-s' in sys.argv:
                    subscribed = True
                else:
                    subscribed = False
                if '--unsubscribed' in sys.argv or '-n' in sys.argv:
                    unsubscribed = True
                else:
                    unsubscribed = False
                if '--available' in sys.argv or '-w' in sys.argv:
                    available = True
                else:
                    available = False
                list_filters(database, custom=custom, subscribed=subscribed, unsubscribed=unsubscribed,
                             available=available)
            elif re.match(r"^-L", sys.argv[1]):
                if '--custom' in sys.argv or '-c' in sys.argv or 'c' in sys.argv[1]:
                    custom = True
                else:
                    custom = False
                if '--subscribed' in sys.argv or '-s' in sys.argv or 's' in sys.argv[1]:
                    subscribed = True
                else:
                    subscribed = False
                if '--unsubscribed' in sys.argv or '-n' in sys.argv or 'n' in sys.argv[1]:
                    unsubscribed = True
                else:
                    unsubscribed = False
                if '--available' in sys.argv or '-w' in sys.argv or 'w' in sys.argv[1]:
                    available = True
                else:
                    available = False
                list_filters(database, custom=custom, subscribed=subscribed, unsubscribed=unsubscribed,
                             available=available)
            elif sys.argv[1] == '--sync':
                check_root()
                update_remote_repo(remote_repo, remote_repo_mirror, remote_repo_version_db, database, tmp_dir,
                                   force=force)
            elif re.match(r"^-Y", sys.argv[1]):
                check_root()
                if 'f' in sys.argv[1]:
                    force = True
                update_remote_repo(remote_repo, remote_repo_mirror, remote_repo_version_db, database, tmp_dir,
                                   force=force)
            elif sys.argv[1] == '--update-hosts':
                check_root()
                with sqlite3.connect(database) as db:
                    update_hosts(hosts, db, default_hosts, default_ip, force=force)
            elif re.match(r"^-H", sys.argv[1]):
                check_root()
                if 'f' in sys.argv[1]:
                    force = True
                with sqlite3.connect(database) as db:
                    update_hosts(hosts, db, default_hosts, default_ip, force=force)
            elif sys.argv[1] == '--restore':
                check_root()
                restore_hosts(hosts, default_hosts, force=force)
            elif re.match(r"^-D", sys.argv[1]):
                check_root()
                if 'f' in sys.argv[1]:
                    force = True
                restore_hosts(hosts, default_hosts, force=force)
            else:
                sys.exit(f"Error: invalid operation: '{sys.argv[1]}'\nRun 'tblock -h' to show help page")
    except KeyboardInterrupt:
        print("\ntblock: received interrupt signal")
        sys.exit(1)


def run_converter() -> None:
    """Run the CLI filter converter
    """
    try:
        if len(sys.argv) <= 1:
            sys.exit(run_converter_help)
        elif '-h' in sys.argv or '--help' in sys.argv or re.findall(r"^-h", sys.argv[1]):
            print(run_converter_help)
        elif '-v' in sys.argv or '--version' in sys.argv or re.findall(r"^-v", sys.argv[1]):
            print(version_info.replace(
                'TBlock',
                'TBlockc'
            ).replace(
                'An anticapitalist ad-blocker that uses the hosts file',
                'TBlock\'s built-in filter converter'
            ))
        else:
            if '-f' in sys.argv or '--force' in sys.argv or re.findall(r"^-.*f", sys.argv[1]):
                force = True
            else:
                force = False
            if '-g' in sys.argv or '--get-syntax' in sys.argv or re.findall(r"^-g", sys.argv[1]):
                file_to_scan = None
                for arg in sys.argv[1:]:
                    if not re.findall(r"^-[0-9a-zA-Z\-]", arg) and not arg == file_to_scan:
                        file_to_scan = arg
                        break
                if file_to_scan is None:
                    sys.exit('Error: you need to specify the file to scan')
                elif not os.path.isfile(os.path.realpath(file_to_scan)):
                    sys.exit(f'Error: file not found: "{file_to_scan}"')
                else:
                    with open(file_to_scan, 'rt') as f:
                        print(f' => Syntax detected: {detect_syntax(f)}')
            else:
                input_file = None
                output_file = None
                permissions = 'abr'
                syntax = None
                original_syntax = None
                comments = False
                try:
                    if '-r' in sys.argv:
                        permissions = sys.argv[sys.argv.index('-r') + 1]
                    elif '--rules' in sys.argv:
                        permissions = sys.argv[sys.argv.index('--rules') + 1]
                    elif re.match(r"^-.*r", sys.argv[1]):
                        permissions = sys.argv[2]
                except IndexError:
                    sys.exit('Error: you need to specify rule policies to convert')
                try:
                    if '-o' in sys.argv:
                        original_syntax = sys.argv[sys.argv.index('-o') + 1]
                    elif '--original' in sys.argv:
                        original_syntax = sys.argv[sys.argv.index('--original') + 1]
                    elif re.match(r"^-.*o", sys.argv[1]):
                        original_syntax = sys.argv[2]
                except IndexError:
                    sys.exit('Error: you need to specify rule policies to convert')
                try:
                    if '-s' in sys.argv:
                        syntax = sys.argv[sys.argv.index('-s') + 1]
                    elif '--syntax' in sys.argv:
                        syntax = sys.argv[sys.argv.index('--syntax') + 1]
                    elif re.match(r"^-.*s", sys.argv[1]):
                        syntax = sys.argv[2]
                except IndexError:
                    sys.exit('Error: you need to specify output syntax to use')
                if '-c' in sys.argv or '--comments' in sys.argv or re.findall(r"^-.*c", sys.argv[1]):
                    comments = True
                for arg in sys.argv[1:]:
                    if not re.findall(r"^-[0-9a-zA-Z\-]", arg) and not arg == input_file and not arg == output_file and \
                            not arg == permissions and not arg == syntax and not arg == original_syntax:
                        if input_file is None:
                            input_file = arg
                        elif output_file is None:
                            output_file = arg
                        else:
                            sys.exit(f'Error: option {arg} is invalid')
                if syntax is None:
                    sys.exit('Error: you need to specify output syntax with "--syntax"')
                elif input_file is None:
                    sys.exit('Error: you need to specify the file to convert')
                elif output_file is None:
                    sys.exit('Error: you need to specify an output file where to write converted filter')
                else:
                    allow = True if 'a' in permissions else False
                    block = True if 'b' in permissions else False
                    redirect = True if 'r' in permissions else False
                    convert_filter(input_file, output_file, syntax, original_syntax, allow, block, redirect, comments,
                                   force=force)
    except KeyboardInterrupt:
        print("\ntblockc: received interrupt signal")
        sys.exit(1)


version_info = f'''TBlock version {__version__} - An anticapitalist ad-blocker that uses the hosts file
Copyright (C) 2021 Twann <twann@ctemplar.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.'''
