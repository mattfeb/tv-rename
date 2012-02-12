import sys, os, shutil, glob, re, PBar
from PBar import *
from time import strftime

#################################################

def fixName(fileName, titleList):
    Season = ""
    Episode = ""
    fileType = ""

    # Check if the file is already fixed
    fixedRegex = re.compile("[\w ]*S\d\d E\d\d\.[\w]*")
    if fixedRegex.search(fileName): return None

    for i in range(0, len(titleList)):
        title = titleList[i].replace(" ", "[\. _-]*")
        regex1 = re.compile("[\w\d\. '-]*(" + title + ")[\w\d\. '-\[\]\{\}]*S(\d\d)[\w\. ]*E(\d\d)[\w\d\. '-\[\]\{\}]*", re.IGNORECASE)
        regex2 = re.compile("[\w\d\. '-]*(" + title + ")[\w\d\. '-\[\]\{\}]*(\d\d)[\.x]*(\d\d)[\w\d\. '-\[\]\{\}]*", re.IGNORECASE)
        regex3 = re.compile("[\w\d\. '-]*(" + title + ")[\w\d\. '-\[\]\{\}]*(\d)[\w\. ]*(\d\d)[\w\d\. '-\[\]\{\}]*", re.IGNORECASE)

        if regex1.search(fileName):
            return getCorrectTitle(regex1, titleList[i], fileName)

        elif regex2.search(fileName):
            return getCorrectTitle(regex2, titleList[i], fileName)

        elif regex3.search(fileName):
            return getCorrectedTitle(regex3, titleList[i], fileName)

    return None

def getCorrectTitle(regex, title, fileName):
    season   = " S" + getNum(regex.search(fileName).group(2))
    episode  = " E" + getNum(regex.search(fileName).group(3))
    fileType = fileName[fileName.rfind("."):len(fileName)]

    return title + season + episode + fileType

def rename(downPath, titleListPath):
    output = open(outputFileLocation, 'a')
    output.write(strftime("%d %b %Y %I:%M:%S") + "\n")

    titleList = list(line.strip() for line in open(titleListPath))
    downList = os.listdir(downPath)
    os.chdir(downPath)

    for i in range(0, len(downList)):
        originalFileName = downList[i]
        fixed = fixName(downList[i], titleList)

        if fixed is not None :
            output.write(originalFileName + "\n")
            output.write(fixed + "\n\n")

            print("Original: " + originalFileName)
            print("Fixed:    " + fixed + "\n")

            try:
                os.rename(downList[i], fixed)
            except:
                print("Yeah...Something happened, I'm going to need you to come in on sunday.")

    output.close()

def getNum(n):
    number = int(n)
    if int(n) < 10:
        return "0" + str(number) 
    else:
        return n


def moveFiles(downPath, storagePath):
    totalCount = 0
    count = 0
    regexPattern = re.compile("([\w \d\.-]+)S(\d\d) E(\d\d)")
    downList = os.listdir(downPath)

    for j in range(0, len(downList)):
        if regexPattern.search(downList[j]):
            totalCount += 1

    progress = PBar(totalCount)

    for i in range(0, len(downList)):
        if regexPattern.search(downList[i]):
            progress.progress(count)
            count += 1

            title = regexPattern.search(downList[i]).group(1).strip()
            seasonInt = int(regexPattern.search(downList[i]).group(2))
            season = str(seasonInt)

            if os.path.exists(storagePath + "\\" + title + "\Season " + season):
                try:
                    shutil.move(downPath + "\\" + downList[i], storagePath + "\\" + title + "\Season " + season)
                except(shutil.Error):
                    print("Unable to move: " + downList[i])
                except:
                    print("Something broke while moving a file, sorry and please come again")
                    raise
            else:
                try:
                    os.makedirs(storagePath + "\\" + title + "\Season " + season)
                    shutil.move(downPath + "\\" + downList[i], storagePath + "\\" + title + "\Season " + season)
                except shutil.Error as inst:
                    print("Unable to move: " + downList[i])
                    print(type(inst))
                except:
                    print("Something broke while moving a file, sorry and please come again")
                    raise
    progress.progress(totalCount)

#################################################
titleList = "C:/tv-rename/names.txt"
outputFileLocation = "C:/tv-rename/output.txt"

downPath = sys.argv[1]
storagePath = sys.argv[2]

rename(downPath, titleList)
moveFiles(downPath, storagePath)
