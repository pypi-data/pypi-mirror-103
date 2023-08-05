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

__version__ = '0.0.3'

run_help = '''TBlock - An anticapitalist ad-blocker that uses the hosts file
Copyright (c) 2021 Twann <twann@ctemplar.com>

usage: tblock <operation> <options>

<operations>
* General
  -h  --help                              Show this help page
  -s  --status                            Show status information
  -v  --version                           Show version information
* Rules
  -a  --allow        [domain]             Allow a domain
  -b  --block        [domain]             Block a domain
  -r  --redirect     [domain]  [ip]       Redirect a domain to another address
  -d  --delete-rule  [domain]             Delete a rule for a domain
  -l  --list-rules   <options>            List active rules
* Filters
  -S  --subscribe    <options> [filter]   Subscribe to a new filter
  -R  --remove       <options> [filter]   Remove a filter (unsubscribe)
  -U  --update       <options> [filter]   Update a filter
  -M  --mod          {a|b|r}   [filter]   Change permissions of a filter
  -I  --info         [filter]             Show information about a filter
  -L  --list         <options>            List all filters
  -Y  --sync                              Update remote filters repository
* Hosts
  -H  --update-hosts                      Update hosts file
  -D  --restore                           Restore default hosts file

<options>
* General
  -f  --force                             Do not prompt user for anything
* Rules
  -s  --standard     [filter]             Only show standard rules
  -u  --user                              Only show user rules
* Filters
  -c  --custom       [file/url]           Subscribe to a custom filter
  -y  --sync                              Update remote filters repository
  -m  --mod          {a|b|r}              Configure filter permissions when subscribing
  -c  --custom                            List only custom filters
  -s  --subscribed                        List only subscribed filters
  -n  --unsubscribed                      List only unsubscribed filters
  -w  --available                         List only filters available in remote repository

For more information, see tblock(1)'''

run_converter_help = '''TBlockc - TBlock's built-in filter converter
Copyright (c) 2021 Twann <twann@ctemplar.com>

usage: tblockc <options> {-s|--syntax} [syntax] [file] [output_file]

<options>
* General
  -h  --help                              Show this help page
  -f  --force                             Do not prompt user for anything
  -v  --version                           Show version information
* Converting
  -r  --rules        {a|b|r}              Choose which policies to allow during converting
  -c  --comments                          Also convert comments
  -o  --original     <syntax>             Specify the original syntax of the filter to convert
  -s  --syntax       <syntax>             Specify the new syntax to use (required)
* Other
  -g  --get-syntax   [file]               Scan a filter to get its syntax

<syntax>
  adblockplus                             AdBlock Plus syntax
  hosts                                   Hosts file format
  dnsmasq                                 dnsmasq.conf syntax
  list                                    Simple domain blacklist
  tblock                                  TBlock filter syntax
  opera                                   Opera filter syntax

For more information, see tblockc(1)'''
