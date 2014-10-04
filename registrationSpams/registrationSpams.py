'''
	@author Shashank Jaiswal
	@since 01-08-2014
	@version 0.0.0.1
	@description
		SpamBot:: Using mechanize and OCR for junk registrations
				  <http://elan.org.in/fifamania/signup/index.php> 
				  is just an example. Please don't make a big issue
				  out of it.
		Author: Shashank Jaiswal <shashank_jaiswal@live.com>
		Copyright (c): 2014 Shashank Jaiswal, all rights reserved
		Version: 0.0.0.1
		* This library is free software; you can redistribute it and/or
		* modify it under the terms of the GNU Lesser General Public
		* License as published by the Free Software Foundation; either
		* version 2.1 of the License, or (at your option) any later version.
		*
		* This library is distributed in the hope that it will be useful,
		* but WITHOUT ANY WARRANTY; without even the implied warranty of
		* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
		* Lesser General Public License for more details.
		*
		* You should have received a copy of the GNU Lesser General Public
		* License along with this library; if not, write to the Free Software
		* Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
	
	You may contact the author at: shashank_jaiswal@live.com
'''

import urllib
import urllib2
from PIL import Image
from pytesser import *
import MySQLdb
import mechanize
import cookielib
import re
from bs4 import BeautifulSoup


# Browser
br = mechanize.Browser()

# Cookie Jar
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)

# Browser options
br.set_handle_equiv(True)
br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)

# Follows refresh 0 but not hangs on refresh > 0
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

# Want debugging messages?
br.set_proxies({
    "http"  : "127.0.0.1:8888",
    "https" : "127.0.0.1:8888",})
br.add_proxy_password("unknown", "password")
br.set_debug_http(True)
br.set_debug_redirects(True)
br.set_debug_responses(True)

# User-Agent (this is cheating, ok?)
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

# <http://elan.org.in/fifamania/signup/index.php> is just an example...Don't panic
r=br.open('http://elan.org.in/fifamania/signup/index.php')
br.select_form(nr=0)
br.form['fname'] = 'ABC';
br.form['lname'] = 'XYZ';
br.form['college'] = 'Unknown';
br.form['email'] = 'unknown@unknown.co.in';
br.form['pass'] =  'unknown';
br.form['cpass'] =  'unknown';

soup = BeautifulSoup(r.get_data())
img = soup.find_all('img')[1];
image = br.open_novisit(img['src']).read();

# Save the file to local directory
localFile = open('_captcha_.png', 'wb')
localFile.write(image)
localFile.close()

# resize the PNG image and save it as JPEG
size = (376, 184);
im = Image.open("_captcha_.png")
im = im.resize(size, Image.ANTIALIAS)
im.save("_captcha_.jpg", "JPEG")

# get the captcha text using OCR
im = Image.open("_captcha_.jpg");
captchaSolution = image_to_string(im);
print 'Captcha:', captchaSolution ;

br.form['captcha'] =  captchaSolution;

r = br.submit()
m = r.read();
print m;


# Data from the html
##soup = BeautifulSoup(m)
##l = (soup.find(id="signup_box").get_text());


if "Try again" in m:
    print "Error";
