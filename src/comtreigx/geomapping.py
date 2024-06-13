import pandas as pd
import pycountry
import yaml

from comtreigx.paths import CONFIG_PATH

pycountry.countries.add_entry(alpha_2='xx', alpha_3='xxx', name='areas, nes', numeric='')
pycountry.countries.add_entry(alpha_2='xx', alpha_3='xxx', name='other europe, nes', numeric='')
pycountry.countries.add_entry(alpha_2='xx', alpha_3='xxx', name='bunkers', numeric='')
pycountry.countries.add_entry(alpha_2='xx', alpha_3='xxx', name='free zones', numeric='')
pycountry.countries.add_entry(alpha_2='xx', alpha_3='xxx', name='special categories', numeric='')
pycountry.countries.add_entry(alpha_2='xx', alpha_3='xxx', name='other asia, nes', numeric='')

def add_correctedcodes(data, isocode_all):
    # add new columns with corrected iso code numbers of partner and reporter
    data['partnercode_c'] = data.apply(lambda row: row['partnerCode'] if row['partnerCode'] in isocode_all else truecode(row['partnerDesc']), axis=1)
    data['reportercode_c'] = data.apply(lambda row: row['reporterCode'] if row['reporterCode'] in isocode_all else truecode(row['reporterDesc']), axis=1)
    return data

def truecode(countryDesc):
    lst = pycountry.countries.search_fuzzy(countryDesc)
    return(lst[0].numeric)

#data2 = add_correctedcodes(idata,isocode_all) #add corrected iso codes to dataframe

# function that return iso code to a given country name
def isonum(country):
    country_full = pycountry.countries.get(name=country)
    if country_full == None:
        country_full = pycountry.countries.search_fuzzy(country)[0]
    return(country_full.numeric)

def geomap(distribution): #function which returns a dictoinary with the regions as keys and the countries which belong to the regions as values
    #input: distribution 'R5', 'R9' or 'R10'
    with open(CONFIG_PATH / 'common.yaml', 'r') as yaml_file: #open common.yaml file which contains the distribution of countrys into (5,9 or 10) regions
        yaml_content = yaml.safe_load(yaml_file)
        
    a = {
        k: {
            key: value["countries"]
            for d2 in v for key, value in d2.items() if "countries" in value
        }
        for d in yaml_content for k, v in d.items() if k != "common"
    }
    b = a[distribution]
    pycountry.countries.add_entry(alpha_2="CG", alpha_3="COG", name="Democratic Republic of the Congo", numeric="178")
    pycountry.countries.add_entry(alpha_2="TR", alpha_3="TUR", name="Turkey", numeric="792")
    pycountry.countries.add_entry(alpha_2="VI", alpha_3="VIR", name="United States Virgin Islands", numeric="850")
    #missing country codes 
    missingcodes = {'178': ['180'], '250':['020'],'214':['212','796'],'724':['292'],'380':['674'],'024':['654'],'554':['612']}
    for key in b.keys():
        countries = b[key].split(', ')
        b[key] = [isonum(c) for c in countries]
        #add missing country codes to dictoinary
        for x in missingcodes.keys():
            if x in b[key]:
                for y in missingcodes[x]:
                    b[key].append(str(y))
                #print(b[key])
    return b



# function that returns the region for a given iso code of an country 
def geo_mapping(country_iso, mapg):
    for key in mapg.keys():
        if country_iso in mapg[key]:
            return(key)
            break

def data_geomap(df):
    wikidata = pd.read_csv('wikipedia-iso-country-codes.csv')
    isocode_all = list(wikidata['Numeric code']) #isocodes of all countries

    #import pycountry
    #pycountry.countries.add_entry(alpha_2='xx', alpha_3='xxx', name='areas, nes', numeric='')
    #pycountry.countries.add_entry(alpha_2='xx', alpha_3='xxx', name='other europe, nes', numeric='')
    #pycountry.countries.add_entry(alpha_2='xx', alpha_3='xxx', name='bunkers', numeric='')
    #pycountry.countries.add_entry(alpha_2='xx', alpha_3='xxx', name='free zones', numeric='')
    #pycountry.countries.add_entry(alpha_2='xx', alpha_3='xxx', name='special categories', numeric='')
    #pycountry.countries.add_entry(alpha_2='xx', alpha_3='xxx', name='other asia, nes', numeric='')

    data2 = add_correctedcodes(df,isocode_all) #add corrected iso codes to dataframe

    #geomap for 10 regions
    mapg = geomap('R10')
    #apply geomapping function to corrected reporter and partner code
    data2.loc[:,'reporter_map'] = data2['reportercode_c'].apply(lambda x: geo_mapping(str(x).zfill(3), mapg))
    data2.loc[:,'partner_map'] = data2['partnercode_c'].apply(lambda y: geo_mapping(str(y).zfill(3), mapg))

    return(data2)