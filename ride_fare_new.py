# -*- coding: utf-8 -*-
"""Copy of xgboost.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1syV8nuHUQAbiwQ5k9mnCyK4HcmfceA6U
"""

import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.preprocessing import StandardScaler,MinMaxScaler
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix

# Load libraries
from pandas import read_csv
from pandas.plotting import scatter_matrix
from matplotlib import pyplot

from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC

X_train = pd.read_csv('/content/drive/My Drive/Ride_Fare/train.csv',index_col='tripid',)

X_train

X_train.info()

X_train.drop('drop_time',axis = 1,inplace=True)
X_train.drop('pickup_time',axis = 1,inplace=True)

from numpy import cos, sin, arcsin, sqrt
from math import radians

def haversine(pick_lon,pick_lat,drop_lon,drop_lat):
    lon1 = pick_lon
    lat1 = pick_lat
    lon2 =drop_lon
    lat2 = drop_lat

    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * arcsin(sqrt(a)) 
    km = 6367 * c

    return km

########### distance harvesian

num_rows=X_train.shape[0]
distance_list = []

for i in range(num_rows):
  pick_lon = X_train.iloc[i]['pick_lon'] 
  pick_lat = X_train.iloc[i]['pick_lat'] 
  drop_lon =  X_train.iloc[i]['drop_lon']
  drop_lat =  X_train.iloc[i]['drop_lat']
  dist = haversine(pick_lon,pick_lat,drop_lon,drop_lat)
  distance_list.append(dist)

X_train['distance'] = distance_list



X_train.drop('pick_lat',axis = 1,inplace=True)
X_train.drop('pick_lon',axis = 1,inplace=True)
X_train.drop('drop_lat',axis = 1,inplace=True)
X_train.drop('drop_lon',axis = 1,inplace=True)

X_train['label'] = X_train['label'].replace({'correct':1 , 'incorrect':0})





incorrect_means = X_train.loc[X_train['label'] == 0].mean()

X_train_incorrect = X_train.loc[X_train['label'] == 0].fillna(incorrect_means)



correct_means = X_train.loc[X_train['label'] == 1].mean()

X_train_correct = X_train.loc[X_train['label'] == 1].fillna(correct_means)





X =pd.concat([X_train_correct,X_train_incorrect] , axis = 0)

X.isna().sum()

X

!pip install xgboost

from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

Y = X_train['label']
X_train.drop('label',axis=1,inplace=True)

X= X_train

X.reset_index(drop=True, inplace=True)

seed = 7
test_size = 0.33
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=test_size, random_state=seed,shuffle=True)

from sklearn.model_selection import GridSearchCV

estimator = XGBClassifier(
    objective= 'binary:logistic',
    nthread=4,
    seed=42,
    
)

parameters = {
    'max_depth': range (2, 10, 1),
    'n_estimators': range(60, 1000, 40),
    'learning_rate': [0.1, 0.01, 0.05]
}

grid_search = GridSearchCV(
    estimator=estimator,
    param_grid=parameters,
    scoring = 'f1',
    n_jobs = 10,
    cv = 10,
    verbose=True
)

grid_search.fit(X, Y)

# fit model no training data
model = XGBClassifier(n_estimators=1000,colsample_bytree=0.9, max_depth=70,random_state=1,subsample=0.6)
model.fit(X_train, y_train)

# make predictions for test data
y_pred = model.predict(X_test)
predictions = [round(value) for value in y_pred]

# evaluate predictions

from sklearn.metrics import f1_score

f1 = f1_score(y_test, predictions, average='macro')
f1

y_test.value_counts()

predictions.count(0)

predictions.count(1)

###########################################

test_df = pd.read_csv('/content/drive/My Drive/Ride_Fare/test.csv',index_col="tripid")

test_df

test_df.drop('drop_time',axis = 1,inplace=True)
test_df.drop('pickup_time',axis = 1,inplace=True)



########### distance harvesian

num_rows=test_df.shape[0]
distance_list = []

for i in range(num_rows):
  pick_lon = test_df.iloc[i]['pick_lon'] 
  pick_lat = test_df.iloc[i]['pick_lat'] 
  drop_lon =  test_df.iloc[i]['drop_lon']
  drop_lat =  test_df.iloc[i]['drop_lat']
  dist = haversine(pick_lon,pick_lat,drop_lon,drop_lat)
  distance_list.append(dist)

test_df['distance'] = distance_list



test_df.drop('pick_lat',axis = 1,inplace=True)
test_df.drop('pick_lon',axis = 1,inplace=True)
test_df.drop('drop_lat',axis = 1,inplace=True)
test_df.drop('drop_lon',axis = 1,inplace=True)

test_df



### NN
test_preds = model.predict(test_df)

test_preds

submission_df = pd.read_csv('/content/drive/My Drive/Ride_Fare/sample_submission.csv',index_col="tripid")
submission_df.head()



# Make sure we have the rows in the same order


# Save predictions to submission data frame
submission_df["prediction"] = test_preds

submission_df.head()

# 1_1 clas wight, H= all data, L = part
submission_df.to_csv('/content/drive/My Drive/Ride_Fare/ride_fare_submission_xgb_410z_5285o.csv', index=True)

submission_df['prediction'].value_counts()