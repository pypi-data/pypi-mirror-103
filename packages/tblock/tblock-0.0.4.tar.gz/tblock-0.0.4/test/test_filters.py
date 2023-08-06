__version__ = '1.0.0'

import sys
import subprocess
import requests
import urllib3
import sqlite3
import datetime
import os.path
import tblock
from tblock.config import setup_database
from tblock.core import Filter, Rule
from tblock.exceptions import UnknownFilterID, InvalidFilterPermissions, AlreadySubscribingToFilter, InvalidFilterID, \
    NotSubscribingToFilter
from tblock.filters import subscribe_to_filter, update_all_filters, change_filter_permissions, update_remote_repo
from time import sleep


def ping_dev_server() -> bool:
    try:
        requests.get("http://0.0.0.0:17213/sample_filter.txt")
    except (requests.exceptions.ConnectionError, urllib3.exceptions.MaxRetryError, ConnectionRefusedError,
            urllib3.exceptions.NewConnectionError):
        return False
    else:
        return True


logfile = open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'TESTS.log'), 'at')
tmp_dir = os.path.join(os.path.dirname(__file__), 'tmp/')
repo_version_file = os.path.join(os.path.dirname(__file__), 'srv', 'repo')

with open(repo_version_file, 'wt') as f:
    f.write("0")

try:
    os.mkdir(tmp_dir)
except FileExistsError:
    pass

msg = f'''\n------------- TEST_FILTERS.PY -------------\n
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

new_filter = Filter("test1", conn, commit=True)

if new_filter.exists:
    msg = f'[{datetime.datetime.now()}] ERROR: please run "make clean" and test again after that'
    print(msg)
    logfile.write(msg + "\n")
    sys.exit(1)
else:
    msg = f'[{datetime.datetime.now()}] SUCCESS: initialized database: {test_db}'
    print(msg)
    logfile.write(msg + "\n")

try:
    new_filter.subscribe("b")
except UnknownFilterID:
    msg = f'[{datetime.datetime.now()}] SUCCESS: exception #1 was successful (UnknownFilterID)'
    print(msg)
    logfile.write(msg + "\n")
else:
    msg = f'[{datetime.datetime.now()}] FAILED: exception #1 was not successful (UnknownFilterID)'
    print(msg)
    logfile.write(msg + "\n")
    sys.exit(1)

try:
    new_filter.subscribe("k", "https://example.com")
except InvalidFilterPermissions:
    msg = f'[{datetime.datetime.now()}] SUCCESS: exception #2 was successful (InvalidFilterPermissions)'
    print(msg)
    logfile.write(msg + "\n")
else:
    msg = f'[{datetime.datetime.now()}] FAILED: exception #2 was not successful (InvalidFilterPermissions)'
    print(msg)
    logfile.write(msg + "\n")
    sys.exit(1)

new_filter.subscribe("b", "https://example.com")

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
    new_filter.subscribe("a")
except AlreadySubscribingToFilter:
    msg = f'[{datetime.datetime.now()}] SUCCESS: exception #3 was successful (AlreadySubscribingToFilter)'
    print(msg)
    logfile.write(msg + "\n")
else:
    msg = f'[{datetime.datetime.now()}] FAILED: exception #3 was not successful (AlreadySubscribingToFilter)'
    print(msg)
    logfile.write(msg + "\n")
    sys.exit(1)

try:
    new_filter.add_from_rfr("https://example.org", new_filter.metadata)
except InvalidFilterID:
    msg = f'[{datetime.datetime.now()}] SUCCESS: exception #4 was successful (InvalidFilterID)'
    print(msg)
    logfile.write(msg + "\n")
else:
    msg = f'[{datetime.datetime.now()}] FAILED: exception #4 was not successful (InvalidFilterID)'
    print(msg)
    logfile.write(msg + "\n")
    sys.exit(1)

try:
    new_filter.update_from_rfr("https://example.org", new_filter.metadata)
except InvalidFilterID:
    msg = f'[{datetime.datetime.now()}] SUCCESS: exception #5 was successful (InvalidFilterID)'
    print(msg)
    logfile.write(msg + "\n")
else:
    msg = f'[{datetime.datetime.now()}] FAILED: exception #5 was not successful (InvalidFilterID)'
    print(msg)
    logfile.write(msg + "\n")
    sys.exit(1)

new_filter.unsubscribe()

if new_filter.exists:
    msg = f'[{datetime.datetime.now()}] ERROR: an unknown error occurred when trying to unsubscribe custom filter'
    print(msg)
    logfile.write(msg + "\n")
    sys.exit(1)
else:
    msg = f'[{datetime.datetime.now()}] SUCCESS: unsubscribed from custom filter'
    print(msg)
    logfile.write(msg + "\n")

new_filter.add_from_rfr("https://example.org", new_filter.metadata)

if not new_filter.exists:
    msg = f'[{datetime.datetime.now()}] ERROR: an unknown error occurred, cannot add remote repo filters to database'
    print(msg)
    logfile.write(msg + "\n")
    sys.exit(1)
else:
    msg = f'[{datetime.datetime.now()}] SUCCESS: add remote repo filter to database'
    print(msg)
    logfile.write(msg + "\n")

try:
    new_filter.subscribe("ab", "https://example.com")
except InvalidFilterID:
    msg = f'[{datetime.datetime.now()}] SUCCESS: exception #6 was successful (InvalidFilterID)'
    print(msg)
    logfile.write(msg + "\n")
else:
    msg = f'[{datetime.datetime.now()}] FAILED: exception #6 was not successful (InvalidFilterID)'
    print(msg)
    logfile.write(msg + "\n")
    sys.exit(1)

try:
    new_filter.unsubscribe()
except NotSubscribingToFilter:
    msg = f'[{datetime.datetime.now()}] SUCCESS: exception #7 was successful (NotSubscribingToFilter)'
    print(msg)
    logfile.write(msg + "\n")
else:
    msg = f'[{datetime.datetime.now()}] FAILED: exception #7 was not successful (NotSubscribingToFilter)'
    print(msg)
    logfile.write(msg + "\n")
    sys.exit(1)

new_filter.subscribe("ab")

if not new_filter.subscribing:
    msg = f'[{datetime.datetime.now()}] ERROR: an unknown error occurred, cannot subscribe to remote repo filters'
    print(msg)
    logfile.write(msg + "\n")
    sys.exit(1)
else:
    msg = f'[{datetime.datetime.now()}] SUCCESS: subscribed to remote repo filter'
    print(msg)
    logfile.write(msg + "\n")

new_filter.unsubscribe()

if not new_filter.exists:
    msg = f'[{datetime.datetime.now()}] ERROR: an unknown error occurred when trying to unsubscribe remote repo filter'
    print(msg)
    logfile.write(msg + "\n")
    sys.exit(1)
else:
    msg = f'[{datetime.datetime.now()}] SUCCESS: unsubscribed from remote repo filter'
    print(msg)
    logfile.write(msg + "\n")

new_filter.update_from_rfr("https://example.org", new_filter.metadata)

if new_filter.source != "https://example.org":
    msg = f'[{datetime.datetime.now()}] ERROR: an unknown error occurred when trying to update remote repo filter'
    print(msg)
    logfile.write(msg + "\n")
    sys.exit(1)
else:
    msg = f'[{datetime.datetime.now()}] SUCCESS: updated remote repo filter'
    print(msg)
    logfile.write(msg + "\n")

new_filter.subscribe("b")
new_filter.change_permissions("a")

if not new_filter.permissions == "a":
    msg = f'[{datetime.datetime.now()}] ERROR: an unknown error occurred when trying to change filter permissions'
    print(msg)
    logfile.write(msg + "\n")
    sys.exit(1)
else:
    msg = f'[{datetime.datetime.now()}] SUCCESS: changed filter permissions'
    print(msg)
    logfile.write(msg + "\n")

try:
    Filter("test3", conn).subscribe("b", "https://example.org")
except AlreadySubscribingToFilter:
    msg = f'[{datetime.datetime.now()}] SUCCESS: exception #8 was successful (AlreadySubscribingToFilter)'
    print(msg)
    logfile.write(msg + "\n")
else:
    msg = f'[{datetime.datetime.now()}] FAILED: exception #8 was not successful (AlreadySubscribingToFilter)'
    print(msg)
    logfile.write(msg + "\n")
    sys.exit(1)

msg = f'[{datetime.datetime.now()}] INFO: starting test for filters.py ...'
print(msg)
logfile.write(msg + "\n")

msg = f'[{datetime.datetime.now()}] INFO: starting development server on port 17213 ...'
print(msg)
logfile.write(msg + "\n")

prc = subprocess.Popen(["python", "-m", "http.server", "--bind", "0.0.0.0", "--directory",
                        os.path.join(os.path.dirname(__file__), "srv"), "17213"],
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)

count = 0

while not ping_dev_server():
    if count < 100:
        sleep(0.1)
        count += 1
    else:
        msg = f'[{datetime.datetime.now()}] FAILED: cannot start development server on port 17213'
        print(msg)
        logfile.write(msg + "\n")
        sys.exit(1)
else:
    msg = f'[{datetime.datetime.now()}] SUCCESS: started development server on port 17213 (PID: {prc.pid})'
    print(msg)
    logfile.write(msg + "\n")

subscribe_to_filter("test2", test_db, tmp_dir, "b", "http://0.0.0.0:17213/sample_filter.txt", False, True)

if not Filter("test2", conn).exists:
    msg = f'[{datetime.datetime.now()}] ERROR: custom filter not added to database'
    print(msg)
    logfile.write(msg + "\n")
    sys.exit(1)
else:
    msg = f'[{datetime.datetime.now()}] SUCCESS: custom filter added to database'
    print(msg)
    logfile.write(msg + "\n")

if not Rule("apx.moatads.com", conn).exists or Rule("apx.moatads.com", conn).policy != "block":
    msg = f'[{datetime.datetime.now()}] ERROR: filter blocking rules not added to database'
    print(msg)
    logfile.write(msg + "\n")
    sys.exit(1)
else:
    msg = f'[{datetime.datetime.now()}] SUCCESS: added filter blocking rules to database'
    print(msg)
    logfile.write(msg + "\n")

if Rule("tblock.codeberg.page", conn).exists:
    msg = f'[{datetime.datetime.now()}] ERROR: filter was not allowed to add allowing rules but it did'
    print(msg)
    logfile.write(msg + "\n")
    sys.exit(1)
else:
    msg = f'[{datetime.datetime.now()}] SUCCESS: allowing rule was not added as filter was not allowed to do it'
    print(msg)
    logfile.write(msg + "\n")

if len(Rule.fetch_all_rules(conn)) != 213:
    msg = f'[{datetime.datetime.now()}] ERROR: some rules were not added or some invalid rules were added to database'
    print(msg)
    logfile.write(msg + "\n")
    sys.exit(1)
else:
    msg = f'[{datetime.datetime.now()}] SUCCESS: all valid rules were added to database'
    print(msg)
    logfile.write(msg + "\n")

Filter("test2", conn).remove_all_rules()

if len(Rule.fetch_all_rules(conn)) != 0:
    msg = f'[{datetime.datetime.now()}] ERROR: some rules were not deleted from database'
    print(msg)
    logfile.write(msg + "\n")
    sys.exit(1)
else:
    msg = f'[{datetime.datetime.now()}] SUCCESS: all rules were deleted from database'
    print(msg)
    logfile.write(msg + "\n")

Filter("test1", conn).unsubscribe()

update_all_filters(test_db, tmp_dir, False, True)

if len(Rule.fetch_all_rules(conn)) != 213:
    msg = f'[{datetime.datetime.now()}] ERROR: cannot update all filters'
    print(msg)
    logfile.write(msg + "\n")
    sys.exit(1)
else:
    msg = f'[{datetime.datetime.now()}] SUCCESS: all filters successfully updated'
    print(msg)
    logfile.write(msg + "\n")

change_filter_permissions("test2", test_db, tmp_dir, "a", False, True)

if Filter("test2", conn).permissions != "a" or len(Rule.fetch_all_rules(conn)) != 1:
    msg = f'[{datetime.datetime.now()}] ERROR: cannot change filter policy'
    print(msg)
    logfile.write(msg + "\n")
    sys.exit(1)
else:
    msg = f'[{datetime.datetime.now()}] SUCCESS: changed filter policy'
    print(msg)
    logfile.write(msg + "\n")

new_filter = Filter("false-test", conn)
new_filter.add_from_rfr("https://example1.com", new_filter.metadata)

update_remote_repo("http://0.0.0.0:17212/index.xml", ["http://0.0.0.0:17213/index.xml"],
                   repo_version_file, test_db, tmp_dir, False, True)

if "test32" not in Filter.get_all_rfr_filter(conn) or "false-test" in Filter.get_all_rfr_filter(conn):
    msg = f'[{datetime.datetime.now()}] ERROR: cannot update remote repository\n' \
          f'[{datetime.datetime.now()}] ERROR: mirror is not working'
    print(msg)
    logfile.write(msg + "\n")
    sys.exit(1)
else:
    msg = f'[{datetime.datetime.now()}] SUCCESS: updated remote repository\n' \
          f'[{datetime.datetime.now()}] SUCCESS: mirror is working'
    print(msg)
    logfile.write(msg + "\n")

subscribe_to_filter('test41', test_db, tmp_dir, 'b', 'http://0.0.0.0:17213/test41', verbosity=False, force=True)

if Rule('tblock.codeberg.page', conn).policy == 'block':
    msg = f'[{datetime.datetime.now()}] ERROR: allowing policy was overwritten by blocking policy'
    print(msg)
    logfile.write(msg + "\n")
    sys.exit(1)
else:
    msg = f'[{datetime.datetime.now()}] SUCCESS: allowing policy was not overwritten by blocking policy'
    print(msg)
    logfile.write(msg + "\n")

if not Rule('www.thisisatest.com', conn).exists:
    msg = f'[{datetime.datetime.now()}] ERROR: a rule was ignored'
    print(msg)
    logfile.write(msg + "\n")
    sys.exit(1)
else:
    msg = f'[{datetime.datetime.now()}] SUCCESS: no rule was ignored'
    print(msg)
    logfile.write(msg + "\n")

msg = f'[{datetime.datetime.now()}] INFO: stopping development server (PID: {prc.pid}) ...'
print(msg)
logfile.write(msg + "\n")
prc.kill()

count = 0

while ping_dev_server():
    if count < 100:
        sleep(0.1)
        count += 1
    else:
        msg = f'[{datetime.datetime.now()}] FAILED: development server not stopped (PID: {prc.pid}), kill it manually'
        print(msg)
        logfile.write(msg + "\n")
else:
    msg = f'[{datetime.datetime.now()}] SUCCESS: development server stopped'
    print(msg)
    logfile.write(msg + "\n")

msg = '\n----------- END OF CURRENT TEST -----------\n'
conn.close()
logfile.write(msg + "\n")
logfile.close()
os.remove(repo_version_file)
os.rmdir(tmp_dir)
