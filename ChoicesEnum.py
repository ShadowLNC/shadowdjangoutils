from django.utils.deconstruct import deconstructible
from collections import OrderedDict

#serialisable enum
@deconstructible
class ChoicesEnum:
    def __init__(self, data):
        self.enumItems = OrderedDict()
        self.addData(data)
    
    def addData(self, data):
        self.enumItems.update(data)
        #re-sort with new data (i.e., ignore insertion order)
        #django can't serialise a lambda, but apparently here is fine
        self.enumItems = OrderedDict(
            sorted(self.enumItems.items(), key=lambda item: item[0]))
    
    def __getattr__(self, name):
        if name in self.enumItems:
            return self.enumItems[name]
    
    def choices(name):
        values = []
        for k,v in name.enumItems.items():
            if v in values: continue
            values.append(v)
            yield (v,k)
    
    def __eq__(self, other):
        if not isinstance(other, self.__class__): return False
        return self.enumItems == other.enumItems
    
    def __repr__(self):
        return "<instance of {0.__class__!s} with values {0.enumItems!r} >".format(self)
