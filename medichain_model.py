# -*- coding: utf-8 -*-
"""Medichain_model.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1fl3cLqMzl98bA88kMmvtSjeot99SpRww
"""

import numpy as np
import pandas as pd
from sklearn import  preprocessing
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression

data = pd.read_csv("Dataset/Training.csv")
# data=data.dropna()
data=data.drop([1678,1691])

def numberof1(l):
    c=0
    d=0
    for i in l:
        if(i==1):
            c=c+1
        else:
            d=d+1
    print(c,"  ",d)
numberof1(data['abdominal_pain'])

import numpy as np
features = list(data.columns)
np.sort(features)

data.prognosis.value_counts()

def check_unique(data,columns):
    unique_values = {}
    for col in columns:
        unique_values[col] = data[col].unique().tolist()
    return unique_values

columns_list = list(data.columns)
print(check_unique(data,columns_list))

x = data.iloc[:,:-2]
y = data.iloc[:, -2]
x.shape
data.shape

y

data_test = pd.read_csv("Dataset/Testing.csv")
x_test = data_test.drop(columns=["prognosis"])
y_test = data_test[['prognosis']]

# data['prognosis'].unique()
data['prognosis'].count()

y_test

x_test

data.dtypes

from sklearn.preprocessing import LabelEncoder
label = LabelEncoder()
label.fit(y)
y = label.transform(y)
x=pd.get_dummies(x)
print(y.shape)
label.fit(y_test)
y_test = label.transform(y_test)
print(y)
print(y_test.shape)

y

y_train_set = set(y)
y_test_set = set(y_test)
if y_train_set == y_test_set:
    print("y_train and y_test encode the same values")
else:
    print("y_train and y_test do not encode the same values")

clf = LogisticRegression()
clf.fit(x,y)
y_pred_clf = clf.predict(x_test)

def random_forest(x,y,x_test,y_test):
    dt = RandomForestClassifier(n_estimators=2, random_state=42,max_depth=20,max_features=10)

    dt.fit(x,y)
    y_pred = dt.predict(x_test)
    accuracy = accuracy_score(y_test,y_pred)
    return accuracy*100

rf = RandomForestClassifier()
a=random_forest(x , y, x_test, y_test)
print("Accuracy: ",a)

from xgboost import XGBClassifier
def xgb_model():
    model = XGBClassifier()
    return model
xgb = xgb_model()
xgb.fit(x,y)
y_pred_xgb = xgb.predict(x_test)
accuracy = accuracy_score(y_test, y_pred_xgb)
print('Accuracy: {:.2f}%'.format(accuracy * 100))

symptoms = x.columns.values


# Creating a symptom index dictionary to encode the
# input symptoms into numerical form
symptom_index = {}
for index, value in enumerate(symptoms):
    symptom = " ".join([i.capitalize() for i in value.split("_")])
    symptom_index[symptom] = index

data_dict = {
    "symptom_index":symptom_index,
    "predictions_classes":label.classes_
}
def predictDisease(symptoms):
    symptoms = symptoms.split(",")
    input_data = [0] * len(data_dict["symptom_index"])
    for symptom in symptoms:
        index = data_dict["symptom_index"][symptom]
        input_data[index] = 1

    input_data = np.array(input_data).reshape(1,-1)

    xgboost_prediction = data_dict["predictions_classes"][xgb.predict(input_data)[0]]
    predictions = {
        xgboost_prediction,
    }
    return predictions
print(predictDisease("Itching,Skin Rash,Nodal Skin Eruptions"))