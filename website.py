# -*- coding:UTF-8 -*-
import urllib
import urllib2
import re
import json
import random
import urlparse
import binascii
import base64
import os

# crc32
def right_shift(val, n):
    return val >> n if val >= 0 else (val + 0x100000000) >> n

#get html content
def getHtml(url):
    req=urllib2.Request(url)
    req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0')
    req.add_header('Accept-Language','zh-CN')
    res=urllib2.urlopen(req)
    html=res.read()
    return html

#get videoid from html content
def getVideoid(html):
    reg = r'videoId: \'(.+?)\''
    videore = re.compile(reg)
    videolist = re.findall(videore,html)
    for videourl in videolist:
        return videourl

#parse video json data
def parseVideoJson(url):
    html = urllib.urlopen(url)
    htmlstr = html.read()
    dictstr = json.loads(htmlstr)
    print 'videojson:'+str(dictstr)
    datastr = dictstr['data']
    dict_videolist = datastr['video_list']
    dict_video1 = dict_videolist.get('video_1')         #极速版
    dict_video2 = dict_videolist.get('video_2')         #高清版
    dict_video = dict_video2
    if (not dict_video) :
        dict_video = dict_video1
    main_url = dict_video['main_url']
    return main_url

#download video
def downLoadVideoFromURL(url):
    try:
        path = os.getcwd()
        file_name = str(random.random())+'.mp4'
        dest_dir=os.path.join(path,file_name)
        urllib.urlretrieve(url , dest_dir)
    except:
        print '\tError retrieving the URL:', dest_dir       

#Step 1: get html
html = getHtml('http://www.toutiao.com/a6406824900753670401/')
file_object = open('video.html', 'w')
file_object.write(html)
file_object.close( )

#Step 2: get videoid
videoid = getVideoid(html)
print 'videoid:'+str(videoid)

#Step 3: get crc32
r = str(random.random())[2:]
#url = 'http://i.snssdk.com/video/urls/v/1/toutiao/mp4/%s' % videoid
url = 'https://ib.365yg.com/video/urls/v/1/toutiao/mp4/%s' % videoid
n = urlparse.urlparse(url).path + '?r=' + r
c = binascii.crc32(n)
s = right_shift(c, 0)
print "crc32:"+str(s)

#Setp 4: parse json
mainvideourl = parseVideoJson(url + '?r=%s&s=%s' % (r, s))

#Step 5: decode url
videourl = base64.b64decode(mainvideourl)
print 'videourl:'+str(videourl)

#Step 6: download video
downLoadVideoFromURL(videourl)