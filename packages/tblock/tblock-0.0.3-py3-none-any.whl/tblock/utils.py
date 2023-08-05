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
# This module contains functions used inside TBlock, and that don't need any local dependencies.                       #
########################################################################################################################

# Standard libraries
import os
import re
import sys
import base64
import getpass

# External libraries
import requests


def check_root() -> None:
    """Check if the user is root. Exits with error code 1 if not.
    """
    if getpass.getuser() != 'root':
        sys.exit('Error: you must run as root to perform this operation')


def is_url(url: str) -> bool:
    """Check whether a string is a valid URL or not

    Args:
        url (str): Tĥe string to check

    Returns:
        bool: True if URL seems valid
    """
    return 'http://' in url or 'https://' in url


def prompt_user(message: str) -> bool:
    """Prompt the user before executing an action

    Args:
        message (str): The message to display
    """
    print(message)
    try:
        answer = input('Are you sure to continue ? [y/n] ')
    except KeyboardInterrupt:
        return False
    else:
        return answer.lower() == 'y'


def is_valid_ip(ip: str) -> bool:
    """Check whether an IP address is valid or not

    Args:
        ip (str): Tĥe IP address to check

    Returns:
        bool: True if IP address seems valid
    """
    if 7 <= len(ip) <= 15:
        if len(re.findall(r"\.", ip)) == 3:
            return True
        else:
            return False
    else:
        return False


def generate_tmp_filename() -> str:
    """Generate a temporary filename
    """
    return str(
        base64.b64encode(os.urandom(16))
    ).split("'")[1].replace('/', '_').replace('=', '_').replace('+', '_') + ".tmp"


def download_file(url: str, output_path: str) -> None:
    """Get the content of an online file and export it into a local file

    Args:
        url (str): The URL of the online file
        output_path (str): Where to export file content
    """
    online_file = requests.get(url)
    with open(os.path.relpath(output_path), 'wb') as f:
        f.write(online_file.content)
