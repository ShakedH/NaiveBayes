import pandas


class Data:
    def __init__(self, data, attributes):
        self.data = data
        self.attributes = attributes
        self.numOfRecords = len(data.index)
        self.cleanData()
        self.initializeMembers()

    def cleanCategorialAttr(self, attrName):
        mode = self.data.mode()[attrName][0]
        self.data[attrName] = self.data[attrName].fillna(mode)

    def cleanNumericalAttr(self, attrName):
        # Replace missing values with the mean value of all observations in the same class
        for classValue in self.attributes['class']:
            mean = self.data.loc[(self.data['class'] == classValue), attrName].mean()
            self.data.loc[(self.data["class"] == classValue) & (self.data[attrName].isnull()), attrName] = mean

    def cleanData(self):
        for attrName in self.attributes:
            if not self.attributes[attrName]:  # empty values array = numeric attribute
                self.cleanNumericalAttr(attrName)
            else:
                self.cleanCategorialAttr(attrName)

testData = pandas.DataFrame.from_csv("C:\\Users\\user\\Desktop\\train.csv")
attrs = {'balance': [], 'class': ['yes', 'no']}
dataobj = Data(testData, attrs)
print dataobj
