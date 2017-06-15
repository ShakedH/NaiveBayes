import pandas


# DATA MEMBERS:
# data, pandas.DataFrame
# attributes, dict<string, string[]> <attrName, attrValues>
# numOfRecords, int
# numOfBins, int
# numericAttrs, string[]
# rowsOfClass, dict<class values, number of rows>
class Data:
    def __init__(self, trainData, attributes, numOfBins):
        self.data = trainData
        self.attributes = attributes
        self.numOfRecords = len(trainData.index)
        self.numOfBins = numOfBins
        self.numericAttrs = []
        self.rowsOfClass = {}
        self.initializeMembers()
        self.cleanData()

    # Replaces numeric attributes with corresponding labels according bins
    def binning(self, column, bins, labels=None):
        if not labels:
            labels = range(len(bins) - 1)
        return pandas.cut(x=column, bins=bins, labels=labels, include_lowest=True, right=False)

    # Returns the number of records in class 'classval' in which the value of 'attrName' is 'attrVal'
    # Categorical attributes only
    def numberOfRecordsByClassAndAttribute(self, classVal, attrName, attrVal):
        return len(self.data.loc[(self.data['class'] == classVal) & (self.data[attrName] == attrVal)].index)

    # Returns attributes dictionary
    def getAttributes(self):
        return self.attributes

    # Returns true if data[attrName] is numeric according structure file. Returns false otherwise
    def isNumerical(self, attrName):
        return attrName in self.numericAttrs

    # Calculates data[attrName] equal-width bins
    # Numerical attributes only
    def discretizeAttr(self, attrName):
        minValue = self.data[attrName].min()
        maxValue = self.data[attrName].max()
        binWidth = (maxValue - minValue) / self.numOfBins
        bins = []
        for i in range(1, self.numOfBins):
            bins.append(minValue + i * binWidth)
        bins = [minValue] + bins + [float("inf")]
        self.attributes[attrName] = bins
        self.data[attrName] = self.binning(self.data[attrName], bins)

    # Calculates number of observations for each class value and updates rowsOfClass dictionary
    def initializeMembers(self):
        for classVal in self.attributes['class']:
            numOfRows = len(self.data.loc[self.data['class'] == classVal].index)
            self.rowsOfClass[classVal] = numOfRows
        del self.attributes['class']

    # Fills missing values with mode
    # Categorical attributes only
    def cleanCategoricalAttr(self, attrName):
        mode = self.data.mode()[attrName][0]
        self.data[attrName] = self.data[attrName].fillna(mode)

    # Fills missing values with the mean value of all observations in the same class
    # Numerical attributes only
    def cleanNumericalAttr(self, attrName):
        for classValue in self.rowsOfClass:
            mean = self.data.loc[(self.data['class'] == classValue), attrName].mean()
            self.data.loc[(self.data["class"] == classValue) & (self.data[attrName].isnull()), attrName] = mean
        self.discretizeAttr(attrName)

    # Cleans data - handles missing values and discretize numerical attributes
    def cleanData(self):
        for attrName in self.attributes:
            if not self.attributes[attrName]:  # empty values array = numeric attribute
                self.numericAttrs.append(attrName)
                self.cleanNumericalAttr(attrName)
            else:
                self.cleanCategoricalAttr(attrName)
