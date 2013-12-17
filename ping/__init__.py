#!/usr/bin/env python

import os
import re

# 20 packets transmitted, 19 received, 5% packet loss, time 18998ms
# rtt min/avg/max/mdev = 37.065/38.430/48.027/2.618 ms

hosts = [
    ['telstra', '139.130.4.5'],
    ['tpg', '203.12.160.187'],
    ['gakman_com', '74.207.242.31'],
    ['google_dns', '8.8.8.8'],
]


def main(stats):
    for num, (name, ip) in enumerate(hosts):
        _, fd, _ = os.popen3('ping -c 10 -i 0.2 %s' % ip)
        data = fd.read()

        last_line = data.strip().split('\n')[-1]
        bits = re.split('([0-9\.]+)', last_line)
        min = float(bits[1])
        avg = float(bits[3])
        max = float(bits[5])

        stats.gauge('ping.{}.avg'.format(name), avg)
        stats.gauge('ping.{}.min'.format(name), min)
        stats.gauge('ping.{}.max'.format(name), max)

