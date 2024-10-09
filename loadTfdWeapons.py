import loadTfdWeaponsDefs as defs
import utils

def loadTfdWeapons():
    weaponList = utils.getDictFromJson('metadata/weapon.json')
    weaponDict = {}
    for weapon in weaponList:
        wDict = {}
        for key in weapon.keys():
            if key in defs.weaponInfoToKeep:
                wDict[utils.formatDictStr(key)] = utils.formatDictStr(weapon[key])
        for stat in weapon['base_stat']:
            if stat['stat_id'] in defs.statIdsDict.keys():
                wDict[utils.formatDictStr(defs.statIdsDict[stat['stat_id']])] = stat['stat_value']
                if stat['stat_id'] == '105000030': # divide firearm critical hit rate by 100
                    wDict[utils.formatDictStr(defs.statIdsDict[stat['stat_id']])] /= 100
        wDict[utils.formatDictStr('firearm_atk')] = weapon['firearm_atk'][99]['firearm'][0]['firearm_atk_value']
        weaponDict[utils.formatDictStr(weapon['weapon_name'])] = wDict
    return weaponDict

def main():
    modulesDict = loadTfdWeapons()
    pass

if __name__ == '__main__':
    main()