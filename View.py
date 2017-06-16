from Tkinter import *
from Classifier import *
from Data import *
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
        self.validBins = False
        master.title("Naive Bayes Classifier")

        gridSize = 20
        for i in range(0, gridSize):
            self.master.grid_columnconfigure(i, weight=(width / gridSize), uniform="tk")
            self.master.grid_rowconfigure(i, weight=(height / gridSize), uniform="tk")

        def browseClicked():
            tempPath = tkFileDialog.askdirectory()
            if not Path(tempPath + "\\Structure.txt").exists():
                tkMessageBox.showinfo("Missing File", "Structure.txt doesn't exist in this path")
            elif not Path(tempPath + "\\train.csv").exists():
                tkMessageBox.showinfo("Missing File", "train.csv doesn't exist in this path")
            elif not Path(tempPath + "\\test.csv").exists():
                tkMessageBox.showinfo("Missing File", "test.csv doesn't exist in this path")
            else:
                tkMessageBox.showinfo("Path OK", "Path contains all required files")
                self.path = tempPath
                if self.validBins:
                    self.buildButton.state([ENABLED])

        def buildClicked():
            attrs = Data.getAttributesDictionary(self.path + "\\Structure.txt")
            trainData = pandas.DataFrame.from_csv(self.path + "\\train.csv", index_col=None)
            processedData = Data(trainData=trainData, attributes=attrs, numOfBins=bins)
            self.classifier = Classifier(data=processedData)
            self.classifyButton.state([ENABLED])
            tkMessageBox.showinfo("Build Completed", "Building classifier using train-set is done!")

        def classifyClicked():
            testData = pandas.DataFrame.from_csv(self.path + "\\test.csv", index_col=None)
            self.classifier.classifySet(testData, filePath=self.path)
            tkMessageBox.showinfo("Classification Completed", "Classification is done!")

        def validateBins():
            binsInput = self.binsEntry.get()
            if binsInput < 2:
                tkMessageBox.showinfo("Classification Completed", "Classification is done!")
            else:
                self.validBins = True
                if self.path:
                    self.buildButton.state([ENABLED])

        # Controls
        self.directoryLabel = Label(master=master, text="Directory Path:")
        self.binsLabel = Label(master=master, text="Discretization Bins:")
        self.directoryEntry = Entry(master=master)
        self.directoryEntry.configure(state='readonly')
        self.binsEntry = Entry(master=master, validate="focusout", validatecommand=validateBins)
        self.browseButton = Button(master=master, text="Browse", command=browseClicked)
        self.buildButton = Button(master=master, text="Build", command=buildClicked, state=DISABLED)
        self.classifyButton = Button(master=master, text="Classify", command=classifyClicked, state=DISABLED)

        # Layout
        self.directoryLabel.grid(row=2, column=1, columnspan=3)
        self.directoryEntry.grid(row=2, column=4, columnspan=12, sticky=W + E)
        self.binsLabel.grid(row=4, column=1, columnspan=3)
        self.binsEntry.grid(row=4, column=4, columnspan=2, sticky=W + E)
        self.browseButton.grid(row=2, column=17, columnspan=2, sticky=W + E)
        self.buildButton.grid(row=7, column=6, columnspan=3, sticky=W + E)
        self.classifyButton.grid(row=9, column=6, columnspan=3, sticky=W + E)


naiveBayes = MainWindow(root)
root.mainloop()
