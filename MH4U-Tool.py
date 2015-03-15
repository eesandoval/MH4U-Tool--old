import sqlite3 as sql
import tkinter as tk

class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.pack()
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

    def createWidgets(self):
        self.calculateButton = tk.Button(self, text="Calculate!", command=self.calculateDamage)
        self.calculateButton.pack(side="left")
        self.createList()
        self.createSharpnessButtons()
        self.createGloveButtons()

    def createList(self):
        optionList = []
        for row in c.execute('SELECT name FROM ChargeBlades'):
            optionList.append(row[0])
        self.chosenWeapon = tk.StringVar()
        self.chosenWeapon.set(optionList[0])
        weaponsMenu = tk.OptionMenu(self, self.chosenWeapon, *optionList)
        weaponsMenu.pack(side="left")

    def createSharpnessButtons(self):
        self.chosenSharpness = tk.StringVar()
        sharpnessLevels = ["sharpness", "sharpness+1"]
        self.chosenSharpness.set("sharpness")
        for sharpness in sharpnessLevels:
            b = tk.Radiobutton(self, text = sharpness, variable = self.chosenSharpness, value = sharpness)
            b.pack(side="left")
            
    def createGloveButtons(self):
        self.chosenGlove = tk.StringVar()
        gloves = ["Latent Power+2", "Challenger+2", "None"]
        self.chosenGlove.set("None")
        for glove in gloves:
            b = tk.Radiobutton(self, text = glove, variable = self.chosenGlove, value = glove)
            b.pack(side="bottom")
        
    def calculateDamage(self):
        weapon = self.chosenWeapon.get()
        c.execute("SELECT * FROM ChargeBlades WHERE name=\"" + weapon + "\"")
        row = c.fetchone()
        
        rawSharpness = self.rawSharpnessLevels[row[self.chosenSharpness.get()]]
        eleSharpness = self.eleSharpnessLevels[row[self.chosenSharpness.get()]]
        affinity = row['affinity']
        trueRaw = row['attack']/self.modifiers['ChargeBlades']
        
        if (self.chosenGlove.get() == "Latent Power+2"):
            affinity += 0.50
        elif (self.chosenGlove.get() == "Challenger+2"):
            trueRaw += 25
            affinity += 0.20
        if (affinity > 1):
            affinity = 1

        print("Damage from raw:", (trueRaw * (1 + 0.25 * affinity) * 0.2 * 0.35 * rawSharpness))            
        print("Damage from element:", (row['special attack']/10 * 0.2 * eleSharpness))
        print("Total damage:", (trueRaw * (1 + 0.25 * affinity) * 0.2 * 0.35 * rawSharpness) +
              (row['special attack']/10 * 0.2 * eleSharpness))


if __name__ == '__main__':
    conn = sql.connect("MH4U.db")
    conn.row_factory = sql.Row
    c = conn.cursor()
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()
    conn.close()
