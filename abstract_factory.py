import abc
import urllib2
from BeautifulSoup import BeautifulStoneSoup

class AbstractFactory(object):
  """ Abstract factory interface  which will provide methods to implement in its subclasses """
  __metaclass__ = abc.ABCMeta
  
  def __init__(self, is_secure):
    """ if is_secure is True, factory  tries to make connection secure, otherwise not. """
    self.is_secure = is_secure
  
  @abc.abstractmethod
  def create_protocol(self):
    pass
  
  @abc.abstractmethod
  def create_port(self):
    pass
  
  @abc.abstractmethod
  def create_parser(self):
    pass

#HTTP Factory class 
class HTTPFactory(AbstractFactory):
  """ Concrete factory for building http connections """
  def create_protocol(self):
    if self.is_secure:
      return "https"
    return "http"
  
  def create_port(self):
    if self.is_secure:
      return HTTPSecurePort()
    return HTTPPort()

  def create_parser(self):
    return HTTPParser()

# FTP Factory class
class FTPFactory(AbstractFactory):
  """ Concrete factory for building FTP connections """
  def create_protocol(self):
    return "ftp"
  
  def create_port(self):
    return FTPPort()

  def create_parser(self):
    return FTPParser()


class Port(object):
  __metaclass__ = abc.ABCMeta
  """ An abstract product which reporesents the port to connect. """
  @abc.abstractmethod
  def __str__(self):
    pass
  

class HTTPPort(Port):
  """ A concrete class which reporesents the http port """
  def __str__(self):
    return '80'


class HTTPSecurePort(Port):
  """ A concrete class which represents the https port """
  def __str__(self):
    return '443'


class FTPPort(Port):
  """ A concrete class which represents the ftp port """
  def __str__(self):
    return '21'


class Parser(object):
  """ An abstract product ,reporesents parser to parse web content """
  __metaclass__ = abc.ABCMeta

  @abc.abstractmethod
  def __call__(self, content):
    pass


class HTTPParser(Parser):
  def __call__(self, content):
    filenames = []
    soup = BeautifulStoneSoup(content)
    links = soup.table.findAll('a')
    for link in links:
      filenames.append(link)
    return '\n'.join(filenames)


class FTPParser(Parser):
  def __call__(self, content):
    lines = content.split('\n')
    filenames = []
    for line in lines:
      split_line = line.split(None, 8)
    if len(split_line) == 9:
      filenames.append(split_line[-1])
    return "\n".join(filenames)


class Connector(object):
  def __init__(self, factory):
    self.protocol = factory.create_protocol()
    self.port = factory.create_port()
    self.parse = factory.create_parser()
  
  def read(self, host, path):
    url = self.protocol + "://" + host + ":" + str(self.port) + path
    print "Connecting to: ", url
    return urllib2.urlopen(url, timeout=2).read()

  @abc.abstractmethod
  def parse(self):
    pass
  

if __name__ == "__main__":
  domain = "ftp.freebsd.org"
  path = "/pub/FreeBSD"
  protocol = input("Connecting to {}. Which protocol to use? (0 - http; 1 - ftp):".format(domain))

  if protocol == 0:
    is_secure = bool(input("Use secure connection? (1- Yes; 0 - No)"))
    factory = HTTPFactory(is_secure)
  elif protocol == 1:
    is_secure = False
    factory = FTPFactory(is_secure)
  else:
    print "Sorry, could not connect"
  
  connector = Connector(factory)
  try:
    content = connector.read(domain, path)
  except urllib2.URLError,e:
    print "Cannot access resource"
  else:
    print connector.parse(content)

    
