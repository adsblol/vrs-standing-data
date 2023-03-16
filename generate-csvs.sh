#!/bin/bash
set -ex
TMPDIR=$(mktemp -d)
GITREPO=$(mktemp -d)
THIS_DIR=$(dirname $0)
git clone --depth=1 https://github.com/vradarserver/standing-data $GITREPO


# routes

for file in $(find $GITREPO/routes -name '*.csv'); do
    # Remove the first line
    cat $file | tail -n +2 >> $TMPDIR/routes.csv
    # If ROUTE_HEADER is not set,
    if [ -z "$ROUTE_HEADER" ]; then
        # Set it to the first line
        ROUTE_HEADER=$(head -n 1 $file)
    fi
done
# Add the header to the top of the file
echo $ROUTE_HEADER > $TMPDIR/header-routes.csv
cat $TMPDIR/routes.csv >> $TMPDIR/header-routes.csv
mv $TMPDIR/header-routes.csv $TMPDIR/routes.csv

# airports

for file in $(find $GITREPO/airports -name '*.csv'); do
    # Remove the first line
    cat $file | tail -n +2 >> $TMPDIR/airports.csv
    # If AIRPORT_HEADER is not set,
    if [ -z "$AIRPORT_HEADER" ]; then
        # Set it to the first line
        AIRPORT_HEADER=$(head -n 1 $file)
    fi
done
# Add the header to the top of the file
echo $AIRPORT_HEADER > $TMPDIR/header-airports.csv
cat $TMPDIR/airports.csv >> $TMPDIR/header-airports.csv
mv $TMPDIR/header-airports.csv $TMPDIR/airports.csv

mv $TMPDIR/routes.csv $THIS_DIR/routes.csv
mv $TMPDIR/airports.csv $THIS_DIR/airports.csv
