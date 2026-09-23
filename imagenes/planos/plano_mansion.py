"""Genera el plano interior de la mansión en SVG (plano-mansion.svg, junto a este script).

Uso: python3 imagenes/planos/plano_mansion.py [salida.svg]

Coordenadas en metros: x hacia el este, y hacia el sur (0 = extremo norte de las alas).
Las huellas de los edificios se repiten en plano_global.py: si se mueve un muro aquí, actualizarlo allí también.
"""
import os
import random
import sys

S = 10                      # px por metro
X0, Y0, X1, Y1 = -24, -20, 140, 76
W, H = (X1 - X0) * S, (Y1 - Y0) * S

C = {
    'bg': '#e6edd9', 'bosque': '#a9c095', 'arbol': '#86a571', 'arbol2': '#6f915c',
    'serv': '#f2e4cc', 'priv': '#dbe6f2', 'soc': '#f5eedc', 'circ': '#ebe7de',
    'anexo': '#e4dcd2', 'garaje': '#dcdcdc', 'patio': '#eee8dc', 'deck': '#d8c19c',
    'agua': '#a6d6e8', 'agua_b': '#4f9fbf', 'muro': '#3b3834', 'vent': '#5fa8cf',
    'camino': '#d9d2c2', 'texto': '#2e2b27', 'sub': '#6b655c', 'porche': '#e9dfcb',
}

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

def room(x0, y0, x1, y1, name, fill, dims=True, size=11, sub=None):
    rect(x0, y0, x1, y1, fill, C['muro'], 2.2)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    lines = name.split('\n')
    extra = []
    if sub: extra.append(sub)
    if dims: extra.append(f'{x1 - x0:g} × {y1 - y0:g} m')
    total = len(lines) + len(extra)
    start = cy - (total - 1) * 0.65 + 0.4
    for i, l in enumerate(lines):
        text(cx, start + i * 1.3, l, size, 'bold')
    for j, e in enumerate(extra):
        text(cx, start + (len(lines) + j) * 1.3, e, size - 2, color=C['sub'])

# aberturas: 'v' = muro vertical en x (de y0 a y1), 'h' = muro horizontal en y (de x0 a x1)
def opening(kind, at, a, b, fill, style='door', d=1):
    """d = lado hacia el que abre la hoja: +1 este/sur, -1 oeste/norte."""
    if kind == 'v':
        rect(at - 0.25, a, at + 0.25, b, fill)
    else:
        rect(a, at - 0.25, b, at + 0.25, fill)
    if style == 'open':        # abertura sin puerta: línea discontinua
        if kind == 'v':
            (xa, ya), (xb, yb) = P(at, a), P(at, b)
        else:
            (xa, ya), (xb, yb) = P(a, at), P(b, at)
        add(f'<line x1="{xa}" y1="{ya}" x2="{xb}" y2="{yb}" stroke="{C["muro"]}" stroke-width="1" stroke-dasharray="3 3"/>')
    elif style == 'door':      # hoja de puerta + arco
        r = b - a
        if kind == 'v':
            hx, hy = P(at, a); ex, ey = P(at + d * r, a); fx, fy = P(at, b)
            sweep = 1 if d > 0 else 0
        else:
            hx, hy = P(a, at); ex, ey = P(a, at + d * r); fx, fy = P(b, at)
            sweep = 0 if d > 0 else 1
        add(f'<line x1="{hx}" y1="{hy}" x2="{ex}" y2="{ey}" stroke="{C["muro"]}" stroke-width="1.2"/>')
        add(f'<path d="M{ex},{ey} A{px(r)},{px(r)} 0 0 {sweep} {fx},{fy}" fill="none" stroke="{C["muro"]}" stroke-width="0.7"/>')

def window(kind, at, a, b):
    if kind == 'v':
        rect(at - 0.22, a, at + 0.22, b, '#ffffff', C['vent'], 1.4)
    else:
        rect(a, at - 0.22, b, at + 0.22, '#ffffff', C['vent'], 1.4)

# ------------------------------------------------------------------ exterior
add(f'<rect width="{W}" height="{H}" fill="{C["bg"]}"/>')
rect(X0, Y0, X1, -3, C['bosque'])
random.seed(7)
for i in range(260):
    tx, ty = random.uniform(X0, X1), random.uniform(Y0 + 0.5, -4)
    r = random.uniform(0.9, 1.8)
    X, Y = P(tx, ty)
    add(f'<circle cx="{X}" cy="{Y}" r="{px(r)}" fill="{random.choice([C["arbol"], C["arbol2"]])}" opacity="0.85"/>')
text(60, -9.5, 'B O S Q U E', 16, 'bold', '#3f5a31')

# camino de entrada (grava) y senderos
for (x0, y0, x1, y1) in [(58.5, 48, 61.5, 55), (3, 53, 61.5, 56), (3, 38, 6, 56)]:
    rect(x0, y0, x1, y1, C['camino'])
rect(113, 37, 125, 39, C['camino'])                      # sendero a casa de Claire
rect(12.5, 16, 14.5, 30.4, C['camino'])                  # sendero de la casa de huéspedes a la pasarela
rect(4, 6, 16, 16, '#d9e6ef', C['muro'], 1.4, 'stroke-dasharray="6 3"')
text(10, 10.6, 'Casa de huéspedes', 11, 'bold')
text(10, 12, 'Vera · 12 × 10 m', 9, color=C['sub'])
text(10, 13.3, '(solo huella)', 8, color=C['sub'], italic=True)
text(33, 58.2, 'camino de entrada (grava)', 10, color=C['sub'], italic=True)

# patio, terraza, piscina
rect(45, 0, 73, 34, C['patio'])
rect(45, 24, 73, 34, C['deck'])
for yy in range(25, 34):
    X1_, Y_ = P(45, yy); X2_, _ = P(73, yy)
    add(f'<line x1="{X1_}" y1="{Y_}" x2="{X2_}" y2="{Y_}" stroke="#c7ae86" stroke-width="0.6"/>')
rect(54, 8, 64, 24, C['agua'], C['agua_b'], 2, 'rx="6"')
text(59, 15.6, 'PISCINA', 12, 'bold', '#1f5f79')
text(59, 17, '10 × 16 m', 9, color='#1f5f79')
rect(66, 24, 70, 28, C['agua'], C['agua_b'], 2, 'rx="12"')
text(68, 26.4, 'jacuzzi', 9, 'bold', '#1f5f79')
for yy in (10, 13.5, 17, 20.5):                         # tumbonas
    rect(50.5, yy, 52.5, yy + 1, '#ffffff', '#9c8f7a', 1)
    rect(65.5, yy, 67.5, yy + 1, '#ffffff', '#9c8f7a', 1)
rect(56, 27.5, 60, 30, '#c9b089', '#8c7656', 1, 'rx="3"')     # mesa
text(58, 29.2, 'mesa', 8, color='#5a4a35')
text(59, 3.2, 'PATIO INTERIOR', 13, 'bold', C['sub'])
text(59, 4.8, 'abierto al bosque', 10, color=C['sub'], italic=True)
text(59, 25.6, 'TERRAZA', 11, 'bold', '#6b5537')

# ------------------------------------------------------------------ estancias
# ala oeste (servicio)
room(34, 0, 43, 6, 'Hab. Dana', C['serv'], sub='+ baño')
room(34, 6, 43, 12, 'Hab. Sophie', C['serv'], sub='+ baño')
room(34, 12, 43, 18, 'Hab. Rachel', C['serv'], sub='+ baño')
room(34, 18, 43, 22, 'C. técnico', C['serv'], size=10)
room(34, 22, 43, 26, 'Lavandería', C['serv'], size=10)
room(34, 26, 43, 30, 'Despensa', C['serv'], size=10)
room(43, 0, 45, 30, '', C['circ'], dims=False)
# anexo, pasillo, garaje
room(16, 22, 24, 30, 'Bodega', C['anexo'], sub='medio vacía')
room(24, 22, 32, 30, 'Sala de\nyesos', C['anexo'], sub='sin ventanas')
room(16, 30, 48, 34, '', C['circ'], dims=False)
text(30, 32.4, 'PASILLO OESTE', 10, 'bold', C['sub'])
rect(11, 30.4, 16, 33.6, '#f0ede6', C['muro'], 1, 'stroke-dasharray="4 3"')
text(13.5, 35.2, 'pasarela', 9, color=C['sub'], italic=True)
text(13.5, 36.3, 'cubierta', 9, color=C['sub'], italic=True)
room(0, 26, 11, 38, 'Garaje', C['garaje'], sub='3 vehículos')
# base
room(34, 34, 45, 44, 'Cocina', C['serv'], sub='abierta')
room(45, 34, 54, 44, 'Comedor', C['soc'])
room(54, 34, 66, 40, 'Corredor amplio', C['soc'])
room(54, 40, 57, 44, 'Aseo', C['soc'], dims=False, size=8)
room(57, 40, 63, 44, 'Vestíbulo', C['soc'], size=9)
room(63, 40, 66, 44, 'Rop.', C['soc'], dims=False, size=8)
rect(57, 44, 63, 48, C['porche'], C['muro'], 1.2, 'stroke-dasharray="5 3"')
text(60, 46.4, 'Porche', 10, 'bold')
# salón en L
pts = [(66, 30), (73, 30), (73, 34), (85, 34), (85, 44), (66, 44)]
add('<polygon points="' + ' '.join('%s,%s' % P(x, y) for x, y in pts) + f'" fill="{C["soc"]}" stroke="{C["muro"]}" stroke-width="2.2"/>')
text(75.5, 38.6, 'Salón', 13, 'bold')
text(75.5, 40, 'sala principal · ~218 m²', 9, color=C['sub'])
text(75.5, 41.2, '19 × 10 m + bahía 7 × 4 m', 9, color=C['sub'])
rect(76, 42, 82, 43.2, '#cdbfa5', '#8c7e66', 1, 'rx="3"')   # sofá
text(69.5, 32.4, 'bahía', 9, color=C['sub'], italic=True)
# ala este (Marcie)
room(73, 0, 85, 8, 'Habitación\nprincipal', C['priv'], size=12)
room(73, 8, 76, 34, '', C['circ'], dims=False)
rect(73.6, 9, 75.4, 33, 'none', '#b6ad9b', 1, 'stroke-dasharray="3 3"')
X, Y = P(74.5, 21)
add(f'<text x="{X}" y="{Y}" font-size="10" font-weight="bold" fill="{C["sub"]}" text-anchor="middle" transform="rotate(-90 {X} {Y})">GALERÍA · luz cenital</text>')
room(76, 8, 85, 14, 'Baño principal', C['priv'], size=10, sub='ducha de cristal')
room(76, 14, 85, 18, 'Vestidor', C['priv'], size=10)
room(76, 18, 85, 26, 'Invitados 1', C['priv'], sub='+ baño')
room(76, 26, 85, 34, 'Invitados 2', C['priv'], sub='+ baño')
# bloque este
room(85, 36, 113, 40, '', C['circ'], dims=False)
text(99, 38.4, 'CORREDOR ESTE', 10, 'bold', C['sub'])
room(91, 26, 99, 36, 'Estudio', C['priv'])
room(99, 28, 113, 36, 'Biblioteca', C['priv'], size=12)
X, Y = P(44, 15)
add(f'<text x="{X}" y="{Y}" font-size="10" font-weight="bold" fill="{C["sub"]}" text-anchor="middle" transform="rotate(-90 {X} {Y})">CORREDOR LATERAL</text>')

# ------------------------------------------------------------------ puertas y aberturas
serv, circ, soc, priv = C['serv'], C['circ'], C['soc'], C['priv']
for y in (2, 8, 14):
    opening('v', 43, y, y + 1, serv, d=-1)
for y in (19.5, 23.5, 27.5):
    opening('v', 43, y, y + 1, serv, d=-1)
opening('h', 30, 43.3, 44.7, circ, 'open')             # corredor lateral -> pasillo
opening('h', 30, 19.5, 20.5, C['anexo'], d=-1)                # bodega
opening('h', 30, 27.5, 28.5, C['anexo'], d=-1)                # sala de yesos
opening('v', 16, 30.8, 33.2, circ, 'open')              # pasillo -> pasarela
opening('v', 11, 30.8, 33.2, C['garaje'], 'open')       # pasarela -> garaje
opening('h', 30.4, 12.5, 14.5, '#f0ede6', 'open')      # pasarela -> sendero de la casa de huéspedes
opening('h', 34, 38.5, 39.5, serv)                      # pasillo -> cocina
opening('h', 34, 46, 47, soc)                           # pasillo -> comedor (3)
opening('v', 48, 31, 32, circ)                          # pasillo -> terraza (4)
opening('v', 45, 35.5, 42.5, soc, 'open')               # cocina abierta al comedor
opening('v', 54, 36, 38, soc, 'open')                   # comedor <-> corredor amplio
opening('v', 66, 35, 39, soc, 'open')                   # corredor amplio <-> salón
opening('h', 40, 58, 62, soc, 'open')                   # vestíbulo -> corredor amplio
opening('v', 57, 41.5, 42.5, soc, d=-1)                       # aseo
opening('v', 63, 41.5, 42.5, soc)                       # ropero
opening('h', 44, 58.5, 61.5, C['porche'], d=-1)               # puertas principales
opening('h', 34, 73.3, 75.7, soc, 'open')               # galería -> salón
opening('h', 34, 66.3, 72.7, soc, 'open')               # bahía abierta al salón
opening('h', 8, 73.5, 75.3, priv, d=-1)                       # galería -> habitación principal
opening('h', 8, 80, 81, priv)                           # habitación -> baño
opening('h', 14, 80, 81, priv)                          # baño -> vestidor
opening('v', 76, 10, 11, priv)
opening('v', 76, 15.5, 16.5, priv)
opening('v', 76, 21, 22, priv)
opening('v', 76, 29, 30, priv)
opening('v', 85, 37.2, 38.8, circ, 'open')              # salón -> corredor este
opening('h', 36, 94.5, 95.5, priv, d=-1)                      # estudio
opening('h', 36, 105.5, 106.5, priv, d=-1)                    # biblioteca
opening('v', 113, 37.2, 38.8, C['camino'])              # puerta lateral
opening('h', 38, 1, 10, C['camino'], 'open')            # portón del garaje

# ventanas
for (x0, x1) in [(36, 41)]: window('h', 0, x0, x1)
for (a, b) in [(1.5, 4.5), (7.5, 10.5), (13.5, 16.5), (23, 25)]: window('v', 34, a, b)
for (a, b) in [(2, 8), (10, 16), (18, 24)]: window('v', 45, a, b)            # corredor lateral al patio
window('h', 0, 75, 83); window('v', 73, 1.5, 6.5)                         # habitación principal
for (a, b) in [(9.5, 12.5), (19.5, 24.5), (27.5, 32.5)]: window('v', 85, a, b)
for (a, b) in [(10, 16), (18, 24), (26, 32)]: window('v', 73, a, b)       # galería al patio
window('h', 28, 101, 111); window('v', 113, 29.5, 34.5)                   # biblioteca
window('h', 26, 93, 97); window('v', 91, 28, 34)                          # estudio
window('h', 44, 70, 82); window('v', 85, 41, 43)                          # salón
window('h', 44, 47, 52); window('h', 44, 37, 42); window('v', 34, 36, 42)  # comedor / cocina
# ventanales y vidrieras a la terraza
window('h', 34, 49, 53)                                 # comedor
window('h', 34, 55, 65)                                 # corredor amplio (corredera)
window('h', 30, 67, 72); window('v', 66, 30.6, 33.4)    # bahía del salón

# ------------------------------------------------------------------ rótulos exteriores
text(-11, 30, '← jardín oeste', 11, 'bold', C['sub'], 'middle')
text(128, 37.2, 'jardín este →', 11, 'bold', C['sub'])
text(128, 38.8, 'casa de Claire', 10, color=C['sub'], italic=True)
text(117.5, 36.4, 'puerta lateral', 9, color=C['sub'], italic=True)
text(99, 45, 'jardín', 10, color=C['sub'], italic=True)
text(60, 51, 'entrada', 10, color=C['sub'], italic=True)

# norte
nx, ny = P(130, 4)
add(f'<g transform="translate({nx},{ny})"><polygon points="0,-22 8,8 0,2 -8,8" fill="{C["muro"]}"/>'
    f'<text y="24" font-size="13" font-weight="bold" text-anchor="middle" fill="{C["muro"]}">N</text></g>')

# ------------------------------------------------------------------ leyenda
ly = 61
text(X0 + 2, ly, 'La mansión — planta única', 20, 'bold', anchor='start')
text(X0 + 2, ly + 2.2, 'Escala real · medidas en metros · x hacia el este, y hacia el sur', 11, color=C['sub'], anchor='start')
# barra de escala
bx, by = X0 + 2, ly + 6
for i in range(4):
    rect(bx + i * 5, by, bx + (i + 1) * 5, by + 0.8, C['muro'] if i % 2 == 0 else '#ffffff', C['muro'], 1)
for i, lbl in enumerate(['0', '5', '10', '15', '20 m']):
    text(bx + i * 5, by + 2.6, lbl, 10, anchor='middle')
# zonas
zonas = [('serv', 'Servicio'), ('soc', 'Zona social'), ('priv', 'Zona privada'), ('circ', 'Circulación'),
         ('anexo', 'Anexo (bodega · yesos)'), ('garaje', 'Garaje')]
for i, (k, lbl) in enumerate(zonas):
    zx = 30 + (i % 3) * 22
    zy = ly - 0.6 + (i // 3) * 3
    rect(zx, zy, zx + 2.5, zy + 1.6, C[k], C['muro'], 1)
    text(zx + 3.3, zy + 1.25, lbl, 11, anchor='start')
# símbolos
sx, sy = 100, ly - 0.6
opening('h', sy + 1, sx, sx + 1.4, C['bg'])
rect(sx - 0.6, sy + 0.75, sx, sy + 1.25, C['muro'])
text(sx + 3.2, sy + 1.25, 'Puerta', 11, anchor='start')
rect(sx - 0.2, sy + 3.3, sx + 2.4, sy + 3.7, C['muro'])
window('h', sy + 3.5, sx - 0.2, sx + 2.4)
text(sx + 3.2, sy + 3.85, 'Ventana / ventanal', 11, anchor='start')
Xa, Ya = P(sx - 0.2, sy + 6.2); Xb, _ = P(sx + 2.4, sy + 6.2)
add(f'<line x1="{Xa}" y1="{Ya}" x2="{Xb}" y2="{Ya}" stroke="{C["muro"]}" stroke-width="1" stroke-dasharray="3 3"/>')
text(sx + 3.2, sy + 6.55, 'Abertura sin puerta', 11, anchor='start')

svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
       f'font-family="Helvetica, Arial, sans-serif">\n<title>La mansión — planta</title>\n' + '\n'.join(out) + '\n</svg>\n')
destino = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), 'plano-mansion.svg')
open(destino, 'w').write(svg)
print('escrito', destino)
