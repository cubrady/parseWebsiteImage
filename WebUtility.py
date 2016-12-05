#-*- coding:utf-8 -*-

import urllib2, sys, socket

WEBPAGE_ENCODE = "big5"

SUCCESS = 1
ERR_TIMEOUT = 2
ERR_HTTP = 3
ERR_URL = 4
ERR_GENERAL = 5

def __retrieveWebPage(address):
	web_handle = None
	user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
	#headers = { 'User-Agent' : user_agent }
	try:
		request = urllib2.Request(address)
		request.add_header('User-Agent', user_agent)
		web_handle = urllib2.urlopen(request, timeout = 10)
		#web_handle = urllib2.urlopen(address)
		#log('header:%s' % web_handle.headers)
	except socket.timeout, e:
		# For Python 2.7
		#raise MyException("There was an error: %r" % e)
		return None, ERR_TIMEOUT
	except urllib2.HTTPError, e:
		#import BaseHTTPServer
		error_desc = ""#BaseHTTPServer.BaseHTTPRequestHandler.responses[e.code][0]
		print "Cannot retrieve URL: " + str(e.code) + ": " + error_desc
		#log("Cannot retrieve URL: HTTP Error Code", e.code)
		return None, ERR_HTTP
	except urllib2.URLError, e:
		#log("Cannot retrieve URL: " + e.reason[1])
		return None, ERR_URL
	except:
		#log("Cannot retrieve URL: unknown error")
		return None, ERR_GENERAL

	return web_handle, SUCCESS

def getWebContent(url, encodeBig5 = True):
	website_handle, err = __retrieveWebPage(url)
	if website_handle and err == SUCCESS:

		try:
			website_text = website_handle.read()	# UTF-8
		except socket.timeout, e:
			return None

		try:
			if encodeBig5:
				type = sys.getfilesystemencoding()	# local encode format
				website_text = website_text.decode(WEBPAGE_ENCODE).encode(type)  # convert encode format
			else:
				print "[getWebContent]try again , don't decode %s" % WEBPAGE_ENCODE
		except UnicodeDecodeError:
			print "[Err]'%s' codec can't decode bytes" % WEBPAGE_ENCODE
			return getWebContent(url, encodeBig5 = False)
		#return "".join([chr(ord(x)) for x in website_text]).decode(WEBPAGE_ENCODE)
		return website_text
	else:
		#log ("[Err]%d is not exist" % stockNo)
		return None

def seleniumAutomation(url):
	from selenium import webdriver
	import time

	driver = webdriver.Firefox()
	driver.get(url)
	time.sleep(1)

	'''
	elements = driver.find_elements_by_class_name('SwatchAnchor')

	for element in elements:
		element.click()
		time.sleep(2)
		print driver.find_element_by_class_name('bigPriceText1').text + driver.find_element_by_class_name('smallPriceText1').text
	'''
	driver.quit()
