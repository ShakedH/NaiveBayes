from View import getAttributesDictionary
from Data import *
from Classifier import *

path = "C:\\Users\\user\\Desktop\\"
# path = "C:\\Users\\Ron Michaeli\\Desktop\\"
attrsPath = path + "Structure.txt"
attrs = getAttributesDictionary(attrsPath)
trainData = pandas.DataFrame.from_csv(path + "train.csv", index_col=None)
myData = Data(trainData=trainData, attributes=attrs, numOfBins=2)
classify = Classifier(data=myData)
testData = pandas.DataFrame.from_csv(path + "test.csv", index_col=None)
classify.classifySet(testData, filePath=path)
