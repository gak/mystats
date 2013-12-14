import os
import yaml

import pystatsd


ROOT = os.path.abspath(os.path.dirname(__file__))


class Stats():
    def __init__(self):
        self.config = yaml.load(open(os.path.join(ROOT, 'config.yaml')))
        self.stats = pystatsd.Client(self.config['host'])
        self.stats.prefix = self.config['prefix']

    def run(self):
        for module in self.config['modules']:
            print(module)
            m = __import__(module)
            m.main()

    def gauge(self, name, value):
        self.stats.gauge(name, value)

