"""Genera el plano general de la propiedad en SVG (plano-global.svg, junto a este script).

Uso: python3 imagenes/planos/plano_global.py [salida.svg]

Solo muestra la huella de cada edificio, sin el interior. Mismas coordenadas que plano_mansion.py:
metros, x hacia el este, y hacia el sur (0 = extremo norte de las alas de la mansión).
Si cambia un muro exterior en plano_mansion.py, actualizar HUELLA_MANSION aquí.
"""
import os
import random
import sys

S = 10                      # px por metro
X0, Y0, X1, Y1 = -22, -18, 92, 52
W, H = (X1 - X0) * S, (Y1 - Y0) * S

C = {
    'bg': '#e3ebd4', 'jardin': '#d6e4c2', 'bosque': '#a9c095', 'arbol': '#86a571', 'arbol2': '#6f915c',
    'edif': '#e9dcc3', 'edif_b': '#3b3834', 'claire': '#e4d9ee', 'huesp': '#d9e6ef', 'garaje': '#dcdcdc',
    'patio': '#eee8dc', 'deck': '#d8c19c', 'agua': '#a6d6e8', 'agua_b': '#4f9fbf',
    'camino': '#d9d2c2', 'seto': '#6f915c', 'texto': '#2e2b27', 'sub': '#6b655c',
}

# huella exterior de la mansión (bloques, sin divisiones interiores)
HUELLA_MANSION = [
    (21, 0, 27.5, 20),     # ala oeste (servicio)
    (11, 15, 20, 20),      # anexo oeste: bodega + habitación de yesos
    (11, 20, 29, 21.5),    # pasillo oeste
    (21, 21.5, 49, 27.5),  # base: cocina, comedor, corredor amplio, vestíbulo, salón
    (38.5, 19, 42, 21.5),  # bahía del salón
    (42, 0, 49, 21.5),     # ala este (Marcie)
    (49, 0, 53, 6),        # baño principal + vestidor, al este de la habitación principal
    (49, 23, 63, 24.5),    # corredor este
    (52, 18, 63, 23),      # estudio + biblioteca
]
GARAJE = (0, 17, 9, 23.5)
PASARELA = (9, 20.2, 11, 21.3)
PORCHE = (34, 27.5, 37, 29.5)
CASA_HUESPEDES = (0.5, 4, 10.5, 12)      # 10 × 8 m, al norte del garaje y del anexo
CASA_CLAIRE = (70, 19.5, 80, 27.5)       # 10 × 8 m, jardín este
SETO_X = 66.5                            # seto entre la mansión y la casa de Claire
PUERTA_SETO = (23.0, 24.5)

out = []
def px(v): return round(v * S, 1)
def P(x, y): return px(x - X0), px(y - Y0)
def add(s): out.append(s)

def rect(x0, y0, x1, y1, fill, stroke=None, sw=0, extra=''):
    x, y = P(x0, y0)
    st = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ''
    add(f'<rect x="{x}" y="{y}" width="{px(x1 - x0)}" height="{px(y1 - y0)}" fill="{fill}"{st} {extra}/>')

def text(x, y, s, size=11, weight='normal', color=None, anchor='middle', italic=False):
    X, Y = P(x, y)
    st = ' font-style="italic"' if italic else ''
    add(f'<text x="{X}" y="{Y}" font-size="{size}" font-weight="{weight}" fill="{color or C["texto"]}" text-anchor="{anchor}"{st}>{s}</text>')

# ------------------------------------------------------------------ terreno
add(f'<rect width="{W}" height="{H}" fill="{C["bg"]}"/>')
rect(X0, -3, X1, Y1, C['jardin'])
rect(X0, Y0, X1, -3, C['bosque'])
random.seed(11)
for _ in range(300):
    tx, ty = random.uniform(X0, X1), random.uniform(Y0 + 0.4, -3.6)
    X, Y = P(tx, ty)
    add(f'<circle cx="{X}" cy="{Y}" r="{px(random.uniform(0.8, 1.7))}" fill="{random.choice([C["arbol"], C["arbol2"]])}" opacity="0.85"/>')
for _ in range(34):                                     # árboles sueltos en los jardines
    tx, ty = random.choice([(random.uniform(-20, -3), random.uniform(0, 30)),
                            (random.uniform(69, 90), random.uniform(1, 16)),
                            (random.uniform(69, 90), random.uniform(31, 50))])
    X, Y = P(tx, ty)
    add(f'<circle cx="{X}" cy="{Y}" r="{px(random.uniform(1.0, 1.8))}" fill="{C["arbol"]}" opacity="0.75"/>')
text(35, -10, 'B O S Q U E', 18, 'bold', '#3f5a31')

# ------------------------------------------------------------------ caminos
for r in [(34.9, 29.5, 36.1, Y1), (1.5, 31.2, 36.1, 32.5), (0.5, 23.5, 8.5, 25.0), (1.5, 25.0, 3.0, 32.5),
          (9.6, 12, 10.4, 20.2),                          # sendero casa de huéspedes -> pasarela
          (63, 23.3, 68, 24.2)]:                          # sendero a la casa de Claire
    rect(*r, C['camino'])
text(37, 48, 'camino hacia la ciudad ↓', 11, color=C['sub'], italic=True, anchor='start')

# seto con puerta entre las dos propiedades
for (a, b) in [(-2, PUERTA_SETO[0]), (PUERTA_SETO[1], 46)]:
    rect(SETO_X - 0.5, a, SETO_X + 0.5, b, C['seto'], extra='rx="4"')
text(SETO_X + 0.9, 29.2, '↑ puerta entre setos', 9, color=C['sub'], italic=True, anchor='start')

# ------------------------------------------------------------------ patio
rect(27.5, 0, 42, 21.5, C['patio'])
rect(27.5, 16, 42, 21.5, C['deck'])
rect(32.75, 3, 36.75, 13, C['agua'], C['agua_b'], 1.5, 'rx="4"')
rect(39.2, 16.2, 41.5, 18.5, C['agua'], C['agua_b'], 1.5, 'rx="8"')
text(34.75, 8.3, 'piscina', 10, 'bold', '#1f5f79')
text(34.75, 1.6, 'patio interior', 10, color=C['sub'], italic=True)
text(33.5, 19.4, 'terraza', 10, color='#6b5537', italic=True)

# ------------------------------------------------------------------ edificios
def huella(bloques, fill, stroke=C['edif_b'], sw=2.4):
    for b in bloques:                                   # contorno de la unión: trazo grueso debajo, relleno encima
        rect(*b, fill, stroke, sw * 2)
    for b in bloques:
        rect(*b, fill)

huella(HUELLA_MANSION, C['edif'])
huella([PORCHE], C['edif'], sw=1.2)
rect(*PASARELA, '#f0ede6', C['edif_b'], 1, 'stroke-dasharray="4 3"')
huella([GARAJE], C['garaje'])
huella([CASA_HUESPEDES], C['huesp'])
huella([CASA_CLAIRE], C['claire'])
rect(CASA_CLAIRE[0] - 2, 22, CASA_CLAIRE[0], 25.5, C['edif'], C['edif_b'], 1, 'stroke-dasharray="4 3"')   # porche

text(24.2, 10, 'servicio', 10, color=C['sub'], italic=True)
text(46.5, 11, 'Marcie', 10, color=C['sub'], italic=True)
text(35, 24.6, 'LA MANSIÓN', 14, 'bold')
text(35, 26.2, '≈ 28 × 28 m', 10, color=C['sub'])
text(15.5, 18, 'anexo', 9, color=C['sub'], italic=True)
text(57.5, 20.8, 'estudio · biblioteca', 9, color=C['sub'], italic=True)
text(4.5, 20.2, 'Garaje', 11, 'bold')
text(4.5, 21.6, '3 vehículos', 9, color=C['sub'])
text(5.5, 8.2, 'Casa de', 11, 'bold')
text(5.5, 9.6, 'huéspedes', 11, 'bold')
text(5.5, 10.9, 'Vera · 10 × 8 m', 9, color=C['sub'], italic=True)
text(75, 22.8, 'Casa de', 11, 'bold')
text(75, 24.2, 'Claire', 11, 'bold')
text(75, 25.6, '10 × 8 m', 9, color=C['sub'])
text(-11, 20, 'jardín oeste', 10, color=C['sub'], italic=True)
text(79, 17, 'jardín de Claire', 10, color=C['sub'], italic=True)
text(58, 30, 'jardín este', 10, color=C['sub'], italic=True)
text(38.2, 31, 'entrada', 9, color=C['sub'], italic=True, anchor='start')
text(63, 26.2, 'puerta lateral ↑', 8, color=C['sub'], italic=True, anchor='end')

# norte
nx, ny = P(86, 4)
add(f'<g transform="translate({nx},{ny})"><polygon points="0,-20 7,7 0,2 -7,7" fill="{C["edif_b"]}"/>'
    f'<text y="22" font-size="12" font-weight="bold" text-anchor="middle" fill="{C["edif_b"]}">N</text></g>')

# ------------------------------------------------------------------ leyenda
ly = 38
text(X0 + 2, ly, 'La propiedad — plano general', 18, 'bold', anchor='start')
text(X0 + 2, ly + 1.8, 'Huella de los edificios, sin interiores · escala real', 10, color=C['sub'], anchor='start')
bx, by = X0 + 2, ly + 4
for i in range(4):
    rect(bx + i * 5, by, bx + (i + 1) * 5, by + 0.7, C['edif_b'] if i % 2 == 0 else '#ffffff', C['edif_b'], 1)
for i, lbl in enumerate(['0', '5', '10', '15', '20 m']):
    text(bx + i * 5, by + 2.3, lbl, 10)
items = [('edif', 'Mansión'), ('garaje', 'Garaje'), ('huesp', 'Casa de huéspedes'), ('claire', 'Casa de Claire'),
         ('camino', 'Caminos de grava'), ('seto', 'Seto')]
for i, (k, lbl) in enumerate(items):
    zx = X0 + 2 + (i % 3) * 15
    zy = by + 5 + (i // 3) * 2.2
    rect(zx, zy, zx + 2, zy + 1.3, C[k], C['edif_b'], 1)
    text(zx + 2.7, zy + 1.05, lbl, 11, anchor='start')

svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
       f'font-family="Helvetica, Arial, sans-serif">\n<title>La propiedad — plano general</title>\n' + '\n'.join(out) + '\n</svg>\n')
destino = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), 'plano-global.svg')
open(destino, 'w').write(svg)
print('escrito', destino)
