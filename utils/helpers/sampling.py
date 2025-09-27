import csv
import numpy as np
import pandas as pd
from typing import Optional

# Standardized length bins (4 bins for consistency across all processing)
LENGTH_BINS = [0, 50, 200, 500, float("inf")]
LENGTH_LABELS = ["short", "medium", "long", "extra_long"]


def add_length_info(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["review_length"] = out["review_body"].fillna("").str.split().str.len()
    out = out[out["review_length"] > 0]
    out["length_bin"] = pd.cut(out["review_length"],
                               bins=LENGTH_BINS,
                               labels=LENGTH_LABELS,
                               include_lowest=True)
    out["month"] = out["review_date"].dt.to_period("M")
    return out
  
  
def stratified_sample_by_month_and_bin(df: pd.DataFrame,
                                       target_n: int,
                                       seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)

    # valid cells only (drop NaT months or NA bins)
    work = df.dropna(subset=["month", "length_bin"])
    if work.empty:
        return work

    # groups = each (month, length_bin)
    groups = list(work.groupby(["month", "length_bin"], observed=True))
    cell_sizes = np.array([len(g) for _, g in groups], dtype=int)
    n_cells = len(groups)

    # base quota per cell
    base = target_n // n_cells
    rem  = target_n - base * n_cells

    # first pass: take min(base or base+1, size)
    # give the first `rem` cells one extra
    take = np.minimum(cell_sizes, base + (np.arange(n_cells) < rem).astype(int))

    # leftover to still allocate
    leftover = target_n - int(take.sum())

    # remaining capacity per cell
    remaining = cell_sizes - take
    if leftover > 0 and remaining.sum() > 0:
        # distribute leftover proportionally to remaining capacity
        share = np.floor(remaining / remaining.sum() * leftover).astype(int)
        take += np.minimum(remaining, share)
        leftover2 = target_n - int(take.sum())

        # if rounding left a few, hand them out one-by-one to cells with capacity
        if leftover2 > 0:
            idx_order = np.argsort(-remaining)  # cells with the most capacity first
            for i in idx_order:
                if leftover2 == 0:
                    break
                if take[i] < cell_sizes[i]:
                    take[i] += 1
                    leftover2 -= 1

    # actually sample
    parts = []
    for (key, grp), n in zip(groups, take):
        if n > 0:
            parts.append(grp.sample(n=int(n), random_state=seed))

    if not parts:
        return work.iloc[0:0]  # empty

    sampled = pd.concat(parts, ignore_index=True)
    sampled = sampled.sample(frac=1, random_state=seed).reset_index(drop=True)
    return sampled


def print_sampling_summary(df: pd.DataFrame) -> None:
    """
    Print a summary of the sampling results.
    
    Args:
        df (pd.DataFrame): Sampled dataframe with length_bin and month columns
    """
    if df.empty:
        print("No data to summarize")
        return
    
    print(f"Total samples: {len(df)}")
    print(f"Length bin distribution:")
    for label in LENGTH_LABELS:
        count = (df["length_bin"] == label).sum()
        print(f"  {label}: {count}")
    
    print(f"Month distribution:")
    month_counts = df["month"].value_counts().sort_index()
    for month, count in month_counts.items():
        print(f"  {month}: {count}")