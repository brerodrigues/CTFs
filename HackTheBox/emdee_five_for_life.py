#!/usr/bin/env python3

import requests
import hashlib
import time
import re

start_time = time.clock()
url = 'http://144.126.196.214:30773/'
# the biggest gotcha is keeping the same session
# over the request to get the string to hash
# and posting the answer -.-
s = requests.Session()

def get_html_from_url(url, cookies=None):
    response = s.get(url, cookies=cookies)
    #print (time.clock() - start_time, 'seconds to get the html')
    return response.text
    
def extract_string_from_html(html):
    string = re.findall('([a-z0-9A-z]{20})', html)[0] # get first match using regular expressions
    #print (time.clock() - start_time, 'seconds to get hash from html')
    return string
    
def hash_string_to_md5(string):
    #print (time.clock() - start_time, 'seconds to get hash the string')
    return hashlib.md5(string.encode("utf-8")).hexdigest()
    
def post_hash_and_get_flag(md5):
    md5_hash = dict(hash=md5)
    response = s.post(url=url, data=md5_hash)
    #print (time.clock() - start_time, 'seconds to get response')
    return response.text
    
html = get_html_from_url(url)
#print(html)
string_to_hash = extract_string_from_html(html)
#print(string_to_hash)
md5_hash = hash_string_to_md5(string_to_hash)
#print(md5_hash)
print(post_hash_and_get_flag(md5_hash))
