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
# This module contains functions to convert rules from a filter syntax into another syntax. Exit with error code 1 if  #
# an error occurs.                                                                                                     #
########################################################################################################################

# Standard libraries
import os.path
import sys

# Local libraries
from . import Syntax
from .parser import get_filter_content
from ..utils import prompt_user


def convert_filter(input_file: str, output_file: str, output_syntax: str, origin_syntax: str = None,
                   allow: bool = True, block: bool = True, redirect: bool = True, comments: bool = False,
                   verbosity: bool = True, force: bool = True) -> None:
    """Convert a filter into another syntax

    Args:
        input_file (str): The path to the filter to convert
        output_file (str): The path to the converted filter
        output_syntax (str): The syntax of the converted filter
        origin_syntax (str, optional): The syntax of the filter to convert
        allow (bool, optional): Also return allowing rules (default)
        block (bool, optional): Also return blocking rules (default)
        redirect (bool, optional): Also return redirecting rules (default)
        comments (bool, optional): Also return comments (default)
        verbosity (bool, optional): Display information
        force (bool, optional): Do not prompt for anything
    """
    if not os.path.isfile(os.path.realpath(input_file)):
        if verbosity:
            print(f'Error: file not found: "{input_file}"')
        sys.exit(1)
    elif os.path.isfile(os.path.realpath(output_file)) and \
            not force and not prompt_user(f'File "{output_file}" already exists, it will be overwritten.'):
        sys.exit()
    elif not hasattr(Syntax, output_syntax):
        if verbosity:
            print(f'Error: invalid syntax: "{output_syntax}"')
        sys.exit(1)
    elif origin_syntax and not hasattr(Syntax, origin_syntax):
        if verbosity:
            print(f'Error: invalid syntax: "{output_syntax}"')
        sys.exit(1)
    else:
        if verbosity:
            print(f':: Converting {input_file} into syntax {output_syntax}')
        all_rules = get_filter_content(input_file, origin_syntax, allow, block, redirect, comments, verbosity)
        if output_syntax == Syntax.adblockplus:
            output_content = '[Adblock Plus 3.1]\n'
        elif output_syntax == Syntax.tblock:
            output_content = '@BEGIN_RULES\n\n'
        else:
            output_content = ''
        tblock_syntax = None
        opera_policy = None
        count = 1
        for rule in all_rules:
            if verbosity:
                if count < len(all_rules):
                    print(f' => Converting rules ... ({count}/{len(all_rules)})', end='\r')
                else:
                    print(f' => Rules have been converted ({count}/{len(all_rules)})')
            if rule[0] == 'comment' and comments:
                if output_syntax == Syntax.adblockplus:
                    output_content += f'!{rule[1]}\n'
                elif not output_syntax == Syntax.list:
                    output_content += f'#{rule[1]}\n'
            elif rule[0] == 'rule':
                if rule[2] == 'allow' and allow:
                    if output_syntax == Syntax.adblockplus:
                        output_content += f'@@||{rule[1]}^\n'
                    elif output_syntax == Syntax.tblock:
                        if tblock_syntax != 'allow':
                            tblock_syntax = 'allow'
                            output_content += f'!allow\n{rule[1]}\n'
                        else:
                            output_content += f'{rule[1]}\n'
                    elif output_syntax == Syntax.opera:
                        if opera_policy != 'allow':
                            opera_policy = 'allow'
                            output_content += f'[include]\nhttp://{rule[1]}/*\n'
                        else:
                            output_content += f'http://{rule[1]}/*\n'
                            output_content += f'http://*.{rule[1]}/*\n'
                elif rule[2] == 'block' and block:
                    if output_syntax == Syntax.adblockplus:
                        output_content += f'||{rule[1]}^\n'
                    elif output_syntax == Syntax.dnsmasq:
                        output_content += f'server=/{rule[1]}/\n'
                    elif output_syntax == Syntax.hosts:
                        output_content += f'127.0.0.1    {rule[1]}\n'
                    elif output_syntax == Syntax.list:
                        output_content += f'{rule[1]}\n'
                    elif output_syntax == Syntax.tblock:
                        if tblock_syntax != 'block':
                            tblock_syntax = 'block'
                            output_content += f'!block\n{rule[1]}\n'
                        else:
                            output_content += f'{rule[1]}\n'
                    elif output_syntax == Syntax.opera:
                        if opera_policy != 'block':
                            opera_policy = 'block'
                            output_content += f'[exclude]\nhttp://{rule[1]}/*\n'
                        else:
                            output_content += f'http://{rule[1]}/*\n'
                elif rule[2] == 'redirect' and redirect:
                    if output_syntax == Syntax.hosts:
                        output_content += f'{rule[3]}    {rule[1]}\n'
                    elif output_syntax == Syntax.tblock:
                        if tblock_syntax != f'redirect {rule[3]}':
                            tblock_syntax = f'redirect {rule[3]}'
                            output_content += f'!redirect {rule[3]}\n{rule[1]}\n'
                        else:
                            output_content += f'{rule[1]}\n'
            count += 1
        if output_syntax == Syntax.tblock:
            output_content += '\n@END_RULES\n'
        if verbosity:
            print(' => Writing converted rules inside new filter...', end='\r')
        with open(os.path.realpath(output_file), 'wt') as f:
            f.write(output_content)
        if verbosity:
            print(' => Converted rules have been written inside new filter')
