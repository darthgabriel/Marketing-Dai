#!/usr/bin/env python3
import json, sys
sys.stdout.reconfigure(encoding="utf-8")
from collections import Counter

for h in ["cherymaracaibo", "daimotorsmcbo"]:
    d = json.load(open(f"context/datos/2026-10-22/{h}-reels.json", encoding="utf-8"))
    items = d["items"]
    dates = sorted([(it.get("timestamp") or "")[:10] for it in items if it.get("timestamp")])
    print(f"== {h}: {len(items)} items | de {dates[0]} a {dates[-1]}")
    meses = Counter(x[:7] for x in dates)
    print("   por mes:", dict(meses))
    followers = None
    for it in items:
        if it.get("userInfo") or it.get("profilePicUrl"):
            followers = (it.get("userInfo") or {}).get("followerCount")
    print("   followers en payload:", followers)
    print("   meta:", d["_meta"]["fetched_at"], d["_meta"]["actor"])
