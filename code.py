import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import pandas as pd
import textdistance
import os
import re
from sklearn import model_selection, preprocessing, linear_model, naive_bayes, metrics, svm
os.chdir(r"path")
df= pd.read_csv(r'file.csv')
# creating a List of Names
fullDrugsNameList = df['FULL_NAME'].str.upper().tolist()
cleanFullDrugNamesList = []
deletingAfterNumberCompiler = re.compile('(?<=[0-9]).+')
deletingNumberCompiler = re.compile(r' [0-9]+| [0-9]+\.[0-9]+')
deletingBegginingPoint = re.compile(r'^\.(?=\w)')
# cleaning the variables
for text in fullDrugsNameList:
    textWihoutAfterNumber = deletingAfterNumberCompiler.sub('',text)
    cleanText = deletingNumberCompiler.sub('',textWihoutAfterNumber)
    cleanText = deletingBegginingPoint.sub('',cleanText)
    cleanFullDrugNamesList.append(cleanText)
len(cleanFullDrugNamesList)
# addding a column to dataset
df['cleanFullNames1']=cleanFullDrugNamesList
# creating a list of variabless
uniqueMedicineID = []
medicineListWithNotCleanText = []
medicineListWithtCleanText = []
dictOfDrugsAlreadyAdded = { i : False for i in range(len(cleanFullDrugNamesList)) }
# creating a group of dic
medicineUniqueID = 0
for textNumber in range(len(cleanFullDrugNamesList)):
    if not dictOfDrugsAlreadyAdded[textNumber]:
        text = cleanFullDrugNamesList[textNumber]
        comparisonList = cleanFullDrugNamesList[textNumber+1:]
        for textNumberComparison in range(len(comparisonList)):
            if not dictOfDrugsAlreadyAdded[textNumberComparison+textNumber+1]:
                textComparison = comparisonList[textNumberComparison]
                distance = textdistance.damerau_levenshtein(text, textComparison)
                if distance <2:
                    uniqueMedicineID.append(medicineUniqueID)
                    medicineListWithtCleanText.append(textComparison)
                    medicineListWithNotCleanText.append(fullNamesList[textNumberComparison+textNumber+1])
                    dictOfDrugsAlreadyAdded[textNumberComparison+textNumber+1] = True
        medicineListWithNotCleanText.append(fullNamesList[textNumber])
        uniqueMedicineID.append(medicineUniqueID)
        medicineUniqueID = medicineUniqueID + 1
        medicineListWithtCleanText.append(text)
len(uniqueMedicineID)
newDf = pd.DataFrame()
newDf['textClean']=medicineListWithtCleanText
newDf['medicineID']=uniqueMedicineID
newDf['text Not Clean']=medicineListWithNotCleanText
newDf.to_csv('resultsAfterOrdering4.csv',encoding='utf-8')
