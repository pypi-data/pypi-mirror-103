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
# This module contains functions to get rules and comments from a filter of any syntax.                                #
########################################################################################################################

# Standard libraries
import re

# Local libraries
from . import Syntax
from .detector import detect_syntax, is_comment
from ..exceptions import InvalidFilterSyntax


def get_rules_from_filter(filter_path: str, syntax: str = None, allow: bool = True, block: bool = True,
                          redirect: bool = True, verbosity: bool = True) -> dict:
    """Get all rules from a filter

    Args:
        filter_path (str): The path to the filter
        syntax (str, optional): Specify the syntax of the filter
        allow (bool, optional): Also return allowing rules (default)
        block (bool, optional): Also return blocking rules (default)
        redirect (bool, optional): Also return redirecting rules (default)
        verbosity (bool, optional): Display information
    """
    with open(filter_path, 'rt') as f:
        rules = f.readlines()
    filter_data = {}
    if syntax is None:
        try:
            with open(filter_path, 'rt') as f:
                if verbosity:
                    print(' => Detecting filter syntax...', end='\r')
                syntax = detect_syntax(f)
        except UnicodeDecodeError:
            raise InvalidFilterSyntax(f'cannot read file "{filter_path}"')
        else:
            if verbosity:
                print(f' => Detected filter syntax: {syntax}')
    if not hasattr(Syntax, syntax):
        raise InvalidFilterSyntax(f'"{syntax}" is not a valid syntax')
    else:
        tblock_begin = None
        tblock_policy = None
        opera_policy = None
        count = 0
        for rule in rules:
            if verbosity:
                if not count + 1 == len(rules):
                    print(f" => Parsing filter... ({count + 1}/{len(rules)})", end='\r')
                else:
                    print(f" => Parsing filter: done ({count + 1}/{len(rules)})")
            if rule != "\n":
                if not is_comment(rule, syntax):
                    if syntax == Syntax.adblockplus:
                        if not re.findall(re.compile(r'([$/&%?:*()=,;#\"+])'), rule):
                            if '^' in rule:
                                if rule[0:2] == '||' and block:
                                    filter_data[rule.split("\n")[0].split('||')[1].split('^')[0]] = ['block']
                                elif rule[0:4] == '@@||' and allow:
                                    filter_data[rule.split("\n")[0].split('||')[1].split('^')[0]] = ['allow']
                    elif syntax == Syntax.hosts:
                        if re.match(re.compile(r"(127\.0\.0\.1 |0\.0\.0\.0 )"), rule):
                            if not re.findall(re.compile(r'([$/&%?:*()=,;#\"+])'), rule):
                                rule = rule.split("\n")[0]
                                rule = rule.split(' ')[len(rule.split(' ')) - 1].replace(' ', '')
                                if 'localhost' not in rule and '.localdomain' not in rule and rule and block:
                                    filter_data[rule] = ['block']
                    elif syntax == Syntax.list:
                        if not re.findall(re.compile(r'([$/&%?:*()=,;#\"+])'), rule) and block:
                            filter_data[rule.split("\n")[0]] = ['block']
                    elif syntax == Syntax.dnsmasq:
                        if re.match(re.compile(r"(server=/|domain=/)"), rule):
                            if not re.findall(re.compile(r'([$&%?:*(),;#\"+])'), rule) and block:
                                filter_data[rule.split("\n")[0].split('=/')[1].split('/')[0]] = ['block']
                    elif syntax == Syntax.tblock:
                        if tblock_begin == "rules":
                            if rule.split('\n')[0] == '@END_RULES':
                                tblock_begin = None
                            elif rule[0:1] == "!":
                                if rule.split('\n')[0] == "!allow":
                                    tblock_policy = "allow"
                                elif rule.split('\n')[0] == "!block":
                                    tblock_policy = "block"
                                elif rule[0:10] == "!redirect ":
                                    tblock_policy = "redirect " + rule.split('!redirect ')[1].split('\n')[0]
                            else:
                                if not re.findall(re.compile(r'([$/&%?:*()=,;#\"+])'), rule):
                                    if 'redirect' in tblock_policy and redirect:
                                        filter_data[rule.split("\n")[0]] = [
                                            'redirect', tblock_policy.split('redirect ')[1]
                                        ]
                                    elif tblock_policy == "block" and block or tblock_policy == "allow" and allow:
                                        filter_data[rule.split("\n")[0]] = [tblock_policy]
                        elif tblock_begin == "metadata":
                            if rule.split('\n')[0] == '@END_METADATA':
                                tblock_begin = None
                        elif tblock_begin is None:
                            if rule.split('\n')[0] == '@BEGIN_RULES':
                                tblock_begin = "rules"
                            elif rule.split('\n')[0] == '@BEGIN_METADATA':
                                tblock_begin = "metadata"
                    elif syntax == Syntax.opera:
                        if rule.split('\n')[0] == '[include]':
                            opera_policy = 'allow'
                        elif rule.split('\n')[0] == '[exclude]':
                            opera_policy = 'block'
                        if re.match(r'^http://[a-z0-9]*\.[a-z0-9.]*/\*', rule.split('\n')[0]):
                            if opera_policy == 'allow':
                                filter_data[rule.split("http://")[1].split('/*')[0]] = ['allow']
                            elif opera_policy == 'block':
                                filter_data[rule.split("http://")[1].split('/*')[0]] = ['block']
            count += 1
    if verbosity:
        print(f' => Skipped {len(rules) - len(filter_data)} invalid rule(s)')
    return filter_data


def get_filter_content(filter_path: str, syntax: str = None, allow: bool = True, block: bool = True,
                       redirect: bool = True, comments: bool = True, verbosity: bool = True) -> list:
    """Get all rules from a filter

    Args:
        filter_path (str): The path to the filter
        syntax (str, optional): Specify the syntax of the filter
        allow (bool, optional): Also return allowing rules (default)
        block (bool, optional): Also return blocking rules (default)
        redirect (bool, optional): Also return redirecting rules (default)
        comments (bool, optional): Also return comments (default)
        verbosity (bool, optional): Display information
    """
    with open(filter_path, 'rt') as f:
        rules = f.readlines()
    filter_data = []
    if syntax is None:
        try:
            with open(filter_path, 'rt') as f:
                if verbosity:
                    print(' => Detecting filter syntax...', end='\r')
                syntax = detect_syntax(f)
        except UnicodeDecodeError:
            raise InvalidFilterSyntax(f'cannot read file "{filter_path}"')
        else:
            if verbosity:
                print(f' => Detected filter syntax: {syntax}')
    if not hasattr(Syntax, syntax):
        raise InvalidFilterSyntax(f'"{syntax}" is not a valid syntax')
    else:
        tblock_begin = None
        tblock_policy = None
        opera_policy = None
        count = 0
        for rule in rules:
            if verbosity:
                if not count + 1 == len(rules):
                    print(f" => Parsing filter... ({count + 1}/{len(rules)})", end='\r')
                else:
                    print(f" => Parsing filter: done ({count + 1}/{len(rules)})")
            if rule != "\n":
                if not is_comment(rule, syntax):
                    if syntax == Syntax.adblockplus:
                        if not re.findall(re.compile(r'([$/&%?:*()=,;#\"+])'), rule):
                            if '^' in rule:
                                if rule[0:2] == '||' and block:
                                    filter_data.append(
                                        ['rule', rule.split("\n")[0].split('||')[1].split('^')[0], 'block']
                                    )
                                elif rule[0:4] == '@@||' and allow:
                                    filter_data.append(
                                        ['rule', rule.split("\n")[0].split('||')[1].split('^')[0], 'allow']
                                    )
                    elif syntax == Syntax.hosts:
                        if re.match(re.compile(r"(127\.0\.0\.1 |0\.0\.0\.0 )"), rule):
                            if not re.findall(re.compile(r'([$/&%?:*()=,;#\"+])'), rule):
                                rule = rule.split("\n")[0]
                                rule = rule.split(' ')[len(rule.split(' ')) - 1].replace(' ', '')
                                if 'localhost' not in rule and '.localdomain' not in rule and rule and block:
                                    filter_data.append(['rule', rule, 'block'])
                    elif syntax == Syntax.list:
                        if not re.findall(re.compile(r'([$/&%?:*()=,;#\"+])'), rule) and block:
                            filter_data.append(['rule', rule.split("\n")[0], 'block'])
                    elif syntax == Syntax.dnsmasq:
                        if re.match(re.compile(r"(server=/|domain=/)"), rule):
                            if not re.findall(re.compile(r'([$&%?:*(),;#\"+])'), rule) and block:
                                filter_data.append(['rule', rule.split("\n")[0].split('=/')[1].split('/')[0], 'block'])
                    elif syntax == Syntax.tblock:
                        if tblock_begin == "rules":
                            if rule.split('\n')[0] == '@END_RULES':
                                tblock_begin = None
                            elif rule[0:1] == "!":
                                if rule.split('\n')[0] == "!allow":
                                    tblock_policy = "allow"
                                elif rule.split('\n')[0] == "!block":
                                    tblock_policy = "block"
                                elif rule[0:10] == "!redirect ":
                                    tblock_policy = "redirect " + rule.split('!redirect ')[1].split('\n')[0]
                            else:
                                if not re.findall(re.compile(r'([$/&%?:*()=,;#\"+])'), rule):
                                    if 'redirect' in tblock_policy and redirect:
                                        filter_data.append([
                                            'rule', rule.split("\n")[0], 'redirect', tblock_policy.split('redirect ')[1]
                                        ])
                                    elif tblock_policy == "block" and block or tblock_policy == "allow" and allow:
                                        filter_data.append(['rule', rule.split("\n")[0], tblock_policy])
                        elif tblock_begin == "metadata":
                            if rule.split('\n')[0] == '@END_METADATA':
                                tblock_begin = None
                        elif tblock_begin is None:
                            if rule.split('\n')[0] == '@BEGIN_RULES':
                                tblock_begin = "rules"
                            elif rule.split('\n')[0] == '@BEGIN_METADATA':
                                tblock_begin = "metadata"
                    elif syntax == Syntax.opera:
                        if rule.split('\n')[0] == '[include]':
                            opera_policy = 'allow'
                        elif rule.split('\n')[0] == '[exclude]':
                            opera_policy = 'block'
                        if re.match(r'^http://[a-z0-9]*\.[a-z0-9.]*/\*', rule.split('\n')[0]):
                            if opera_policy == 'allow':
                                filter_data.append(['rule', rule.split("http://")[1].split('/*')[0], 'allow'])
                            elif opera_policy == 'block':
                                filter_data.append(['rule', rule.split("http://")[1].split('/*')[0], 'block'])
                elif comments:
                    if syntax == Syntax.adblockplus:
                        filter_data.append(['comment', rule.split('!')[1].replace('\n', '')])
                    else:
                        filter_data.append(['comment', rule.split('#')[1].replace('\n', '')])
            count += 1
    if verbosity:
        print(f' => Skipped {len(rules) - len(filter_data)} invalid rule(s)')
    return filter_data
