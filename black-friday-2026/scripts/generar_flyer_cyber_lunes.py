"""Flyer Cyber Lunes · Black Friday 2026 · 3 cuentas · 1080x1350 PNG (post de feed).
Sin precios: el precio se da solo en el showroom. Sin palabra "extensión": lunes = evento nuevo.
Salida: black-friday-2026/entregables/Flyer-CyberLunes-{Hyundai,Chery,Yantai}.png (+ .html fuente)
Uso: python black-friday-2026/scripts/generar_flyer_cyber_lunes.py
"""
import base64
import io
import os
import subprocess
import time

from PIL import Image

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(BASE, "entregables")
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

LOGO_DAI = r"C:\Users\DELL\Desktop\daiweb\public\img\logo-dai.png"
LOGO_CHERY = r"C:\Users\DELL\Desktop\autowebv26\public\img\logo-1-2.png"
LOGO_YANTAI = r"C:\Users\DELL\Desktop\marketing\.opencode\openwork\inbox\chat-attachments\ses_decc99786ffe8JnQzzO3sSTw7Q\93fc9cb9-8ac9-4173-af39-e5545bc308e8-yantai-motors 2.png"

FLYERS = [
    dict(key="Hyundai", logo=LOGO_DAI, color="#0032C0", marca="Dai Motors",
         pie="Showroom Dai Motors · Maracaibo · Hyundai en Dai Motors"),
]

CSS = f"""
* {{ box-sizing: border-box; margin: 0; padding: 0 }}
body {{ width: 1080px; height: 1350px; overflow: hidden; position: relative; font-family: Inter, 'Segoe UI', Arial, sans-serif;
  color: #fff; background: #0B0E14; -webkit-print-color-adjust: exact; print-color-adjust: exact }}
.bgr {{ position: absolute; right: -180px; top: -180px; width: 640px; height: 640px; border-radius: 50%;
  background: radial-gradient(circle, var(--c), transparent 68%); opacity: .38 }}
.bgb {{ position: absolute; left: -220px; bottom: -260px; width: 700px; height: 700px; border-radius: 50%;
  background: radial-gradient(circle, #0032C0, transparent 70%); opacity: .30 }}
.band {{ position: absolute; left: 0; right: 0; top: 0; height: 14px; background: var(--c) }}
.head {{ display: flex; justify-content: space-between; align-items: center; padding: 56px 70px 0; position: relative; z-index: 2 }}
.head img {{ height: 64px }}
.head img.tall {{ height: 46px; margin-top: 6px }}
.fecha {{ text-align: right }}
.fecha b {{ display: block; font: 900 30px Inter, Arial; letter-spacing: .04em }}
.fecha span {{ font: 700 16px Inter, Arial; color: #94A3B8; letter-spacing: .22em; text-transform: uppercase }}
.mid {{ padding: 120px 70px 0; position: relative; z-index: 2 }}
.mid .lbl {{ font: 800 26px Inter, Arial; letter-spacing: .3em; text-transform: uppercase; color: #FFD84D }}
.mid h1 {{ font: 900 180px/0.95 'Arial Black', Inter, Arial; letter-spacing: .01em; margin-top: 20px }}
.mid h1 em {{ color: var(--c); font-style: normal; -webkit-text-stroke: 2px #fff; text-stroke: 2px #fff }}
.mid .sub {{ font: 700 44px/1.25 Inter, Arial; margin-top: 34px; color: #E2E8F0 }}
.mid .sub b {{ color: #FFD84D }}
.chips {{ display: flex; gap: 18px; margin-top: 70px; flex-wrap: wrap }}
.chips span {{ font: 900 36px 'Arial Black', Inter, Arial; padding: 22px 32px; border-radius: 16px;
  background: rgba(255,255,255,.07); border: 2px solid rgba(255,255,255,.22) }}
.price {{ margin: 60px 70px 0; border: 3px solid #FFD84D; border-radius: 18px; padding: 26px 32px;
  display: flex; align-items: center; gap: 20px; position: relative; z-index: 2 }}
.price i {{ font-style: normal; font-weight: 900; width: 52px; height: 52px; border-radius: 50%; background: #FFD84D;
  color: #0B0E14; display: grid; place-items: center; font-size: 30px; flex: none }}
.price b {{ font: 900 38px 'Arial Black', Inter, Arial; letter-spacing: .02em }}
.price small {{ display: block; font: 600 20px Inter, Arial; color: #94A3B8; margin-top: 6px }}
.price, .car {{ position: relative }}
.intriga {{ color: #94A3B8; font-weight: 600; font-size: 30px }}
.car {{ position: absolute; left: 0; right: 0; top: 985px; text-align: center; z-index: 1 }}
.car svg {{ width: 700px; display: block; margin: 0 auto; opacity: .55 }}
.foot {{ position: absolute; bottom: 0; left: 0; right: 0; padding: 40px 70px 46px; display: flex;
  justify-content: space-between; align-items: flex-end; background: linear-gradient(transparent, rgba(0,0,0,.65)) }}
.cta {{ font: 900 34px 'Arial Black', Inter, Arial; color: #FFD84D }}
.cta small {{ display: block; font: 600 20px Inter, Arial; color: #CBD5E1; margin-top: 8px }}
.marca {{ text-align: right; font: 700 20px Inter, Arial; color: #94A3B8; line-height: 1.45 }}
"""


def logo_white(path):
    im = Image.open(path).convert("RGBA")
    im = im.crop(im.getbbox())
    white = Image.new("RGBA", im.size, (255, 255, 255, 255))
    white.putalpha(im.split()[-1])
    white.thumbnail((900, 900))
    buf = io.BytesIO()
    white.save(buf, "PNG")
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()


CARRO = ('<svg viewBox="0 0 700 240">'
         '<path d="M40 190 L55 120 Q62 78 110 68 L180 56 Q250 -8 380 -8 L470 -8 Q540 -8 580 40 L610 62 Q660 74 665 120 L662 190" '
         'fill="none" stroke="#3A4652" stroke-width="9" stroke-linejoin="round"/>'
         '<path d="M210 48 Q262 -2 368 -2 L460 -2 Q522 -2 556 40 L568 52 L232 52 Q200 52 210 48 Z" fill="none" stroke="#3A4652" stroke-width="7"/>'
         '<line x1="240" y1="20" x2="480" y2="20" stroke="var(--c)" stroke-width="6" stroke-linecap="round" opacity=".8"/>'
         '<circle cx="170" cy="190" r="46" fill="none" stroke="#3A4652" stroke-width="10"/>'
         '<circle cx="540" cy="190" r="46" fill="none" stroke="#3A4652" stroke-width="10"/>'
         '<line x1="20" y1="190" x2="124" y2="190" stroke="#3A4652" stroke-width="9"/>'
         '<line x1="216" y1="190" x2="494" y2="190" stroke="#3A4652" stroke-width="9"/>'
         '<line x1="586" y1="190" x2="662" y2="190" stroke="#3A4652" stroke-width="9"/>'
         '<line x1="60" y1="130" x2="128" y2="122" stroke="var(--c)" stroke-width="8" stroke-linecap="round"/>'
         '</svg>')


def build(f):
    logo = logo_white(f["logo"])
    html = f"""<!doctype html><html lang="es"><head><meta charset="utf-8"><title>Flyer Cyber Lunes · {f['key']}</title>
<style>{CSS.replace("--c:#0032C0", f"--c:{f['color']}")}</style></head><body>
<div class="bgr"></div><div class="bgb"></div><div class="band"></div>
<div class="head"><img src="{logo}"{"" if f["key"] != "Yantai" else ' class="tall"'}><div class="fecha"><span>Lunes</span><b>30 NOV</b></div></div>
<div class="mid">
  <h1>BLACK<br><em>DAYS</em></h1>
  <div class="sub">El <b>precio de Black Friday</b> se queda toda la semana.<br>
  <span class="intriga">¿Cuáles son? En el showroom.</span></div>
</div>
<div class="car">{CARRO}</div>
<div class="foot">
  <div class="cta">VISÍTANOS HOY<small>Hasta las 6:00 pm</small></div>
  <div class="marca">{f['pie']}</div>
</div>
</body></html>"""
    out_html = os.path.join(OUT_DIR, f"Flyer-BlackDays-{f['key']}.html")
    out_png = os.path.join(OUT_DIR, f"Flyer-BlackDays-{f['key']}.png")
    with open(out_html, "w", encoding="utf-8") as fh:
        fh.write(html)
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                    f"--screenshot={out_png}", "--window-size=1080,1350",
                    "--force-device-scale-factor=1", out_html], check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return out_png


if __name__ == "__main__":
    for f in FLYERS:
        print(build(f))
        time.sleep(1)
