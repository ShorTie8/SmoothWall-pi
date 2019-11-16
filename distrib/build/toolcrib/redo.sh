#! /bin/bash

# Preliminaries
    death=0;
    if [ `basename $PWD` != 'build' ]; then
        tput smso;
        echo "Can't redo; you must be in the build directory";
        tput rmso;
        death=1;
    fi;
    if [ $# -eq 0 -o `basename $PWD` != "build" ]; then
        echo "Usage: redo package [ package ... ]";
        echo "  Example: redo whois noip";
        echo "You must be in the build directory to redo.";
        death=1;
    fi;
    if [ $death -ne 0 ]; then
        return 1;
    fi;

# We seem to have valid args and are in the build dir, so prepare
# each pkg and group to be rebuilt
    while [ $# -gt 0 ]; do
        # Remove each pkg's built flag
        pkg=${1/+/\\+};
        rm -f sources/${1}/Final.built;

        # Remove the respective 'group built' flag
        egrep -i "build ${pkg} |build ${pkg}$|-e.*grp" toolcrib/make_final | while read a b c d e; do
            if [ "$a" == "if" ]; then
                GRP=`echo $d | sed -e 's/.*grp//' -e 's/\.compiled.*//'`;
            else
                rm -f crumbs/Final.grp${GRP}.compiled;
                break;
            fi;
        done;
        shift;
    done;

# And remove the 'all built' flag
    rm -f crumbs/Final.compiled crumbs/Final.built;

# Now rebuild those pkgs.
    make build
