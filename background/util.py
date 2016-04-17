# -*- coding: utf-8 -*-

"""
@author: Darren Vong
"""
import urllib2
import os
from time import sleep

from views.helpers import headers

def list_missing_imgs(col):
    photo_urls = [photo for photo in col.find({}, {"_id": 0, "photo": 1})]
    missing_photos = [p["photo"] for p in photo_urls if not os.path.isfile("../faces/"+p["photo"])]
    return missing_photos

def get_missing_photos(missing_urls):
    face_url = "http://cdn.ismfg.net/static/plfpl/img/shirts/photos/"
    for i, player_pic in enumerate(missing_urls, start=1):
        with open(player_pic, "wb") as face:
            try:
                request = urllib2.Request(face_url+player_pic, None, headers)
                feed = urllib2.urlopen(request)
                face.write(feed.read())
            except:
                print "Can't find picture "+player_pic
        if i%50 == 0:
            print "%d done!" % i
            sleep(3)