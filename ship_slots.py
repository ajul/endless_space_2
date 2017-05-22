from _initpath import *
import os
import re
import xml.etree.ElementTree as ET
import itertools

def slotInfo(slot, extraCategories = []):
    techPrerequisite = slot.find('TechnologyPrerequisite')
                
    if techPrerequisite is None:
        techPrerequisite = ''
    else:
        techPrerequisite = techPrerequisite.text

    categories = [category.text for category in slot.findall('RestrictedModuleCategory')]
    categories += extraCategories
    categories = '/'.join(sorted(categories))

    return techPrerequisite, categories

battlesDir = os.path.join(baseDir, 'Simulation/Battles')

result = '{|class = "wikitable sortable"\n'
result += '! Name !! Slots \n'

for fileName in os.listdir(battlesDir):
    if not re.match('^HullDefinitions.*\.xml$', fileName): continue
    fullPath = os.path.join(battlesDir, fileName)
    if not os.path.isfile(fullPath): continue

    tree = ET.parse(fullPath)
    for hullDefinition in tree.findall('HullDefinition'):
        name = hullDefinition.attrib['Name']
        for shipDesignLayout in hullDefinition.findall('ShipDesignLayout'):
            result += '|-\n| ' + name + '\n|<ul>'

            # tech name -> list of slots
            techSlots = {}
            techSlots[''] = []
            
            for slot in shipDesignLayout.findall('.//WeaponSlot'):
                techPrerequisite, categories = slotInfo(slot, ['Weapon'])
                if techPrerequisite not in techSlots:
                    techSlots[techPrerequisite] = []
                techSlots[techPrerequisite].append(categories)
                
            for slot in shipDesignLayout.findall('.//Slot'):
                techPrerequisite, categories = slotInfo(slot)
                if techPrerequisite not in techSlots:
                    techSlots[techPrerequisite] = []
                techSlots[techPrerequisite].append(categories)

            for techPrerequisite, slots in sorted(techSlots.items()):
                if techPrerequisite == '':
                    for slot in sorted(slots):
                        result += '<li>' + slot + '</li>'
                else:
                    result += '<li>' + techPrerequisite + ':<ul>'
                    for slot in sorted(slots):
                        result += '<li>' + slot + '</li>'
                    result += '</ul></li>'
            result += '</ul>'
            result += '\n'

result += '|}\n'
print(result)
