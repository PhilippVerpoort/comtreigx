
import pandas as pd 
import seaborn as sns
from si_prefix import si_format
import plotly.graph_objects as go


def sankey_geomapped(df):
    # sankey data for geomapped data 
    source_indices = []
    target_indices = []
    values = []
    colors = []
    colors2 = []

    # Dictionary für die Summen der ausgehenden Flüsse von Reportern
    sum_rep = {}
    for reporter in df['reporterDesc'].unique():
        sum_rep[reporter] = si_format(df[df['reporterDesc'] == reporter]['correctedqtyinkg'].sum()/1000) #tonnen

    # Dictionary für die Summen der eingehenden Flüsse von Partnern
    sum_par = {}
    for partner in df['partnerDesc'].unique():
        sum_par[partner] = si_format(df[df['partnerDesc'] == partner]['correctedqtyinkg'].sum()/1000) #tonnen

    # Aktualisierung des DataFrames mit den Summen der ausgehenden Flüsse von Reportern
    df['reporterDesc'] = df['reporterDesc'] + ' (' + df['reporterDesc'].map(sum_rep).astype(str) + 't )'

    # Aktualisierung des DataFrames mit den Summen der eingehenden Flüsse von Partnern
    df['partnerDesc'] = df['partnerDesc'] + ' (' + df['partnerDesc'].map(sum_par).astype(str) + 't )'


    # colors for geomapped data 
    countrylist = df['reporter_map'].unique() #countrylist for reporter_map = countrylist for partner_map
    #colorlist = plt.cm.tab10.colors
    colorlist = sns.color_palette("husl", len(countrylist))
    colorlist = colorlist.as_hex()

    color_dict = {}
    for i, country in enumerate(countrylist):
        #color = 'rgb' + str(colorlist[i][:3])
        color = colorlist[i]
        color_dict[country] = color


    # sankey data 
    for index, row in df.iterrows():
        source_indices.append(df['partner_map'].tolist().index(row['partner_map']))
        target_indices.append(len(df['partner_map']) + df['reporter_map'].tolist().index(row['reporter_map']))
        values.append(row['correctedqtyinkg']/1000) #value in Tonnen
        colors.append(color_dict.get(row['partner_map'], 'blue'))
        colors2.append(color_dict.get(row['reporter_map'], 'blue'))

    colors3 = colors+colors2
    
    # sankey diagram for geomapped data
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=30,
            thickness=50,
            line=dict(color="black", width=1),
            label=mapped['partner_map'].tolist() + mapped['reporter_map'].tolist(),
            color=colors3
        ),
        link=dict(
            source=source_indices,
            target=target_indices,
            value=values,
            color=colors,
            hovertemplate='%{value}t<extra></extra>'
        )
    )])

    fig.update_layout(title_text="Sankey diagram for ammonia - mapped regions",
                      font=dict(size=10),
                      height = 800)

    fig.show()

def sankey_d(df,colors_target):
    # sankey data
    source_indices = []
    target_indices = []
    values = []
    colors = []
    

    # Dictionary für die Summen der ausgehenden Flüsse von Reportern
    sum_rep = {}
    for reporter in df['reporterDesc'].unique():
        sum_rep[reporter] = si_format(df[df['reporterDesc'] == reporter]['correctedqtyinkg'].sum()/1000) #tonnen

    # Dictionary für die Summen der eingehenden Flüsse von Partnern
    sum_par = {}
    for partner in df['partnerDesc'].unique():
        sum_par[partner] = si_format(df[df['partnerDesc'] == partner]['correctedqtyinkg'].sum()/1000) #tonnen

    # Aktualisierung des DataFrames mit den Summen der ausgehenden Flüsse von Reportern
    df['reporterDesc'] = df['reporterDesc'] + ' (' + df['reporterDesc'].map(sum_rep).astype(str) + 't )'

    # Aktualisierung des DataFrames mit den Summen der eingehenden Flüsse von Partnern
    df['partnerDesc'] = df['partnerDesc'] + ' (' + df['partnerDesc'].map(sum_par).astype(str) + 't )'

    if colors_target == 'yes':
        colors2 = []
        # colors
        countrylist1 = df['partnerDesc'].unique().tolist()
        countrylist2 = df['reporterDesc'].unique().tolist()
        countrylist = np.unique(countrylist1 + countrylist2)
        colorlist = sns.color_palette("husl", len(countrylist))
        colorlist = colorlist.as_hex()
        colorlist = colorlist[0:len(countrylist)]

        color_dict = {}
        for i, country in enumerate(countrylist):
            color = colorlist[i]
            color_dict[country] = color
    else:
        # colors
        countrylist = df['partnerDesc'].unique()
        colorlist = plt.cm.tab10.colors
        colorlist = colorlist[0:5]

        color_dict = {}
        for i, country in enumerate(countrylist):
            color = 'rgb' + str(colorlist[i][:3])
            color_dict[country] = color
    

    # sankey data
    for index, row in df.iterrows():
        source_indices.append(df['partnerDesc'].tolist().index(row['partnerDesc']))
        target_indices.append(len(df['partnerDesc']) + df['reporterDesc'].tolist().index(row['reporterDesc']))
        values.append(row['correctedqtyinkg']/1000) #value in Tonnen
        colors.append(color_dict.get(row['partnerDesc'], 'blue'))
        colors2.append(color_dict.get(row['reporterDesc'], 'blue'))
     
    colors3 = colors+colors2
    # sankey diagram
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=30,
            thickness=50,
            line=dict(color= 'black',width=1),
            label=df['partnerDesc'].tolist() + df['reporterDesc'].tolist(),
            color=colors3 
        ),
        link=dict(
            source=source_indices,
            target=target_indices,
            value=values,
            color=colors,
            hovertemplate='%{value}t<extra></extra>'
        )
    )])

    fig.update_layout(title_text="Sankey diagram for ammonia",
                      font=dict(size=10),
                      height = 800)
    fig.update_traces(visible= True, selector=dict(type='sankey')) 
    fig.update_traces(legend= 'legend' , selector=dict(type='sankey')) 
    fig.show()
