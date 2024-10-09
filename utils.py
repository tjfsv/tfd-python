import json
import re

def NoneToZero(number):
    ret = 0
    if number is not None:
        ret = number
    return ret

# Format: No spaces, dashes, underscores; first letter of each word is capitalized
def formatDictStr(dictStr):
    if dictStr is None:
        return ""
    return dictStr.title().replace(' ', '').replace('-', '').replace('_', '')

def getDictFromJson(jsonFilename):
    f = open(jsonFilename, 'r')
    jsonDict = json.load(f)
    f.close()
    return jsonDict

def getNumberFromString(stringWithNumber):
    if stringWithNumber.count('.') > 0:
        numStr = re.findall(r'[0-9]+.[0-9]+', stringWithNumber)
    else:
        numStr = re.findall(r'[0-9]+', stringWithNumber)
    numStr = float(numStr[0])
    if stringWithNumber.count('-'):
        numStr = numStr * -1
    if stringWithNumber.count('%'):
        numStr = numStr / 100
    return numStr