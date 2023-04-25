import pandas as pd
from pandas.core.series import Series
from rapidfuzz import process, fuzz
from typing import Tuple


def fuzzymatch_attr_from_cpu_name(cpu_name: str, df) -> Tuple[str, str, str, str, int, int, int, str, str]:
    score = lambda x: fuzz.token_set_ratio(f'{x["name"]} {"" if pd.isna(x["frequency"]) else x["frequency"]}'.lower(), cpu_name.lower())  # token_set_ratio seems a bit better than ratio
    best = df.iloc[df.apply(score, axis=1).idxmax()]  # Find the best fuzzy match
    best = best.where(pd.notna(best), None)  # Replace all NaN by None
    safe_int = lambda x: x if x is None else int(x)  # Cast from float to int but keep None values
    return best["name"], best.manufacturer, best.code_name, best.model_range, safe_int(best.tdp), safe_int(best.cores), safe_int(best.total_die_size), best.total_die_size_source, best.source  # best.name is reserved by pandas for indexes


def fuzzymatch_attr_from_pdf(name: str, attr: str, pdf: pd.DataFrame) -> str:
    name_list = list(pdf[attr].unique())

    result = process.extractOne(name, name_list, scorer=fuzz.WRatio)
    if result is not None:
        result = result[0] if result[1] > 88.0 else None
    return result or None


def fuzzymatch(s: pd.Series, value: str, threshold: float = 90.) -> pd.Series:
    return s.apply(lambda x: fuzz.token_sort_ratio(x.lower(), value.lower()) >= threshold)


def pandas() -> None:
    Series.fuzzymatch = fuzzymatch
