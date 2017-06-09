#-*- coding:utf-8 -*-

import os, time
import re, sys
import hashlib
import imghdr
from shutil import copyfile

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

def getAllImages(folderPath, count, lstFolder):
    if os.path.isfile(folderPath):
        return count + 1

    lstPath = os.listdir(folderPath)
    for path in lstPath:
        if os.path.isfile(path) and (path.endswith(".jpg") or path.endswith(".jpeg")):
            count += 1
        else:
            count += getAllImages(os.path.join(folderPath, path), 0, lstFolder)
    lstFolder.append((folderPath, count))
    return count

def showFolderImgCount(lstFolder):
    lstFolder = sorted(lstFolder, key = lambda x : x[0])
    for folderPath, count in lstFolder:
       print "%s : %d" % (folderPath, count)

def copyFolderFiles(srcPath, tarFolder):
    copiedFiles = 0
    files = os.listdir(srcPath)
    for f in files:
        srcFilePath = os.path.join(srcPath, f)
        srcFileMd5 = md5(srcFilePath)
        tarFilePath = os.path.join(tarFolder, srcFileMd5 + ".jpg")
        copyfile(srcFilePath, tarFilePath)
        copiedFiles += 1
    return copiedFiles, len(files)

def mergeFolders(srcFolder, count, tarFolder):
    root_path = "/home/brad_chang/Share/dataset/xxx_images"
    totalSrcFile = 0
    copiedFiles = 0
    for i in xrange(1, count):
        src = srcFolder % i
        srcPath = os.path.join(root_path, src)
        copied, total = copyFolderFiles(srcPath, os.path.join(root_path, tarFolder))
        '''
        files = os.listdir(srcPath)
        totalSrcFile += len(files)
        for f in files:
            srcFilePath = os.path.join(root_path, srcPath, f)
            srcFileMd5 = md5(srcFilePath)
            tarFilePath = os.path.join(root_path, tarFolder, srcFileMd5 + ".jpg")
            copyfile(srcFilePath, tarFilePath)
            copiedFiles += 1
        '''
        totalSrcFile += total
        copiedFiles += copied
        print "%s folder complete " % src

    print "Copied %d / %d " % (copiedFiles, totalSrcFile)

def checkValidImage(srcFolder, format = "jpeg"):
    if os.path.isfile(srcFolder):
        if imghdr.what(srcFolder) != format:
            print "Invlaid format:%s, Remove : %s" % (imghdr.what(srcFolder), srcFolder)
            os.remove(srcFolder)
    else:
        lstPath = os.listdir(srcFolder)
        for path in lstPath:
            checkValidImage(os.path.join(srcFolder, path), format)

if __name__ == '__main__':
    t = time.time()

    dicWebsites = {
        #OUTPUT + "/pornhub":"http://www.pornhub.com/",
        #OUTPUT + "/xnxx" : "http://www.xnxx.com/",
        #OUTPUT + "/xnxx1" : "http://www.xnxx.com/home/1",
        }

    for i in xrange(0, 1):
        # http://multi.xnxx.com/p-2
        #http://www.xnxx.com/best/108/
        dicWebsites[OUTPUT + "/xnxx_best_v%d" % i] = "http://www.xnxx.com/best/%d/" % i
        pass

    for folder, url in dicWebsites.iteritems():
        checkFolder(folder)
        lstMd5Sum = loadMd5List(folder)
        parseWebImages(url, folder, lstMd5Sum)
        loadMd5List(folder)

    print "spend:%.2fs" % (time.time() - t)
    lstFolder = []
    print "Now we have %d images !!" % getAllImages(OUTPUT, 0, lstFolder)

    showFolderImgCount(lstFolder)
