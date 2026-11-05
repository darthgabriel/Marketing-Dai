import io

base = r"C:\Users\gabri\Escritorio\marketing\scripts"
target = base + r"\generar_special_dai_unificado.py"
block = base + r"\_bloque_guiones.py.txt"

with io.open(target, encoding="utf-8") as f:
    src = f.read()
with io.open(block, encoding="utf-8") as f:
    new = f.read()

init = "# ============================================================ HOJA 4"
end = "# ============================================================ BUILD"

i = src.index(init)
j = src.index(end)
out = src[:i] + new.rstrip() + "\n\n\n" + src[j:]

with io.open(target, "w", encoding="utf-8", newline="\n") as f:
    f.write(out)

print("spliced", i, j, "->", len(out))
