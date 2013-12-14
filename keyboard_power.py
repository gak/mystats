#!/usr/bin/env python
import re
import subprocess

from stats import Stats


def main():
    global output, found, line, match, amount
    output = subprocess.check_output('upower -d', shell=True)
    found = False
    for line in output.split('\n'):
        if found and 'percentage:' in line:
            match = re.search(r'(\d+)%', line)
            amount = float(match.groups()[0])
            Stats().gauge('keyboard.power', amount)
            break

        if 'K750' in line:
            found = True

if __name__ == '__main__':
    main()




