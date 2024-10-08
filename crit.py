from math import comb
from itertools import combinations
import get_modules

def ntz(x):
    if x is None:
        return 0
    else:
        return x

class gunDamageCalc:
    def __init__(self, modDict):
        self.modDict = modDict
    
    def calcGunDamage(self, modDictKeys, gun):
        FirearmAtkModifiers = 0
        FireRateModifiers = 0
        FirearmCriticalHitRateModifiers = 0
        FirearmCriticalHitDamageModifiers = 0
        WeakPointDamageModifiers = 0
        RoundsPerMagazineModifiers = 0
        ReloadTimeModifierModifiers = 0

        for modDictKey in modDictKeys:
            FirearmAtkModifiers += ntz(self.modDict[modDictKey].get('FirearmAtk'))
            FireRateModifiers += ntz(self.modDict[modDictKey].get('FireRate'))
            FirearmCriticalHitRateModifiers += ntz(self.modDict[modDictKey].get('FirearmCriticalHitRate'))
            FirearmCriticalHitDamageModifiers += ntz(self.modDict[modDictKey].get('FirearmCriticalHitDamage'))
            WeakPointDamageModifiers += ntz(self.modDict[modDictKey].get('WeakPointDamage'))
            RoundsPerMagazineModifiers += ntz(self.modDict[modDictKey].get('RoundsPerMagazine'))
            ReloadTimeModifierModifiers += ntz(self.modDict[modDictKey].get('ReloadTimeModifier'))

        FirearmAtkTotal = gun['FirearmAtk'] * (1 + FirearmAtkModifiers)
        FireRateTotal = gun['FireRate'] * (1 + FireRateModifiers)
        FirearmCriticalHitRateTotal = gun['FirearmCriticalHitRate'] * (1 + FirearmCriticalHitRateModifiers)
        FirearmCriticalHitDamageTotal = gun['FirearmCriticalHitDamage'] * (1 + FirearmCriticalHitDamageModifiers)
        WeakPointDamageTotal = gun['WeakPointDamage'] * (1 + WeakPointDamageModifiers)
        RoundsPerMagazineTotal = gun['RoundsPerMagazine'] * (1 + RoundsPerMagazineModifiers)
        ReloadTimeModifierTotal = gun['ReloadTime'] * (1 - ReloadTimeModifierModifiers)
        FirearmAtkAvg = FirearmAtkTotal * (FirearmCriticalHitRateTotal * (FirearmCriticalHitDamageTotal - 1) + 1)
        FirearmWeakPointAtkAvg = FirearmAtkAvg * (WeakPointDamageTotal + 0.25)

        timeShooting = RoundsPerMagazineTotal / (FireRateTotal / 60)
        timeReloading = ReloadTimeModifierTotal
        D = timeShooting / timeReloading

        FirearmDpsAvg = D * FirearmAtkAvg
        FirearmWeakPointAtkAvg = D * FirearmWeakPointAtkAvg
        return {'FirearmDpsAvg':FirearmDpsAvg, 'FirearmWeakPointAtkAvg':FirearmWeakPointAtkAvg, 'MaxAtkAvg':max(FirearmDpsAvg, FirearmWeakPointAtkAvg)}

    def checkIfModIsValid(self, modDictKeys, newMod):
        numPurpleFirearmAtkMods = int(self.modDict[newMod]['PrimaryEffect'] == 'FirearmAtk' and self.modDict[newMod]['Tier'] == 'Rare')
        maxPurpleFirearmAtkMods = 1
        numFireRateMods = int(self.modDict[newMod]['PrimaryEffect'] == 'FireRate')
        maxFireRateMods = 1
        numPurpleWeakpointMods = int(self.modDict[newMod]['PrimaryEffect'] == 'WeakPointDamage' and self.modDict[newMod]['Tier'] == 'Rare')
        maxPurpleWeakpointMods = 1
        numPurpleFirearmCriticalHitDamage = int(self.modDict[newMod]['PrimaryEffect'] == 'FirearmCriticalHitDamage' and self.modDict[newMod]['Tier'] == 'Rare')
        maxPurpleFirearmCriticalHitDamage = 1

        for modName in modDictKeys:
            numPurpleFirearmAtkMods += int(self.modDict[modName]['PrimaryEffect'] == 'FirearmAtk' and self.modDict[modName]['Tier'] == 'Rare')
            numFireRateMods += int(self.modDict[modName]['PrimaryEffect'] == 'FireRate')
            numPurpleWeakpointMods += int(self.modDict[modName]['PrimaryEffect'] == 'WeakPointDamage' and self.modDict[modName]['Tier'] == 'Rare')
            numPurpleFirearmCriticalHitDamage += int(self.modDict[modName]['PrimaryEffect'] == 'FirearmCriticalHitDamage' and self.modDict[modName]['Tier'] == 'Rare')

        if numPurpleFirearmAtkMods > maxPurpleFirearmAtkMods or \
           numFireRateMods > maxFireRateMods or \
           numPurpleWeakpointMods > maxPurpleWeakpointMods or\
           numPurpleFirearmCriticalHitDamage > maxPurpleFirearmCriticalHitDamage:
            return False
        else:
            return True

enduringLegacy = {'FirearmAtk':13155.0,\
                  
                  'FirearmCriticalHitRate':0.2,\
                  'FirearmCriticalHitDamage':2.3,\
                  'WeakPointDamage':1.0,\
                  'RoundsPerMagazine':115.0,\
                  'FireRate':571.0,\
                  'ReloadTime':2.7,\
                  'Class':'General Rounds'}

gdc = gunDamageCalc(get_modules.test1()[enduringLegacy['Class']])
a = gdc.calcGunDamage([], enduringLegacy)

evaluation_metric = 'MaxAtkAvg'
modNameList = []
modDictKeys = list(gdc.modDict.keys())

for j in range(10):
    max_i = -1
    max_modName = None
    max_dmgIncrease = -1
    current_dps = gdc.calcGunDamage(modNameList, enduringLegacy)[evaluation_metric]
    for i, modName in enumerate(modDictKeys):
        dmgIncrease = gdc.calcGunDamage(modNameList + [modName], enduringLegacy)[evaluation_metric] / current_dps
        if dmgIncrease > max_dmgIncrease:
            validMod = gdc.checkIfModIsValid(modNameList, modName)

            if validMod is True:    
                max_i = i
                max_modName = modName
                max_dmgIncrease = dmgIncrease
            else:
                modDictKeys.remove(modName)

    modDictKeys.remove(max_modName)
    modNameList = modNameList + [max_modName]
pass
# class addCrit:
#     def __init__(self, addRate, addDmg):
#         self.addRate = addRate
#         self.addDmg = addDmg

# class baseCrit:
#     def __init__(self, baseRate, baseDmg, reactor):
#         self.baseRate = baseRate
#         self.baseDmg = baseDmg
#         self.reactor = reactor

# class critCalc:
#     def __init__(self, baseCrit, addCritDict):
#         self.baseCrit = baseCrit
#         self.addCritDict = addCritDict
    
#     def calcDamage(self, addCritKeys):
#         addRate = self.baseCrit.reactor.addRate
#         addDmg = self.baseCrit.reactor.addDmg
#         for i in addCritKeys:
#             addRate += self.addCritDict[i].addRate
#             addDmg += self.addCritDict[i].addDmg
#         finalCritRate = min(self.baseCrit.baseRate * (1 + addRate), 1)
#         finalCritDmg = self.baseCrit.baseDmg * (1 + addDmg)
#         finalDmg = finalCritRate * finalCritDmg
#         return {'damage':round(finalDmg, 2), 'crit rate':round(finalCritRate, 2),'crit_damage':round(finalCritDmg, 2)}

# bunny = baseCrit(0.25, 1.3, addCrit(0, 0.249))

# addCritDict = {'skill_insight':addCrit(1.154, 0),
#                'skill_concentration':addCrit(0, 1.154),
#                'front_lines':addCrit(0.227, 0.646),
#                'emergency_measures':addCrit(0.646, 0.247),}
# a = {}
# cc = critCalc(bunny, addCritDict)
# for i in range(len(addCritDict)):
#     numberOfMods = len(addCritDict) - i
#     modListList = list(combinations(addCritDict.keys(), numberOfMods))
#     modListDict = {}
#     for modList in modListList:
#         modListDict[','.join(modList)] = cc.calcDamage(modList)
#     print(modListDict)
#     a[numberOfMods] = modListDict