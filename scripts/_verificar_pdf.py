from pypdf import PdfReader

pdf = r"entregables\Noviembre-daimotorsmcbo-chery-special-dai-evento-unico.pdf"
r = PdfReader(pdf)
pages = [(i + 1, (p.extract_text() or "").replace("\n", " ")) for i, p in enumerate(r.pages)]

esperado = {
    1: ["Seis objetivos", "Dominar la región", "10 ventas objetivo"],
    2: ["Seis ideas", "Revelación Himla 2027", "cuenta regresiva"],
    3: ["Seis alianzas arriba", "15 PARTIDAS", "Planta"],
    4: ["Del teaser al anuncio", "se llama SPECIAL DAI", "Aparta tu pase"],
    5: ["La semana que enciende el anuncio", "Se acaba el domingo", "Escribe VIP"],
    6: ["La semana que se vende", "Seis días en 20 segundos", "sigue disponible"],
}

print("paginas:", len(pages))
ok = True
for n, txt in pages:
    faltan = [s for s in esperado.get(n, []) if s.lower() not in txt.lower()]
    marca = "OK " if not faltan else "FALTA"
    if faltan:
        ok = False
    print(f"p{n}: {marca} {len(txt)} chars | cierre: ...{txt[-70:].strip()}")
    if faltan:
        print("      no encontrado:", faltan)

# detectar si una hoja se desbordó a otra página
mezcla = [("Seis objetivos", 1), ("Seis ideas", 2), ("Seis alianzas arriba", 3),
          ("Del teaser al anuncio", 4), ("enciende el anuncio", 5), ("se vende", 6)]
for texto, donde in mezcla:
    hit = [n for n, t in pages if texto.lower() in t.lower()]
    if hit != [donde]:
        ok = False
        print("POSIBLE CORTE/DESFASE:", texto, "aparece en", hit, "esperaba", [donde])

print("RESULTADO:", "TODO OK" if ok else "REVISAR")
