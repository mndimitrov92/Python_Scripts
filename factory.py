import abc
import urllib2
from BeautifulSoup import BeautifulStoneSoup

class Connector(object):
  """ This is an abstract class to connect to remote recources """
  __metaClass__ = abc.ABCMeta # Declaring the class as abstract

  def __init__(self, is_secure):
    self.is_secure = is_secure
    self.port = self.port_factory_method()
    self.protocol = self.protocol_factory_method()
    
  @abc.abstractmethod
  def parse(self):
    """ Parsing the web content . This method will be redefined runtime"""
    pass
  
  def read(self, host, path):
    """ Generic method for reading the web content """
    url = self.protocol + "://" + host + ":" + str(self.port) + path
    print "Connecting to: ", url
    return urllib2.urlopen(url, timeout=2).read()

  @abc.abstractmethod
  def protocol_factory_method(self):
    """ Factory method that is to be redefined """
    pass
  
  @abc.abstractmethod
  def port_factory_method(self):
    """ Another factory method that is to be redefined in a subclass """
    return FTPPort()


class HTTPConnector(Connector):
  """A concrete creator that creates a http connection """
  def protocol_factory_method(self):
    if self.is_secure:
      return 'https'
    return 'http'

  def port_factory_method(self):
    """ HTTP port and HTTP Secure port are concrete objects that are created by the factory method """
    if self.is_secure:
      return HTTPSecurePort()
    return HTTPPort()

  def parse(self, content):
    """Parsing the web content """
    filenames = []
    soup = BeautifulStoneSoup(content)
    links = soup.table.findAll('a')
    
    for link in links:
      filenames.append(link['href'])
    return '\n'.join(filenames)


class FTPConnector(Connector):
  """ A concrete creator that creates FTP connector """
  def protocol_factory_method(self):
    return 'ftp'
  
  def port_factory_method(self):
    return FTPPort()

  def parse(self, content):
    lines = content.split('\n')
    filenames = []
    for line in lines:
      #FTP format only contains 8 columns
      splitted_line = line.split(None, 8)
      if len(splitted_line) == 9:
        filenames.append(splitted_line[-1])    
    return '\n'.join(filenames)

class Port(object):
  __metaClass__ = abc.ABCMeta
  """ Abstract product. One of its subclassed will be created in factory methods."""

  @abc.abstractmethod
  def __str__(self):
    pass
  

class HTTPPort(Port):
  """ A concrete product which represents the http port """
  def __str__(self):
    return '80'


class HTTPSecurePort(Port):
  """A concrete product which represents the http port """
  def __str__(self):
    return '443'
  

class FTPPort(Port):
  """A concrete product which represents the ftp port """
  def __str__(self):
    return '21'
    
if __name__ == "__main__":
  domain = 'ftp.freebsd.org'
  path = '/pub/FreeBSD'

  protocol = input("Connecting to {}. Which protocol to use? (0 = http, 1= ftp):".format(domain))
  if protocol == 0:
    is_secure = bool(input('Use secure connection? (1= Yes, 0 = No):'))
    connector = HTTPConnector(is_secure)
  else:
    is_secure = False
    connector = FTPConnector(is_secure)
  
  try:
    content = connector.read(domain, path)
  except urllib2.URLError, e :
    print "Cannot connect to resource"
  else:
    print connector.parse(content)