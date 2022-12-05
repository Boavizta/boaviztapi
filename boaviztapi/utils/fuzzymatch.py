import pandas as pd
from pandas import DataFrame
from pandas.core.series import Series
from rapidfuzz import process, fuzz


def fuzzymatch_attr_from_pdf(name: str, attr: str, pdf: DataFrame) -> str:
    name_list = list(pdf[attr].unique())

    result = process.extractOne(name, name_list, scorer=fuzz.WRatio)
    if result is not None:
        result = result[0] if result[1] > 88.0 else None
    return result or None


def fuzzymatch(s: pd.Series, value: str, threshold: float = 90.) -> pd.Series:
    return s.apply(lambda x: fuzz.token_sort_ratio(x.lower(), value.lower()) >= threshold)


def pandas() -> None:
    Series.fuzzymatch = fuzzymatch
