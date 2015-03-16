import sqlite3 as sql
import tkinter as tk

class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid()
        self.column = 1
        self.lastRow = 0
        self.createWidgets()
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

        self.elementMultipliers = {"Element+1":1.05, "Element+2":1.10, "Element+3":1.15, "None":1}
        self.elementAdditions = {"Element+1":40, "Element+2":60, "Element+3":90, "None":0}

    def createWidgets(self):
        self.calculateButton = tk.Button(self, text="Calculate!", command=self.calculateDamage)
        self.calculateButton.grid(row=0, sticky="w")
        self.createList()
        self.createKitchenButtons()
        self.createMightButtons()
        self.createDangerBuffButtons()
        self.createFortifyButtons()
        self.createHHBuffButtons()
        self.createElementUpButtons()
        self.createAttackButtons()
        self.createAffinityButtons()
        self.createGloveButtons()
        self.createText()
        self.createMiscButtons()

    def createTextLabels(self, r, t):
        l = tk.Label(self, text=t)
        l.grid(row=r, column=self.column, sticky="w")

    def createList(self):
        optionList = []
        for row in c.execute('SELECT name FROM ChargeBlades'):
            optionList.append(row[0])
        self.chosenWeapon = tk.StringVar()
        self.chosenWeapon.set(optionList[0])
        weaponsMenu = tk.OptionMenu(self, self.chosenWeapon, *optionList)
        weaponsMenu.grid(row=0, column=self.column, sticky="w")
        self.column += 1
            
    def createGloveButtons(self):
        r = 0
        self.chosenGlove = tk.StringVar()
        gloves = ["None", "Peak Performance", "Latent Power+1", "Latent Power+2", "Challenger+1", "Challenger+2"]
        self.chosenGlove.set("None")
        for glove in gloves:
            b = tk.Radiobutton(self, text = glove, variable = self.chosenGlove, value = glove)
            b.grid(row=r, column=self.column, sticky="w")
            r += 1
        self.column += 1
        if (r > self.lastRow):
            self.lastRow = r

    def createAttackButtons(self):
        r = 0
        self.chosenAttack = tk.StringVar()
        attacks = ["None", "AuS", "AuM", "AuL", "AuXL"]
        self.chosenAttack.set("None")
        for attack in attacks:
            b = tk.Radiobutton(self, text = attack, variable = self.chosenAttack, value = attack)
            b.grid(row=r, column=self.column, sticky="w")
            r += 1
        self.column += 1
        if (r > self.lastRow):
            self.lastRow = r

    def createAffinityButtons(self):
        r = 0
        self.chosenCriticalEye = tk.StringVar()
        criticalEyes = ["None", "CE+1", "CE+2", "CE+3", "Critical God"]
        self.chosenCriticalEye.set("None")
        for criticalEye in criticalEyes:
            b = tk.Radiobutton(self, text = criticalEye, variable = self.chosenCriticalEye, value = criticalEye)
            b.grid(row=r, column=self.column, sticky="w")
            r += 1
        self.column += 1
        if (r > self.lastRow):
            self.lastRow = r

    def createKitchenButtons(self):
        r = 0
        self.chosenKitchen = tk.StringVar()
        kitchenSkills = ["None", "Kitchen Attack Small", "Kitchen Attack Large"]
        self.chosenKitchen.set("None")
        for kitchenSkill in kitchenSkills:
            b = tk.Radiobutton(self, text = kitchenSkill, variable = self.chosenKitchen, value = kitchenSkill)
            b.grid(row=r, column=self.column, sticky="w")
            r += 1
        self.column += 1
        if (r > self.lastRow):
            self.lastRow = r

    def createMightButtons(self):
        r = 0
        self.chosenMight = tk.StringVar()
        mightItems = ["None", "Might Seed", "Might Pill"]
        self.chosenMight.set("None")
        for mightItem in mightItems:
            b = tk.Radiobutton(self, text = mightItem, variable = self.chosenMight, value = mightItem)
            b.grid(row=r, column=self.column, sticky="w")
            r += 1
        self.column += 1
        if (r > self.lastRow):
            self.lastRow = r

    def createHHBuffButtons(self):
        r = 0
        self.chosenHHBuff = tk.StringVar()
        self.HHReplay = tk.IntVar()
        HHBuffs = ["None", "HH AuS", "HH AuL"]
        self.chosenHHBuff.set("None")
        for HHBuff in HHBuffs:
            b = tk.Radiobutton(self, text = HHBuff, variable = self.chosenHHBuff, value = HHBuff)
            b.grid(row=r, column = self.column, sticky = "w")
            r += 1
        c = tk.Checkbutton(self, text = "Replay", variable = self.HHReplay)
        c.grid(row=r, column=self.column, sticky="w")
        r += 1
        self.column += 1
        if (r > self.lastRow):
            self.lastRow = r

    def createDangerBuffButtons(self):
        r = 0
        self.chosenDanger = tk.StringVar()
        dangerBuffs = ["None", "Adrenaline+2", "Felyne Heroics"]
        self.chosenDanger.set("None")
        for dangerBuff in dangerBuffs:
            b = tk.Radiobutton(self, text = dangerBuff, variable = self.chosenDanger, value = dangerBuff)
            b.grid(row=r, column=self.column, sticky="w")
            r += 1
        self.column += 1
        if (r > self.lastRow):
            self.lastRow = r

    def createFortifyButtons(self):
        r = 0
        self.chosenFortify = tk.StringVar()
        fortifyBuffs = ["None", "Fortify Cartx1", "Fortify Cartx2"]
        self.chosenFortify.set("None")
        for fortifyBuff in fortifyBuffs:
            b = tk.Radiobutton(self, text = fortifyBuff, variable = self.chosenFortify, value = fortifyBuff)
            b.grid(row=r, column=self.column, sticky="w")
            r += 1
        self.column += 1
        if (r > self.lastRow):
            self.lastRow = r

    def createElementUpButtons(self):
        r = 0
        self.chosenElementUp = tk.StringVar()
        self.elementAtkUp = tk.IntVar()
        elementBuffs = ["None", "Element+1", "Element+2", "Element+3"]
        self.chosenElementUp.set("None")
        for elementBuff in elementBuffs:
            b = tk.Radiobutton(self, text = elementBuff, variable = self.chosenElementUp, value = elementBuff)
            b.grid(row=r, column=self.column, sticky="w")
            r += 1
        c = tk.Checkbutton(self, text = "Element Atk Up", variable = self.elementAtkUp)
        c.grid(row=r, column=self.column, sticky="w")
        r += 1
        self.column += 1
        if (r > self.lastRow):
            self.lastRow = r

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
        
    def calculateDamage(self):
        weapon = self.chosenWeapon.get()
        c.execute("SELECT * FROM ChargeBlades WHERE name=\"" + weapon + "\"")
        row = c.fetchone()

        if (self.sharpness.get() == 1):
            rawSharpness = self.rawSharpnessLevels[row['sharpness+1']]
            eleSharpness = self.eleSharpnessLevels[row['sharpness+1']]
        else:
            rawSharpness = self.rawSharpnessLevels[row['sharpness']]
            eleSharpness = self.eleSharpnessLevels[row['sharpness']]

        trueElement = row['special attack']/10
        affinity = row['affinity']
        trueRaw = row['attack']/self.modifiers['ChargeBlades']
        rawHitzone = 0.45

        if (self.chosenGlove.get() == "Latent Power+1"):
            affinity += 0.30
        elif (self.chosenGlove.get() == "Latent Power+2"):
            affinity += 0.50
        elif (self.chosenGlove.get() == "Challenger+1"):
            trueRaw += 0.10
            affinity += 0.10
        elif (self.chosenGlove.get() == "Challenger+2"):
            trueRaw += 25
            affinity += 0.20
        elif (self.chosenGlove.get() == "Peak Performance"):
            trueRaw += 20
            
        trueRaw += self.attackAdditions[self.chosenAttack.get()]
        
        affinity += self.affinityAdditions[self.chosenCriticalEye.get()]

        trueRaw += self.attackAdditions[self.chosenKitchen.get()]

        trueRaw += self.attackAdditions[self.chosenMight.get()]

        trueElement = trueElement * self.elementMultipliers[self.chosenElementUp.get()] + self.elementAdditions[self.chosenElementUp.get()]

        if (self.elementAtkUp.get() == 1):
            trueElement *= 1.1

        if (self.powerCharm.get() == 1):
            trueRaw += 6

        if (self.powerTalon.get() == 1):
            trueRaw += 9

        if (self.criticalDraw.get() == 1):
            affinity += 1

        if (self.HHReplay.get() == 1 and self.chosenHHBuff.get() != "None"):
            trueRaw *= (self.attackMultipliers[self.chosenHHBuff.get()] + 0.05)
        else:
            trueRaw *= self.attackMultipliers[self.chosenHHBuff.get()]
            
        if (self.weaknessExploit.get() == 1 and rawHitzone >= 0.45):
            rawHitzone += 0.05

        trueRaw *= self.attackMultipliers[self.chosenDanger.get()]

        trueRaw *= self.attackMultipliers[self.chosenFortify.get()]
        
        if (affinity > 1):
            affinity = 1

        rawDamage = trueRaw * (1 + 0.25 * affinity) * 0.2 * rawHitzone * rawSharpness
        eleDamage = trueElement * 0.25 * eleSharpness
        totalDamage = rawDamage + eleDamage
        
        self.rawText.set("Damage from raw: {0:.2f}".format(rawDamage))
        self.eleText.set("Damage from element: {0:.2f}".format(eleDamage))
        self.totalText.set("Total damage: {0:.2f}".format(totalDamage))


if __name__ == '__main__':
    conn = sql.connect("MH4U.db")
    conn.row_factory = sql.Row
    c = conn.cursor()
    root = tk.Tk()
    root.wm_title("MH4U-Tool")
    app = Application(master=root)
    app.mainloop()
    conn.close()
