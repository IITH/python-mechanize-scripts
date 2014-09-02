import mechanize
import cookielib
import time
from urllib2 import HTTPError
import Queue
import threading

br = mechanize.Browser()
cj= cookielib.LWPCookieJar()
br.set_cookiejar(cj)

br.set_handle_equiv(True)
br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)

start_time=time.time()
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

#br.set_proxies({"http": "joe:password@myproxy.example.com:3128"})
br.set_proxies({"http": "cs11b029:123@192.168.36.22:3128"})
q = Queue.Queue()

def open_url(q,url):
  try:
    r=br.open(url)
#    q.put(r)
#    html=r.read()
  except HTTPError, e:
      print "Got Error Code", e.code
  print url
  
with open('websites.txt') as f:
	content = f.readlines()
	

for url in content:
  t = threading.Thread(target=open_url, args = (q,url))
  t.daemon=True
  t.start()
  
latency=time.time() - start_time
print "latency=  " , latency
 

