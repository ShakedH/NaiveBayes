# rowsOfClass - dictionary<class Values, number of rows>
# m - constant
class Data:
    m = 2

    def __init__(self, trainData, attributes, numOfBins):
        self.data = trainData
        self.attributes = attributes
        self.numOfRecords = len(trainData.index)
        self.numOfBins = numOfBins
        self.cleanData()
        self.initializeMembers()

    def numberOfRecordsByClassAndAttribute(self, classVal, attrName, attrVal):
        # For Categorial:
        return len(self.data.loc[(self.data['class'] == classVal) & self.data[attrName] == attrVal].index)

    def discretizateAttr(self, attrName):
        minValue = self.data[attrName].min
        maxValue = self.data[attrName].max
        binWidth = (maxValue - minValue) / self.numOfBins
        binLimit = minValue + binWidth
        bins = []
        while binLimit <= maxValue:
            bins.append(binLimit)
            binLimit = min(maxValue, binLimit + binWidth)
        self.numericAttrBins[attrName] = bins

    def initializeMembers(self):
        self.rowsOfClass = {}
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

    def cleanData(self):
        for attrName in self.attributes:
            if not self.attributes[attrName]:  # empty values array = numeric attribute
                self.cleanNumericalAttr(attrName)
            else:
                self.cleanCategorialAttr(attrName)

