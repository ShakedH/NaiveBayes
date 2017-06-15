class Classifier:
    m_estimator = 2

    def __init__(self, data):
        self.data = data

    # Returns the m-estimate of class 'classVal' and attribute 'attrName' with value 'attrVal'
    def Prob_Xk_Ci(self, classVal, attrName, attrVal, numOfValues):
        nc = self.data.numberOfRecordsByClassAndAttribute(classVal=classVal, attrName=attrName, attrVal=attrVal)
        p = 1. / numOfValues
        n = self.data.numOfRecords
        return (nc + self.m_estimator * p) / (n + self.m_estimator)

    def classifyObservation(self, record):
        maxClass = ""
        maxCnb = float("-inf")
        attributes = self.data.getAttributes()
        for classVal in self.data.rowsOfClass:
            pCi = 1. * self.data.rowsOfClass[classVal] / self.data.numOfRecords
            multiply = 1
            for attrName in attributes:
                attrVal = record[[attrName]]
                numOfValues = len(attributes[attrName])
                if self.data.isNumerical(attrName):
                    attrVal = self.data.binning(attrVal, self.data.getAttributes()[attrName])
                    numOfValues -= 1
                # todo Delete this
                if self.index == 410:
                    print 'wait!'
                attrVal = attrVal[0]
                multiply *= self.Prob_Xk_Ci(classVal=classVal, attrName=attrName, attrVal=attrVal,
                                            numOfValues=numOfValues)
            Cnb = pCi * multiply
            if Cnb > maxCnb:
                maxCnb = Cnb
                maxClass = classVal
        return maxClass

    def classifySet(self, dataFrame):
        for index, row in dataFrame.iterrows():
            # todo Delete this
            self.index = index
            print "row:\n{}".format(row)
            print "class: {}".format(self.classifyObservation(row))
