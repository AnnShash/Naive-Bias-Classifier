# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 17:37:42 2020
@author: Home

Naive Bias Algorithm
Data file assumed to be a CSV with column names in the first row. 
Data file should have the class lable as the last column
This program is written including the biasing estimate(m-estimate)
P(ai|vj)= (nc + m*p)/(n+m)
where m = constant (eqvlnt sample size)
      p = prior estimate of the prob
      n = no of training examples
      nc = no of ex. for which v = vj and a = ai 
use m = 0 to calculate without using the biasing estimate
"""

import pandas as pd
import numpy as np

def length(data):
    '''this returns the count of class labels''' 
    cls = data.columns[-1]
    vals = data[cls].unique()
    l = []
    for v  in vals:
        occr = len(data[data[cls] == v])
        l.append(occr)
    return l

def est_prob(data):
    '''calculate the prior estimate of the probabilty'''
    hd = list(data.columns[:-1])
    p = []
    for ftr in hd:
        val = len(data[ftr].unique())
        p.append(1/val)
    return p

def numerator(data,feature,value,es_pr,m):
    '''returns the count of class labels w.r.t attribute value 
    including estimating probabilities'''
    cls = data.columns[-1]
    vals = data[cls].unique()
    #es_pr = est_prob(data)
    up = []
    attr = data[data[feature] == value]
    #for i in range(len(es_pr)):
    for v in vals:
        occur = len(attr[attr[cls] == v]) + (m*es_pr)
        up.append(occur)
    return up

def cal_prob(data,feature,value,es_pr,m):
    '''calculate the respective prob for seperate classes, including estimating
    probabilitie'''
    prob = []
    for i in range(2):
        p = numerator(data,feature,value,es_pr,m)[i]/(length(data)[i] + m)
        prob.append(p)
    return(prob)

def NB(vector,data):
    '''applyng the Naive bias algorithm'''
    len_y = length(data)[0]
    len_n = length(data)[1]
    prob_val = np.array([])
    pos = np.array([])
    neg = np.array([])
    
    for v in vector:
        pos = np.append(pos,v[0])
        neg = np.append(neg,v[1])
        
    pos_prob = np.prod(pos)  
    neg_prob = np.prod(neg)
    
    yes_prob = len_y/len(data)
    no_prob = len_n/len(data)
    
    prob_val = np.append(prob_val,[pos_prob,yes_prob,neg_prob,no_prob])
    return prob_val
    
def decision(value):
    '''making the decision '''
    yes = value[0]*value[1]
    no = value[2]*value[3]
    tot = yes+no
    p_yes = (yes/tot)*100
    p_no = (no/tot)*100

    
    print ('Probability of being a mammal: '+'{:.4f}'.format(yes)+' --> {:.2f}'.format(p_yes)+'% as a percentage')
    print ('Probability of being a non-mammal: '+'{:.4f}'.format(no)+' --> {:.2f}'.format(p_no)+'% as a percentage')
    print ('\n')
    print ('decision')
    if yes > no:
        print("It's a Mammal")
    else:
        print("It's a Non-mammal")
        
if __name__=="__main__":
    
    data = pd.read_excel('BA2002-A2-18880323.xlsx', sheetname = 'animals')
    feature = list(data.columns[:-1])
    es_pr = est_prob(data)
    n = len(feature)
    vector1 = []
    vector2 = []
    
    #calculate without estimating probability, m = 0
    value1 = ['cold','yes','no','yes']
    for i in range(n):
        v = cal_prob(data,feature[i],value1[i],es_pr[i],0)
        vector1.append(v)
    
    #calculate with estimating probability, m = a constant
    value2 = ['cold','yes','no','sometimes']
    for i in range(n):
        v = cal_prob(data,feature[i],value2[i],es_pr[i],6)
        vector2.append(v)
    
    value1 = NB(vector1,data)
    value2 = NB(vector2,data)
    print('Question 1a ------>')
    decision(value1)
    print('\n')
    print('Question 1b ------>')
    decision(value2)
 