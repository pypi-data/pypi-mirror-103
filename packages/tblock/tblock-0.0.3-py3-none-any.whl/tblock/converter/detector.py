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
# This module contains functions to detect filter syntax and to check if a rule is in fact a comment.                  #
########################################################################################################################

# Standard libraries
from _io import TextIOWrapper
import re

# Local libraries
from . import Syntax
from ..exceptions import InvalidFilterSyntax


def detect_syntax(f: TextIOWrapper) -> str:
    """Detect the syntax of a filter

    Args:
        f (TextIOWrapper): The read-only opened filter

    Returns:
        str: The syntax. Can be 'adblockplus', 'tblock', 'hosts', 'dnsmasq', 'list' or ''
    """
    rules = []
    for rule in f.readlines():
        if rule != '\n':
            rules.append(rule.split("\n")[0])
    f.close()
    if re.findall(re.compile(r'(\[adblock plus)', re.IGNORECASE), str(rules)):
        return Syntax.adblockplus
    elif re.findall(re.compile(r'(@BEGIN_[ADEGLMRSTU]*|@END_[ADEGLMRSTU]*)'), str(rules)):
        return Syntax.tblock
    elif len(re.findall(re.compile(r'(\|\|[.a-z\-]*[$^]|![ A-z]*[.]*:|!)'), str(rules))) * 100 / len(rules) >= 50:
        return Syntax.adblockplus
    elif len(re.findall(re.compile(r'(127\.0\.[01]\.[0-9] |0\.0\.0\.0 )'), str(rules))) * 100 / len(rules) >= 50:
        return Syntax.hosts
    elif len(re.findall(re.compile(r'(server=/|domain=/)'), str(rules))) * 100 / len(rules) >= 50:
        return Syntax.dnsmasq
    elif len(re.findall(re.compile(r'(http://)'), str(rules))) * 100 / len(rules) >= 50:
        return Syntax.opera
    elif len(re.findall(re.compile(r'([0-9a-z]*\.[.a-z]*)'), str(rules))) * 100 / len(rules) >= 50:
        return Syntax.list
    else:
        return ''


def is_comment(line: str, syntax: str) -> bool:
    """Check if a line is a comment

    Args:
        line (str): The line to check
        syntax (str): The syntax to use for check

    Returns:
        bool: True if line is a comment
    """
    if hasattr(Syntax, syntax):
        if syntax == Syntax.adblockplus:
            return line[0:1] == '!'
        else:
            return line[0:1] == '#'
    else:
        raise InvalidFilterSyntax(f'"{syntax}" is not a valid syntax')
