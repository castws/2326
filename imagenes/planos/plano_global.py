"""Genera el plano general de la propiedad en SVG (plano-global.svg, junto a este script).

Uso: python3 imagenes/planos/plano_global.py [salida.svg]

Solo muestra la huella de cada edificio, sin el interior. Mismas coordenadas que plano_mansion.py:
metros, x hacia el este, y hacia el sur (0 = extremo norte de las alas de la mansión).
Si cambia un muro exterior en plano_mansion.py, actualizar HUELLA_MANSION aquí.
"""
import os
import random
import sys

S = 6                       # px por metro
X0, Y0, X1, Y1 = -44, -34, 164, 92
W, H = (X1 - X0) * S, (Y1 - Y0) * S

C = {
    'bg': '#e3ebd4', 'jardin': '#d6e4c2', 'bosque': '#a9c095', 'arbol': '#86a571', 'arbol2': '#6f915c',
    'edif': '#e9dcc3', 'edif_b': '#3b3834', 'claire': '#e4d9ee', 'huesp': '#d9e6ef', 'garaje': '#dcdcdc',
    'patio': '#eee8dc', 'deck': '#d8c19c', 'agua': '#a6d6e8', 'agua_b': '#4f9fbf',
    'camino': '#d9d2c2', 'seto': '#6f915c', 'texto': '#2e2b27', 'sub': '#6b655c',
}

# huella exterior de la mansión (bloques, sin divisiones interiores)
HUELLA_MANSION = [
    (34, 0, 45, 30),     # ala oeste (servicio)
    (16, 22, 32, 30),    # anexo oeste: bodega + habitación de yesos
    (16, 30, 48, 34),    # pasillo oeste
    (34, 34, 85, 44),    # base: cocina, comedor, corredor amplio, vestíbulo, salón
    (66, 30, 73, 34),    # bahía del salón
    (73, 0, 85, 34),     # ala este (Marcie)
    (85, 36, 113, 40),   # corredor este
    (91, 26, 99, 36),    # estudio
    (99, 28, 113, 36),   # biblioteca
]
GARAJE = (0, 26, 11, 38)
PASARELA = (11, 30.4, 16, 33.6)
PORCHE = (57, 44, 63, 48)
CASA_HUESPEDES = (4, 6, 16, 16)          # 12 × 10 m, al norte del garaje y del anexo
CASA_CLAIRE = (128, 32, 142, 42)         # 14 × 10 m, jardín este
SETO_X = 121                             # seto entre la mansión y la casa de Claire
PUERTA_SETO = (36.8, 39.2)

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
for _ in range(420):
    tx, ty = random.uniform(X0, X1), random.uniform(Y0 + 0.5, -3.5)
    X, Y = P(tx, ty)
    add(f'<circle cx="{X}" cy="{Y}" r="{px(random.uniform(1.2, 2.6))}" fill="{random.choice([C["arbol"], C["arbol2"]])}" opacity="0.85"/>')
for _ in range(40):                                     # árboles sueltos en los jardines
    tx, ty = random.choice([(random.uniform(-42, -6), random.uniform(0, 60)),
                            (random.uniform(118, 162), random.uniform(0, 28)),
                            (random.uniform(118, 162), random.uniform(48, 80))])
    X, Y = P(tx, ty)
    add(f'<circle cx="{X}" cy="{Y}" r="{px(random.uniform(1.5, 2.8))}" fill="{C["arbol"]}" opacity="0.75"/>')
text(60, -18, 'B O S Q U E', 18, 'bold', '#3f5a31')

# ------------------------------------------------------------------ caminos
for r in [(58.5, 48, 61.5, Y1), (3, 53, 61.5, 56), (3, 38, 6, 56),          # entrada, ramal al garaje
          (12.5, 16, 14.5, 30.4),                                           # sendero casa de huéspedes -> pasarela
          (113, 37, 128, 39)]:                                              # sendero a la casa de Claire
    rect(*r, C['camino'])
text(66, 86, 'camino hacia la ciudad ↓', 11, color=C['sub'], italic=True, anchor='start')

# seto con puerta entre las dos propiedades
for (a, b) in [(-2, PUERTA_SETO[0]), (PUERTA_SETO[1], 70)]:
    rect(SETO_X - 0.8, a, SETO_X + 0.8, b, C['seto'], extra='rx="4"')
text(SETO_X + 2, 44.6, 'puerta entre setos', 9, color=C['sub'], italic=True, anchor='start')

# ------------------------------------------------------------------ patio
rect(45, 0, 73, 34, C['patio'])
rect(45, 24, 73, 34, C['deck'])
rect(54, 8, 64, 24, C['agua'], C['agua_b'], 1.5, 'rx="4"')
rect(66, 24, 70, 28, C['agua'], C['agua_b'], 1.5, 'rx="8"')
text(59, 16.6, 'piscina', 10, 'bold', '#1f5f79')
text(59, 4.5, 'patio interior', 10, color=C['sub'], italic=True)
text(59, 30.4, 'terraza', 10, color='#6b5537', italic=True)

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
rect(CASA_CLAIRE[0] - 3, 35, CASA_CLAIRE[0], 39, C['edif'], C['edif_b'], 1, 'stroke-dasharray="4 3"')   # porche

text(40, 16, 'servicio', 10, color=C['sub'], italic=True)
text(79, 16, 'Marcie', 10, color=C['sub'], italic=True)
text(59, 39.8, 'LA MANSIÓN', 14, 'bold')
text(59, 42, '51 × 44 m', 10, color=C['sub'])
text(24, 27, 'anexo', 9, color=C['sub'], italic=True)
text(102, 32.6, 'estudio · biblioteca', 9, color=C['sub'], italic=True)
text(5.5, 32.2, 'Garaje', 11, 'bold')
text(5.5, 34, '3 vehículos', 9, color=C['sub'])
text(10, 10.4, 'Casa de', 11, 'bold')
text(10, 12.2, 'huéspedes', 11, 'bold')
text(10, 14, 'Vera', 9, color=C['sub'], italic=True)
text(135, 36.4, 'Casa de', 11, 'bold')
text(135, 38.2, 'Claire', 11, 'bold')
text(135, 40, '14 × 10 m', 9, color=C['sub'])
text(-16, 30, 'jardín oeste', 10, color=C['sub'], italic=True)
text(140, 26, 'jardín de Claire', 10, color=C['sub'], italic=True)
text(104, 48, 'jardín este', 10, color=C['sub'], italic=True)
text(60, 51.8, 'entrada', 9, color=C['sub'], italic=True)
text(113, 42.6, 'puerta lateral ↑', 8, color=C['sub'], italic=True, anchor='end')

# norte
nx, ny = P(154, 6)
add(f'<g transform="translate({nx},{ny})"><polygon points="0,-20 7,7 0,2 -7,7" fill="{C["edif_b"]}"/>'
    f'<text y="22" font-size="12" font-weight="bold" text-anchor="middle" fill="{C["edif_b"]}">N</text></g>')

# ------------------------------------------------------------------ leyenda
ly = 68
text(X0 + 3, ly, 'La propiedad — plano general', 18, 'bold', anchor='start')
text(X0 + 3, ly + 3, 'Huella de los edificios, sin interiores · escala real', 10, color=C['sub'], anchor='start')
bx, by = X0 + 3, ly + 7
for i in range(4):
    rect(bx + i * 10, by, bx + (i + 1) * 10, by + 1.2, C['edif_b'] if i % 2 == 0 else '#ffffff', C['edif_b'], 1)
for i, lbl in enumerate(['0', '10', '20', '30', '40 m']):
    text(bx + i * 10, by + 4, lbl, 10)
items = [('edif', 'Mansión'), ('garaje', 'Garaje'), ('huesp', 'Casa de huéspedes'), ('claire', 'Casa de Claire'),
         ('camino', 'Caminos de grava'), ('seto', 'Seto')]
for i, (k, lbl) in enumerate(items):
    zx = X0 + 3 + (i % 3) * 24
    zy = by + 8 + (i // 3) * 3.4
    rect(zx, zy, zx + 3, zy + 2, C[k], C['edif_b'], 1)
    text(zx + 4, zy + 1.6, lbl, 11, anchor='start')

svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
       f'font-family="Helvetica, Arial, sans-serif">\n<title>La propiedad — plano general</title>\n' + '\n'.join(out) + '\n</svg>\n')
destino = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), 'plano-global.svg')
open(destino, 'w').write(svg)
print('escrito', destino)
