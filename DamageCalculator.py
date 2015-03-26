import sqlite3 as sql
	
def calculateSharpness(sharpness : int, row) -> list:
	'''
	This will calculate the sharpness level multiplier given
	a 1 for sharpness+1 and 0 for no sharpness+1 and the row
	Returns a list with the 0th element containing the 
	rawSharpness multiplier and the 1st element containing
	the eleSharpness multiplier
	'''
	rawSharpnessLevels = {"Purple":1.45, "White":1.32, "Blue":1.20,
							"Green":1.05, "Yellow":1.00, "Orange":0.75,
							"Red":0.50}
	eleSharpnessLevels = {"Purple":1.20, "White":1.12, "Blue":1.06,
							"Green":1.00, "Yellow":0.75, "Orange":0.50,
							"Red":0.25}
	result = []
	level = "sharpness"
	if (sharpness == 1):
		level += "+1"
	result.append(rawSharpnessLevels[row[level]])
	result.append(eleSharpnessLevels[row[level]])
	return result

def calculateRaw(modifiers : dict, weaponType : str, row) -> float:
	'''
	This will calculate the true raw given the raw and
	its modifiers. Returns a float of the true raw
	'''
	weaponModifiers = {"Hammers":5.2, "HuntingHorns":5.2, "SwitchAxes":5.4,
						"GreatSwords":4.2, "ChargeBlades":3.6, "LongSwords":3.3,
						"InsectGlaives":3.1, "Lances":2.3, "Gunlances":2.3,
						"HeavyBowguns":1.5, "SwordnShields":1.4, "DualBlades":1.4,
						"LightBowguns":1.3, "Bow":1.2}
	attackAdditions = {"AuS":10, "AuM":15, "AuL":20, "AuXL":25,
						"Kitchen Attack Small":5, "Kitchen Attack Large":7,
						"Might Seed":10, "Might Pill":25, "None":0,
						"Challenger+1":10, "Challenger+2":25, "Peak Performance":20,
						"PowerCharm":6, "PowerTalon":9}
	attackMultipliers = {"HH AuS":1.10, "HH AuL":1.15,
							"Adrenaline+2":1.30, "Felyne Heroics":1.35,
							"Fortify Cartx1":1.1, "Fortify Cartx2":1.21, "None":1}
	result = (row['attack']/weaponModifiers[weaponType])
	result += attackAdditions[modifiers['AuX']]
	result += attackAdditions[modifiers['kitchen']]
	result += attackAdditions[modifiers['seed']]
	result += attackAdditions[modifiers['glove']]
	result += attackAdditions[modifiers['powerCharm']] + attackAdditions[modifiers['powerTalon']]
	result *= (attackMultipliers[modifiers['HH']] + modifiers['replay'])
	result *= attackMultipliers[modifiers['danger']]
	result *= attackMultipliers[modifiers['fortify']]
	return result
	
def calculateElement(modifiers : dict, row) -> float:
	'''
	This will calculate the true element given the element and
	its modifiers. Returns a float of the true element
	'''
	elementAdditions = {"Element+1":40, "Element+2":60, "Element+3":90, "None":0}
	elementMultipliers = {"Element+1":1.05, "Element+2":1.10, "Element+3":1.15, "None":1}
	result = (row['special attack'] + elementAdditions[modifiers['addition']])/10
	elementMultiplier = elementMultipliers[modifiers['multiplier']] * modifiers['HH'] * modifiers['elementAtkUp']
	if (elementMultiplier > 1.2):
		elementMultiplier = 1.2
	return result * elementMultiplier

def calculateAffinity(modifiers : dict, row) -> float:
	'''
	This will calculate the true affinity given the affinity and 
	its modifiers. Returns a float of the true affinity
	'''
	affinityAdditions = {"CE+1":0.10, "CE+2":0.15, "CE+3":0.20, "Critical God":0.30, "None":0, 
							"Latent Power+1":0.30, "Latent Power+2":0.50, 
							"Challenger+1":0.10, "Challenger+2":0.20}
	result = row['affinity'] 
	result += affinityAdditions[modifiers['addition']] 
	result += affinityAdditions[modifiers['glove']]
	result += modifiers['criticalDraw'] 
	if (result > 1):
		result = 1
	return result
	
def calculateRawHitzone(rawHitzone : float, modifiers : dict) -> float:
	result = rawHitzone
	if (rawHitzone > 0.45 and modifiers['weaknessExploit']):
		result += 0.05
	return result
	
def calculateEleHitzone(eleHitzone : float, modifiers : dict) -> float:
	result = eleHitzone
	return result
	
def calculateWeaponAffinityMultiplier(weaponType : str) -> float:
	weaponAffinityModifiers = {"Hammers":0.25, "HuntingHorns":0.25, "SwitchAxes":0.25,
								"GreatSwords":0.2, "ChargeBlades":0.25, "LongSwords":0.25,
								"InsectGlaives":0.25, "Lances":0.25, "Gunlances":0.25,
								"HeavyBowguns":0.25, "SwordnShields":0.35, "DualBlades":0.35,
								"LightBowguns":0.25, "Bow":0.35}
	result = weaponAffinityModifiers[weaponType]
	return result

def calculateDamage(rawHitzone : float, eleHitzone : float, sharpness : int, weaponType : str, modifiers : dict, row) -> dict:
	'''
	This will calculate the damage given a whole list of 
	parameters. Returns a dict of floats (rawDamage), (eleDamage), (totalDamage)
	'''
	sharpnessLevels = calculateSharpness(sharpness, row)
	trueRawSharpness = sharpnessLevels[0]
	trueEleSharpness = sharpnessLevels[1]
	trueElement = calculateElement(modifiers['element'], row)
	trueAffinity = calculateAffinity(modifiers['affinity'], row)
	trueRaw = calculateRaw(modifiers['raw'], weaponType, row)
	trueRawHitzone = calculateRawHitzone(rawHitzone, modifiers['rawHitzone'])
	trueEleHitzone = calculateEleHitzone(eleHitzone, modifiers['eleHitzone'])
	trueAffinityMultiplier = calculateWeaponAffinityMultiplier(weaponType)
	trueMotionValue = 0.48
	
	rawDamage = trueRaw * (1 + trueAffinityMultiplier * trueAffinity) * trueMotionValue * trueRawHitzone * trueRawSharpness
	eleDamage = trueElement * trueEleHitzone * trueEleSharpness
	totalDamage = rawDamage + eleDamage
	result = {"rawDamage":rawDamage, "eleDamage":eleDamage, "totalDamage":totalDamage}
	
	return result
