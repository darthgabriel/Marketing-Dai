#!/usr/bin/env python3
import json, statistics, sys
sys.stdout.reconfigure(encoding="utf-8")
from datetime import datetime

for h in ["cherymaracaibo", "daimotorsmcbo"]:
    d = json.load(open(f"context/datos/2026-10-22/{h}-reels.json", encoding="utf-8"))
    items = d["items"]
    pts = []
    for it in items:
        pts.append({
            "v": it.get("videoPlayCount") or it.get("playCount") or 0,
            "l": it.get("likesCount") or 0,
            "c": it.get("commentsCount") or 0,
            "t": (it.get("timestamp") or "")[:10],
            "cap": (it.get("caption") or "").replace("\n", " ")[:70],
        })
    pts = [p for p in pts if p["t"]]
    total = sum(p["v"] for p in pts)
    med = statistics.median([p["v"] for p in pts]) if pts else 0
    days = [(datetime.strptime(p["t"], "%Y-%m-%d")).timestamp() for p in pts]
    span_days = (max(days) - min(days)) / 86400 if pts else 0
    weeks = max(1.0, span_days / 7)
    print(f"== {h}: {len(pts)} reels | {pts[-1]['t']} a {pts[0]['t']} | ritmo {len(pts)/weeks:.1f}/sem | total {total:,} | mediana {med:,.0f}")
    print("  TOP:")
    for p in sorted(pts, key=lambda x: -x["v"])[:4]:
        print(f"    {p['v']:>10,} l={p['l']:>5} c={p['c']:>4} {p['t']} {p['cap']}")
    print("  PEOR:")
    for p in sorted(pts, key=lambda x: x["v"])[:3]:
        print(f"    {p['v']:>10,} l={p['l']:>5} c={p['c']:>4} {p['t']} {p['cap']}")
