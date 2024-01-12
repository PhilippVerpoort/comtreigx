import pandas
import comtradeapicall
import yaml
subscription_key = '199c3865f7304c358fc1012098e09186'
# dataframe for naturalgas (271111 liquid, 271121 gaseous)
naturalgas_2022 = comtradeapicall.getTarifflineData(subscription_key, typeCode='C', freqCode='A', clCode='HS', period='2022',
                                         reporterCode='', cmdCode='271111,271121', flowCode='', partnerCode='',
                                         partner2Code=None,
                                         customsCode=None, motCode=None, maxRecords=250000, format_output='JSON',
                                         countOnly=None, includeDesc=True)
naturalgas_2022 = naturalgas_2022[['cmdCode','reporterDesc','flowDesc','partnerDesc','motDesc','netWgt','qty','qtyUnitAbbr']]


def geomap(distribution): #function which returns a dictoinary with the regions as keys and the countries which belong to the regions as values
    #input: distribution 'R5', 'R9' or 'R10'
    with open("common.yaml", 'r') as yaml_file: #open common.yaml file which contains the distribution of countrys into (5,9 or 10) regions
        yaml_content = yaml.safe_load(yaml_file)
        
    a = {
        k: {
            key: value["countries"]
            for d2 in v for key, value in d2.items() if "countries" in value
        }
        for d in yaml_content for k, v in d.items() if k != "common"
    }
    return(a[distribution]) 

def geo_mapping(country,geomap): #function which returns the region the country belongs to according to the geomap for a given country and geomap (from geomap function) 

    
    country = country.rstrip()
    country = country.rstrip('.')
    index = -1
    index = country.find(' (')
    if index == -1:
        index = country.find(', ')
    if index != -1:
        country = country[:index]
    
    for key in geomap.keys(): #check for every key (region) if the country is listed 
        if country in geomap[key]:
            return(key)
            break
    else: #if the country is not found in the dictoinary values, change it manually 
        if country == 'United States of America':
            country = 'United States'
        elif country == 'USA':
            country = 'United States'
        elif country == 'Andorra':
            country = 'Italy'
        elif country == 'Türkiye':
            country = 'Turkey'
        elif country == 'Gibraltar':
            country = 'Spain'
        elif country == 'Bosnia Herzegovina':
            country = 'Bosnia and Herzegovina'
        elif country == 'Dem. Rep. of the Congo':
            country = 'Congo'
        elif country == 'State of Palestine':
            country = 'Palestine'
        elif country == 'Rep. of Korea':
            country = 'South Korea'
        elif country == 'Other Asia':
            country = 'Taiwan'
        elif country == 'Rep. of Moldova':
            country = 'Romania'
        elif country == 'United Rep. of Tanzania':
            country = 'Tanzania'
        elif country == 'Metropolitan France':
            country = 'France'
        elif country == 'Other Europe':
            country = 'Germany'
        elif country == 'Turks and Caicos Isds':
            country = 'Cuba'
        #elif country == 'Areas':
            #country = ''
        #elif country == 'Bunkers':
            #country = ''
        elif country == 'San Marino':
            country = 'Italy'
        #elif country == 'Free Zones':
            #country = 
        elif country == 'Saint Helena':
            country = 'Angola'
        #elif country == 'Special Categories':
            #country =
        elif country == "Lao People's Dem. Rep":
            country = 'Laos'
        elif country == 'Pitcairn':
            country = 'Chile' #? 
        for key in geomap.keys(): #after changing the country variable manually go through the dictoinary again
            if country in geomap[key]:
                return(key)
                break

allocation = geomap('R10') #allocation for distribution in 10 regions
#new columns for mapped reporter and partner region 
naturalgas_2022.loc[:,'reporter_map'] = naturalgas_2022['reporterDesc'].apply(lambda x: geo_mapping(x, allocation))
naturalgas_2022.loc[:,'partner_map'] = naturalgas_2022['partnerDesc'].apply(lambda y: geo_mapping(y, allocation))
#grouped dataframe for total sum of weight in kg 
grouped = naturalgas_2022.groupby(['reporter_map', 'partner_map', 'flowDesc'])['netWgt'].sum().reset_index()
print(grouped['flowDesc'].unique()) #diffenrent types of flows
#dataframes for export and import flows individually 
grouped_i = grouped[grouped['flowDesc'].isin(['Import', 'Foreign Import'])]
grouped_e = grouped[grouped['flowDesc'].isin(['Export', 'Re-export', 'Export of goods for outward processing'])]