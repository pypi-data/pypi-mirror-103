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
# This module contains functions used to subscribe or unsubscribe to filters, to update them, as well as a function to #
# update the remote filters repository. If an error occurs, the program exits with error code 1.                       #
########################################################################################################################

# Standard libraries
import re
import sys
import os
import sqlite3
from xml.etree import ElementTree

# External libraries
import urllib3
import requests

# Local libraries
from .utils import download_file, is_url, generate_tmp_filename, prompt_user
from .converter.parser import get_rules_from_filter
from .core import Filter, Rule, Policy
from .exceptions import InvalidFilterSyntax


def subscribe_to_filter(filter_id: str, db_path: str, tmp_dir: str, permissions: str = None,
                        source: str = None, verbosity: bool = True, force: bool = False) -> None:
    """Subscribe to a filter

    Args:
        filter_id (str): The ID of the filter to subscribe to
        db_path (str): The path to the SQLite database
        tmp_dir (str): The directory where to store temporary files
        permissions (str, optional): Permissions of the filter (may contain one or more of these letters: 'abr')
        source (str, optional): If filter is a custom filter that does not already exists, its source
        verbosity (bool, optional): Enable verbosity (default)
        force (bool, optional): Do not prompt user for anything
    """
    db_path = os.path.realpath(db_path)
    if not os.path.isfile(db_path):
        if verbosity:
            print(f'Error: file not found: "{db_path}"')
        sys.exit(1)
    db = sqlite3.connect(db_path)
    new_filter = Filter(filter_id, db)
    if not new_filter.exists and source is None:
        if verbosity:
            print(f'Error: filter "{filter_id}" does not exists')
        db.close()
        sys.exit(1)
    elif new_filter.exists and new_filter.subscribing:
        if verbosity:
            print(f'Error: already subscribing to filter "{filter_id}"')
        db.close()
        sys.exit(1)
    elif source in Filter.fetch_all_filters_by_source(db).keys():
        if verbosity:
            print(f'Error: already subscribing to source "{source}" '
                  f'({Filter.fetch_all_filters_by_source(db)[source]["id"]})')
        db.close()
        sys.exit(1)
    elif not re.findall(re.compile(r'([abr])', re.IGNORECASE), permissions) and permissions is not None:
        if verbosity:
            print(f'Error: "{permissions}" is not a valid permission')
        sys.exit(1)
    else:
        if force or prompt_user(f'You are about to subscribe to filter "{filter_id}"'):
            if source is not None and not is_url(source):
                source = os.path.realpath(source)
            if verbosity:
                print(f':: Subscribing to filter: {filter_id}')
            if new_filter.exists:
                new_filter.subscribe(permissions)
                if verbosity:
                    print(' => Marked already existing filter as subscribed in database')
            else:
                new_filter.subscribe(permissions, source)
                if verbosity:
                    print(' => Added new custom filter into database')
            db.close()
            update_filter(filter_id, db_path, tmp_dir, verbosity, force=True)
        else:
            db.close()


def unsubscribe_to_filter(filter_id: str, db_path: str, verbosity: bool = True, force: bool = False) -> None:
    """Unsubscribe to a filter

    Args:
        filter_id (str): The ID of the filter to subscribe to
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
    new_filter = Filter(filter_id, db)
    if not new_filter.exists:
        if verbosity:
            print(f'Error: filter "{filter_id}" does not exists')
        db.close()
        sys.exit(1)
    elif new_filter.exists and not new_filter.subscribing:
        if verbosity:
            print(f'Error: not subscribing to filter "{filter_id}"')
        db.close()
        sys.exit(1)
    else:
        if force or prompt_user(f'You are about to unsubscribe to filter "{filter_id}"'):
            if verbosity:
                print(f':: Unsubscribing to filter: {filter_id}')
            if verbosity:
                print(' => Removing all filters rules ...', end='\r')
            new_filter.remove_all_rules()
            if verbosity:
                print(' => Removing all filters rules: done')
            new_filter.unsubscribe()
            if verbosity:
                if new_filter.on_rfr:
                    print(' => Marked filter as unsubscribed in database')
                else:
                    print(' => Removed custom filter from database')
                print('All rules from filter have been removed. However, it is recommended to run "tblock -U" to update'
                      ' rules from all other filters.')
            db.close()
        else:
            db.close()


def update_filter(filter_id: str, db_path: str, tmp_dir: str, verbosity: bool = True, force: bool = False) -> None:
    """Update a filter

    Args:
        filter_id (str): The ID of the filter to subscribe to
        db_path (str): The path to the SQLite database
        tmp_dir (str): The directory where to store temporary files
        verbosity (bool, optional): Enable verbosity (default)
        force (bool, optional): Do not prompt user for anything
    """
    db_path = os.path.realpath(db_path)
    if not os.path.isfile(db_path):
        if verbosity:
            print(f'Error: file not found: "{db_path}"')
        sys.exit(1)
    db = sqlite3.connect(db_path)
    new_filter = Filter(filter_id, db)
    allow = True if 'a' in new_filter.permissions else False
    block = True if 'b' in new_filter.permissions else False
    redirect = True if 'r' in new_filter.permissions else False
    if not new_filter.exists:
        if verbosity:
            print(f'Error: filter "{filter_id}" does not exists')
        db.close()
        sys.exit(1)
    elif not new_filter.subscribing:
        if verbosity:
            print(f'Error: not subscribing to filter "{filter_id}"')
        db.close()
        sys.exit(1)
    elif not force and not prompt_user(f'You are about to update filter: "{filter_id}" and its rules'):
        db.close()
        sys.exit()
    else:
        if verbosity:
            print(f':: Updating filter: {filter_id}')
            print(f' => Get source: {new_filter.source}')
        if is_url(new_filter.source):
            tmp_filter = os.path.join(tmp_dir, generate_tmp_filename())
            try:
                download_file(new_filter.source, tmp_filter)
            except (requests.exceptions.ConnectionError, urllib3.exceptions.MaxRetryError, ConnectionRefusedError,
                    urllib3.exceptions.NewConnectionError):
                if verbosity:
                    print(' => Failed to get source')
                    print(f' => Failed to update filter: {filter_id}')
                db.close()
                sys.exit(1)
        else:
            tmp_filter = new_filter.source
        if not os.path.isfile(tmp_filter):
            if verbosity:
                print(f'Error: file not found: "{new_filter.source}"')
            sys.exit(1)
        all_rules = None
        try:
            all_rules = get_rules_from_filter(tmp_filter, syntax=new_filter.metadata['syntax'],
                                              allow=allow, block=block, redirect=redirect, verbosity=verbosity)
        except InvalidFilterSyntax:
            if verbosity:
                print(f'Error: syntax of filter {filter_id} is not supported')
                sys.exit(1)
        if verbosity:
            print(' => Removing all previous filter rules ...', end='\r')
        Filter(filter_id, db).remove_all_rules()
        if verbosity:
            print(' => Removing all previous rules from filter: done')
        # Only remove local filter if filter has been downloaded, not if it is a local file
        if new_filter.source != tmp_filter:
            os.remove(tmp_filter)
        count = 1
        all_rules_count = len(all_rules.keys())
        cursor = db.cursor()
        all_rules_in_db = Rule.fetch_all_rules(db)
        for rule in all_rules:
            if verbosity:
                if count < len(all_rules.keys()):
                    print(f' => Adding new rules to database... ({count}/{all_rules_count})', end='\r')
                else:
                    print(f' => Added all new rules from filter into database ({count}/{all_rules_count})')
            if rule in all_rules_in_db and all_rules_in_db[rule]['priority']:
                pass
            elif all_rules[rule][0] == Policy.allow and allow or all_rules[rule][0] == Policy.block and block:
                if rule in all_rules_in_db:
                    if all_rules[rule][0] == Policy.block and all_rules_in_db[rule]['policy'] \
                            in [Policy.redirect, Policy.allow] or all_rules[rule][0] == Policy.redirect \
                            and all_rules_in_db[rule]['policy'] == Policy.allow:
                        print('yo')
                        continue
                    sql = 'UPDATE "rules" SET policy=?, filter_id=?, priority=? WHERE domain=?;'
                    params = (all_rules[rule][0], filter_id, False, rule)
                    cursor.execute(sql, params)
                else:
                    sql = 'INSERT INTO "rules" ("domain", "policy", "filter_id", "priority") VALUES (?, ?, ?, ?)'
                    params = (rule, all_rules[rule][0], filter_id, False)
                    cursor.execute(sql, params)
            elif all_rules[rule][0] == Policy.redirect and redirect:
                if rule in all_rules_in_db:
                    sql = 'UPDATE "rules" SET policy=?, filter_id=?, priority=?, ip=? WHERE domain=?;'
                    params = (all_rules[rule][0], filter_id, False, all_rules[rule][1], rule)
                    cursor.execute(sql, params)
                else:
                    sql = 'INSERT INTO "rules" ("domain", "policy", "filter_id", "priority", "ip") ' \
                          'VALUES (?, ?, ?, ?, ?)'
                    params = (rule, all_rules[rule][0], filter_id, False, all_rules[rule][1])
                    cursor.execute(sql, params)
            count += 1
        db.commit()
        db.close()


def update_all_filters(db_path: str, tmp_dir: str, verbosity: bool = True, force: bool = False) -> None:
    """Update all filters the user is subscribing to

    Args:
        db_path (str): The path to the SQLite database
        tmp_dir (str): The directory where to store temporary files
        verbosity (bool, optional): Enable verbosity (default)
        force (bool, optional): Do not prompt user for anything
    """
    db_path = os.path.realpath(db_path)
    if not os.path.isfile(db_path):
        if verbosity:
            print(f'Error: file not found: "{db_path}"')
        sys.exit(1)
    if force or prompt_user('You are about to update all filters and their rules'):
        db = sqlite3.connect(db_path)
        for filter_id in Filter.get_all_subscribing_filter(db):
            update_filter(filter_id, db_path, tmp_dir, verbosity, True)
        db.close()


def change_filter_permissions(filter_id: str, db_path: str, tmp_dir: str,
                              permissions: str, verbosity: bool = True, force: bool = False) -> None:
    """Change permissions of a filter

    Args:
        filter_id (str): The ID of the filter to subscribe to
        db_path (str): The path to the SQLite database
        tmp_dir (str): The directory where to store temporary files
        permissions (str, optional): Permissions of the filter (may contain one or more of these letters: 'abr')
        verbosity (bool, optional): Enable verbosity (default)
        force (bool, optional): Do not prompt user for anything
    """
    db_path = os.path.realpath(db_path)
    if not os.path.isfile(db_path):
        if verbosity:
            print(f'Error: file not found: "{db_path}"')
        sys.exit(1)
    db = sqlite3.connect(db_path)
    new_filter = Filter(filter_id, db)
    if not new_filter.exists:
        if verbosity:
            print(f'Error: filter "{filter_id}" does not exists')
        db.close()
        sys.exit(1)
    elif not new_filter.subscribing:
        if verbosity:
            print(f'Error: not subscribing to filter "{filter_id}"')
        db.close()
        sys.exit(1)
    elif not re.findall(re.compile(r'([abr])', re.IGNORECASE), permissions) and permissions is not None:
        if verbosity:
            print(f'Error: "{permissions}" is not a valid permission')
        db.close()
        sys.exit(1)
    else:
        if force or prompt_user(f'You are about to change permissions of filter: "{filter_id}"'):
            new_filter.change_permissions(permissions)
            db.close()
            update_filter(filter_id, db_path, tmp_dir, verbosity, force=True)
        else:
            db.close()


def update_remote_repo(repo_url: str, repo_mirror: list, version_file: str,
                       db_path: str, tmp_dir: str, verbosity: bool = True, force: bool = False) -> None:
    """Update remote filters repository

    Args:
        repo_url (str): The URL of the remote repo index
        repo_mirror (list): The URLs of the remote repo index mirrors, in case main index is inaccessible
        version_file (str): The path to the file that contains local version info
        db_path (str): The path to the SQLite database
        tmp_dir (str): The directory where to store temporary files
        verbosity (bool, optional): Enable verbosity (default)
        force (bool, optional): Do not prompt user for anything
    """
    db_path = os.path.realpath(db_path)
    if not os.path.isfile(db_path):
        if verbosity:
            print(f'Error: file not found: "{db_path}"')
        sys.exit(1)
    db = sqlite3.connect(db_path)
    tmp_index = os.path.join(tmp_dir, generate_tmp_filename())
    if force or prompt_user('You are about to update online filters repository'):
        pass
    else:
        db.close()
        sys.exit()
    if verbosity:
        print(':: Updating remote repository')
        print(f' => Get index: {repo_url}')
    try:
        download_file(repo_url, tmp_index)
    except (requests.exceptions.ConnectionError, urllib3.exceptions.MaxRetryError, ConnectionRefusedError,
            urllib3.exceptions.NewConnectionError):
        if verbosity:
            print(' => Failed to get index')
        for mirror in repo_mirror:
            try:
                if verbosity:
                    print(f' => Get mirror: {mirror}')
                download_file(mirror, tmp_index)
            except (requests.exceptions.ConnectionError, urllib3.exceptions.MaxRetryError, ConnectionRefusedError,
                    urllib3.exceptions.NewConnectionError):
                if verbosity:
                    print(f' => Failed to get mirror: {mirror}')
                if repo_mirror.index(mirror) == len(repo_mirror) - 1:
                    if verbosity:
                        print(' => Failed to update remote repository')
                    db.close()
                    sys.exit(1)
    try:
        data = ElementTree.parse(tmp_index).getroot()
    except ElementTree.ParseError:
        if verbosity:
            print(' => Repository seems invalid')
            print(' => Failed to update remote repository')
        db.close()
        sys.exit(1)
    if os.path.isfile(os.path.realpath(version_file)):
        with open(os.path.realpath(version_file), 'rt') as f:
            current_version = int(f.read())
    else:
        current_version = 0
    if data.tag == 'repository':
        if current_version == int(data.attrib['version']) and not force:
            if verbosity:
                print(' => Remote repository is up-to-date')
        else:
            if verbosity:
                print(f' => Upgrading repository version {data.attrib["version"]} over {str(current_version)}')
            with open(os.path.realpath(version_file), 'wt') as f:
                f.write(data.attrib["version"])
            all_filters = []
            count = 1
            for _filter in data:
                all_filters.append(_filter.attrib['id'])
            for _filter in data:
                if count < len(all_filters) and verbosity:
                    print(f' => Updating filters ({count}/{len(all_filters)})', end='\r')
                elif verbosity:
                    print(f' => Updating filters ({count}/{len(all_filters)})')
                metadata = {
                    "title": None,
                    "description": None,
                    "homepage": None,
                    "license": None,
                    "syntax": None
                }
                new_filter = Filter(_filter.attrib['id'], db)
                if new_filter.exists and new_filter.on_rfr:
                    source = new_filter.source
                else:
                    source = None
                for attr in _filter:
                    if attr.tag == 'title':
                        metadata['title'] = attr.text
                    elif attr.tag == 'desc':
                        metadata['description'] = attr.text
                    elif attr.tag == 'homepage':
                        metadata['homepage'] = attr.text
                    elif attr.tag == 'license':
                        metadata['license'] = attr.text
                    elif attr.tag == 'syntax':
                        metadata['syntax'] = attr.text
                    elif attr.tag == 'source':
                        source = attr.text
                if new_filter.exists and new_filter.on_rfr:
                    new_filter.update_from_rfr(source, metadata, True)
                elif not new_filter.exists:
                    new_filter.add_from_rfr(source, metadata)
                else:
                    pass
                count += 1
            db.commit()
            all_filters_in_db = Filter.get_all_rfr_filter(db)
            for filter_id in all_filters_in_db:
                if filter_id not in all_filters:
                    new_filter = Filter(filter_id, db)
                    if new_filter.subscribing:
                        new_filter.update_from_rfr(new_filter.source, new_filter.metadata, False)
                    else:
                        new_filter.delete()
            db.commit()
        db.close()
        os.remove(tmp_index)
    else:
        os.remove(tmp_index)
        db.close()
        if verbosity:
            print('Error: cannot update remote filters repository (cannot read index)')
        sys.exit(1)


def show_filter_info(filter_id: str, db_path: str, verbosity: bool = True) -> None:
    """Print information about a filter

    Args:
        filter_id (str): The ID of the filter to show info about
        db_path (str): The path to the SQLite database
        verbosity (bool, optional): Enable verbosity (default)
    """
    db_path = os.path.realpath(db_path)
    if not os.path.isfile(db_path):
        if verbosity:
            print(f'Error: file not found: "{db_path}"')
        sys.exit(1)
    db = sqlite3.connect(db_path)
    new_filter = Filter(filter_id, db)
    if not new_filter.exists:
        if verbosity:
            print(f'Error: filter "{filter_id}" does not exists')
        db.close()
        sys.exit(1)
    else:
        if new_filter.on_rfr:
            if new_filter.subscribing:
                print(
                    f'Filter ID:    {filter_id}\n'
                    f'Title:        {new_filter.metadata["title"]}\n'
                    f'Homepage:     {new_filter.metadata["homepage"]}\n'
                    f'License:      {new_filter.metadata["license"]}\n'
                    f'Syntax:       {new_filter.metadata["syntax"]}\n'
                    f'Type:         available on online repository\n'
                    f'Source:       {new_filter.source}\n'
                    f'Subscribing:  yes\n'
                    f'Permissions:  {new_filter.permissions}\n'
                    f'Total rules:  {new_filter.get_rules_count()}\n'
                    f'Description:  {new_filter.metadata["description"]}'
                )
            else:
                print(
                    f'Filter ID:    {filter_id}\n'
                    f'Title:        {new_filter.metadata["title"]}\n'
                    f'Homepage:     {new_filter.metadata["homepage"]}\n'
                    f'License:      {new_filter.metadata["license"]}\n'
                    f'Syntax:       {new_filter.metadata["syntax"]}\n'
                    f'Type:         available on online repository\n'
                    f'Source:       {new_filter.source}\n'
                    f'Subscribing:  no\n'
                    f'Description:  {new_filter.metadata["description"]}'
                )
        else:
            print(
                f'Filter ID:    {filter_id}\n'
                f'Type:         custom\n'
                f'Source:       {new_filter.source}\n'
                f'Subscribing:  yes\n'
                f'Permissions:  {new_filter.permissions}\n'
                f'Total rules:  {new_filter.get_rules_count()}\n'
            )


def list_filters(db_path: str, custom: bool, subscribed: bool, unsubscribed: bool, available: bool,
                 verbosity: bool = True) -> None:
    """Print a list of filters

    Args:
        db_path (str): The path to the SQLite database
        custom (bool): List only custom filters
        subscribed (bool): List only subscribed filters
        unsubscribed (bool): List only unsubscribed filters
        available (bool): List only filters available in remote repository
        verbosity (bool, optional): Enable verbosity (default)
    """
    db_path = os.path.realpath(db_path)
    if not os.path.isfile(db_path):
        if verbosity:
            print(f'Error: file not found: "{db_path}"')
        sys.exit(1)
    db = sqlite3.connect(db_path)
    if subscribed and unsubscribed:
        print('Error: no filter can be both subscribed and unsubscribed')
        db.close()
        sys.exit(1)
    elif custom and available:
        print('Error: no filter can be both custom and available on the online repository')
        db.close()
        sys.exit(1)
    elif unsubscribed and custom:
        print('Error: no filter can be both custom and unsubscribed')
        db.close()
        sys.exit(1)
    else:
        all_filters = Filter.fetch_all_filters(db)
        for filter_id in all_filters:
            if all_filters[filter_id]['on_rfr'] and available:
                if all_filters[filter_id]['subscribing'] and subscribed:
                    print(filter_id)
                elif not all_filters[filter_id]['subscribing'] and unsubscribed:
                    print(filter_id)
                elif not subscribed and not unsubscribed:
                    print(filter_id)
            elif not all_filters[filter_id]['on_rfr'] and custom:
                print(filter_id)
            elif all_filters[filter_id]['subscribing'] and subscribed:
                if all_filters[filter_id]['on_rfr'] and available:
                    print(filter_id)
                elif not all_filters[filter_id]['on_rfr'] and not available:
                    print(filter_id)
                elif not available and not custom:
                    print(filter_id)
            elif not all_filters[filter_id]['subscribing'] and unsubscribed:
                print(filter_id)
            elif not custom and not subscribed and not unsubscribed and not available:
                print(filter_id)
    db.close()
