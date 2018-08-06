# Scripts using the proxy design patern which instantiate an big object with 10 000 000 digits
from abc import ABCMeta, abstractmethod
import random

class abstractSubject(object):
    """ A common interface for the real and proxy objects """
    __metaClass__ = ABCMeta

    @abstractmethod
    def sort(self, revese=False):
        pass

class realSubject(abstractSubject):
    """ A class for the heavy object which take a lot of memory and time to instantiate"""
    def __init__(self):
        self.digits = []

        for i in xrange(10000000):
            self.digits.append(random.random())

    def sort(self,reverse=False):
        self.digits.sort()
        
        if reverse:
            self.digits.reverse()

class  proxy(abstractSubject):
    """ A proxy which has the same interface as the realSubject """
    reference_count = 0

    def __init__(self):
        """ A constructor which creates an object if it does not already exist and caches it otherwise """
        
        if not getattr(self.__class__, "cached_object", None):
            self.__class__.cached_object = realSubject()
            print "Created new object"
        else:
            print "Using cached object"

        self.__class__.reference_count += 1

        print "Count of references: ", self.__class__.reference_count

    def sort(self, reverse=False):
        """ The args are logged by the proxy"""
        print "Called sort method with args"
        print locals().items()

        self.__class__.cached_object.sort(reverse=reverse)

    def __del__(self):
        """Decreases a reference to an object , if the number of refernces is 0 - object is deleted"""
        self.__class__.reference_count -= 1

        if self.__class__.reference_count == 0:
            print "The number of references is 0. Deleting cached object..."
            del self.__class__.cached_object
        
        print "Object deleted. Count of objects =", self.__class__.reference_count

    
if __name__ == "__main__":
    proxy1 = proxy()
    print 

    proxy2 = proxy()
    print 

    proxy3 = proxy()
    print 

    proxy1.sort(reverse=True)
    print

    print "Deleting proxy 2"
    del proxy2
    print

    print "The other objects are deleted upon program termination"
    