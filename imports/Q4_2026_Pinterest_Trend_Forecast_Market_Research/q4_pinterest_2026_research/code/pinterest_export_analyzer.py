#!/usr/bin/env python3
"""Analyze Pinterest Analytics CSV exports using only pandas.

Usage:
  python pinterest_export_analyzer.py export1.csv export2.csv --out pin_rankings.csv

The script tolerates common Pinterest column-name variants and calculates
commerce-focused rates. It does not require API access.
"""
import argparse
import glob
import os
import re
import sys
import pandas as pd

ALIASES = {
    "pin_id": ["pin id", "pin_id", "pin id (all)", "pin"],
    "date": ["date", "day"],
    "impressions": ["impressions", "impression"],
    "saves": ["saves", "save"],
    "pin_clicks": ["pin clicks", "pin_clicks", "pin clicks (all)"],
    "outbound_clicks": ["outbound clicks", "outbound_clicks", "outbound clicks (all)", "link clicks"],
    "title": ["pin title", "title", "pin_title"],
}

def norm(s):
    return re.sub(r"\s+", " ", str(s).strip().lower())

def find_col(cols, names):
    by_norm = {norm(c): c for c in cols}
    for n in names:
        if norm(n) in by_norm:
            return by_norm[norm(n)]
    for c in cols:
        cn = norm(c)
        for n in names:
            if norm(n) in cn:
                return c
    return None

def load(paths):
    frames = []
    for p in paths:
        df = pd.read_csv(p)
        mapped = {}
        for canonical, aliases in ALIASES.items():
            c = find_col(df.columns, aliases)
            if c is not None:
                mapped[canonical] = c
        out = pd.DataFrame()
        for canonical in ALIASES:
            if canonical in mapped:
                out[canonical] = df[mapped[canonical]]
        out["source_file"] = os.path.basename(p)
        if "pin_id" not in out:
            if "title" in out:
                out["pin_id"] = out["title"].astype(str)
            else:
                out["pin_id"] = [f"row-{i}" for i in range(len(out))]
        frames.append(out)
    if not frames:
        raise SystemExit("No CSVs supplied")
    return pd.concat(frames, ignore_index=True)

def num(s):
    return pd.to_numeric(s.astype(str).str.replace(",", "", regex=False), errors="coerce").fillna(0)

def analyze(df):
    for c in ["impressions", "saves", "pin_clicks", "outbound_clicks"]:
        if c not in df:
            df[c] = 0
        df[c] = num(df[c])
    if "date" in df:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
    else:
        df["date"] = pd.NaT

    df["save_per_1k"] = (df["saves"] / df["impressions"].replace(0, pd.NA) * 1000).fillna(0)
    df["outbound_per_1k"] = (df["outbound_clicks"] / df["impressions"].replace(0, pd.NA) * 1000).fillna(0)
    df["pin_click_rate"] = (df["pin_clicks"] / df["impressions"].replace(0, pd.NA)).fillna(0)
    df["outbound_to_pin_click"] = (df["outbound_clicks"] / df["pin_clicks"].replace(0, pd.NA)).fillna(0)

    agg = {
        "impressions": "sum",
        "saves": "sum",
        "pin_clicks": "sum",
        "outbound_clicks": "sum",
        "source_file": "nunique",
    }
    g = df.groupby("pin_id", dropna=False).agg(agg).reset_index()
    dates = df.groupby("pin_id")["date"].agg(["min", "max", "nunique"]).reset_index()
    dates.columns = ["pin_id", "first_date", "last_date", "active_days_observed"]
    g = g.merge(dates, on="pin_id", how="left")
    g["active_span_days"] = (g["last_date"] - g["first_date"]).dt.days.fillna(0) + 1
    g["active_weeks_span"] = (g["active_span_days"] / 7).clip(lower=1)
    g["impressions_per_day"] = g["impressions"] / g["active_span_days"].clip(lower=1)
    g["save_per_1k"] = (g["saves"] / g["impressions"].replace(0, pd.NA) * 1000).fillna(0)
    g["outbound_per_1k"] = (g["outbound_clicks"] / g["impressions"].replace(0, pd.NA) * 1000).fillna(0)
    g["pin_click_per_1k"] = (g["pin_clicks"] / g["impressions"].replace(0, pd.NA) * 1000).fillna(0)

    # Account-relative percentiles: more portable than an absolute 800k threshold.
    for c in ["impressions_per_day", "save_per_1k", "outbound_per_1k"]:
        g[c + "_pct"] = g[c].rank(pct=True)

    # A transparent heuristic, not a conversion prediction.
    g["signal_score_100"] = (
        35 * g["impressions_per_day_pct"] +
        25 * g["save_per_1k_pct"] +
        30 * g["outbound_per_1k_pct"] +
        10 * (g["active_weeks_span"].clip(upper=10) / 10)
    ).round(1)

    return g.sort_values(["signal_score_100", "outbound_clicks"], ascending=False)

def expand_inputs(items):
    out = []
    for item in items:
        matches = glob.glob(item)
        out.extend(matches or [item])
    return [p for p in out if os.path.exists(p)]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csv", nargs="+", help="Pinterest CSV export path(s) or globs")
    ap.add_argument("--out", default="pin_rankings.csv")
    args = ap.parse_args()
    paths = expand_inputs(args.csv)
    if not paths:
        raise SystemExit("No matching CSVs")
    df = load(paths)
    ranked = analyze(df)
    ranked.to_csv(args.out, index=False)
    print(ranked.head(20).to_string(index=False))
    print(f"\nWrote {args.out}")

if __name__ == "__main__":
    main()
