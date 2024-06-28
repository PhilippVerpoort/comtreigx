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

    #nomissingdata for netwgt
    nomissingdata = df[df['netWgt'] != 0]
    #nomissingdata for qty
    nomissingdata_kg = df[(df['qtyUnitAbbr'] == 'kg') & (df['qty'] != 0)]
    #boundaries valueperqty
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

    def add_lines_and_legend(ax, a, b, m1):
        ax.axvline(x=a, color='g', linestyle='--', label=f'Boundaries ({round(a,2)}, {round(b,2)})')
        ax.axvline(x=b, color='g', linestyle='--')
        ax.axvline(x=m, color='r', linestyle='-', label=f'Correcting value\n m: {round(m,2)}')
        ax.legend(loc='upper right')
    
    fig, axs = plt.subplots(2, 2, figsize=(12, 10))

    # Plot 1: Histogram valueperqty
    axs[0, 0].hist(nomissingdata_kg['valueperqty'], bins=50, edgecolor='black',range=(0, 2*b))
    axs[0, 0].set_title('Histogram of valueperqty [USD/kg]')
    add_lines_and_legend(axs[0, 0], a, b, m1)

    # Plot 2 Histogram of valueperqty (Weighted by qty)
    axs[0, 1].hist(nomissingdata_kg['valueperqty'], bins=50, weights=nomissingdata_kg['qty'], edgecolor='black' ,range=(0, 2*b))
    axs[0, 1].set_title('Histogram of valueperqty (Weighted by qty) [USD/kg]')
    add_lines_and_legend(axs[0, 1], a, b, m1)
    # Plot 3: Histogram of valuepernetwgt [USD/kg]
    axs[1, 0].hist(nomissingdata['valuepernetwgt'], bins=50, edgecolor='black' ,range=(0, 2*d))
    axs[1, 0].set_title('Histogram of valuepernetwgt [USD/kg]')
    add_lines_and_legend(axs[1, 0], c, d, m2)
    # Plot 4: Histogram of valuepernetwgt (Weighted by netwgt)
    axs[1, 1].hist(nomissingdata['valuepernetwgt'], bins=50, weights=nomissingdata['netWgt'], edgecolor='black' ,range=(0, 2*d))
    axs[1, 1].set_title('Histogram of valuepernetwgt (Weighted by netwgt) [USD/kg]')
    add_lines_and_legend(axs[1, 1], c, d, m2)
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
        diff = 0
        w = row['qty'] #weight
        return(row['qty'],diff,w)
    elif (row['netWgt'] != 0) and (c <= row['valuepernetwgt'] <= d ):
        diff = 0
        w = row['netWgt']
        return(row['netWgt'],diff,w)
    else:
        if (row['qtyUnitAbbr'] == 'kg') and (row['qty'] != 0):
            w = row['qty'] #weight
            diff = 100*(row['qty']-(row['primaryValue']/m))/(row['primaryValue']/m)
        elif row['netWgt'] != 0:
            w = row['netWgt'] #weight
            diff = 100*(row['netWgt']-(row['primaryValue']/m))/(row['primaryValue']/m)
        else:
            diff = -1 #(0-row['primaryValue']/m)/(row['primaryValue']/m)
            w = row['primaryValue']/m
        return(row['primaryValue']/m, diff, w)
    
def differences(df):
    import numpy as np
    d = df[df['diff'] != 0]
    mini = d['diff'].min()
    
    if np.isneginf(mini):
        mini = 1/10*df['diff'].median()-2*abs(df['diff'].median())
        l = mini - 10*abs(df['diff'].median())
    else:
        l = d['diff'].min()
    if np.isposinf(d['diff'].max()):
        u = 10*df['diff'].median()+10*abs(df['diff'].median())
    else:
        u = d['diff'].max()
    maxi = -mini  
    print(l,u,d['diff'].median())
    fig, axs = plt.subplots(2, 2, figsize=(12, 10))

    # Plot 
    axs[0,0].hist(d['diff'], bins=50, edgecolor='black',range=(l,u))
    axs[0,0].set_title('Difference between qty and corrected qty [%]')
    axs[0,1].hist(d['diff'], bins=50, weights= d['w'], edgecolor='black' ,range=(l,u))
    axs[0,1].set_title('Difference between qty and corrected qty [%] (Weighted by qty)')
    axs[1,0].hist(d['diff'], bins=150, edgecolor='black',range=(mini,maxi))
    axs[1,0].set_title('Difference between qty and corrected qty [%]')
    axs[1,1].hist(d['diff'], bins=150, weights= d['w'], edgecolor='black',range=(mini,maxi) )
    axs[1,1].set_title('Difference between qty and corrected qty [%] (Weighted by qty)')


def correction_and_results(comm,year,subscription_key,directory):
    from get_data import load_data
    idata = load_data(year,comm,directory,subscription_key)
    df = before_correcting(idata) 
    a,b,c,d,m = boundaries_10(df) 
    df[['correctedqtyinkg', 'diff','w']] = df.apply(qty_correcting, args=(a, b, c, d, m), axis=1, result_type='expand')
    differences(df)
