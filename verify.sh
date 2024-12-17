#!/bin/bash

# Build Time Autovars
SCRIPT=`realpath "$0"`
SCRIPT_DIR=`dirname "$SCRIPT"`
PROJECT_ROOT=$SCRIPT_DIR

cd $PROJECT_ROOT
time stdbuf -i0 -o0 -e0 python3 -u verify.py 2>&1| tee verify.log