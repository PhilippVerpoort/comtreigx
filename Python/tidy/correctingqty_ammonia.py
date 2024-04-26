import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt

def boundaries(df):
    nomissingdata = df[(df['qty'] != 0) & (df['netWgt'] != 0) & (df['primaryValue'] != 0)]
    # boundaries valueperqty
    hist, bins, _ = plt.hist(nomissingdata['valueperqty'],range=(0,2*nomissingdata['valueperqty'].median()), bins=50)
    a = round(bins[np.where(hist > 0.25*hist.max())[0][0]],2) # lower boundary for valueperqty
    b = round(bins[(np.where(hist > 0.25*hist.max())[0][-1])+1],2) # upper boundary for valueperqty
    m1 = (a+b)/2 # value in the middle between boundaries
    
    #boundaries valuepernetwgt
    hist, bins, _ = plt.hist(nomissingdata['valuepernetwgt'],range=(0,2*nomissingdata['valuepernetwgt'].median()), bins=50)
    c = round(bins[np.where(hist > 0.25*hist.max())[0][0]],2) # lower boundary for valuepernetwgt
    d = round(bins[(np.where(hist > 0.25*hist.max())[0][-1])+1],2) # upper boundary for valuepernetwgt
    m2 = (c+d)/2 # value in the middle between boundaries
    # mean value between valuepernetwgt and valueperqty in kg
    m = (m1+m2)/2
    #import statistics
    #m = (nomissingdata['valueperqty'].median() + nomissingdata['valuepernetwgt'].median() )/2
    
    return(a,b,c,d,m)

def correctedqtyinkg(row,a,b,c,d,m):
    qty = row['qty']
    netwgt = row['netWgt']
    primaryvalue = row['primaryValue']
    valueperqty = row['valueperqty']
    valuepernetwgt = row['valuepernetwgt']
#qty in u
    if row['qtyUnitAbbr'] == 'u':
        valueperqty = np.inf
# qty in l 
    if row['qtyUnitAbbr'] == 'l':
        qty = qty/1.466 # liter to kg
        valueperqty = valueperqty*1.466 #pro liter to pro kg
# qty in N/A
    if row['qtyUnitAbbr'] == 'N/A':
        valueperqty = np.inf
# qty im m^3
    if row['qtyUnitCode'] == 12:
        qty = qty/1.386
        valueperqty = valueperqty*1.386

#qty in kg
    if (a <= valueperqty <= b) and (c <= valuepernetwgt <= d):
        if abs(valueperqty - m) < abs(valuepernetwgt - m):
            return(qty)
        else:
            return(netwgt)
    elif (a <= valueperqty <= b) and (valuepernetwgt > d or valuepernetwgt < c ):
        return(qty)
    elif (valueperqty < a or valueperqty > b) and (c <= valuepernetwgt <= d):
        return(netwgt)
    elif (valueperqty < a or valueperqty > b ) and (valuepernetwgt < c or valuepernetwgt > d):
        return(primaryvalue/m) #value in USD/(m in USD/kg)->kg