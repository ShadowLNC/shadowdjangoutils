from django.utils.deconstruct import deconstructible
from collections import OrderedDict

# Serialisable Enum type for Django "choices" values, typically integer fields.
@deconstructible
class ChoicesEnum:
    @classmethod
    def from_list(cls, *data):
        return cls([ (j,i) for i,j in enumerate(data) ])

    def __init__(self, data):
        self.enumItems = OrderedDict()
        self.addData(data)

    def addData(self, data):
        self.enumItems.update(data)
        # Re-sort with new data (i.e., ignore insertion order).
        # Django can't serialise a lambda, but apparently this is fine.
        self.enumItems = OrderedDict(
            sorted(self.enumItems.items(), key=lambda item: item[0]))

    def __getattr__(self, name):
        if name in self.enumItems:
            return self.enumItems[name]
        raise AttributeError("{} does not exist".format(name))

    def choices(self):
        values = []
        for k,v in self.enumItems.items():
            if v in values: continue
            values.append(v)
            yield (v,k)

    def __eq__(self, other):
        if not isinstance(other, self.__class__): return False
        return self.enumItems == other.enumItems

    def __repr__(self):
        return "<instance of {0.__class__!s} with values {0.enumItems!r} >".format(self)
