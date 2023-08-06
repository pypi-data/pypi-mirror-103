import json
import csv
import os

__all__ = ['BaseDict']


class BaseDict(dict):
    def __add__(self, other):
        o_keys = other.keys()
        for key in self.keys():
            if key in o_keys:
                raise KeyError('Cannot concatenate both dictionaries. Key %s duplicated' % key)
        self.update(other)
        return self

    def __radd__(self, other):
        if other == 0:
            return self
        else:
            return self.__add__(other)

    def write(self, path):
        path = os.path.splitext(path)[0]
        with open('%s.json' % path, 'w') as outfile:
            json.dump(self, outfile)

    def load(self, path):
        with open(path, 'r') as f:
            datastore = json.load(f)
            self.update(datastore)
        return self


def csv_reader(path):
    with open(path, mode='r') as csv_file:
        csv_instance = csv.DictReader(csv_file)
        for row in csv_instance:
            for key in row:
                try:
                    row[key] = float(row[key])
                except ValueError:
                    pass
            yield row
