from Tkinter import *


class MainWindow:
    def __init__(self, master):
        self.master = master
        master.title("Naive Bayes Classifier")

        self.label = Label(master, text="This is our first GUI!")
        self.label.pack()

        self.greet_button = Button(master, text="Greet", command=self.greet)
        self.greet_button.pack()

        self.close_button = Button(master, text="Close", command=master.quit)
        self.close_button.pack()


    def greet(self):
        print("Greetings!")


def getAttributesDictionary(structureFilePath):
    attrDictionary = {}
    structureFile = open(structureFilePath, "r").read().split()
    for i in xrange(1, len(structureFile), 3):
        attrName = structureFile[i]
        attrValues = structureFile[i + 1]
        attrDictionary[attrName] = []
        if attrValues == "NUMERIC":
            continue
        attrDictionary[attrName] = attrValues[1:-1].split(',')  # remove '{' and '}' and separate by comma
    return attrDictionary

root = Tk()
my_gui = MainWindow(root)
root.mainloop()
