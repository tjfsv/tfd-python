import math

import loadTfdModules
import loadTfdWeapons
import loadTfdModulesDefs as defs
import utils

def weaponDamageCalc(weapon, weaponModulesList):
    modifiers = {}
    totals = {}

    for m in defs.weaponStatValuetests:
        modifiers[utils.formatDictStr(m)] = 1
        totals[utils.formatDictStr(m)] = weapon[utils.formatDictStr(m)]

    for mod in weaponModulesList:
        mEff = mod['ModuleEffect']
        for m in defs.weaponStatValuetests:
            modifiers[utils.formatDictStr(m)] += utils.NoneToZero(mEff.get(utils.formatDictStr(m)))
    
    for m in defs.weaponStatValuetests:
        totals[utils.formatDictStr(m)] *= modifiers[utils.formatDictStr(m)]
        if utils.formatDictStr(m) == 'RoundsPerMagazine':
            totals[utils.formatDictStr(m)] = float(math.floor(totals[utils.formatDictStr(m)]))

    avgFirearmAtk = totals['FirearmAtk'] * (totals['FirearmCriticalHitRate'] * (totals['FirearmCriticalHitDamage'] - 1) + 1)
    avgFirearmAtkWeakPoint = avgFirearmAtk * (totals['WeakPointDamage'] + 0.25)
    
    roundsPerSecond = totals['FireRate'] / 60
    tShooting = totals['RoundsPerMagazine'] / roundsPerSecond
    tReloading = totals['ReloadTime']
    D = tShooting / (tReloading + tShooting)
    avgFirearmDps = avgFirearmAtk * roundsPerSecond * D
    avgFirearmWeakPointDps = avgFirearmAtkWeakPoint * roundsPerSecond * D

    return {'AvgFirearmDps':avgFirearmDps, 'AvgFirearmWeakPointDps':avgFirearmWeakPointDps}

def checkIfWeaponModIsValid(weaponModList, newMod):
    return True

def main():
    weaponModulesDict = loadTfdModules.loadTfdModules()
    weaponsDict = loadTfdWeapons.loadTfdWeapons()
    weapon = weaponsDict['ThunderCage']
    modsOfInterest = weaponModulesDict[weapon['WeaponRoundsType']]
    
    modList = [
        modsOfInterest['ActionAndReaction'],
        modsOfInterest['ConcentrationPriority'],
        modsOfInterest['ExpandWeaponCharge'],
        modsOfInterest['FireRateUp'],
        modsOfInterest['InsightFocus'],
        modsOfInterest['RiflingReinforcement'],
        modsOfInterest['BetterInsight'],
        modsOfInterest['BetterConcentration'],
        modsOfInterest['MagazineCompulsive'],
               ]
    
    print(weaponDamageCalc(weapon, modList))

    for i in range(10):
        pass
    pass

if __name__ == '__main__':
    main()