import pandas as pd
from pandas.core.series import Series
from rapidfuzz import process, fuzz
from typing import Tuple, Union

from boaviztapi import config


def fuzzymatch_attr_from_cpu_name(cpu_name: str, df: pd.DataFrame) -> Union[
    Tuple[str, str, str, str, int, int, int, int, str, str], None]:
    cpu_name = cpu_name.lower()
    score = df["name"].str.lower().apply(lambda x: fuzz.token_set_ratio(x, cpu_name))
    max_score = score.max()
    if max_score <= config["cpu_name_fuzzymatch_threshold"]:
        return None
    else:
        best = df.iloc[score.idxmax()]
        best = best.mask(best.isnull(), None)  # replace all NaN by None
        safe_int = lambda x: x if x is None else int(x)  # float to int but keep None

        return (
            best["name"],  # .name is reserved by pandas for indexes
            best.manufacturer,
            best.code_name,
            best.model_range,
            safe_int(best.tdp),
            safe_int(best.cores),
            safe_int(best.threads),
            safe_int(best.total_die_size),
            best.total_die_size_source,
            best.source,
        )


def fuzzymatch_attr_from_pdf(name: str, attr: str, pdf: pd.DataFrame) -> str:
    name_list = list(pdf[attr].unique())

    result = process.extractOne(name, name_list, scorer=fuzz.WRatio)
    if result is not None:
        result = result[0] if result[1] > 79.0 else None
    return result or None


def fuzzymatch(s: pd.Series, value: str, threshold: float = 90.0) -> pd.Series:
    return s.apply(lambda x: fuzz.token_sort_ratio(x.lower(), value.lower()) >= threshold)


def pandas() -> None:
    Series.fuzzymatch = fuzzymatch
