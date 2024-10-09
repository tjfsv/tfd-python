import json
import re
import loadTfdModulesDefs as defs
import utils

def loadTfdModules():
    # TODO Handle ultimate mods, Enhancement mods, Priority mods
    def parseWeaponStatValue(mod):
        modEffects = {}

        if mod['module_tier'] == 'Ultimate':
            return modEffects
        elif 'Enhancement' in mod['module_name']:
            return modEffects
        
        statValueStrS = mod['module_stat'][-1]['value']
        for s in statValueStrS.split(','):
            for key in defs.weaponStatValuetests:
                if key.lower() in s.lower():
                    modEffects[utils.formatDictStr(key)] = utils.getNumberFromString(s) * (-2 * (key == 'Reload Time') + 1)
            
        return modEffects

    moduleList = utils.getDictFromJson('metadata/module.json')
    modDict = dict()

    for mod in moduleList:
        if mod['module_class'] == 'Descendant':
            pass
        else:
            effect = parseWeaponStatValue(mod)
            if len(effect) > 0:
                moduleClassStr = utils.formatDictStr(mod['module_class'])
                if moduleClassStr not in modDict:
                    modDict[moduleClassStr] = {}
                a = {}
                for modInfo in defs.moduleInfoToKeep:
                    a[utils.formatDictStr(modInfo)] = utils.formatDictStr(mod[modInfo])
                a[utils.formatDictStr('module_effect')] = effect
                modDict[moduleClassStr][utils.formatDictStr(mod['module_name'])] = a
    return modDict

def main():
    modulesDict = loadTfdModules()
    pass

if __name__ == '__main__':
    main()