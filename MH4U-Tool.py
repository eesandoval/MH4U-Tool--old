import sqlite3 as sql
import tkinter as tk

class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        self.okButton = tk.Button(self, text="OK", command=self.calculateDamage)
        self.okButton.pack(side="left")
        self.createList()
        self.createSharpnessButtons()

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
        sharpnessLevels = ["Red", "Orange", "Yellow", "Blue", "White", "Purple"]
        self.chosenSharpness.set("Purple")
        for sharpness in sharpnessLevels:
            b = tk.Radiobutton(self, text = sharpness, variable = self.chosenSharpness, value = sharpness)
            b.pack(side="left")
        
    def calculateDamage(self):
        weapon = self.chosenWeapon.get()
        print("You chose sharpness level", self.chosenSharpness.get())
        c.execute("SELECT * FROM ChargeBlades WHERE name='" + weapon + "'")
        row = c.fetchone()
        print((row['attack'] * (1 + 0.25 * row['affinity']) *
              0.2 * 0.35 * 1.44) + (row['special attack']/100 * 0.2 * 1.2))

if __name__ == '__main__':
    conn = sql.connect("MH4U.db")
    conn.row_factory = sql.Row
    c = conn.cursor()
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()
    conn.close()
