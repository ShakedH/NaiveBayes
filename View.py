from Tkinter import *
from Classifier import *
from Data import *
import os
import tkFileDialog
import tkMessageBox
import pandas

root = Tk()
width = 700
height = 500
root.geometry('{}x{}'.format(width, height))
root.resizable(width=False, height=False)


class MainWindow:
    def __init__(self, master):
        self.master = master
        self.path = None
        self.classifier = None
        self.numOfBins = 0
        self.validBins = False
        master.title("Naive Bayes Classifier")

        gridSize = 20
        for i in range(0, gridSize):
            self.master.grid_columnconfigure(i, weight=(width / gridSize), uniform="tk")
            self.master.grid_rowconfigure(i, weight=(height / gridSize), uniform="tk")

        # Controls
        self.directoryLabel = Label(master=master, text="Directory Path:")
        self.binsLabel = Label(master=master, text="Discretization Bins:")
        self.directoryEntry = Entry(master=master, state="readonly")
        vcmd = master.register(self.validateBins)
        self.binsEntry = Entry(master=master, validate="key", validatecommand=(vcmd, '%P'))
        self.browseButton = Button(master=master, text="Browse", command=self.browseClicked)
        self.buildButton = Button(master=master, text="Build", command=self.buildClicked, state=DISABLED)
        self.classifyButton = Button(master=master, text="Classify", command=self.classifyClicked, state=DISABLED)

        # Layout
        self.directoryLabel.grid(row=2, column=1, columnspan=3)
        self.directoryEntry.grid(row=2, column=4, columnspan=12, sticky=W + E)
        self.binsLabel.grid(row=4, column=1, columnspan=3)
        self.binsEntry.grid(row=4, column=4, columnspan=2, sticky=W + E)
        self.browseButton.grid(row=2, column=17, columnspan=2, sticky=W + E)
        self.buildButton.grid(row=7, column=6, columnspan=3, sticky=W + E)
        self.classifyButton.grid(row=9, column=6, columnspan=3, sticky=W + E)

    def browseClicked(self):
        tempPath = tkFileDialog.askdirectory(initialdir=self.directoryEntry.get())
        if not os.path.exists(tempPath + "\\Structure.txt"):
            tkMessageBox.showinfo("Missing File", "Structure.txt doesn't exist in this path")
        elif not os.path.exists(tempPath + "\\train.csv"):
            tkMessageBox.showinfo("Missing File", "train.csv doesn't exist in this path")
        elif not os.path.exists(tempPath + "\\test.csv"):
            tkMessageBox.showinfo("Missing File", "test.csv doesn't exist in this path")
        else:
            self.path = tempPath
            self.directoryEntry.configure(state="normal")
            self.directoryEntry.delete(0, END)
            self.directoryEntry.insert(0, self.path)
            self.directoryEntry.configure(state="readonly")
            if self.validBins:
                self.buildButton['state'] = 'normal'
            else:
                self.buildButton['state'] = 'disabled'

    def buildClicked(self):
        attrs = Data.getAttributesDictionary(self.path + "\\Structure.txt")
        trainData = pandas.DataFrame.from_csv(self.path + "\\train.csv", index_col=None)
        processedData = Data(trainData=trainData, attributes=attrs, numOfBins=self.numOfBins)
        self.classifier = Classifier(data=processedData)
        self.classifyButton['state'] = 'normal'
        tkMessageBox.showinfo("Build Completed", "Building classifier using train-set is done!")

    def classifyClicked(self):
        testData = pandas.DataFrame.from_csv(self.path + "\\test.csv", index_col=None)
        self.classifier.classifySet(testData, filePath=self.path)
        tkMessageBox.showinfo("Classification Completed", "Classification is done!")

    def validateBins(self, numOfBins):
        if numOfBins != "":
            try:
                numOfBins = int(float(numOfBins))
                if numOfBins < 2:
                    raise ValueError
                self.validBins = True
                self.numOfBins = numOfBins
                if self.path:
                    self.buildButton['state'] = 'normal'
                return True
            except:
                self.validBins = False
                tkMessageBox.showinfo("Invalid Bins", "Discretization bins must be an integer greater than 1")
                return False


naiveBayes = MainWindow(root)
root.mainloop()
