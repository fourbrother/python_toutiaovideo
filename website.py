import urllib
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
    page = urllib.urlopen(url)
    html = page.read()
    return html

#get videoid from html content
def getVideoid(html):
    reg = r'videoid:(.+?),'
    videore = re.compile(reg)
    videolist = re.findall(videore,html)
    for videourl in videolist:
        lens = len(videourl)-1
        videourl = videourl[1 : lens]
        return videourl

#parse video json data
def parseVideoJson(url):
    html = urllib.urlopen(url)
    htmlstr = html.read()
    dictstr = json.loads(htmlstr)
    print 'videojson:'+str(dictstr)
    datastr = dictstr['data']
    dict_videolist = datastr['video_list']
    dict_video1 = dict_videolist['video_1']
    main_url = dict_video1['main_url']
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
html = getHtml('http://www.toutiao.com/a6361599161015468545/')
file_object = open('video.html', 'w')
file_object.write(html)
file_object.close( )

#Step 2: get videoid
videoid = getVideoid(html)
print 'videoid:'+str(videoid)

#Step 3: get crc32
r = str(random.random())[2:]
url = 'http://i.snssdk.com/video/urls/v/1/toutiao/mp4/%s' % videoid
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