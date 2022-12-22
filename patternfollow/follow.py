#!/usr/bin/env python3

#import subprocess
import os
import time

INPUT="/var/log/odoo/odoo-server.log"

# Based on : https://medium.com/@aliasav/how-follow-a-file-in-python-tail-f-in-python-bca026a901cf

FOLLOW_SLEEP_TIME = 0.1 # [s]
def follow(infile):
    '''
    Follow a file ; Emulating tail -f
    '''
    infile.seek(0, os.SEEK_END)
    while True:
        try:
            line = infile.readline()
            if not line:
                time.sleep(FOLLOW_SLEEP_TIME)
                continue
            yield line
        except KeyboardInterrupt as ki: # Normal behavior in this context.
            break;

def prefollow(infile,numlines=10):
    '''
    Read the last numlines of infile before following:
    '''
    lastlines = []
    while True:
        line = infile.readline()
        if not line:
            break
        if numlines:
            lastlines.append(line)
            if len(lastlines) >= numlines:
                del lastlines[0]
        else:
            yield line
    if numlines:
        yield from lastlines

def linegen(filename, numlines=10):
    '''
    '''
    with open(filename) as mfile:
        yield from prefollow(mfile,numlines=numlines)
        yield from follow(mfile)

if __name__ == '__main__':
    for l in linegen(INPUT,10):
        print(l.rstrip('\n'))
