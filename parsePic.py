#-*- coding:utf-8 -*-

import os, time
import re, sys
import hashlib
import wget

from WebUtility import getWebContent

hash_md5 = hashlib.md5()

OUTPUT = "images"

def checkFolder(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)

def parseWebImages(targetUrl, folder, lstMd5Sum):
    html = getWebContent(targetUrl, False)
    print "Get web page '%s' complete" % targetUrl

    urlList = re.findall(r'[\'"]?([^\'" >]+)', html)
    i = 1
    for url in urlList:
        if ".jpg" in url and "http://" in url:
            os.popen('wget -nv "%s" -P %s' % (url, folder))
            # imgPath = wget.download(url, out = folder)
            # md5sum = md5(imgPath)
            # if md5sum not in lstMd5Sum:
            #     lstMd5Sum.append(md5sum)
            # else:
            #     os.remove(imgPath)
            #     print "Remove %s" % imgPath
            #time.sleep(0.2)
            print "\n"
        if i % 50 == 0 or i > len(urlList) - 3:
            print "[%.2f%%] %d / %d " % (i / float(len(urlList)) * 100, i, len(urlList))
        i += 1

def md5(fname):
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def loadMd5List(folder):
    lstMd5Sum = []
    fileList = os.listdir(folder)
    print "File count:%d" % len(fileList)
    removeCount = 0
    for f in fileList:
        if not f.endswith(".jpg"):
            newName = f + ".jpg"
            os.rename(os.path.join(folder, f), os.path.join(folder, newName))
            f = newName
        imgPath = os.path.join(folder, f)
        md5sum = md5(imgPath)
        if md5sum not in lstMd5Sum:
            lstMd5Sum.append(md5sum)
        else:
            os.remove(imgPath)
            removeCount += 1
    print "Remove:%d, Left:%d" % (removeCount, len(lstMd5Sum))
    return lstMd5Sum

if __name__ == '__main__':
    t = time.time()

    dicWebsites = {
        #OUTPUT + "/pornhub":"http://www.pornhub.com/",
        #OUTPUT + "/xnxx" : "http://www.xnxx.com/",
        #OUTPUT + "/xnxx1" : "http://www.xnxx.com/home/1"
        }

    for i in xrange(0, 109):
        # http://multi.xnxx.com/p-2
        #http://www.xnxx.com/best/108/
        dicWebsites[OUTPUT + "/xnxx_best_v%d" % i] = "http://www.xnxx.com/best/%d/" % i

    for folder, url in dicWebsites.iteritems():
        checkFolder(folder)
        lstMd5Sum = loadMd5List(folder)
        parseWebImages(url, folder, lstMd5Sum)
        loadMd5List(folder)

    print "spend:%.2fs" % (time.time() - t)
    print "Now we have %d images !!" % len(os.listdir("images"))
