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

    def cleanNumericalAttr(self, attrName):
        for classValue in self.attributes['class']:
            mean = self.data.loc[(self.data['class'] == classValue), attrName].mean()
            self.data[attrName & 'class' == classValue] = self.data[attrName & 'class' == classValue].fillna(mean)

    def cleanData(self):
        for attrName in self.attributes:
            if not self.attributes[attrName]:  # empty values array = numeric attribute
                self.cleanNumericalAttr(attrName)
            else:
                self.cleanCategorialAttr(attrName)