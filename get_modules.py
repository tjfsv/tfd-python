import pandas as pd
import re

def test1():
    def extractNumber(string_with_number):
        if string_with_number.count('.') > 0:
            nstr = re.findall(r'[0-9]+.[0-9]+',string_with_number)
        else:
            nstr = re.findall(r'[0-9]+',string_with_number)
        nstr = float(nstr[0])
        if string_with_number.count('-'):
            nstr = nstr * -1
        # if string_with_number.count('%'):
        #     nstr = nstr / 100
        return nstr/100

    a = extractNumber('test +12.2%')
    b = extractNumber('test +162%')
    c = extractNumber('test -15.3%')
    d = extractNumber('test -132%')

    a = pd.read_excel('TFD - Module Metadata.xlsx', 'Modules')
    modNameHeader = 'Name'
    modEffectHeader = 'Level 11 Effect'
    modSocketTypeHeader = 'Socket Type'
    modTierHeader = 'Tier'
    modClassHeader = 'Class'

    test1 = dict()

    # get info for max level mod
    for i, header in enumerate(a):
        if (header.count('Level') == 0) or (header.count('Effect') == 0):
            continue
        for j, header_val in enumerate(a[header]):
            if isinstance(header_val, float):
                continue
            test1[j] = header_val

    modNames = a[modNameHeader]
    modEffectsMaxLevel = list(test1.values())
    modSocketTypes = a[modSocketTypeHeader]
    modTiers = a[modTierHeader]
    modClasses = a[modClassHeader]
    # extract info from str
    modEffectsDict = {}
    for c in list(set(modClasses)):
        modEffectsDict[c] = {}

    for i, effectStr in enumerate(modEffectsMaxLevel):
        a = dict()

        if (modClasses[i] != 'Descendant') and (modTiers[i] != 'Ultimate') and (modNames[i].count('Enhancement') == 0):
            for effect in effectStr.split(','):
                if effect.lower().count('Firearm Atk'.lower()) > 0:
                    a['FirearmAtk'] = extractNumber(effect)
                if effect.lower().count('Fire Rate'.lower()) > 0:
                    a['FireRate'] = extractNumber(effect)
                if effect.lower().count('Firearm Critical Hit Rate'.lower()) > 0:
                    a['FirearmCriticalHitRate'] = extractNumber(effect)
                if effect.lower().count('Firearm Critical Hit Damage'.lower()) > 0:
                    a['FirearmCriticalHitDamage'] = extractNumber(effect)
                if effect.lower().count('Weak Point Damage'.lower()) > 0:
                    a['WeakPointDamage'] = extractNumber(effect)
                if effect.lower().count('Rounds per Magazine'.lower()) > 0:
                    a['RoundsPerMagazine'] = extractNumber(effect)
                if effect.lower().count('Reload Time Modifier'.lower()) > 0:
                    a['ReloadTimeModifier'] = extractNumber(effect)
        else:
            pass
        if len(a) > 0:
            a['PrimaryEffect'] = list(a.keys())[list(a.values()).index(max(a.values()))]
            a['Tier'] = modTiers[i]
            a['SocketType'] = modSocketTypes[i]
            modEffectsDict[modClasses[i]][modNames[i]] = a
    return modEffectsDict
