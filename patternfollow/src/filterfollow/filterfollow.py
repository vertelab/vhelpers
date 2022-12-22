#!/usr/bin/env python3
'''
FilterFollow
'''
import os
import re
import sys
import time

import click

#%%
# Based on :
# https://medium.com/@aliasav/how-follow-a-file-in-python-tail-f-in-python-bca026a901cf

class FilterFollow():
    '''
    '''
    def __init__(self, startpattern, endpattern=None, filename=None,
                 matchingonly=False, includestarting=False, includeclosing=False,
                 lines=None, follow=False):
        '''
        FilterFollow parses a file for input patterns and returns matching rows.
        By default rows between start and end patterns are returned.

        Parameters
        ==========
        startpattern : str
            Start regex pattern

        '''
        self.filename = filename # File to read from. stdin if not set.
        self.startpattern =  re.compile(startpattern) # Default
        self.endpattern = re.compile(endpattern) if endpattern else None

        self.readline = False   # Wether or not to return the readline.
                                # Not applicable if endpattern is false.
        self.matchingonly = matchingonly        # Include only matching lines.
        self.includeclosing = includeclosing    # Include the closing line after
                                                # a read.
        self.includestarting = includestarting

        self.follow_file = True if not startpattern else follow
        self.follow_sleep_time = 0.1
        self.numlines = lines # Nbr of lines to try collect from the file.

    def run(self,numlines=None):
        '''
        Generator returning rows from input according to how the object was
        initialized.
        '''
        if numlines:
            self.numlines = numlines
        if self.filename:
            with open(self.filename) as mfile:
                yield from self.prefollow(mfile)
                if self.follow_file:
                    yield from self.follow(mfile)
        else:
            yield from self.prefollow(sys.stdin)
            if self.follow_file:
                yield from self.follow(sys.stdin)

    def filter(self,line):
        '''
        Determine if the input line should be collected or not.
        '''
        # Mode 1: No end filter only return match lines.
        if self.matchingonly:
            return bool(self.startpattern.search(line))
        # else:
        # Mode 2: Return anything between start- and end-filters
        # Rows matching filters can be included or excluded.
        if not self.readline and self.startpattern.search(line):
            if self.includestarting:
                self.readline = True
            else:
                self.readline = True
                return False
        elif self.readline and self.endpattern.search(line):
            # Test if the end pattern row should be caught.
            if self.includeclosing and self.readline:
                self.readline = False
                return True
            else:
                self.readline = False
        return self.readline

    def follow(self,infile):
        '''
        Follow a file ; Emulating tail -f but with filters.
        '''
         # Do we even need the seek if prefollow has already read to the end?
        if infile.seekable():
            infile.seek(0, os.SEEK_END)
        while True:
            try:
                line = infile.readline()
                if not line:
                    time.sleep(self.follow_sleep_time)
                    continue
                if not self.filter(line):
                    continue
                yield line
            except KeyboardInterrupt: # Normal behavior in this context.
                break

    def prefollow(self,infile):
        '''
        Read the last matching numlines of infile before following the files.
        '''
        lastlines = []
        while True:
            line = infile.readline()
            if not line:
                break
            if not self.filter(line):
                continue
            if self.numlines:
                lastlines.append(line)
                if len(lastlines) >= self.numlines:
                    del lastlines[0]
            else:
                yield line
        if self.numlines:
            yield from lastlines
#%% Click cli:
@click.command()
@click.option("-f", "--filename", help="File to follow.",required=False)
@click.option("-s", "--startpattern", help="Start filter regex.",required=True)
@click.option("-e", "--endpattern", help="End pattern regex.")
@click.option("--follow", help="Follow the file or stdin.", is_flag=True)
@click.option("--matching-only",
              help="Only return rows matching the startpattern. Override the include/exclude options.",
              required=False, default=False,show_default=True)
@click.option("--include-closing/--exclude-closing",
              help="Include end pattern in output.",
              default=False, show_default=True)
@click.option("--include-starting/--exclude-starting",
              help="Include start pattern in output.",
              default=True, show_default=True)
@click.option("-n","--lines",
              help="Start scanning the last N number of lines in input file.",
              type=int, required=False, default=None)
def main(**kwargs):
    '''
    Print rows from filterfollow to stdout.
    '''
    click.echo(kwargs)
    initdict = {
        "filename": kwargs["filename"] if kwargs["filename"] else None,
        "startpattern": kwargs["startpattern"],
        "endpattern": kwargs["endpattern"] if kwargs["endpattern"] else None,
        "follow": kwargs["follow"] if kwargs["follow"] else False,
        "includestarting": kwargs["include_starting"],
        "includeclosing": kwargs["include_closing"],
        "lines": int(kwargs["lines"]) if kwargs["lines"] else None
    }
    ffollow = FilterFollow(**initdict)
    for line in ffollow.run():
        click.echo(line.rstrip("\n"))

#%%
if __name__ == '__main__':
    main()
