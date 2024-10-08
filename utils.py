def NoneToZero(number):
    ret = 0
    if number is not None:
        ret = number
    return ret

def formatDictStr(dictStr):
    return dictStr.title().replace(' ', '').replace('-', '')