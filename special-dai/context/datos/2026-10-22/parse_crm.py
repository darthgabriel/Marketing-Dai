#!/usr/bin/env python3
"""Parsea el reporte crudo 'Inventario Valorado | Dai Motors, S.A.' del CRM autoweb.

Entrada: context/datos/2026-10-22/crm-inventario-valorado-raw.json (filas extraídas del DOM)
Salida estructurada: context/datos/2026-10-22/crm-inventario-valorado.json
Resumen: context/datos/2026-10-22/crm-inventario-valorado-resumen.json
"""
import json, re, statistics
from collections import defaultdict

SRC = "context/datos/2026-10-22/crm-inventario-valorado-raw.json"
OUT = "context/datos/2026-10-22/crm-inventario-valorado.json"
RES = "context/datos/2026-10-22/crm-inventario-valorado-resumen.json"

def num(s):
    s = (s or "0").replace(".", "").replace(",", ".")
    try:
        return float(s)
    except ValueError:
        return 0.0

raw = json.load(open(SRC, encoding="utf-8"))
BANDS = {"FACTURADO | EN EXHIBICION", "FACTURADO | EN PLANTA",
         "TRANSITO | EN EXHIBICION", "TRANSITO | EN PLANTA"}
BRANDS = {"CHERY", "HYUNDAI", "KARRY", "MITSUBISHI"}

records, band = [], None
for r in raw:
    if len(r) == 1 and r[0] in BANDS:
        band = r[0]
        continue
    if len(r) == 1:  # otras leyendas, saltar
        continue
    if "TOTALES" in r[1:3]:
        continue
    if len(r) < 20 or (len(r) > 6 and r[6] not in BRANDS):
        continue
    rec = {
        "estado": band,
        "compra": r[0], "f_recepcion": r[1], "stock": r[2], "pedido": r[3],
        "marca": r[6], "modelo": r[7], "placa": r[8], "serial": r[9],
        "color": r[10], "costo_venta": num(r[11]), "total_compra": num(r[28]),
        "total_pagar": num(r[29]), "forma_pago": r[31],
        "dias_inventario": int(num(r[33])) if re.match(r"^\d+$", r[33].strip() or "x") else None,
    }
    records.append(rec)

count_tot = {t: 0 for t in list(BANDS)}
for rec in records:
    count_tot[rec["estado"]] += 1
print(dict(count_tot))
print(f"total registros: {len(records)}")

json.dump(records, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# ---- Resumen ----
groups = defaultdict(lambda: {"n": 0, "dias": [], "valor": 0.0})
for rec in records:
    key = (rec["estado"], rec["marca"], rec["modelo"])
    g = groups[key]
    g["n"] += 1
    g["valor"] += rec["total_pagar"]
    if rec["dias_inventario"] is not None:
        g["dias"].append(rec["dias_inventario"])

summary = []
for (estado, marca, modelo), g in sorted(groups.items()):
    d = g["dias"]
    summary.append({
        "estado": estado, "marca": marca, "modelo": modelo, "n": g["n"],
        "dias_promedio": round(statistics.mean(d), 1) if d else None,
        "dias_max": max(d) if d else None,
        "valor_usd": round(g["valor"], 2),
    })

resumen = {"fuente": "CRM autoweb ~ Inventario Valorado | Dai Motors, S.A. (reporte 22 oct 2026)",
           "notas": ["EN EXHIBICION / EN PLANTA = unidades físicas disponibles para el evento",
                     "TRANSITO = por llegar; PEDIDO indica lote de origen"],
           "grupos": summary}
json.dump(resumen, open(RES, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

for s in summary:
    print(f"{s['estado']:28s} {s['marca']:10s} {s['modelo']:28s} n={s['n']:3d} dias={s['dias_promedio']} max={s['dias_max']} valor={s['valor_usd']:,.0f}")
