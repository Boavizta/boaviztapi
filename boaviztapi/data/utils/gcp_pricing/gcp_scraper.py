import os
import glob

import pandas as pd

from tqdm import tqdm

from boaviztapi import data_dir

gcp_dir = os.path.join(data_dir, 'instances/gcp')
gcp_paths = glob.glob(os.path.join(gcp_dir, '*.csv'))

dfs = []
for path in tqdm(gcp_paths, total=len(gcp_paths)):
    df = pd.read_csv(path)
    df['region'] = os.path.splitext(os.path.basename(path))[0].split('_')[1]
    df.rename(columns={'API Name': 'id'}, inplace=True)
    dfs.append(df)

gcp : pd.DataFrame = pd.concat(dfs, ignore_index=True)
gcp.set_index(['region', 'id'], inplace=True)
gcp.dropna(how='all', inplace=True)

if "__main__" == __name__:
    gcp.to_parquet('gcp.parquet', engine='fastparquet')