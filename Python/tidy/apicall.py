import pandas as pd
import comtradeapicall
def apicall(startyear,endyear, subscription_key, hscode='all'):
    importflows = 'M,FM,MIP,RM,MOP'
    if startyear == endyear:
        year = str(startyear)
    else:
        l = list(range(2019,2022))
        year = [','.join(map(str, l))]
        
    if hscode == 'all':
        hscodes_csv = pd.read_csv('hscodes.csv',sep=';')
        hscodes = hscodes_csv['Full HS code'].astype(str).tolist()
        #hscodes = [','.join(map(str, hscodes))]
        DF_list = list()
        for code in hscodes:
            print(code)
            df= comtradeapicall.getTarifflineData(subscription_key, typeCode='C', freqCode='A', clCode='HS', period=year,
                                             reporterCode='', cmdCode= code, flowCode=importflows, partnerCode='',
                                             partner2Code=None,
                                             customsCode=None, motCode=None, maxRecords=250000, format_output='JSON',
                                             countOnly=None, includeDesc=True)
            if len(df) == 250000:
                print(f'Warning: data may be incomplete, maximum number of records has been reached, hscode:{code}')
            DF_list.append(df)
        
        data = DF_list
        
    else:
        data= comtradeapicall.getTarifflineData(subscription_key, typeCode='C', freqCode='A', clCode='HS', period=year,
                                             reporterCode='', cmdCode= hscode, flowCode=importflows, partnerCode='',
                                             partner2Code=None,
                                             customsCode=None, motCode=None, maxRecords=250000, format_output='JSON',
                                             countOnly=None, includeDesc=True)
        if len(data) == 250000:
            print('Warning: data may be incomplete, maximum number of records has been reached.')
        
    return(data)