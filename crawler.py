import httplib2
import os
import re
import threading
import urllib
from urlparse import urlparse, urljoin
from BeautifulSoup import BeautifulSoup


class Singleton(object):
  def __new__(cls):
    if not hasattr(cls, 'instance'):
      cls.instance = super(Singleton, cls).__new__(cls)
    return cls.instance


class ImageDownloaderThread(threading.Thread):
  """ A Thread for downloading images in parallel. """

  def __init__(self, thread_id, name, counter):
    threading.Thread.__init__(self)
    self.name = name

  def run(self):
    print "Starting thread ", self.name
    download_images(self.name)
    print "Finished thread ", self.name

  def traverse_site(max_links = 10):
    link_parser_singleton = Singleton()

    #While we have pages to parse in queue
    while link_parser_singleton.queue_to_parse:
      if len(link_parser_singleton.to_visit) == max_links:
        return
      
      url = link_parser_singleton.queue_to_parse.pop()

      http = httplib2.Http()
      try:
        status, response = http.request(url)
      except Exception:
        continue
      
      #skip if not a web page
      if status.get('content-type') != 'text/html':
        continue
      
      #Adding the link to queue for downloading images
      link_parser_singleton.to_visit.add(url)
      print "Added ", url, " to queue"
      bs = BeautifulSoup(response)

      for link in BeautifulSoup.findAll(bs, 'a'):
        link_url = link.get("href")
        if not link_url:
          continue
        parsed = urlparse(link_url)

        # if link redirects to an external page, skip
        if parsed.netloc and parsed.netloc != parsed_root.netloc:
          continue
        
        # constructing the full url from a link
        link_url = (parsed.scheme or parsed_root.scheme) + "://" + (parsed.netloc or parsed_root.netloc) + parsed.path or ""

        #IF the link was already added skip
        if link_url in link_parser_singleton.to_visit:
          continue
        
        # Adding a link for further parsing
        link_parser_singleton.queue_to_parse = [link_url] + link_parser_singleton.queue_to_parse

  
  def download_images(thread_name):
    singleton = Singleton()

    while singleton.to_visit:
      url = singleton.to_visit.pop()
      http = httplib2.Http()
      print thread_name, "Starting downloading images from", url

      try:
        status, response = http.request(url)
      except Exception:
        continue
      
      bs = BeautifulSoup(response)
      images = BeautifulSoup.findAll(bs, 'img')
      
      for image in images:
        #Getting the image source url
        src = image.get('src')
        #Constructing the full url
        src = urljoin(url, src)

        # Getting the base name 
        basename = os.path.basename(src)

        if src not in singleton.downloaded:
          singleton.downloaded.add(src)
          print "Downloading", src
          # Downloading image to local filesystem
          urllib.urlretrieve(src, os.path.join('images', basename))

      print thread_name, ' finished downloading images from ', url


if __name__ == '__main__':
  root = "http://python/org"

  parsed_root = urlparse(root)
  singleton = Singleton()
  singleton.queue_to_parse = [root]
  #A set of urls to download the images from
  singleton.to_visit = set()
  # Downloaded images
  singleton.downloaded = set()

  ImageDownloaderThread.traverse_site()

  # Creating images directory  if now existent
  if not os.path.exists('images'):
    os.makedirs('images')

  #Create now threads 
  thread1 = ImageDownloaderThread(1, "Thread - 1", 1)
  thread2 = ImageDownloaderThread(2, "Thread - 2", 2)

  # Starting the threads
  thread1.start()
  thread2.start()




