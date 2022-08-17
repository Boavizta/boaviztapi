from typing import Optional

from pandas import DataFrame
from rapidfuzz import process, fuzz


def fuzzymatch_attr_from_pdf(name: str, attr: str, pdf: DataFrame) -> str:
    name_list = list(pdf[attr].unique())

    result = process.extractOne(name, name_list, scorer=fuzz.WRatio)
    if result is not None:
        result = result[0] if result[1] > 88.0 else None
    return result or None
