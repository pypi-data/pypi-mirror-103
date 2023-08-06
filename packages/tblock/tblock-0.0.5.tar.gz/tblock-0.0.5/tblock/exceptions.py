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
# This module contains all exceptions for TBlock, and does not have any dependencies                                   #
########################################################################################################################


class TBlockError(IOError):
    def __init__(self, *args):
        super(TBlockError, self).__init__(*args)


class UnknownFilterID(TBlockError):
    def __init__(self, *args):
        super(UnknownFilterID, self).__init__(*args)


class AlreadySubscribingToFilter(TBlockError):
    def __init__(self, *args):
        super(AlreadySubscribingToFilter, self).__init__(*args)


class NotSubscribingToFilter(TBlockError):
    def __init__(self, *args):
        super(NotSubscribingToFilter, self).__init__(*args)


class InvalidFilterSource(TBlockError):
    def __init__(self, *args):
        super(InvalidFilterSource, self).__init__(*args)


class InvalidFilterID(TBlockError):
    def __init__(self, *args):
        super(InvalidFilterID, self).__init__(*args)


class InvalidFilterPermissions(TBlockError):
    def __init__(self, *args):
        super(InvalidFilterPermissions, self).__init__(*args)


class FilterPermissionsError(TBlockError):
    def __init__(self, *args):
        super(FilterPermissionsError, self).__init__(*args)


class InvalidFilterSyntax(TBlockError):
    def __init__(self, *args):
        super(InvalidFilterSyntax, self).__init__(*args)


class InvalidRulePolicy(TBlockError):
    def __init__(self, *args):
        super(InvalidRulePolicy, self).__init__(*args)


class InvalidAddress(TBlockError):
    def __init__(self, *args):
        super(InvalidAddress, self).__init__(*args)


class RulePriorityError(TBlockError):
    def __init__(self, *args):
        super(RulePriorityError, self).__init__(*args)


class RuleExist(TBlockError):
    def __init__(self, *args):
        super(RuleExist, self).__init__(*args)


class RuleNotExist(TBlockError):
    def __init__(self, *args):
        super(RuleNotExist, self).__init__(*args)
