#!/bin/sh
# Test that running server.py makes no changes to RND files,
# except TIME.RND

TMPDIR="`mktemp -dp .`"
cp -r orbit-files/* "$TMPDIR"

RETVAL=0

./serverv-py/server.py --sevpath "$TMPDIR/sevpath.RND"

for f in `find orbit-files -type f -printf '%P\n'`; do
  if [ "`basename $f`" != 'TIME.RND' ]; then
    diff "orbit-files/$f" "$TMPDIR/$f"
    [ $? -eq 0 ] || RETVAL=$?
  fi
done

rm -rf "$TMPDIR"
exit $RETVAL
