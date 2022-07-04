import os

import pandas as pd
from fastapi import APIRouter

utils_router = APIRouter(
    prefix='/v1/utils',
    tags=['utils']
)

data_dir = os.path.join(os.path.dirname(__file__), '../data')
_countries_df = pd.read_csv(os.path.join(data_dir, 'electricity/electricity_impact_factors.csv'))


@utils_router.get('/country_code')
async def utils_get_all_countries():
    res = {}
    for ind in _countries_df.index:
        res[_countries_df["country"][ind]] = _countries_df["code"][ind]

    return res
