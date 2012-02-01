import itertools
import time

from collections import defaultdict

class MetricsSearch(object):

    def index(self, data):
        index = defaultdict(list)
        for line in data:
            parts = line.split('.')
            for part in parts:
                index[part].append(line)
        return index

    def search(self, query, index):
        keys = itertools.ifilter(lambda x: x.find(query) >= 0, index.keys())
        return itertools.chain(*itertools.imap(index.get, keys))
