import pandas as pd

from comtreigx.paths import CONFIG_PATH


hs_codes_map = pd.read_csv(CONFIG_PATH / 'hs_codes.csv', sep=';', dtype='str') \
    .set_index('commodity') \
    .loc[:, 'hs_codes'] \
    .str.split(',')
