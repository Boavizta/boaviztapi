from api.model.impacts import Impact, Impacts

import pandas as pd
import re
import os



def ref_data_server(server):
    database_file = "./api/service/server_impact/ref/boavizta-data-us.csv"
    database = pd.read_csv(database_file)
    df = database[database['name'].str.contains(server.model.name, regex=False, flags=re.IGNORECASE)]
    if(len(df) >0):
        # add a scope 3 computation
        df['scope_3'] = df.apply(lambda row: row['gwp_total'] * row['gwp_manufacturing_ratio'], axis=1)
        mon_serveur = df.loc[df.scope_3 == df.scope_3.max()]
        return {"gwp": df.scope_3.max()}
        #impact_codes = {}
        #impact_codes["gwp"] = df.scope_3.max()
        #impacts_list = {}
        #return Impacts(impacts_list, hypothesis="not implemented")
    else:
        return {"gwp": database.iloc[1]['gwp_total'] * database.iloc[1]['gwp_manufacturing_ratio']}

'''
search :

model : (name) - done 



'''