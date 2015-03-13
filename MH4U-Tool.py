import sqlite3
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
        for row in c.execute("SELECT * FROM ChargeBlades WHERE name='" + weapon + "'"):
            print(row)

if __name__ == '__main__':
    conn = sqlite3.connect("MH4U.db")
    c = conn.cursor()
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()
    conn.close()
