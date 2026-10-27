"""Write data/sensitivity_derived.json: small derived tables from the pre-registered sensitivity test.

Reads (never writes) the tool repo:
  CE/experiments/results/sensitivity/sensitivity_<model>.json   summary and per_question (the answer rows' text is
                                                                 never read into the output)
  CE/experiments/explorer/sensitivity.py                        the registered criteria as the harness applies them
                                                                 (H1 off-topic bar, H2 bar and its p bar), with lines

Per model it writes the per-question means of the four conditions, the per-question differences
(after - before, exploratory; answer_first - before, registered H2 contrast), their mean, SD, a 95% t interval over
the 8 questions, the number of questions up, the largest single-question gain, the exact two-sided sign-flip p
(recomputed here and checked against the harness's summary), the relative change of the pooled means, and a post hoc
minimum detectable difference (paired t approximation, two-sided alpha 0.05, power 0.80, n = 8 questions).
Everything after the registered H1/H2 outcomes is exploratory or post hoc and is labelled so in the output.

Usage: .venv/bin/python -I -B scripts/derive_sensitivity.py [--ce-root <CE>]
"""
from __future__ import annotations

import argparse
import itertools
import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figdata  # noqa: E402
import figstyle  # noqa: E402

ALPHA, POWER = 0.05, 0.80  # post hoc MDE settings (conventional; not from the pre-registration)


# ---------------------------------------------------------------------------------------- Student t (no scipy needed)
def _betacf(a, b, x, itmax=300, eps=3e-16):
    qab, qap, qam = a + b, a + 1.0, a - 1.0
    c, d = 1.0, 1.0 - qab * x / qap
    d = 1.0 / (d if abs(d) > 1e-300 else 1e-300)
    h = d
    for m in range(1, itmax + 1):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1.0 + aa * d
        d = 1.0 / (d if abs(d) > 1e-300 else 1e-300)
        c = 1.0 + aa / c if abs(1.0 + aa / c) > 1e-300 else 1e-300
        h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1.0 + aa * d
        d = 1.0 / (d if abs(d) > 1e-300 else 1e-300)
        c = 1.0 + aa / c if abs(1.0 + aa / c) > 1e-300 else 1e-300
        delta = d * c
        h *= delta
        if abs(delta - 1.0) < eps:
            break
    return h


def _betai(a, b, x):
    if x <= 0.0:
        return 0.0
    if x >= 1.0:
        return 1.0
    bt = math.exp(math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b) + a * math.log(x) + b * math.log(1.0 - x))
    if x < (a + 1.0) / (a + b + 2.0):
        return bt * _betacf(a, b, x) / a
    return 1.0 - bt * _betacf(b, a, 1.0 - x) / b


def t_cdf(t, df):
    x = df / (df + t * t)
    tail = 0.5 * _betai(df / 2.0, 0.5, x)
    return 1.0 - tail if t >= 0 else tail


def t_ppf(q, df):
    lo, hi = -50.0, 50.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if t_cdf(mid, df) < q:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


# ---------------------------------------------------------------------------------------- statistics
def sign_flip_p(diffs):
    """Exact two-sided sign-flip p, the same rule as CE/experiments/explorer/sensitivity.py sign_flip_p()."""
    obs = abs(sum(diffs))
    hits = sum(1 for s in itertools.product((1, -1), repeat=len(diffs))
               if abs(sum(a * d for a, d in zip(s, diffs))) >= obs - 1e-12)
    return hits / 2 ** len(diffs)


def describe(diffs):
    n = len(diffs)
    mean = sum(diffs) / n
    sd = math.sqrt(sum((d - mean) ** 2 for d in diffs) / (n - 1))
    se = sd / math.sqrt(n)
    tcrit = t_ppf(1 - ALPHA / 2, n - 1)
    mde = (tcrit + t_ppf(POWER, n - 1)) * se
    return {
        "n_questions": n, "mean": mean, "sd": sd, "ci95_t": [mean - tcrit * se, mean + tcrit * se],
        "n_up": sum(d > 0 for d in diffs), "n_down": sum(d < 0 for d in diffs),
        "max": max(diffs), "min": min(diffs), "p_sign_flip": sign_flip_p(diffs),
        "mde_post_hoc": mde,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ce-root", default=figdata.CE_ROOT_DEFAULT)
    ap.add_argument("--out", default=os.path.join(figdata.DATA, "sensitivity_derived.json"))
    a = ap.parse_args()
    ce = os.path.abspath(a.ce_root)
    models, paths = figdata.sensitivity_raw(ce)
    thr, thr_paths = figdata.harness_thresholds(ce)

    out_models = []
    for m in models:
        s, pq = m["summary"], m["per_question"]
        keys = list(pq["before"].keys())
        if any(list(pq[c].keys()) != keys for c in figdata.CONDITIONS):
            raise SystemExit(f"derive_sensitivity: question keys differ between conditions in {m['path']}")
        if any(pq[c][k] is None for c in figdata.CONDITIONS for k in keys):
            raise SystemExit(f"derive_sensitivity: a question has no valid answer in {m['path']}")
        d_after = [pq["after"][k] - pq["before"][k] for k in keys]
        d_answer = [pq["answer_first"][k] - pq["before"][k] for k in keys]
        c_after, c_answer = describe(d_after), describe(d_answer)
        # Consistency with the harness's own summary (rounded to 4 places there; p exact).
        for name, c, ref in (("after", c_after, s["after_minus_before_exploratory"]),
                             ("answer_first", c_answer, s["answer_first_minus_before"])):
            if abs(round(c["mean"], 4) - ref["mean"]) > 1e-9 or abs(c["p_sign_flip"] - ref["p_sign_flip"]) > 1e-12:
                raise SystemExit(f"derive_sensitivity: {m['label']} {name} disagrees with the harness summary")
        mts = s["mean_target_share"]
        h1 = mts["offtopic"] <= thr["h1_offtopic_max"]["value"]
        h2 = (mts["answer_first"] - mts["before"] >= thr["h2_min_gain"]["value"]
              and c_answer["p_sign_flip"] <= thr["h2_max_p"]["value"])
        if h1 != s["H1_floor"] or h2 != s["H2_sensitivity"]:
            raise SystemExit(f"derive_sensitivity: {m['label']} H1/H2 recomputation disagrees with the harness")
        per_sample = {}
        for key, short in figdata.SAMPLES:
            per_sample[key] = {
                "label": short,
                **{f"{c}_mean": figdata.per_sample_mean(pq, c, key) for c in figdata.CONDITIONS},
            }
            per_sample[key]["after_minus_before"] = per_sample[key]["after_mean"] - per_sample[key]["before_mean"]
        out_models.append({
            "model": m["id"], "label": m["label"], "source": os.path.relpath(m["path"], ce),
            "valid_rate": s["valid_rate"], "chance_share": s["chance_share"],
            "mean_sources_cited": s["mean_sources_cited"],
            "target_cited_rate": s["target_cited_rate"],
            "mean_target_share": mts,
            "relative_change_after": mts["after"] / mts["before"] - 1.0,
            "relative_change_answer_first": mts["answer_first"] / mts["before"] - 1.0,
            "registered": {"H1_floor": s["H1_floor"], "H2_sensitivity": s["H2_sensitivity"],
                           "usable_for_E2": s["usable_for_E2"]},
            "questions": keys,
            "per_question": {c: [pq[c][k] for k in keys] for c in figdata.CONDITIONS},
            "diff_after_minus_before": d_after,
            "diff_answer_first_minus_before": d_answer,
            "after_minus_before": {**c_after, "tier": "exploratory, uncorrected"},
            "answer_first_minus_before": {**c_answer, "tier": "registered contrast (H2); interval and MDE post hoc"},
            "per_sample": per_sample,
        })

    def rng(key, field):
        vals = [mm[key][field] for mm in out_models]
        return [min(vals), max(vals)]

    out = {
        "_provenance": {
            "producer": "scripts/derive_sensitivity.py",
            "note": ("Derived from the tool repo's sensitivity results (model outputs' text not copied). "
                     "Means over the 8 questions; per-question values are means over 8 seeds of valid answers. "
                     "Intervals are 95% t intervals over questions; mde_post_hoc is a paired t approximation "
                     f"(two-sided alpha {ALPHA}, power {POWER}, n = 8), post hoc."),
            "inputs": [{"path": os.path.relpath(p, ce), "repo": "citation-equity", "sha256": figstyle.sha256(p)}
                       for p in paths + thr_paths],
        },
        "thresholds": {k: {**v, "source": os.path.relpath(thr_paths[0], ce)} for k, v in thr.items()},
        "models": out_models,
        "ranges": {
            "after_minus_before_mean": rng("after_minus_before", "mean"),
            "answer_first_minus_before_mean": rng("answer_first_minus_before", "mean"),
            "mde_post_hoc_after": rng("after_minus_before", "mde_post_hoc"),
            "mde_post_hoc_answer_first": rng("answer_first_minus_before", "mde_post_hoc"),
            "sd_after": rng("after_minus_before", "sd"),
            "sd_answer_first": rng("answer_first_minus_before", "sd"),
            "offtopic_share": [min(mm["mean_target_share"]["offtopic"] for mm in out_models),
                               max(mm["mean_target_share"]["offtopic"] for mm in out_models)],
            "mean_sources_cited": [min(mm["mean_sources_cited"] for mm in out_models),
                                   max(mm["mean_sources_cited"] for mm in out_models)],
            "target_cited_rate_before": [min(mm["target_cited_rate"]["before"] for mm in out_models),
                                         max(mm["target_cited_rate"]["before"] for mm in out_models)],
            "relative_change_after": [min(mm["relative_change_after"] for mm in out_models),
                                      max(mm["relative_change_after"] for mm in out_models)],
        },
    }
    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    with open(a.out, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=2)
        fh.write("\n")
    print(f"wrote {a.out}")
    for mm in out_models:
        aa, af = mm["after_minus_before"], mm["answer_first_minus_before"]
        print(f"  {mm['label']:15s} after-before {aa['mean']:+.4f} [{aa['ci95_t'][0]:+.3f}, {aa['ci95_t'][1]:+.3f}] "
              f"up {aa['n_up']}/8 p {aa['p_sign_flip']:.4f} max {aa['max']:.3f} | answer-before {af['mean']:+.4f} "
              f"[{af['ci95_t'][0]:+.3f}, {af['ci95_t'][1]:+.3f}] up {af['n_up']}/8 p {af['p_sign_flip']:.4f} "
              f"max {af['max']:.3f} | MDE {aa['mde_post_hoc']:.3f}/{af['mde_post_hoc']:.3f}")


if __name__ == "__main__":
    main()
