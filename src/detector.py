# -*- coding: utf-8 -*-
"""
Created on Wed Nov  9 10:59:11 2022

@author: Tshegofatso Mohlala
"""
import datetime
import subprocess
from sklearn.preprocessing import StandardScaler
from pickle import load
import numpy as np


def pre_proc(feat_values):
    """
        * Extracts features
        * Transform the feature values using standard scaler and returns the transformed values
    """

    scaler = StandardScaler()  #Scale the data the same way it was scaled when training the model
    scaler.fit(np.array(feat_values).reshape(1, -1))
    scaled_data = scaler.transform(np.array(feat_values).reshape(1, -1))
    
    return scaled_data   #Return the scaled features


def detection(website):
    rf_model = load(open('./asserts/rf_model.pkl', 'rb'))  #Load the model from the pickel file
    if rf_model.predict(list(pre_proc(website).reshape(1, -1)))[0]:   #Perform the prediction, if it returns a value of 1 then it is a good website otherwise it is bad
        return 'good'
    else:
        return 'bad'


