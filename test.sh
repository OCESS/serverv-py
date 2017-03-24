#!/bin/sh
# Test that running server.py makes no changes to RND files,
# except TIME.RND

TMPDIR="`mktemp -dp .`"

trap "rm -rf $TMPDIR; exit 1" EXIT HUP INT TERM

cp -r orbit-files/* "$TMPDIR"

RETVAL=0

timeout --signal=TERM 3 ./serverv-py/server.py --sevpath "$TMPDIR/sevpath.RND"

for f in `find orbit-files -type f -printf '%P\n'`; do
  if [ "`basename $f`" != 'TIME.RND' ]; then
    diff "orbit-files/$f" "$TMPDIR/$f"
    [ $? -eq 0 ] || RETVAL=$?
  fi
done

exit $RETVAL
