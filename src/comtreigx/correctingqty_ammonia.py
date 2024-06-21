import numpy as np
import matplotlib.pyplot as plt


def boundaries_ammonia(df):
    df = df[df['qtyUnitAbbr'] == 'kg']  #qty in kg
    nomissingdata = df[(df['qty'] != 0) & (df['netWgt'] != 0) & (df['primaryValue'] != 0)]
    nomissingdata['valueperqty'] = nomissingdata['primaryValue']/nomissingdata['qty']
    nomissingdata['valuepernetwgt'] = nomissingdata['primaryValue']/nomissingdata['netWgt']
    # boundaries valueperqty
    hist, bins, _ = plt.hist(nomissingdata['valueperqty'], range=(0, 2 * nomissingdata['valueperqty'].median()),
                             bins=50)
    a = round(bins[np.where(hist > 0.25 * hist.max())[0][0]], 2)  # lower boundary for valueperqty
    b = round(bins[(np.where(hist > 0.25 * hist.max())[0][-1]) + 1], 2)  # upper boundary for valueperqty
    m1 = (a + b) / 2  # value in the middle between boundaries

    #boundaries valuepernetwgt
    hist, bins, _ = plt.hist(nomissingdata['valuepernetwgt'], range=(0, 10 * nomissingdata['valuepernetwgt'].median()),
                             bins=50)
    c = round(bins[np.where(hist > 0.25 * hist.max())[0][0]], 2)  # lower boundary for valuepernetwgt
    d = round(bins[(np.where(hist > 0.25 * hist.max())[0][-1]) + 1], 2)  # upper boundary for valuepernetwgt
    m2 = (c + d) / 2  # value in the middle between boundaries
    # mean value between valuepernetwgt and valueperqty in kg
    m = (m1 + m2) / 2
    #import statistics
    #m = (nomissingdata['valueperqty'].median() + nomissingdata['valuepernetwgt'].median() )/2

    return a, b, c, d, m

def boundaries_10(df): 
    #df = df[df['qtyUnitAbbr'] == 'kg']  #qty in kg
    #nomissingdata = df[(df['qty'] != 0) & (df['netWgt'] != 0) & (df['primaryValue'] != 0)]
    #nomissingdata for netwgt
    nomissingdata = df[df['netWgt'] != 0]
    #nomissingdata['valueperqty'] = nomissingdata['primaryValue']/nomissingdata['qty']
    #nomissingdata['valuepernetwgt'] = nomissingdata['primaryValue']/nomissingdata['netWgt']
    
    # boundaries valueperqty
    nomissingdata_kg = df[(df['qtyUnitAbbr'] == 'kg') & (df['qty'] != 0)]
    #nomissingdata_kg['valueperqty'] = nomissingdata_kg['primaryValue']/nomissingdata_kg['qty']
    #nomissingdata_kg['valuepernetwgt'] = nomissingdata_kg['primaryValue']/nomissingdata_kg['netWgt']
    hist, bins, _ = plt.hist(nomissingdata_kg['valueperqty'], range=(0, 2 * nomissingdata_kg['valueperqty'].median()),
                            bins=150)

    max_count_index = np.argmax(hist)
    bin_with_max_count = (bins[max_count_index] + bins[max_count_index + 1])/2

    a = 1/10 * bin_with_max_count # lower boundary for valueperqty
    b = 10 * bin_with_max_count  # upper boundary for valueperqty
    m1 = bin_with_max_count  

    #boundaries valuepernetwgt
    hist, bins, _ = plt.hist(nomissingdata['valuepernetwgt'], range=(0, 2 * nomissingdata['valuepernetwgt'].median()),
                            bins=150)

    max_count_index = np.argmax(hist)
    bin_with_max_count = (bins[max_count_index] + bins[max_count_index + 1])/2

    c = 1/10 * bin_with_max_count # lower boundary for valuepernetwgt
    d = 10 * bin_with_max_count  # upper boundary for valuepernetwgt
    m2 = bin_with_max_count  

    # correcting value in USD/kg
    m = (m1 + m2) / 2
    #plot
    # Erstellen der Subplots
    fig, axs = plt.subplots(2, 2, figsize=(12, 10))

    # Plot 1: Histogramm von nomissingdata_kg['valueperqty']
    axs[0, 0].hist(nomissingdata_kg['valueperqty'], bins=50, edgecolor='black',range=(0, 10 * nomissingdata_kg['valueperqty'].median()))
    axs[0, 0].set_title('Histogram of valueperqty')
    axs[0, 0].axvline(x=a, color='g', linestyle='--', label = 'boundaries')
    axs[0, 0].axvline(x=b, color='g', linestyle='--')   
    axs[0, 0].axvline(x=m1, color='r', linestyle='-', label = 'correction value')
    axs[0, 0].legend(loc='upper right')

    # Plot 2: Histogramm von nomissingdata_kg['valueperqty'] mit Gewichtung durch nomissingdata_kg['qty']
    axs[0, 1].hist(nomissingdata_kg['valueperqty'], bins=50, weights=nomissingdata_kg['qty'], edgecolor='black' ,range=(0, 10 * nomissingdata_kg['valueperqty'].median()))
    axs[0, 1].set_title('Histogram of valueperqty (Weighted by qty)')
    axs[0, 1].axvline(x=a, color='g', linestyle='--', label = 'boundaries')
    axs[0, 1].axvline(x=b, color='g', linestyle='--')
    axs[0, 1].axvline(x=m1, color='r', linestyle='-', label = 'correction value')
    axs[0, 1].legend(loc='upper right')
    # Plot 3: Histogramm von nomissingdata['valuepernetwgt']
    axs[1, 0].hist(nomissingdata['valuepernetwgt'], bins=50, edgecolor='black' ,range=(0, 10 * nomissingdata['valuepernetwgt'].median()))
    axs[1, 0].set_title('Histogram of valuepernetwgt')
    axs[1, 0].axvline(x=c, color='g', linestyle='--', label = 'boundaries')
    axs[1, 0].axvline(x=d, color='g', linestyle='--')
    axs[1, 0].axvline(x=m2, color='r', linestyle='-', label = 'correction value')
    axs[1, 0].legend(loc='upper right')
    # Plot 4: Histogramm von nomissingdata['valuepernetwgt'] mit Gewichtung durch nomissingdata['netwgt']
    axs[1, 1].hist(nomissingdata['valuepernetwgt'], bins=50, weights=nomissingdata['netWgt'], edgecolor='black' ,range=(0, 10 * nomissingdata['valuepernetwgt'].median()))
    axs[1, 1].set_title('Histogram of valuepernetwgt (Weighted by netwgt)')
    axs[1, 1].axvline(x=c, color='g', linestyle='--', label = 'boundaries')
    axs[1, 1].axvline(x=d, color='g', linestyle='--')
    axs[1, 1].axvline(x=m2, color='r', linestyle='-', label = 'correction value')
    axs[1, 1].legend(loc='upper right')
    # Layout-Anpassungen
    plt.tight_layout()

    # Anzeigen des Plots
    plt.show()


    return a,b,c,d,m



def correctedqtyinkg_ammonia(row, a, b, c, d, m):
    qty = row['qty']
    netwgt = row['netWgt']
    primaryvalue = row['primaryValue']
    valueperqty = primaryvalue/row['qty']
    valuepernetwgt = primaryvalue/row['netwgt']
    #qty in u
    if row['qtyUnitAbbr'] == 'u':
        valueperqty = np.inf
    # qty in l
    if row['qtyUnitAbbr'] == 'l':
        qty = qty / 1.466  # liter to kg
        valueperqty = valueperqty * 1.466  #pro liter to pro kg
    # qty in N/A
    if row['qtyUnitAbbr'] == 'N/A':
        valueperqty = np.inf
    # qty im m^3
    if row['qtyUnitCode'] == 12:
        qty = qty / 1.386
        valueperqty = valueperqty * 1.386

    #qty in kg
    if (a <= valueperqty <= b) and (c <= valuepernetwgt <= d):
        if abs(valueperqty - m) < abs(valuepernetwgt - m):
            return (qty)
        else:
            return (netwgt)
    elif (a <= valueperqty <= b) and (valuepernetwgt > d or valuepernetwgt < c):
        return (qty)
    elif (valueperqty < a or valueperqty > b) and (c <= valuepernetwgt <= d):
        return (netwgt)
    elif (valueperqty < a or valueperqty > b) and (valuepernetwgt < c or valuepernetwgt > d):
        return (primaryvalue / m)  #value in USD/(m in USD/kg)->kg

def before_correcting(df):
    df['valueperqty'] = df['primaryValue']/df['qty']
    df['valuepernetwgt'] = df['primaryValue']/df['netWgt']
    return(df)

def qty_correcting(row ,a ,b, c, d, m):
    if (row['qtyUnitAbbr'] == 'kg') and (a <= row['valueperqty'] <= b):
        return(row['qty'])
    elif (row['netWgt'] != 0) and (c <= row['valuepernetwgt'] <= d ):
        return(row['netWgt'])
    else:
        return(row['primaryValue']/m)
    

