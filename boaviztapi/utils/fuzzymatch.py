import pandas as pd
from pandas.core.series import Series
from rapidfuzz import process, fuzz
from rapidfuzz.distance import Hamming, Levenshtein
from typing import List, Optional, Tuple, Union

from boaviztapi import config


def best_name_matches(name: str, df: pd.DataFrame, threshold: int) -> pd.DataFrame:
    """Rows whose name ties for the best fuzzy score, or no rows if none passes the threshold."""
    name = name.lower()
    score = df["name"].str.lower().apply(lambda x: fuzz.token_set_ratio(x, name))
    max_score = score.max()
    if max_score <= threshold:
        return df.iloc[:0]
    return df[score == max_score]


def ambiguous_name_warning(
    name: str, df: pd.DataFrame, threshold: int, kind: str
) -> Optional[str]:
    """Warning for a name that matches several rows equally well, or None if the match is unique."""
    names = list(best_name_matches(name, df, threshold)["name"])
    if len(names) < 2:
        return None
    shown = ", ".join(names[:5])
    if len(names) > 5:
        shown += f" and {len(names) - 5} more"
    return (
        f"'{name}' matches {len(names)} {kind}s equally well ({shown}). "
        f"Used '{names[0]}'; give the full name to choose another."
    )


def fuzzymatch_attr_from_cpu_name(
    cpu_name: str, df: pd.DataFrame
) -> Union[Tuple[str, str, str, str, int, int, int, int, str, str], None]:
    matches = best_name_matches(cpu_name, df, config.cpu_name_fuzzymatch_threshold)
    if matches.empty:
        return None
    else:
        best = matches.iloc[0]
        best = best.mask(best.isnull(), None)  # replace all NaN by None

        def safe_int(x: Optional[float]) -> Optional[int]:
            return x if x is None else int(x)

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
        float,
        float,
        str,
    ],
    None,
]:
    matches = best_name_matches(gpu_name, df, config.gpu_name_fuzzymatch_threshold)
    if matches.empty:
        return None
    else:
        best = matches.iloc[0]
        best = best.mask(best.isnull(), None)  # replace all NaN by None

        def safe_float(x: Optional[float]) -> Optional[float]:
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
            safe_float(best.tdp),  # board power per card, in W
            safe_float(best.gpus_per_card),
            best.source,
        )


def fuzzymatch_attr_from_pdf(name: str, attr: str, pdf: pd.DataFrame) -> Optional[str]:
    name_list = list(pdf[attr].unique())

    result = process.extractOne(name, name_list, scorer=fuzz.WRatio)
    if result is not None:
        result = result[0] if result[1] > 79.0 else None
    return result or None


def _canonical_forms(name: str) -> set[str]:
    """All separator/case variants of a name for parallel normalization matching."""
    base = name.strip().lower()
    if base.startswith("standard_"):
        base = base[len("standard_") :]
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
    for candidate in candidates:
        if req_forms & _canonical_forms(candidate):
            return candidate

    threshold = config.cloud_instance_name_fuzzymatch_threshold / 100.0
    # One representative key per candidate (space/dash → underscore)
    candidate_keys = {
        c.lower().replace(" ", "_").replace("-", "_"): c for c in candidates
    }

    # Stage 2: Hamming — try every request form, keep best equal-length hit
    best_cand: Union[str, None] = None
    best_score = 0.0
    for req_key in req_forms:
        same_len = {k: v for k, v in candidate_keys.items() if len(k) == len(req_key)}
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
            req_key,
            list(candidate_keys.keys()),
            scorer=Levenshtein.normalized_similarity,
        )
        if hit and hit[1] > best_score:
            best_cand, best_score = candidate_keys[hit[0]], hit[1]
    if best_cand and best_score >= threshold:
        return best_cand
    return None


def fuzzymatch(s: pd.Series, value: str, threshold: float = 90.0) -> pd.Series:
    return s.apply(
        lambda x: fuzz.token_sort_ratio(x.lower(), value.lower()) >= threshold
    )


def pandas() -> None:
    Series.fuzzymatch = fuzzymatch
