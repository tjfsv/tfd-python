import json
import re
import loadTfdModulesDefs as defs
import utils

metadata_folder = 'metadata'
f = open( metadata_folder + '/module.json', 'r')
moduleList = json.load(f)
f.close()

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

def parseWeaponStatValue(mod):
    modEffects = {}

    if mod['module_tier'] == 'Ultimate':
        return modEffects
    elif 'Enhancement' in mod['module_name']:
        return modEffects
    elif 'Priority' in mod['module_name']:
        return modEffects
    
    statValueStrS = mod['module_stat'][-1]['value']
    for s in statValueStrS.split(','):
        for key in defs.weaponStatValuetests:
            if key.lower() in s.lower():
                modEffects[utils.formatDictStr(key)] = getNumberFromString(s)
    return modEffects

modListNew = list()
modDict = dict()
for mod in moduleList:
    modMaxLevelStatValue = mod['module_stat'][-1]['value']
    if mod['module_class'] == 'Descendant':
        pass
    else:
        effect = parseWeaponStatValue(mod)
        if len(effect) > 0:
            asdf = utils.formatDictStr(mod['module_class'])
            if asdf not in modDict:
                modDict[asdf] = {}
            modListNew.append(mod | {'module_effect':effect})
pass