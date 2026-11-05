# Extracción de datos en Meta Business Suite (navegador integrado)

El usuario inicia sesión él mismo. Nunca escribir credenciales.
Abrir con `preview_start` url `https://business.facebook.com/latest/insights`; si sale login, pedir al usuario que entre (Ctrl+Shift+B muestra el panel).

## Cuentas (portafolio → activo)

| Cuenta Excel | business_id | asset_id |
|---|---|---|
| daimotorsmcbo | 111630715178971 | 111627418512634 |
| cherymaracaibo | 157452856983316 | 100273082910667 |
| kyotomotorsmcbo | 522357754838291 | 113228954949628 |
| yantaimotors | 137350159097976 | 103052142651424 |
| karrymaracaibo | 1302612785187381 | 1244396322101217 |

Si un ID deja de funcionar: abrir el selector de activos (hover en barra izquierda → clic en el nombre del activo arriba → buscar) y leer `location.href` tras elegir.

## URLs (siempre `platform=Instagram` y `time_range=%2522LAST_MONTH%2522`)

Plantilla: `https://business.facebook.com/latest/insights/<vista>?business_id=<B>&asset_id=<A>&time_range=%2522LAST_MONTH%2522&platform=Instagram`

| Vista | Qué sale |
|---|---|
| `results` | Visualizaciones, alcance, interacciones, visitas al perfil, nuevos seguidores |
| `people` | Total seguidores (`Seguidores\nTotal\nN`) |
| `content` | Lista de piezas del mes (contenido) |

Confirmar en la página el texto `El mes pasado: 1 <mes> - <último día>`. El selector de fecha de la vista Resumen está deshabilitado; usar la URL.

## Snippets (javascript_tool)

### results — totales por gráfico
```js
await new Promise(r=>setTimeout(r,4500));const t=document.body.innerText;const parts=t.split('Exportar\n').slice(1);const out=parts.map(p=>{const head=p.split('\n')[0];const prim=(p.match(/Primary((\t[\d\.]+)+)/)||[])[1]||'';const vals=prim.trim().split('\t').map(x=>+x.replace(/\./g,''));const lbl=(p.match(/\n​\n([^\n]+)\n/)||[])[1];return lbl+': '+head+' / sum '+vals.reduce((a,b)=>a+b,0)});const i=t.indexOf('Visualizaciones\n');JSON.stringify({rango:(t.match(/El mes pasado[^\n]*/)||[])[0],vis:t.slice(i+30,i+110),out})
```
- **Visualizaciones**: usar el número "N visualizaciones" de Instagram (segunda línea en `vis`; la primera es Facebook).
- **Interacciones, visitas al perfil, nuevos seguidores**: la suma diaria (`sum`) es exacta.
- **Alcance**: NO sumar días (se duplica). El encabezado viene redondeado ("85,2 mil"): `find` ese texto, `hover` sobre su ref y leer `[role=tooltip]` → valor exacto.
- Nuevos seguidores `‑‑` = cuenta con <100 seguidores; Meta no lo da → null.

### people — total seguidores
```js
await new Promise(r=>setTimeout(r,4000));(document.body.innerText.match(/Seguidores\n​\nTotal\n([\d\.]+)/)||[])[1]
```
Es el total al día de hoy, no al cierre del mes.

### content — conteo de piezas
La tabla carga más filas con la rueda del mouse (no con scrollTop). Hacer `browser_batch` con ~10 × (`scroll` down 10 en (440,450) + `wait` 2s), luego:
```js
const rs=[...document.querySelectorAll('[role=row]')].slice(1).map(r=>r.innerText.replace(/\s+/g,' '));const d=rs.map(s=>s.match(/\w+, \d+ de \w+ \d+:\d+/)?.[0]).filter(Boolean);const c={};rs.forEach(s=>{if(!/de \w+ \d+:\d+/.test(s))return;const ty=(s.match(/ (Historia|Foto|Reel|Video|Varios archivos multimedia) /)||[])[1]||'?';c[ty]=(c[ty]||0)+1});JSON.stringify({rows:rs.length,dated:d.length,c,last:d.at(-1)})
```
Repetir scroll hasta que `last` sea el día 1 del mes y `rows` no cambie. Contenido = `dated`.

## Visitas Google
No vienen de Meta: el usuario las da (Google Business Profile → Rendimiento). Solo daimotorsmcbo, cherymaracaibo y yantaimotors; Kyoto y Karry ya no se llevan (null).
