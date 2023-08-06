from urllib import request
import urllib

import easygui as easygui
import numpy as np


def setup(url):
    req = urllib.request.urlopen(url)
    return req.read().decode("utf8")


def likes(url):
    url = setup(url)
    return str(url).split(
        'likes"}},"simpleText":"')[1].split(
        '"')[0]



def views(url):
    url = setup(url)
    return str(url).split('viewCount":"')[1].split('"')[0]


def subs(url):
    url = setup(url)
    return str(url).split('subscriberCountText":{"accessibility":{"accessibilityData":{"label":"')[1].split(
        ' abonnenter"')[0]


def dislikes(url):
    url = setup(url)
    return str(url).split('DISLIKE"},"defaultText":{"accessibility":{"accessibilityData":{"label":"')[1].split(
        ' dislikes')[0]


def creator(url):
    url = setup(url)
    return str(url).split('author":"')[1].split('"')[0]


def is_private(url):
    url = setup(url)
    return str(url).split('isPrivate":')[1].split(',"')[0]


def average_rating(url):
    url = setup(url)
    return str(url).split('averageRating":')[1].split(',"')[0]

def finish(url):

    if np.isscalar(url) == False:
        for i in url:
            print("\n\nCreator: " + creator(
                i) + "\nViews: " + views(
                i) + "\nSubscribers: " + subs(i) + "\nLikes: " + likes(
                i) + "\nDislikes: " + dislikes(
                i) + "\n\nADDITIONAL INFO:\n\nIs Private: " + is_private(
                i) + "\nAverage Ratings: " + average_rating(i) + "\n\n")


    else:
        print("Creator: " + creator(
            url) + "\nViews: " + views(
            url) + "\nSubscribers: " + subs(url) + "\nLikes: " + likes(
            url) + "\nDislikes: " + dislikes(
            url) + "\n\nADDITIONAL INFO:\n\nIs Private: " + is_private(
            url) + "\nAverage Ratings: " + average_rating(url) + "\n")





