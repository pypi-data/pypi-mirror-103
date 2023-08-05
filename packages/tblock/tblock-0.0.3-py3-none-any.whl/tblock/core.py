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
# This module contains basic classes and functions to interact with rules and filters. It is recommended to use this   #
# module for developers, as the modules "tblock.rules" and "tblock.filters" both exit with error code 1 if an error    #
# occurs. In this one, the functions only raise the exceptions.                                                        #
########################################################################################################################

# Standard libraries
import os
import re
import json
import sys
import sqlite3

# External libraries
from colorama import Fore, Style

# Local libraries
from .exceptions import TBlockError, InvalidFilterID, InvalidFilterSource, UnknownFilterID, AlreadySubscribingToFilter,\
    InvalidFilterPermissions, NotSubscribingToFilter, RuleExist, InvalidRulePolicy, InvalidAddress, RulePriorityError, \
    FilterPermissionsError, RuleNotExist
from .utils import is_valid_ip, prompt_user

UserRule = '!user'


class Policy:
    allow = 'allow'
    block = 'block'
    redirect = 'redirect'


class Filter:

    def __init__(self, filter_id: str, sqlite_obj: sqlite3.Connection, commit: bool = True) -> None:
        """Filter that contains rules

        Args:
            filter_id (str): The ID of the filter
            commit (bool, optional): Commit changes to the database (default)
            sqlite_obj (sqlite3.Connection, optional): If changes are not committed, sqlite connector to use
        """
        if not commit and sqlite_obj is None:
            raise TBlockError('sqlite_obj cannot be NoneType if commit is False')
        self.id = filter_id
        self.db = sqlite_obj
        self.commit = commit
        all_filters = self.fetch_all_filters(self.db)
        self.source = None
        self.metadata = {
            "title": None,
            "version": None,
            "description": None,
            "license": None,
            "homepage": None,
            "syntax": None
        }
        self.subscribing = False
        self.on_rfr = False
        self.permissions = None
        self.exists = filter_id in all_filters.keys()
        if self.exists:
            self.source = all_filters[filter_id]['source']
            self.metadata = json.loads(all_filters[filter_id]['metadata'])
            self.subscribing = all_filters[filter_id]['subscribing']
            self.on_rfr = all_filters[filter_id]['on_rfr']
            self.permissions = all_filters[filter_id]['permissions']

    def add_from_rfr(self, source: str, metadata: dict) -> None:
        """Add a filter from the remote filter repository into the database

        Args:
            source (str): The source of the filter
            metadata (dict): Metadata, such as syntax, title, version
        """
        if self.exists:
            raise InvalidFilterID(f'filter already exists: {self.id}')
        elif source is None:
            raise InvalidFilterSource(f'source cannot remain empty for filter: {self.id}')
        else:
            sql = 'INSERT INTO "filters" ("id", "source", "metadata", "subscribing", "on_rfr", "permissions") ' \
                  'VALUES (?, ?, ?, ?, ?, ?)'
            params = (self.id, source, json.dumps(metadata), False, True, None)
            self.db.cursor().execute(sql, params)
            if self.commit:
                self.db.commit()
                self.__init__(self.id, self.db)

    def update_from_rfr(self, source: str, metadata: dict, on_rfr: bool = True) -> None:
        """Add a filter from the remote filter repository into the database

        Args:
            source (str): The source of the filter
            metadata (str): Metadata, such as syntax, title, version
            on_rfr (bool, optional): The filter is available on the remote repo. False if it is not anymore
        """
        if not self.exists:
            raise UnknownFilterID(f'filter does not exists: {self.id}')
        elif not self.on_rfr:
            raise InvalidFilterID(f'filter does not exists on the remote filter repository: {self.id}')
        elif source is None:
            raise InvalidFilterSource(f'source cannot remain empty for filter: {self.id}')
        else:
            self.db.cursor().execute(
                'UPDATE "filters" SET source=?, metadata=?, on_rfr=? WHERE id=?;',
                (source, json.dumps(metadata), on_rfr, self.id)
            )
            if self.commit:
                self.db.commit()
                self.__init__(self.id, self.db)

    def delete(self) -> None:
        """Delete a filter from database
        """
        if self.exists and self.subscribing:
            raise AlreadySubscribingToFilter(f'cannot delete filter: {self.id}')
        elif not self.exists:
            raise UnknownFilterID(
                f'filter is not available on the remote filter repository: {self.id}'
            )
        else:
            sql = 'DELETE FROM "filters" WHERE "id"=?'
            params = (self.id,)
            self.db.cursor().execute(sql, params)
            if self.commit:
                self.db.commit()
                self.__init__(self.id, self.db)

    def rename(self, new_filter_id: str) -> None:
        """Change the filter ID of a filter and its rules

        Args:
            new_filter_id (str): The new filter ID to use
        """
        if not self.exists:
            raise UnknownFilterID(f'cannot find filter in database: {self.id}')
        if new_filter_id in self.fetch_all_filters(self.db).keys():
            raise InvalidFilterID('filter already exists')
        sql = 'UPDATE "filters" SET id=? WHERE id=?;'
        params = (new_filter_id, self.id)
        self.db.cursor().execute(sql, params)
        sql = 'UPDATE "rules" SET filter_id=? WHERE filter_id=?;'
        params = (new_filter_id, self.id)
        self.db.cursor().execute(sql, params)
        if self.commit:
            self.db.commit()
            self.__init__(self.id, self.db)

    def subscribe(self, permissions: str, source: str = None) -> None:
        """Subscribe to a filter (in the database only)

        Args:
            permissions (str): Permissions of the filter (may contain one or more of these letters: 'abr')
            source (str, optional): If filter is a custom filter, you need to specify its source manually
        """
        if self.exists and self.subscribing:
            raise AlreadySubscribingToFilter(f'already subscribing to filter: {self.id}')
        elif not self.exists and source is None:
            raise UnknownFilterID(
                f'filter is not available on the remote filter repository: {self.id}, please specify a custom source'
            )
        elif source is not None and self.exists:
            raise InvalidFilterID(f'filter already exists on the remote filter repository: {self.id}')
        elif source is not None and source in self.fetch_all_filters_by_source(self.db):
            raise AlreadySubscribingToFilter(f'already subscribing to filter: {source}')
        elif not re.findall(re.compile(r'([abr])', re.IGNORECASE), permissions) and permissions is not None:
            raise InvalidFilterPermissions(f'filter permissions can only contain "a", "b" and "r", not: {permissions}')
        elif self.exists:
            sql = 'UPDATE "filters" SET subscribing=?, permissions=?  WHERE id=?;'
            params = (True, permissions.lower(), self.id)
            self.db.cursor().execute(sql, params)
            if self.commit:
                self.db.commit()
                self.__init__(self.id, self.db)
        else:
            self.db.cursor().execute(
                'INSERT INTO "filters" ("id", "source", "metadata", "subscribing", "on_rfr", "permissions") '
                'VALUES (?, ?, ?, ?, ?, ?)',
                (self.id, source, json.dumps(self.metadata), True, False, permissions.lower())
            )
            if self.commit:
                self.db.commit()
                self.__init__(self.id, self.db)

    def unsubscribe(self) -> None:
        """Unsubscribe from a filter (in the database only)
        """
        if not self.exists:
            raise UnknownFilterID(f'cannot find filter in database: {self.id}')
        elif not self.subscribing:
            raise NotSubscribingToFilter(f'not subscribing to filter: {self.id}')
        if self.on_rfr:
            sql = 'UPDATE "filters" SET subscribing=?, permissions=?  WHERE id=?;'
            params = (False, None, self.id)
            self.db.cursor().execute(sql, params)
            if self.commit:
                self.db.commit()
                self.__init__(self.id, self.db)
        else:
            sql = 'DELETE FROM "filters" WHERE "id"=?'
            params = (self.id,)
            self.db.cursor().execute(sql, params)
            if self.commit:
                self.db.commit()
                self.__init__(self.id, self.db)

    def change_permissions(self, permissions: str) -> None:
        """Unsubscribe from a filter (in the database only)

        Args:
            permissions (str): Permissions of the filter (may contain one or more of these letters: 'abr')
        """
        if not self.exists:
            raise UnknownFilterID(f'cannot find filter in database: {self.id}')
        elif not self.subscribing:
            raise NotSubscribingToFilter(f'not subscribing to filter: {self.id}')
        elif not re.findall(re.compile(r'([abr])', re.IGNORECASE), permissions) and permissions is not None:
            raise InvalidFilterPermissions(f'filter permissions can only contain "a", "b" and "r", not: {permissions}')
        else:
            sql = 'UPDATE "filters" SET permissions=?  WHERE id=?;'
            params = (permissions.lower(), self.id)
            self.db.cursor().execute(sql, params)
            if self.commit:
                self.db.commit()
                self.__init__(self.id, self.db)

    def remove_all_rules(self) -> None:
        """Remove all rules set by a filter
        """
        if not self.exists:
            raise UnknownFilterID(f'cannot find filter in database: {self.id}')
        elif not self.subscribing:
            raise NotSubscribingToFilter(f'not subscribing to filter: {self.id}')
        else:
            sql = 'DELETE FROM "rules" WHERE "filter_id"=?'
            params = (self.id,)
            self.db.cursor().execute(sql, params)
            if self.commit:
                self.db.commit()
                self.__init__(self.id, self.db)

    @staticmethod
    def fetch_all_filters(db: sqlite3.Connection) -> dict:
        """Fetch all filters from the database

        Args:
            db (sqlite3.Connection): SQLite connection object

        Returns:
            dict: All filters inside a dictionary. Filter IDs are dictionary keys
        """
        all_filters = {}
        data = db.cursor().execute(
            'SELECT "id", "source", "metadata", "subscribing", "on_rfr", "permissions" FROM "filters";'
        ).fetchall()
        for row in data:
            all_filters[row[0]] = {}
            all_filters[row[0]]['source'] = row[1]
            all_filters[row[0]]['metadata'] = row[2]
            all_filters[row[0]]['subscribing'] = row[3]
            all_filters[row[0]]['on_rfr'] = row[4]
            all_filters[row[0]]['permissions'] = row[5]
        return all_filters

    def get_rules_count(self) -> int:
        """Get the total of rules of the filter

        Returns:
            int: The number of rules
        """
        return len(self.db.cursor().execute(
            'SELECT "domain" FROM "rules" WHERE filter_id=?;', (self.id,)
        ).fetchall())

    @staticmethod
    def fetch_all_filters_by_source(db: sqlite3.Connection) -> dict:
        """Fetch all filters from the database by their sources

        Args:
            db (sqlite3.Connection): SQLite connection object

        Returns:
            dict: All filters inside a dictionary. Filter sources are dictionary keys
        """
        all_filters = {}
        data = db.cursor().execute(
            'SELECT "source", "id", "metadata", "subscribing", "on_rfr", "permissions" FROM "filters";'
        ).fetchall()
        for row in data:
            all_filters[row[0]] = {}
            all_filters[row[0]]['id'] = row[1]
            all_filters[row[0]]['metadata'] = row[2]
            all_filters[row[0]]['subscribing'] = row[3]
            all_filters[row[0]]['on_rfr'] = row[4]
            all_filters[row[0]]['permissions'] = row[5]
        return all_filters

    @staticmethod
    def get_all_subscribing_filter(db: sqlite3.Connection) -> list:
        """Fetch all subscribing filters from the database

        Args:
            db (sqlite3.Connection): SQLite connection object

        Returns:
            list: A list of all filter IDs
        """
        all_filters = []
        data = db.cursor().execute(
            'SELECT "id" FROM "filters" WHERE subscribing=1 ;'
        ).fetchall()
        for row in data:
            all_filters.append(row[0])
        return all_filters

    @staticmethod
    def get_all_rfr_filter(db: sqlite3.Connection) -> list:
        """Fetch all filters available on the remote filters repository from the database

        Args:
            db (sqlite3.Connection): SQLite connection object

        Returns:
            list: A list of all filter IDs
        """
        all_filters = []
        data = db.cursor().execute(
            'SELECT "id" FROM "filters" WHERE on_rfr=1 ;'
        ).fetchall()
        for row in data:
            all_filters.append(row[0])
        return all_filters


class Rule:

    def __init__(self, domain: str, sqlite_obj: sqlite3.Connection, commit: bool = True) -> None:
        """Rule for managing a domain

        Args:
            domain (str): The domain to manage
            commit (bool, optional): Commit changes to the database (default)
            sqlite_obj (sqlite3.Connection, optional): If changes are not committed, sqlite connector to use
        """
        if not commit and sqlite_obj is None:
            raise TBlockError('sqlite_obj cannot be NoneType if commit is False')
        self.domain = domain
        self.db = sqlite_obj
        self.commit = commit
        all_rules = self.fetch_all_rules(self.db)
        self.policy = None
        self.filter_id = None
        self.priority = None
        self.ip = None
        self.exists = domain in all_rules.keys()
        if self.exists:
            self.policy = all_rules[domain]['policy']
            self.filter_id = all_rules[domain]['filter_id']
            self.priority = all_rules[domain]['priority']
            self.ip = all_rules[domain]['ip']

    def add(self, policy: str, filter_id: str, priority: bool, ip: str = None) -> None:
        """Add a rule for a domain inside the database

        Args:
            policy (str): The policy ('allow'|'block'|'redirect')
            filter_id (str): The filter which the rule comes from. For user rule, use tblock.core.UserRule
            priority (str): The priority of the rule. True if user rule, False if standard rule
            ip (str, optional): The IP where to redirect the domain. Required for redirecting and blocking rules only
        """
        filter_origin = Filter(filter_id, self.db)
        if self.exists:
            raise RuleExist(f'rule already exists in database for domain: {self.domain}')
        elif not hasattr(Policy, policy):
            raise InvalidRulePolicy(f'invalid rule policy: {policy}')
        elif policy == Policy.redirect and ip is None:
            raise InvalidAddress(f'redirecting address cannot remain empty for domain: {self.domain}')
        elif policy == Policy.redirect and not is_valid_ip(ip):
            raise InvalidAddress(f'redirecting address seems invalid: {ip}')
        elif filter_id != UserRule and not filter_origin.subscribing:
            raise NotSubscribingToFilter(f'not subscribing to filter: {filter_id}')
        elif filter_id != UserRule and priority:
            raise RulePriorityError('filters are not allowed to add user rules')
        elif filter_id == UserRule and not priority:
            raise RulePriorityError(f'a filter id cannot be: {filter_id}, as it is reserved for user rules')
        elif filter_id != UserRule and 'a' not in filter_origin.permissions and policy == Policy.allow:
            raise FilterPermissionsError(f'filter is not allowed to add allowing rules: {filter_id}')
        elif filter_id != UserRule and 'b' not in filter_origin.permissions and policy == Policy.block:
            raise FilterPermissionsError(f'filter is not allowed to add blocking rules: {filter_id}')
        elif filter_id != UserRule and 'r' not in filter_origin.permissions and policy == Policy.redirect:
            raise FilterPermissionsError(f'filter is not allowed to add redirecting rules: {filter_id}')
        else:
            sql = 'INSERT INTO "rules" ("domain", "policy", "filter_id", "priority", "ip") VALUES (?, ?, ?, ?, ?)'
            params = (self.domain, policy, filter_id, priority, ip)
            self.db.cursor().execute(sql, params)
            if self.commit:
                self.db.commit()
                self.__init__(self.domain, self.db)

    def update(self, policy: str, filter_id: str, priority: bool, ip: str = None) -> None:
        """Add a rule for a domain inside the database

        Args:
            policy (str): The policy ('allow'|'block'|'redirect')
            filter_id (str): The filter which the rule comes from. For user rule, use tblock.core.UserRule
            priority (str): The priority of the rule. True if user rule, False if standard rule
            ip (str, optional): The IP where to redirect the domain. Required for redirecting and blocking rules only
        """
        filter_origin = Filter(filter_id, self.db)
        if not self.exists:
            raise RuleNotExist(f'rule does not exists in database for domain: {self.domain}')
        elif not priority and self.priority:
            raise RulePriorityError(f'filters cannot overwrite user rule set for domain: {self.domain}')
        elif not hasattr(Policy, policy):
            raise InvalidRulePolicy(f'invalid rule policy: {policy}')
        elif policy == Policy.redirect and ip is None:
            raise InvalidAddress(f'redirecting address cannot remain empty for domain: {self.domain}')
        elif policy == Policy.redirect and not is_valid_ip(ip):
            raise InvalidAddress(f'redirecting address seems invalid: {ip}')
        elif filter_id != UserRule and not filter_origin.subscribing:
            raise NotSubscribingToFilter(f'not subscribing to filter: {filter_id}')
        elif filter_id != UserRule and priority:
            raise RulePriorityError('filters are not allowed to add user rules')
        elif filter_id == UserRule and not priority:
            raise RulePriorityError(f'a filter id cannot be: {filter_id}, as it is reserved for user rules')
        elif filter_id != UserRule and 'a' not in filter_origin.permissions and policy == Policy.allow:
            raise FilterPermissionsError(f'filter is not allowed to add allowing rules: {filter_id}')
        elif filter_id != UserRule and 'b' not in filter_origin.permissions and policy == Policy.block:
            raise FilterPermissionsError(f'filter is not allowed to add blocking rules: {filter_id}')
        elif filter_id != UserRule and 'r' not in filter_origin.permissions and policy == Policy.redirect:
            raise FilterPermissionsError(f'filter is not allowed to add redirecting rules: {filter_id}')
        else:
            sql = 'UPDATE "rules" SET policy=?, filter_id=?, priority=?, ip=? WHERE domain=?;'
            params = (policy, filter_id, priority, ip, self.domain)
            self.db.cursor().execute(sql, params)
            if self.commit:
                self.db.commit()
                self.__init__(self.domain, self.db)

    def delete(self) -> None:
        """Delete a rule for a domain from the database

        Warning:
            This should not be used when removing all rules from a filter, use Filter.remove_all_rules() instead
        """
        if not self.exists:
            raise RuleNotExist(f'rule does not exists in database for domain: {self.domain}')
        else:
            sql = 'DELETE FROM "rules" WHERE "domain"=?'
            params = (self.domain,)
            self.db.cursor().execute(sql, params)
            if self.commit:
                self.db.commit()
                self.__init__(self.domain, self.db)

    @staticmethod
    def fetch_all_rules(db: sqlite3.Connection) -> dict:
        """Fetch all rules from the database

        Args:
            db (sqlite3.Connection): SQLite connection object

        Returns:
            dict: All rules inside a dictionary. Domains are dictionary keys
        """
        all_rules = {}
        data = db.cursor().execute('SELECT "domain","policy","filter_id","priority","ip" FROM "rules";').fetchall()
        for row in data:
            all_rules[row[0]] = {}
            all_rules[row[0]]['policy'] = row[1]
            all_rules[row[0]]['filter_id'] = row[2]
            all_rules[row[0]]['priority'] = row[3]
            all_rules[row[0]]['ip'] = row[4]
        return all_rules

    @staticmethod
    def rules_count(db: sqlite3.Connection) -> dict:
        """Get statistics about rules

        Args:
            db (sqlite3.Connection): SQLite connection object

        Returns:
            dict: Stats inside a dictionary
        """
        return {
            "total": db.cursor().execute('SELECT COUNT() FROM rules;').fetchone()[0],
            "allow": db.cursor().execute('SELECT COUNT() FROM rules WHERE policy="allow";').fetchone()[0],
            "block": db.cursor().execute('SELECT COUNT() FROM rules WHERE policy="block";').fetchone()[0],
            "redirect": db.cursor().execute('SELECT COUNT() FROM rules WHERE policy="redirect";').fetchone()[0],
            "user": db.cursor().execute('SELECT COUNT() FROM rules WHERE priority=1;').fetchone()[0],
        }


def update_hosts(hosts_path: str, db: sqlite3.Connection, default_hosts: str, default_ip: str,
                 verbosity: bool = True, force: bool = False) -> None:
    """Update hosts file with rules

    Args:
        hosts_path (str): The path to the hosts file
        db (sqlite3.Connection): SQLite connection object
        default_hosts (str): The default path to the file that contains default hosts file content
        default_ip (str): The default IP address where to redirect blocked domains inside hosts file
        verbosity (bool, optional): Enable verbosity (default)
        force (bool, optional): Do not prompt user for anything
    """
    if not force and not prompt_user('TBlock is going to update the hosts file'):
        sys.exit()
    if verbosity:
        print(':: Updating hosts file')
    was_enabled = os.path.isfile(default_hosts)
    new_hosts = '\n\n# BEGIN BLOCKING RULES\n'
    all_rules = Rule.fetch_all_rules(db)
    count = 1
    for domain in all_rules:
        if verbosity:
            if count < len(all_rules):
                print(f' => Retrieving rules... ({count}/{len(all_rules)})', end='\r')
            else:
                print(f' => Retrieved all rules ({count}/{len(all_rules)})')
        if all_rules[domain]['policy'] == Policy.block:
            new_hosts += f'{default_ip}    {domain}\n'
        elif all_rules[domain]['policy'] == Policy.redirect:
            new_hosts += f'{all_rules[domain]["ip"]}    {domain}\n'
        count += 1
    if not os.path.isfile(default_hosts):
        with open(hosts_path, 'rt') as h:
            default_hosts_content = h.read()
        with open(default_hosts, 'wt') as h:
            h.write(default_hosts_content)
        if verbosity:
            print(' => Backed up previous hosts file')
    else:
        with open(default_hosts, 'rt') as h:
            default_hosts_content = h.read()
    new_hosts = default_hosts_content + new_hosts
    with open(hosts_path, 'wt') as f:
        f.write(
            '# This file is automatically generated by TBlock\n'
            '# To edit it manually, run "tblock -D" first. Otherwise, all your modifications will be '
            'overwritten.\n\n' + new_hosts
        )
    if not was_enabled:
        print(f' => {Fore.GREEN}Protection is now enabled{Style.RESET_ALL}')
    if verbosity:
        print(' => Hosts file updated')


def restore_hosts(hosts_path: str, default_hosts: str,
                  verbosity: bool = True, force: bool = False) -> None:
    """Restore default hosts file

    Args:
        hosts_path (str): The path to the hosts file
        default_hosts (str): The path to the local file containing default hosts content
        verbosity (bool, optional): Enable verbosity (default)
        force (bool, optional): Do not prompt user for anything
    """
    if not os.path.isfile(default_hosts):
        print('Error: default hosts file already restored.')
        sys.exit(1)
    else:
        with open(default_hosts, 'rt') as h:
            default_hosts_content = h.read()
    if not force and not prompt_user('TBlock is going to restore the default hosts file'):
        sys.exit()
    if verbosity:
        print(':: Restoring default hosts file')
    with open(hosts_path, 'wt') as f:
        f.write(default_hosts_content)
    if verbosity:
        print(' => Default hosts file restored')
    os.remove(default_hosts)
    if verbosity:
        print(' => Removed default hosts backup')
    if verbosity:
        print(f' => {Fore.RED}Protection is now disabled{Style.RESET_ALL}')
        print("You can now safely edit your hosts file manually.\n"
              "After that, run 'tblock -H' to update this file while keeping your modifications.")
