# README

Simple help script to follow a file in Python. Comparable to both `tail -f` and
`grep -E`. The input file for file like object will parsed for input start and
end patterns, and returning rows between start pattern and end patterns.

## Behavior - Work in progress

### Basic Behavior
The FilterFollow class is intended to make it easier to parse log files where
you are interested in a certain row pattern optionally interspersed with other
messages belong to said pattern.

Basic options:
* `--startpattern` Start pattern - Pattern to include
* `--endpattern` End pattern - Pattern to trigger exclusion
* `-f/--filename` Filename

An example below:
```
...
PATTERN2 - Not matching this row
PATTERN1
non-pattern - Expected to belong to PATTERN1
non-pattern - and is collected.
PATTERN2 - Not matching
non-pattern - Not collected
PATTERN1
PATTERN2
...
```
The constraints on the patterns is that PATTERN2 should match all normal logging
rows and PATTERN1 the logging row of interest.
The basic expected output of the example above is:
```
...
PATTERN1
non-pattern - Expected to belong to PATTERN1
non-pattern - and is collected.
PATTERN1
...
```
This might be subject to some change as it is a valid use case to having closing
patterns being included.

### Extended Basic
Extended basic:
* `--include-closing` Include closing pattern - Include a closing row after
  collecting one or more rows. See below for the expected output of the example
  input.
```
...
PATTERN1
non-pattern - Expected to belong to PATTERN1
non-pattern - and is collected.
PATTERN2 - Not matching
PATTERN1
PATTERN2
...
```
* `--include-starting` Include starting pattern - Include a starting row after
  not collecting one or more rows. See below for the expected output of the
  example input if set to False.
```
...
non-pattern - Expected to belong to PATTERN1
non-pattern - and is collected.
...
```
### On streams

The script is intended to be able to parse streams, or to follow a growing file.

Stream options:
* `-t/--follow` Follow - Wether to follow the file or not. Implicit if input is a stream.
            Eg: stdin
* `-n/--lines` Lines - How many lines to collect from input file if it is a regular file.
