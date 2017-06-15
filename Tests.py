from View import getAttributesDictionary
from Data import *

path = "C:\\Users\\Ron Michaeli\\Desktop\\"
attrsPath = path + "Structure.txt"
attrs = getAttributesDictionary(attrsPath)
trainData = pandas.DataFrame.from_csv(path + "train.csv", index_col=None)
myData = Data(trainData=trainData, attributes=attrs, numOfBins=2)
test = myData.numberOfRecordsByClassAndAttribute(classVal='no', attrName='job', attrVal='management')
print test
