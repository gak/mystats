#!/usr/bin/env python
import re
import subprocess


def main(stats):
    global output, found, line, match, amount
    output = subprocess.check_output('upower -d', shell=True)
    found = False
    for line in output.split('\n'):
        if found and 'percentage:' in line:
            match = re.search(r'(\d+)%', line)
            amount = float(match.groups()[0])
            if amount > 0:
                stats.gauge('keyboard.power', amount)
            break

        if 'K750' in line:
            found = True

if __name__ == '__main__':
    main()




