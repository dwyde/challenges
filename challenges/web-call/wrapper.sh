#!/bin/sh

#
# A wrapper script for socat
# 
# Run like:
#   socat tcp-l:7777,reuseaddr,fork system:'./wrapper.sh',nofork
#

# CPU time
ulimit -t 1

# Memory (KB)
ulimit -m 300000

# Open files
ulimit -n 100

# File size (blocks)
ulimit -f 1024

node call.js "$1"

