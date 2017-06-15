import pandas


# DATA MEMBERS:
# data, pandas.DataFrame
# attributs, dict<string, string[]> <attrName, attrValues>
# numOfRecords, int
# numOfBins, int
# numericAttrBins, dict<string, int[]> <attrName, attrBinsUpperLimits>

# rowsOfClass - dictionary<class Values, number of rows>
class Data:
    def __init__(self, data, attributes, numOfBins):
        self.data = data
        self.attributes = attributes
        self.numOfRecords = len(data.index)
        self.numOfBins = numOfBins
        self.numericAttrBins = None
        self.cleanData()
        self.initializeMembers()

    def binning(self, column, bins, labels=None):
        bins = [column.min()] + bins + [column.max()]
        if not labels:
            labels = range(len(bins) + 1)
        return pandas.cut(column, bins, labels, True)

    def discretizateAttr(self, attrName):
        minValue = self.data[attrName].min()
        maxValue = self.data[attrName].max()
        binWidth = (maxValue - minValue) / self.numOfBins
        binLimit = minValue + binWidth
        bins = []
        while binLimit < maxValue:
            bins.append(binLimit)
            binLimit += binWidth
        self.numericAttrBins[attrName] = bins
        self.data[attrName] = self.binning(self.data[attrName], bins)

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
