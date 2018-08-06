#excercise printing the timestamp in USA or EU format using the observer design pattern
import time
from abc import ABCMeta,abstractmethod
import datetime

class Subject(object):
    def __init__(self):
        self.observers = []
        self.curr_time = None

    def register_observer(self, observer):
        if observer in self.observers:
            print observer, " is already in subscribed observers"
        else:
            self.observers.append(observer)
        
    def unregister_observer(self, observer):
        try:
            self.observers.remove(observer)
        except ValueError:
            print "No such observer in subject"

    def notify_observers(self):
        self.curr_time = time.time()
        for observer in self.observers:
            observer.notify(self.curr_time)

class Observer(object):
    """Abstract class for observers which provides the notify method as an interface for subjects"""
    __metaclass__ = ABCMeta

    @abstractmethod
    def notify(self, unix_timestamp):
        pass
    
class USAtimeObserver(Observer):
    def __init__(self, name):
        self.name = name
    
    def notify(self, unix_timestamp):
        time = datetime.datetime.fromtimestamp(int(unix_timestamp)).strftime('%Y-%m-%d %I:%M:%S%p')
        print "Observer ", self.name, " says:", time

class EUTimeObserver(Observer):
    def __init__(self, name):
        self.name = name
    
    def notify(self, unix_timestamp):
        time = datetime.datetime.fromtimestamp(int(unix_timestamp)).strftime('%Y-%m-%d %H:%M:%S')
        print "Observer ", self.name, " says:", time

    
if __name__ == "__main__":
    subject = Subject()
    
    print "Adding US time observer"
    observer1 = USAtimeObserver('usa_time_observer')
    subject.register_observer(observer1)
    subject.notify_observers()

    time.sleep(2)
    print "Adding EU time observer"
    observer2 = EUTimeObserver('EU_time_observer')
    subject.register_observer(observer2)
    subject.notify_observers()

    time.sleep(2)
    print "Removing US time observer"
    subject.unregister_observer(observer1)
    subject.notify_observers()


    