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
# This module contains functions used to add and remove user rules. If an error occurs, the program exits with error   #
# code 1.                                                                                                              #
########################################################################################################################

# Standard libraries
import sys
import sqlite3
import os.path

# Local libraries
from .utils import is_valid_ip, prompt_user
from .core import Policy, Rule, UserRule


def add_user_rule(domain: str, policy: str, db_path: str, ip: str = None, verbosity: bool = True,
                  force: bool = False) -> None:
    """Add an user rule to manage a domain

    Args:
        domain (str): The domain to manage
        policy (str): The policy of the rule ('allow', 'block', 'redirect')
        db_path (str): The path to the SQLite database
        ip (str, optional): The IP address where to redirect the domain
        verbosity (bool, optional): Enable verbosity (default)
        force (bool, optional): Do not prompt user for anything
    """
    db_path = os.path.realpath(db_path)
    if not os.path.isfile(db_path):
        if verbosity:
            print(f'Error: file not found: "{db_path}"')
        sys.exit(1)
    db = sqlite3.connect(db_path)
    new_rule = Rule(domain, db)
    if policy == Policy.redirect and not is_valid_ip(ip):
        if verbosity:
            print(f'Error: invalid redirecting ip: "{ip}"')
        sys.exit(1)
    elif not hasattr(Policy, policy):
        if verbosity:
            print(f'Error: invalid policy: "{policy}"')
        sys.exit(1)
    elif force or prompt_user(f'You are about to {policy} domain: "{domain}"'):
        if new_rule.exists:
            new_rule.update(policy, UserRule, True, ip)
        else:
            new_rule.add(policy, UserRule, True, ip)
    db.close()


def delete_user_rule(domain: str, db_path: str, verbosity: bool = True, force: bool = False) -> None:
    """Delete an user rule

    Args:
        domain (str): The domain to manage
        db_path (str): The path to the SQLite database
        verbosity (bool, optional): Enable verbosity (default)
        force (bool, optional): Do not prompt user for anything
    """
    db_path = os.path.realpath(db_path)
    if not os.path.isfile(db_path):
        if verbosity:
            print(f'Error: file not found: "{db_path}"')
        sys.exit(1)
    db = sqlite3.connect(db_path)
    new_rule = Rule(domain, db)
    if not new_rule.exists or not new_rule.priority:
        if verbosity:
            print(f'Error: user rule does not exist for domain: "{domain}"')
        sys.exit(1)
    elif force or prompt_user(f'You are about to delete rule for domain: "{domain}"'):
        new_rule.delete()
    db.close()


def list_rules(db_path: str, standard: bool, user: bool) -> None:
    """List all rules

    Args:
        db_path (str): The path to the SQLite database
        standard (bool): List standard rules only
        user (bool): List user rules only
    """
    db_path = os.path.realpath(db_path)
    if not os.path.isfile(db_path):
        print(f'Error: file not found: "{db_path}"')
        sys.exit(1)
    db = sqlite3.connect(db_path)
    if standard and user:
        print('Error: no rule can be both a standard rule and an user rule')
        sys.exit(1)
    all_rules = Rule.fetch_all_rules(db)
    db.close()
    for rule in all_rules:
        if not user and not standard:
            if all_rules[rule]["policy"] != Policy.redirect:
                print(f'{all_rules[rule]["policy"]}     {rule}')
            else:
                print(f'{all_rules[rule]["policy"]}  {rule}')
        elif user and all_rules[rule]['priority']:
            if all_rules[rule]["policy"] != Policy.redirect:
                print(f'{all_rules[rule]["policy"]}     {rule}')
            else:
                print(f'{all_rules[rule]["policy"]}  {rule}')
        elif standard and not all_rules[rule]['priority']:
            if all_rules[rule]["policy"] != Policy.redirect:
                print(f'{all_rules[rule]["policy"]}     {rule}')
            else:
                print(f'{all_rules[rule]["policy"]}  {rule}')
