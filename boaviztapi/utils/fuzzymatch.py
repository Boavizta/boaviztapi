import pandas as pd
from pandas.core.series import Series
from rapidfuzz import process, fuzz
from rapidfuzz.distance import Hamming, Levenshtein
from typing import List, Tuple, Union

from boaviztapi import config


def fuzzymatch_attr_from_cpu_name(
    cpu_name: str, df: pd.DataFrame
) -> Union[Tuple[str, str, str, str, int, int, int, int, str, str], None]:
    cpu_name = cpu_name.lower()
    score = df["name"].str.lower().apply(lambda x: fuzz.token_set_ratio(x, cpu_name))
    max_score = score.max()
    if max_score <= config.cpu_name_fuzzymatch_threshold:
        return None
    else:
        best = df.iloc[score.idxmax()]
        best = best.mask(best.isnull(), None)  # replace all NaN by None

        def safe_int(x):
            return x if x is None else int(x)  # float to int but keep None

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


def fuzzymatch_attr_from_gpu_name(
    gpu_name: str, df: pd.DataFrame
) -> Union[
    Tuple[
        str,
        str,
        float,
        float,
        float,
        float,
        float,
        float,
        float,
        float,
        float,
        float,
        str,
    ],
    None,
]:
    gpu_name = gpu_name.lower()
    score = df["name"].str.lower().apply(lambda x: fuzz.token_set_ratio(x, gpu_name))
    max_score = score.max()
    if max_score <= config.gpu_name_fuzzymatch_threshold:
        return None
    else:
        best = df.iloc[score.idxmax()]
        best = best.mask(best.isnull(), None)  # replace all NaN by None

        def safe_float(x):
            return x if x is None else float(x)

        return (
            best["name"],  # .name is reserved by pandas for indexes
            best.manufacturer,
            safe_float(best.number),  # number of VRAM dies
            safe_float(best.vram),
            safe_float(best.die_surface),  # effective area, already includes losses
            safe_float(best.pwb_surface),
            safe_float(best.distance_boat),
            safe_float(best.distance_truck),
            safe_float(best.distance_plane),
            safe_float(best.mass_casing),
            safe_float(best.mass_heatsink),
            safe_float(best.mass),
            best.source,
        )


def fuzzymatch_attr_from_pdf(name: str, attr: str, pdf: pd.DataFrame) -> str:
    name_list = list(pdf[attr].unique())

    result = process.extractOne(name, name_list, scorer=fuzz.WRatio)
    if result is not None:
        result = result[0] if result[1] > 79.0 else None
    return result or None


def _canonical_forms(name: str) -> set:
    """All separator/case variants of a name for parallel normalization matching."""
    base = name.strip().lower()
    if base.startswith("standard_"):
        base = base[len("standard_"):]
    return {
        base,
        base.replace(" ", "_").replace("-", "_"),
        base.replace(" ", "-").replace("_", "-"),
        base.replace(" ", "").replace("_", "").replace("-", ""),
    }


def fuzzymatch_cloud_instance_name(
    instance_type: str, candidates: List[str]
) -> Union[str, None]:
    """
    Resolve an instance id by testing all separator/case variants in parallel,
    then falling back to Hamming and Levenshtein distance.
    Returns None when no candidate exceeds the configured threshold.
    """
    req_forms = _canonical_forms(instance_type)

    # Stage 1: any request form matches any candidate form exactly
    for cand in candidates:
        if req_forms & _canonical_forms(cand):
            return cand

    threshold = config.cloud_instance_name_fuzzymatch_threshold / 100.0
    # One representative key per candidate (space/dash → underscore)
    cand_keys = {c.lower().replace(" ", "_").replace("-", "_"): c for c in candidates}

    # Stage 2: Hamming — try every request form, keep best equal-length hit
    best_cand: Union[str, None] = None
    best_score = 0.0
    for req_key in req_forms:
        same_len = {k: v for k, v in cand_keys.items() if len(k) == len(req_key)}
        if not same_len:
            continue
        hit = process.extractOne(
            req_key, list(same_len.keys()), scorer=Hamming.normalized_similarity
        )
        if hit and hit[1] > best_score:
            best_cand, best_score = same_len[hit[0]], hit[1]
    if best_cand and best_score >= threshold:
        return best_cand

    # Stage 3: Levenshtein — try every request form, keep best hit
    best_cand, best_score = None, 0.0
    for req_key in req_forms:
        hit = process.extractOne(
            req_key, list(cand_keys.keys()), scorer=Levenshtein.normalized_similarity
        )
        if hit and hit[1] > best_score:
            best_cand, best_score = cand_keys[hit[0]], hit[1]
    if best_cand and best_score >= threshold:
        return best_cand
    return None


def fuzzymatch(s: pd.Series, value: str, threshold: float = 90.0) -> pd.Series:
    return s.apply(
        lambda x: fuzz.token_sort_ratio(x.lower(), value.lower()) >= threshold
    )


def pandas() -> None:
    Series.fuzzymatch = fuzzymatch
