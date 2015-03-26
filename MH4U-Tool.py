import sqlite3 as sql
import tkinter as tk
import DamageCalculator as MH4UCalculator
class Application(tk.Frame):
	def __init__(self, master=None):
		tk.Frame.__init__(self, master)
		self.grid()
		self.column = 1
		self.lastRow = 0
		self.modifiers = {"Hammers":5.2, "HuntingHorns":5.2, "SwitchAxes":5.4,
						  "GreatSwords":4.2, "ChargeBlades":3.6, "LongSwords":3.3,
						  "InsectGlaives":3.1, "Lances":2.3, "Gunlances":2.3,
						  "HeavyBowguns":1.5, "SwordnShields":1.4, "DualBlades":1.4,
						  "LightBowguns":1.3, "Bow":1.2}
		self.rawSharpnessLevels = {"Purple":1.45, "White":1.32, "Blue":1.20,
								   "Green":1.05, "Yellow":1.00, "Orange":0.75,
								   "Red":0.50}
		self.eleSharpnessLevels = {"Purple":1.20, "White":1.12, "Blue":1.06,
								   "Green":1.00, "Yellow":0.75, "Orange":0.50,
								   "Red":0.25}
		self.attackAdditions = {"AuS":10, "AuM":15, "AuL":20, "AuXL":25,
								"Kitchen Attack Small":5, "Kitchen Attack Large":7,
								"Might Seed":10, "Might Pill":25, "None":0}
		self.affinityAdditions = {"CE+1":0.10, "CE+2":0.15, "CE+3":0.20,
								  "Critical God":0.30, "None":0}
		self.attackMultipliers = {"HH AuS":1.10, "HH AuL":1.15,
								  "Adrenaline+2":1.30, "Felyne Heroics":1.35,
								  "Fortify Cartx1":1.1, "Fortify Cartx2":1.21, "None":1}
		self.weaponAffinityMultipliers = {"Hammers":0.25, "HuntingHorns":0.25, "SwitchAxes":0.25,
										  "GreatSwords":0.2, "ChargeBlades":0.25, "LongSwords":0.25,
										  "InsectGlaives":0.25, "Lances":0.25, "Gunlances":0.25,
										  "HeavyBowguns":0.25, "SwordnShields":0.35, "DualBlades":0.35,
										  "LightBowguns":0.25, "Bow":0.35}

		self.elementMultipliers = {"Element+1":1.05, "Element+2":1.10, "Element+3":1.15, "None":1}
		self.elementAdditions = {"Element+1":40, "Element+2":60, "Element+3":90, "None":0}
		self.createWidgets()

	def createWidgets(self):
		self.calculateButton = tk.Button(self, text="Calculate!", command=self.printDamage)
		self.calculateButton.grid(row=0, sticky="w")
		self.refreshButton = tk.Button(self, text="Refresh", command=self.refreshWidgets)
		self.refreshButton.grid(row=1, sticky="w")
		self.createWeaponTypeList()
		self.createWeaponList()
		self.chosenGlove = tk.StringVar()
		self.chosenAttack = tk.StringVar()
		self.chosenCriticalEye = tk.StringVar()
		self.chosenKitchen = tk.StringVar()
		self.chosenMight = tk.StringVar()
		self.chosenHHBuff = tk.StringVar()
		self.chosenDanger = tk.StringVar()
		self.chosenFortify = tk.StringVar()
		self.chosenElementUp = tk.StringVar()
		self.createButtons(self.chosenKitchen, ["None", "Kitchen Attack Small", "Kitchen Attack Large"])
		self.createButtons(self.chosenMight, ["None", "Might Seed", "Might Pill"])
		self.createButtons(self.chosenHHBuff, ["None", "HH AuS", "HH AuL"])
		self.createButtons(self.chosenDanger, ["None", "Adrenaline+2", "Felyne Heroics"])
		self.createButtons(self.chosenFortify, ["None", "Fortify Cartx1", "Fortify Cartx2"])
		self.createButtons(self.chosenElementUp, ["None", "Element+1", "Element+2", "Element+3"])
		self.createButtons(self.chosenAttack, ["None", "AuS", "AuM", "AuL", "AuXL"])
		self.createButtons(self.chosenCriticalEye, ["None", "CE+1", "CE+2", "CE+3", "Critical God"])
		self.createButtons(self.chosenGlove, ["None", "Peak Performance", "Latent Power+1", "Latent Power+2", "Challenger+1", "Challenger+2"])
		self.createText()
		self.createMiscButtons()

	def refreshWidgets(self):
		try:
			self.weaponsMenu.destroy()
			oldColumn = self.column
			self.column = 1
			self.createWeaponList()
			self.column = oldColumn
		except:
			oldColumn = self.column
			self.column = 1
			self.createWeaponList()
			self.column = oldColumn

	def createButtons(self, strVar, lst):
		r = 0
		strVar.set(lst[0])
		for item in lst:
			b = tk.Radiobutton(self, text = item, variable = strVar, value = item)
			b.grid(row=r, column=self.column, sticky="w")
			r += 1
		self.column += 1
		if (r > self.lastRow):
			self.lastRow = r

	def createWeaponTypeList(self):
		optionList = ["WeaponType"]
		for weaponType in self.modifiers.keys():
			optionList.append(weaponType)
		self.chosenType = tk.StringVar()
		self.chosenType.set(optionList[0])
		weaponsTypeMenu = tk.OptionMenu(self, self.chosenType, *optionList)
		weaponsTypeMenu.grid(row=0, column=self.column, sticky="w")

	def createWeaponList(self):
		optionList = []
		if (self.chosenType.get() == "WeaponType"):
			self.column += 1
			return
		for row in c.execute("SELECT name FROM '" + self.chosenType.get() + "'"):
			optionList.append(row[0])
		self.chosenWeapon = tk.StringVar()
		self.chosenWeapon.set(optionList[0])
		self.weaponsMenu = tk.OptionMenu(self, self.chosenWeapon, *optionList)
		self.weaponsMenu.grid(row=1, column=self.column, sticky="w")
		self.column += 1

	def createMiscButtons(self):
		self.sharpness = tk.IntVar()
		c = tk.Checkbutton(self, text="Sharpness+1", variable=self.sharpness)
		c.grid(row=self.lastRow, column=0, sticky="w")

		self.powerCharm = tk.IntVar()
		c = tk.Checkbutton(self, text="Power Charm", variable=self.powerCharm)
		c.grid(row=self.lastRow, column=1, sticky="w")

		self.powerTalon = tk.IntVar()
		c = tk.Checkbutton(self, text="Power Talon", variable=self.powerTalon)
		c.grid(row=self.lastRow, column=2, sticky="w")
		
		self.weaknessExploit = tk.IntVar()
		c = tk.Checkbutton(self, text="Weakness Exploit", variable=self.weaknessExploit)
		c.grid(row=self.lastRow, column=3, sticky="w")

		self.criticalDraw = tk.IntVar()
		c = tk.Checkbutton(self, text="Critical Draw", variable=self.criticalDraw)
		c.grid(row=self.lastRow, column=4, sticky="w")

		self.elementAtkUp = tk.IntVar()
		c = tk.Checkbutton(self, text="Element Atk Up", variable=self.elementAtkUp)
		c.grid(row=self.lastRow, column=5, sticky="w")

		self.HHReplay = tk.IntVar()
		c = tk.Checkbutton(self, text="HH Replay", variable=self.HHReplay)
		c.grid(row=self.lastRow, column=6, sticky="w")

		self.elementHHBuff = tk.IntVar()
		c = tk.Checkbutton(self, text="HH Element", variable=self.elementHHBuff)
		c.grid(row=self.lastRow, column=7, sticky="w")

	def createText(self):
		self.rawText = tk.StringVar()
		self.eleText = tk.StringVar()
		self.totalText = tk.StringVar()
		self.rawText.set("Damage from raw: 0.00")
		self.eleText.set("Damage from element: 0.00")
		self.totalText.set("Total damage: 0.00")
		rawLabel = tk.Label(self, textvariable=self.rawText)
		eleLabel = tk.Label(self, textvariable=self.eleText)
		totalLabel = tk.Label(self, textvariable=self.totalText)
		rawLabel.grid(row=0, column=self.column, sticky="w")
		eleLabel.grid(row=1, column=self.column, sticky="w")
		totalLabel.grid(row=2, column=self.column, sticky="w")
		self.column += 1

	def createModifiers(self):
		raw = {"AuX":self.chosenAttack.get(), "kitchen":self.chosenKitchen.get(), "seed":self.chosenMight.get(),
						"glove":self.chosenGlove.get(), "danger":self.chosenDanger.get(), "fortify":self.chosenFortify.get(),
						"powerCharm":"None", "powerTalon":"None", "HH":self.chosenHHBuff.get(), "replay":0}
		if (self.powerCharm.get() == 1):
			raw['powerCharm'] = "PowerCharm"
		if (self.powerTalon.get() == 1):
			raw['powerTalon'] = "PowerTalon"
			
		element = {"addition":self.chosenElementUp.get(), "multiplier":self.chosenElementUp.get(), "elementAtkUp":1, "HH":1, "replay":0}
		if (self.elementAtkUp.get() == 1):
			element['elementAtkUp'] = 1.1
		if (self.elementHHBuff.get() == 1):
			element['HH'] = 1.1
		
		affinity = {"addition":self.chosenCriticalEye.get(), "glove":self.chosenGlove.get(), "criticalDraw":0}
		if (self.criticalDraw.get() == 1):
			affinity['criticalDraw'] = 1
		
		rawHitzone = {"weaknessExploit":False}
		if (self.weaknessExploit.get() == 1):
			rawHitzone['weaknessExploit'] = True
		
		eleHitzone = {}
		if (self.HHReplay == 1):
			raw["replay"] = 0.05
			ele["replay"] = 0.05
		
		modifiers = {"raw":raw, "element":element, "affinity":affinity, "rawHitzone":rawHitzone, "eleHitzone":eleHitzone}
		return modifiers
		
	def printDamage(self):
		weapon = self.chosenWeapon.get()
		c.execute("SELECT * FROM \"" + self.chosenType.get() + "\" WHERE name=\"" + weapon + "\"")
		row = c.fetchone()
		modifiers = self.createModifiers()
		calculatedDamage = MH4UCalculator.calculateDamage(0.45, 0.20, self.sharpness.get(), self.chosenType.get(), modifiers, row)
		self.rawText.set("Damage from raw: {0:.2f}".format(calculatedDamage['rawDamage']))
		self.eleText.set("Damage from element: {0:.2f}".format(calculatedDamage['eleDamage']))
		self.totalText.set("Total damage: {0:.2f}".format(calculatedDamage['totalDamage']))
	

if __name__ == '__main__':
	conn = sql.connect("MH4U.db")
	conn.row_factory = sql.Row
	c = conn.cursor()
	root = tk.Tk()
	root.wm_title("MH4U-Tool")
	app = Application(master=root)
	app.mainloop()
	conn.close()
