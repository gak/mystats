from _ast import Break
import os
import time
import yaml

import pystatsd


ROOT = os.path.abspath(os.path.dirname(__file__))


class Stats():
    def __init__(self):
        self.config = yaml.load(open(os.path.join(ROOT, 'config.yaml')))
        self.stats = pystatsd.Client(self.config['host'])
        self.stats.prefix = self.config['prefix']
        self.db = yaml.load(open(os.path.join(ROOT, 'db.yaml'))) or {}

    def run(self):
        for module in self.config['modules']:
            self.current_module = module
            m = __import__(module)
            try:
                m.main(self)
            except (Exception,), e:
                print(e)

    def gauge(self, name, value):
        self.stats.gauge(name, value)

    def get(self, key):
        sub = self.db.get(self.current_module, dict())
        return sub.get(key)

    def set(self, key, value):
        sub = self.db.get(self.current_module, dict())
        sub[key] = value
        self.db[self.current_module] = sub

        file_ptr = open(os.path.join(ROOT, 'db.yaml'), 'w')
        yaml.dump(self.db, file_ptr)

    def has_time_lapsed(self, minutes, key):
        ts = self.get(key) or 0
        diff = time.time() - (ts + minutes * 60)
        return diff >= 0

    def reset_time_lapsed(self, key):
        self.set(key, time.time())

    def run_every_n_minutes(self, minutes, key='last'):
        if self.has_time_lapsed(minutes, key):
            self.reset_time_lapsed(key)
            return True

