#!/bin/bash
#
# gitwait - watch file and git commit all changes as they happen
#

while true; do

  inotifywait -e CLOSE_WRITE ~/finances/demo/db.sqlite3 2>&1

  cd ~/finances; git commit -a -m 'autocommit on change to DB file'; git push origin db_update_branch

done
