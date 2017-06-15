from View import getAttributesDictionary
from Data import *

attrsPath = "C:\\Users\\user\\Desktop\\Structure.txt"
trainData = pandas.DataFrame.from_csv("C:\\Users\\user\\Desktop\\train.csv")
attrs = getAttributesDictionary(attrsPath)
myData = Data(trainData=trainData, attributes=attrs, numOfBins=2)
test = myData.numberOfRecordsByClassAndAttribute('yes', 'job', 'management')
