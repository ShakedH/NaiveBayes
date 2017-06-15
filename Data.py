import pandas


# DATA MEMBERS:
# data, pandas.DataFrame
# attributes, dict<string, string[]> <attrName, attrValues>
# numOfRecords, int
# numOfBins, int
# rowsOfClass, dict<class values, number of rows>
class Data:
    def __init__(self, trainData, attributes, numOfBins):
        self.data = trainData
        self.attributes = attributes
        self.numOfRecords = len(trainData.index)
        self.numOfBins = numOfBins
        self.rowsOfClass = {}
        self.cleanData()
        self.initializeMembers()

    def binning(self, column, bins, labels=None):
        if not labels:
            labels = range(len(bins) - 1)
        return pandas.cut(x=column, bins=bins, labels=labels, include_lowest=True)

    # Returns the number of records in class 'classval' in which the value of 'attrName' is 'attrVal'
    def numberOfRecordsByClassAndAttribute(self, classVal, attrName, attrVal):
        # For Categorial:
        return len(self.data.loc[(self.data['class'] == classVal) & (self.data[attrName] == attrVal)].index)

    def getAttributes(self):
        return self.attributes

    def discretizateAttr(self, attrName):
        minValue = self.data[attrName].min()
        maxValue = self.data[attrName].max()
        binWidth = (maxValue - minValue) / self.numOfBins
        binLimit = minValue + binWidth
        bins = []
        while binLimit < maxValue:
            bins.append(binLimit)
            binLimit += binWidth
        bins = [minValue] + bins + [maxValue]
        self.attributes[attrName] = bins
        self.data[attrName] = self.binning(self.data[attrName], bins)

    def initializeMembers(self):
        for classVal in self.attributes['class']:
            numOfRows = len(self.data.loc[self.data['class'] == classVal].index)
            self.rowsOfClass.update({classVal: numOfRows})

    def cleanCategorialAttr(self, attrName):
        mode = self.data.mode()[attrName][0]
        self.data[attrName] = self.data[attrName].fillna(mode)

    def cleanNumericalAttr(self, attrName):
        # Replace missing values with the mean value of all observations in the same class
        for classValue in self.attributes['class']:
            mean = self.data.loc[(self.data['class'] == classValue), attrName].mean()
            self.data.loc[(self.data["class"] == classValue) & (self.data[attrName].isnull()), attrName] = mean
        self.discretizateAttr(attrName)

    def cleanData(self):
        for attrName in self.attributes:
            if not self.attributes[attrName]:  # empty values array = numeric attribute
                self.cleanNumericalAttr(attrName)
            else:
                self.cleanCategorialAttr(attrName)
