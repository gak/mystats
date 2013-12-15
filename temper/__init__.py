#!/usr/bin/env python
import temper


def main(stats):
    th = temper.TemperHandler()
    device = th.get_devices()[0]
    c = device.get_temperature(format='celsius')
    stats.gauge('room.temperature', c)

if __name__ == '__main__':
    main()

