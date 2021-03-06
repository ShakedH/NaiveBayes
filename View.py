from Tkinter import *

import win32api

from Classifier import *
from Data import *
from threading import Thread
import os
import tkFileDialog
import tkMessageBox
import pandas

root = Tk()
width = 700
height = 300
root.geometry('{}x{}'.format(width, height))
root.resizable(width=False, height=False)


# noinspection PyCompatibility
class MainWindow:
    def __init__(self, master):
        self.master = master
        self._after_id = None
        self.path = None
        self.classifier = None
        self.numOfBins = 0
        self.validBins = False
        master.title("Naive Bayes Classifier")

        numOfRows = 10
        for i in range(0, numOfRows):
            self.master.grid_rowconfigure(i, weight=(height / numOfRows), uniform="tk")
        numOfCols = 20
        for i in range(0, numOfCols):
            self.master.grid_columnconfigure(i, weight=(width / numOfCols), uniform="tk")

        # Controls
        self.directoryLabel = Label(master=master, text="Directory Path:")
        self.binsLabel = Label(master=master, text="Discretization Bins:")
        self.directoryEntry = Entry(master=master, state="readonly")
        self.binsEntry = Entry(master=master)
        self.binsEntry.bind("<Key>", self.handleWait)   # Bind keyPress event to pre-validation waiting function
        self.browseButton = Button(master=master, text="Browse", command=self.browseClicked)
        self.buildButton = Button(master=master, text="Build", command=self.buildClicked, state=DISABLED)
        self.classifyButton = Button(master=master, text="Classify", command=self.classifyClicked, state=DISABLED)

        # Layout
        self.directoryLabel.grid(row=2, column=1, columnspan=2)
        self.directoryEntry.grid(row=2, column=3, columnspan=12, sticky=W + E)
        self.binsLabel.grid(row=4, column=1, columnspan=2)
        self.binsEntry.grid(row=4, column=3, columnspan=2, sticky=W + E)
        self.browseButton.grid(row=2, column=16, columnspan=2, sticky=W + E)
        self.buildButton.grid(row=6, column=6, columnspan=3, sticky=W + E)
        self.classifyButton.grid(row=8, column=6, columnspan=3, sticky=W + E)

    def browseClicked(self):
        tempPath = tkFileDialog.askdirectory(initialdir=self.directoryEntry.get())
        if not os.path.exists(tempPath + "\\Structure.txt"):
            tkMessageBox.showinfo("Naive Bayes Classifier", "ERROR: Structure.txt doesn't exist in this path")
        elif not os.path.exists(tempPath + "\\train.csv"):
            tkMessageBox.showinfo("Naive Bayes Classifier", "ERROR: train.csv doesn't exist in this path")
        elif not os.path.exists(tempPath + "\\test.csv"):
            tkMessageBox.showinfo("Naive Bayes Classifier", "ERROR: test.csv doesn't exist in this path")
        else:
            self.path = tempPath
            self.directoryEntry['state'] = 'normal'
            self.directoryEntry.delete(0, END)
            self.directoryEntry.insert(0, self.path)
            self.directoryEntry['state'] = 'readonly'
            self.buildButton['state'] = 'normal' if self.validBins else 'disabled'

    def buildClicked(self):
        attrs = Data.getAttributesDictionary(self.path + "\\Structure.txt")
        trainData = pandas.DataFrame.from_csv(self.path + "\\train.csv", index_col=None)
        processedData = Data(trainData=trainData, attributes=attrs, numOfBins=self.numOfBins)
        self.classifier = Classifier(data=processedData)
        self.classifyButton['state'] = 'normal'
        tkMessageBox.showinfo("Naive Bayes Classifier", "Building classifier using train-set is done!")

    def classifyClicked(self):
        thread = Thread(target=self.classifyInThread)
        thread.start()
        tkMessageBox.showinfo("Naive Bayes Classifier",
                              "Classification has started. You will be alerted when completed")
        self.binsEntry['state'] = 'readonly'
        self.browseButton['state'] = 'disabled'
        self.buildButton['state'] = 'disabled'
        self.classifyButton['state'] = 'disabled'

    def handleWait(self, event):
        if self._after_id is not None:
            self.master.after_cancel(self._after_id)

        self._after_id = self.master.after(750, self.validateBins)

    def validateBins(self):
        numOfBins = self.binsEntry.get()
        try:
            numOfBins = int(float(numOfBins))
            if numOfBins < 2:
                raise ValueError
            self.validBins = True
            self.numOfBins = numOfBins
            self.buildButton['state'] = 'normal' if self.path else 'disabled'
        except ValueError:
            tkMessageBox.showinfo("Naive Bayes Classifier", "ERROR: Discretization bins must be an integer greater than 1")
            self.validBins = False
            self.buildButton['state'] = 'disabled'
            return 'break'

    def classifyInThread(self):
        testData = pandas.DataFrame.from_csv(self.path + "\\test.csv", index_col=None)
        self.classifier.classifySet(testData, filePath=self.path)
        message = "Classification is done! The results file is located in {}/output.txt".format(self.path)
        win32api.MessageBox(0, message, "Naive Bayes Classifier", 0x00001040)
        os._exit(0)


naiveBayes = MainWindow(root)
root.mainloop()
