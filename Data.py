import pandas


class Data:
    def __init__(self, data, attributes):
        self.data = data
        self.attributes = attributes
        self.numOfRecords = len(data.index)
        self.cleanData()

    def cleanCategorialAttr(self, attrName):
        mode = self.data.mode()[attrName][0]
        self.data[attrName] = self.data[attrName].fillna(mode)

    def cleanData(self):
        for attrName in self.attributes:
            if not self.attributes[attrName]:
                self.cleanNumericalAttr(attrName)
            else:
                self.cleanCategorialAttr(attrName)


testData = pandas.DataFrame.from_csv("C:\\Users\\user\\Desktop\\train.csv")
attrs = {'loan': ['yes', 'no']}
dataobj = Data(testData, attrs)
print dataobj
