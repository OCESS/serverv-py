#!/usr/bin/env bash
# Test that running server.py makes no changes to RND files,
# except TIME.RND

set -euo pipefail

RETVAL=0

# Make a temp directory to store what the .RND files were before testing.
TMPDIR="`mktemp -dp .`"
trap "rm -rf $TMPDIR; exit 1" EXIT HUP INT TERM

cp -r orbit-files/* "$TMPDIR"

# Run server.py.
timeout --preserve-status --signal=TERM 3 \
  ./serverv-py/server.py --sevpath "$TMPDIR/sevpath.RND"
RETVAL=$?

# Check if any .RND files, except TIME.RND, changed during execution.
for f in `find orbit-files -type f -printf '%P\n'`; do
  if [[ "`basename $f`" != 'TIME.RND' ]]; then
    diff "orbit-files/$f" "$TMPDIR/$f"
    diffresult=$?
    echo $diffresult
    if [[ $diffresult -ne 0 ]]; then RETVAL=$diffresult; fi
  fi
done

exit $RETVAL
