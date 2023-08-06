__version__ = '1.0.0'

import sys
import sqlite3
import datetime
import os.path
import tblock
from tblock.config import setup_database
from tblock.core import Rule, Filter, Policy, UserRule
from tblock.exceptions import InvalidRulePolicy, NotSubscribingToFilter, RulePriorityError, FilterPermissionsError, \
    RuleExist
from tblock.rules import add_user_rule, delete_user_rule

logfile = open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'TESTS.log'), 'at')

msg = f'''\n-------------- TEST_RULES.PY --------------\n
TBlock version {tblock.__version__}\nTest script version {__version__}\n'''
logfile.write(msg + "\n")

test_db = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'tblock_test.db')
if os.path.isfile(test_db):
    os.remove(test_db)
setup_database(test_db)
conn = sqlite3.connect(test_db)

msg = f'[{datetime.datetime.now()}] INFO: starting test for core.py ...'
print(msg)
logfile.write(msg + "\n")

new_rule = Rule("example.com", conn)

if Filter("test1", conn).exists:
    msg = f'[{datetime.datetime.now()}] ERROR: please run "make clean" and test again after that'
    print(msg)
    logfile.write(msg + "\n")
    sys.exit(1)
else:
    msg = f'[{datetime.datetime.now()}] SUCCESS: initialized database: {test_db}'
    print(msg)
    logfile.write(msg + "\n")

try:
    new_rule.add("invalid_policy", "test1", False)
except InvalidRulePolicy:
    msg = f'[{datetime.datetime.now()}] SUCCESS: exception #1 was successful (InvalidRulePolicy)'
    print(msg)
    logfile.write(msg + "\n")
else:
    msg = f'[{datetime.datetime.now()}] FAILED: exception #1 was not successful (InvalidRulePolicy)'
    print(msg)
    logfile.write(msg + "\n")
    sys.exit(1)

try:
    new_rule.add(Policy.block, "test1", False)
except NotSubscribingToFilter:
    msg = f'[{datetime.datetime.now()}] SUCCESS: exception #2 was successful (NotSubscribingToFilter)'
    print(msg)
    logfile.write(msg + "\n")
else:
    msg = f'[{datetime.datetime.now()}] FAILED: exception #2 was not successful (NotSubscribingToFilter)'
    print(msg)
    logfile.write(msg + "\n")
    sys.exit(1)

try:
    new_rule.add(Policy.block, UserRule, False)
except RulePriorityError:
    msg = f'[{datetime.datetime.now()}] SUCCESS: exception #3 was successful (RulePriorityError)'
    print(msg)
    logfile.write(msg + "\n")
else:
    msg = f'[{datetime.datetime.now()}] FAILED: exception #3 was not successful (RulePriorityError)'
    print(msg)
    logfile.write(msg + "\n")
    sys.exit(1)

new_filter = Filter("test1", conn)
new_filter.subscribe("b", "https://example.org")

if not new_filter.exists:
    msg = f'[{datetime.datetime.now()}] ERROR: an unknown error occurred, cannot add custom filters to database'
    print(msg)
    logfile.write(msg + "\n")
    sys.exit(1)
else:
    msg = f'[{datetime.datetime.now()}] SUCCESS: added custom filter to database'
    print(msg)
    logfile.write(msg + "\n")

try:
    new_rule.add(Policy.block, "test1", True)
except RulePriorityError:
    msg = f'[{datetime.datetime.now()}] SUCCESS: exception #4 was successful (RulePriorityError)'
    print(msg)
    logfile.write(msg + "\n")
else:
    msg = f'[{datetime.datetime.now()}] FAILED: exception #4 was not successful (RulePriorityError)'
    print(msg)
    logfile.write(msg + "\n")
    sys.exit(1)

try:
    new_rule.add(Policy.allow, "test1", False)
except FilterPermissionsError:
    msg = f'[{datetime.datetime.now()}] SUCCESS: exception #5 was successful (FilterPermissionsError)'
    print(msg)
    logfile.write(msg + "\n")
else:
    msg = f'[{datetime.datetime.now()}] FAILED: exception #5 was not successful (FilterPermissionsError)'
    print(msg)
    logfile.write(msg + "\n")
    sys.exit(1)

new_rule.add(Policy.block, UserRule, True)

if not new_rule.exists:
    msg = f'[{datetime.datetime.now()}] ERROR: an unknown error occurred, cannot add user rules to database'
    print(msg)
    logfile.write(msg + "\n")
    sys.exit(1)
else:
    msg = f'[{datetime.datetime.now()}] SUCCESS: added user rule to database'
    print(msg)
    logfile.write(msg + "\n")

try:
    new_rule.add(Policy.block, "test1", False)
except RuleExist:
    msg = f'[{datetime.datetime.now()}] SUCCESS: exception #6 was successful (RuleExist)'
    print(msg)
    logfile.write(msg + "\n")
else:
    msg = f'[{datetime.datetime.now()}] FAILED: exception #6 was not successful (RuleExist)'
    print(msg)
    logfile.write(msg + "\n")
    sys.exit(1)

try:
    new_rule.update(Policy.block, "test1", False)
except RulePriorityError:
    msg = f'[{datetime.datetime.now()}] SUCCESS: exception #7 was successful (RulePriorityError)'
    print(msg)
    logfile.write(msg + "\n")
else:
    msg = f'[{datetime.datetime.now()}] FAILED: exception #7 was not successful (RulePriorityError)'
    print(msg)
    logfile.write(msg + "\n")
    sys.exit(1)

new_rule.delete()
if new_rule.exists:
    msg = f'[{datetime.datetime.now()}] ERROR: an unknown error occurred, cannot delete user rules from database'
    print(msg)
    logfile.write(msg + "\n")
    sys.exit(1)
else:
    msg = f'[{datetime.datetime.now()}] SUCCESS: deleted user rule from database'
    print(msg)
    logfile.write(msg + "\n")

msg = f'[{datetime.datetime.now()}] INFO: starting test for rules.py ...'
print(msg)
logfile.write(msg + "\n")

add_user_rule("example-domain.com", "block", test_db, verbosity=False, force=True)

if not Rule("example-domain.com", conn).exists:
    msg = f'[{datetime.datetime.now()}] ERROR: an unknown error occurred, cannot add user rules into database'
    print(msg)
    logfile.write(msg + "\n")
    sys.exit(1)
else:
    msg = f'[{datetime.datetime.now()}] SUCCESS: added user rule into database'
    print(msg)
    logfile.write(msg + "\n")

add_user_rule("example-domain.com", "allow", test_db, verbosity=False, force=True)

if not Rule("example-domain.com", conn).exists or Rule("example-domain.com", conn).policy != "allow":
    msg = f'[{datetime.datetime.now()}] ERROR: an unknown error occurred, cannot update user rules in database'
    print(msg)
    logfile.write(msg + "\n")
    sys.exit(1)
else:
    msg = f'[{datetime.datetime.now()}] SUCCESS: updated user rule in database'
    print(msg)
    logfile.write(msg + "\n")

delete_user_rule("example-domain.com", test_db, False, True)

if Rule("example-domain.com", conn).exists:
    msg = f'[{datetime.datetime.now()}] ERROR: an unknown error occurred, cannot delete user rules from database'
    print(msg)
    logfile.write(msg + "\n")
    sys.exit(1)
else:
    msg = f'[{datetime.datetime.now()}] SUCCESS: deleted user rule from database'
    print(msg)
    logfile.write(msg + "\n")

msg = '\n----------- END OF CURRENT TEST -----------\n'
logfile.write(msg + "\n")
logfile.close()
conn.close()
