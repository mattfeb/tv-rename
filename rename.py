import sys
import os
import shutil
import re
import configparser
import PBar
from PBar import *
from time import strftime


def fixName(fileName, titleList):
    Season = ""
    Episode = ""
    fileType = ""

    # Check if the file is already fixed
    fixedRegex = re.compile(parser.get('regex', 'matchCorrect'))
    if fixedRegex.search(fileName): 
        return None

    for i in range(0, len(titleList)):
        title = titleList[i].replace(" ", "[\. _-]*")
        parser.set('regex', 'title', title)

        # Regular expression gets more generic 
        regex1 = re.compile(parser.get('regex', 're1'), re.IGNORECASE)
        regex2 = re.compile(parser.get('regex', 're2'), re.IGNORECASE)
        regex3 = re.compile(parser.get('regex', 're3'), re.IGNORECASE)

        if regex1.search(fileName):
            return getCorrectTitle(regex1, titleList[i], fileName)
        elif regex2.search(fileName):
            return getCorrectTitle(regex2, titleList[i], fileName)
        elif regex3.search(fileName):
            return getCorrectedTitle(regex3, titleList[i], fileName)

    return None

def getCorrectTitle(regex, title, fileName):
    season = " S" + getNum(regex.search(fileName).group(2))
    episode = " E" + getNum(regex.search(fileName).group(3))
    fileType = fileName[fileName.rfind("."):len(fileName)]

    return title + season + episode + fileType

def rename(downPath, titleListPath):
    output = open(parser.get('paths', 'logFilePath'), 'a')
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
                print("Failure trying to rename: " + downList[i])

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
    regexPattern = re.compile(parser.get('regex', 'matchCorrectTitle'))
    downList = os.listdir(downPath)

    for j in range(0, len(downList)):
        if regexPattern.search(downList[j]):
            totalCount += 1

    # Creates a simple progress bar 
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
                    print("Failure while moving a file")
                    raise
            else:
                try:
                    os.makedirs(storagePath + "\\" + title + "\Season " + season)
                    shutil.move(downPath + "\\" + downList[i], storagePath + "\\" + title + "\Season " + season)
                except shutil.Error as inst:
                    print("Unable to move: " + downList[i])
                    print(type(inst))
                except:
                    print("Failure while moving a file")
                    raise
    progress.progress(totalCount)


# Creates a configparser for paths/regular expressions
parser = configparser.ConfigParser()
parser.read(os.getcwd() + '/config.txt')

downPath = parser.get('paths', 'downPath')
titleListPath = parser.get('paths', 'titleListPath')
storagePath = parser.get('paths', 'storagePath')

rename(downPath, titleListPath)
moveFiles(downPath, storagePath)
