import pandas as pd

def loadCSVtoPandas(fileName):

    dataFrame = pd.read_csv(fileName,sep=",")

    return dataFrame

