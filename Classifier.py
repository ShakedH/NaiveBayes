class Classifier:
    m_estimator = 2

    def __init__(self, data):
        self.data = data

    # Returns the m-estimate of class 'classVal' and attribute 'attrName' with value 'attrVal'
    def Prob_Xk_Ci(self, classVal, attrName, attrVal):
        nc = self.data.numberOfRecordsByClassAndAttribute(classVal=classVal, attrName=attrName, attrVal=attrVal)
        p = 1 / (len(self.data.getAttributes[attrVal]))
        n = self.data.numOfRecords
        return (nc + self.m_estimator * p) / (n + self.m_estimator)

    def classifyObservation(self, record):
        maxClass = ""
        maxCnb = float("-inf")
        attributs = self.data.getAttributes()
        for classVal in self.data.rowsOfClass:
            pCi = self.data.rowsOfClass[classVal]
            multiply = 1
            for attrName in attributs:
                attrVal = record[attrName]
                multiply *= self.data.Prob_Xk_Ci(classVal=classVal, attrName=attrName, attrVal=attrVal)
            Cnb = pCi * multiply
            if Cnb > maxCnb:
                maxCnb = Cnb
                maxClass = classVal
        return maxClass
