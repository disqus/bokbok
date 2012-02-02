class Metrics(object):

    def index(self, data):
        index = dict()
        for line in data:
            index[line] = None
        return index

    def find(self, query, index):
        return [metric for metric in sorted(index) if query in metric]
