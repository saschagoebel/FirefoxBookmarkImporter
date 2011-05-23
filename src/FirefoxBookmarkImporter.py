# -*- coding: utf-8 -*-
'''
 See http://code.google.com/p/feedparser/
 See http://code.google.com/p/pydelicious/
'''

#  ###                                          
#   #  #    # #####   ####  #####  #####  ####  
#   #  ##  ## #    # #    # #    #   #   #      
#   #  # ## # #    # #    # #    #   #    ####  
#   #  #    # #####  #    # #####    #        # 
#   #  #    # #      #    # #   #    #   #    # 
#  ### #    # #       ####  #    #   #    #### 

import sys
import getpass
import json
import urllib2
import httplib
import pydelicious
from pydelicious import DeliciousAPI
import re


#   #####                                                                           
#  #     #  ####  #    # ###### #  ####  #    # #####    ##   ##### #  ####  #    # 
#  #       #    # ##   # #      # #    # #    # #    #  #  #    #   # #    # ##   # 
#  #       #    # # #  # #####  # #      #    # #    # #    #   #   # #    # # #  # 
#  #       #    # #  # # #      # #  ### #    # #####  ######   #   # #    # #  # # 
#  #     # #    # #   ## #      # #    # #    # #   #  #    #   #   # #    # #   ## 
#   #####   ####  #    # #      #  ####   ####  #    # #    #   #   #  ####  #    # 

importFile = raw_input('Filename: ')
deliciousUser = raw_input('Username: ')
deliciousPassword = getpass.getpass();
skipFolders = ['Schnellsuche', u'Schlagwörter', u'_IDEA_BOX_', u'_TO_DO_', u'Lesezeichen-Symbolleiste']
skipNames = ['', u'lesezeichen-symbolleiste', u'lesezeichen-menü']


#  #######                                                   
#  #       #    # #    #  ####  ##### #  ####  #    #  ####  
#  #       #    # ##   # #    #   #   # #    # ##   # #      
#  #####   #    # # #  # #        #   # #    # # #  #  ####  
#  #       #    # #  # # #        #   # #    # #  # #      # 
#  #       #    # #   ## #    #   #   # #    # #   ## #    # 
#  #        ####  #    #  ####    #   #  ####  #    #  #### 

def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is one of "yes" or "no".
    """
    valid = {"yes":True,   "y":True,  "ye":True,
             "no":False,     "n":False}
    if default == None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "\
                             "(or 'y' or 'n').\n")
            
#   #####                                                                           
#  #     #  ####  #    # ###### #  ####  #    # #####    ##   ##### #  ####  #    # 
#  #       #    # ##   # #      # #    # #    # #    #  #  #    #   # #    # ##   # 
#  #       #    # # #  # #####  # #      #    # #    # #    #   #   # #    # # #  # 
#  #       #    # #  # # #      # #  ### #    # #####  ######   #   # #    # #  # # 
#  #     # #    # #   ## #      # #    # #    # #   #  #    #   #   # #    # #   ## 
#   #####   ####  #    # #      #  ####   ####  #    # #    #   #   #  ####  #    #

skipUpdate = query_yes_no('Skip Update: ')
skipCreate = query_yes_no('Skip Create: ')
 
#  #######                                                   
#  #       #    # #    #  ####  ##### #  ####  #    #  ####  
#  #       #    # ##   # #    #   #   # #    # ##   # #      
#  #####   #    # # #  # #        #   # #    # # #  #  ####  
#  #       #    # #  # # #        #   # #    # #  # #      # 
#  #       #    # #   ## #    #   #   # #    # #   ## #    # 
#  #        ####  #    #  ####    #   #  ####  #    #  #### 

def isUriValid(uri):
    request = urllib2.Request(uri)
    try:
        response = urllib2.urlopen(request)
        # Handle ugly T-Online DNS-Error Page :-(
        if response.geturl().find('dnserror') != -1:
            return False
        return True
    except urllib2.HTTPError:
        return False
    except urllib2.URLError:
        return False
    except httplib.BadStatusLine:
        return False
    else:
        return True

    
def sortByValue(dict):
    items = [(v, k) for k, v in dict.items()]
    items.sort()
    items.reverse()             # so largest is first
    items = [(k, v) for v, k in items]
    return items


def getBookmarkMeta(uri):
    posts = pydelicious.get_urlposts(uri)
    
    if 0 == len(posts):
        return False
    
    tags = {}
    descriptions = {}
    extendeds = {}
    urls = {}
    for i in range(len(posts)):
        #print posts[i] 
        urls[posts[i]['url']] = urls[posts[i]['url']] + 1 if posts[i]['url'] in urls else 1

        if '' != posts[i]['extended']:
            extendeds[posts[i]['extended']] = extendeds[posts[i]['extended']] + 1 if posts[i]['extended'] in extendeds else 1

        description = re.sub('^\[.*?\]\s', '', posts[i]['description'])
        if '' != description:
            descriptions[description] = descriptions[description] + 1 if description in descriptions else 1

        ts = posts[i]['tags'].split()
        for t in ts:
            if '' != t:
                t = t.lower()
                tags[t] = tags[t] + 1 if t in tags else 1

    urls = sortByValue(urls)
    extendeds = sortByValue(extendeds)
    descriptions = sortByValue(descriptions)
    tags = sortByValue(tags)

    result = {'url': urls[0][0], 
              'extended': extendeds[0][0] if 0 < len(extendeds) else '', 
              'description': descriptions[0][0], 
              'tags': []}
    
    for i in range(len(tags)):
        if tags[i][1] > 1:
            result['tags'].append(tags[i][0])

    return result


def isBookmarkPresent(uri):
    for post in allPosts['posts']:
        if post['href'].lower() == uri.lower() or uri.lower().replace('//www.', '//') in post['href'].lower().replace('//www.', '//') or post['href'].lower().replace('//www.', '//') in uri.lower().replace('//www.', '//'):
            return True
    return False


def processEntry(currentEntry, containers = []):
    
    if 'text/x-moz-place' == currentEntry['type']:
        # Skip javascript bookmarklets
        if currentEntry['uri'].find('javascript') != -1:
            return

        # Remove possible hashes        
        if currentEntry['uri'].rfind('#') != -1:
            currentEntry['uri'] = currentEntry['uri'][0:currentEntry['uri'].rfind('#')]

        # Check if already bookmarked
        if isBookmarkPresent(currentEntry['uri']):
            if not skipUpdate:
                updateEntry(currentEntry, containers)
        else:
            if not skipCreate:
                createEntry(currentEntry, containers)

        return

    # Process containers
    if 'text/x-moz-place-container' == currentEntry['type']:
        # Skip system containers
        if currentEntry['title'] in skipFolders:
            return
        
        print 'Processing: ', '/'.join(containers + [currentEntry['title'].lower()])

        # Process each child
        if 'children' in currentEntry:
            for i in range(0, len(currentEntry['children'])):
                processEntry(currentEntry['children'][i], containers + [currentEntry['title'].lower()] if currentEntry['title'].lower() not in skipNames else containers)
    return


def createEntry(entry, tags):
    
    if not isUriValid(entry['uri']):
        return
        
    print 'Create new bookmark: ', entry['uri']
    meta = getBookmarkMeta(entry['uri'])
    
    if False == meta:
        print 'Unable to fetch meta data. Skipping'
        return
    
    result = {'url': meta['url'],
              'description': meta['description'] if '' != meta['description'] else entry['title'],
              'extended': meta['extended'],
              'tags': ' '.join(tags + meta['tags'])}

    deliciousApi.posts_add(result['url'], result['description'], extended=result['extended'], tags=result['tags'], dt='2010-01-01T07:00:00Z', replace=True, shared=False)
    print 'Created: ', result['url']


def updateEntry(entry, tags):
    print 'Update existing bookmark: ', entry['uri']
    meta = getBookmarkMeta(entry['uri'])
    own = deliciousApi.posts_get(url=entry['uri'])
  
    result = {'url': meta['url'],
              'description': own['posts'][0]['description'],
              'extended': own['posts'][0]['extended'] if '' != own['posts'][0]['extended'] else meta['extended'],
              'tags': ' '.join(tags + meta['tags']) + ' ' + own['posts'][0]['tag']}

    deliciousApi.posts_add(result['url'], result['description'], extended=result['extended'], tags=result['tags'], replace=True, shared=False)


#  #     #                 
#  ##   ##   ##   # #    # 
#  # # # #  #  #  # ##   # 
#  #  #  # #    # # # #  # 
#  #     # ###### # #  # # 
#  #     # #    # # #   ## 
#  #     # #    # # #    #

# Init delicious api
deliciousApi = DeliciousAPI(deliciousUser, deliciousPassword)
allPosts = deliciousApi.posts_all() 

# Read and process JSON Data
jsonDataFile = open(importFile)
jsonData = json.load(jsonDataFile)
jsonDataFile.close()
processEntry(jsonData)

print 'All done ... have a nice day!'