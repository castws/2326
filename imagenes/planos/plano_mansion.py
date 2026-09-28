"""Genera el plano interior de la mansión en SVG, junto a este script.

Uso:
  python3 imagenes/planos/plano_mansion.py                 -> plano-mansion.svg (con rótulos)
  python3 imagenes/planos/plano_mansion.py --mobiliario    -> plano-mansion-mobiliario.svg (muebles a escala, sin rótulos)
  Se puede añadir una ruta de salida distinta como argumento.

Coordenadas en metros: x hacia el este, y hacia el sur (0 = extremo norte de las alas).
Las huellas de los edificios se repiten en plano_global.py: si se mueve un muro aquí, actualizarlo allí también.
"""
import os
import random
import sys

MOB = '--mobiliario' in sys.argv
SIN_TEXTO = MOB             # con mobiliario, el plano va sin rótulos (solo título, escala y leyenda)
S = 16                      # px por metro
X0, Y0, X1, Y1 = -12, -9, 80, (61 if MOB else 46)   # con mobiliario, más alto para su leyenda
W, H = (X1 - X0) * S, (Y1 - Y0) * S

C = {
    'bg': '#e6edd9', 'bosque': '#a9c095', 'arbol': '#86a571', 'arbol2': '#6f915c',
    'serv': '#f2e4cc', 'priv': '#dbe6f2', 'soc': '#f5eedc', 'circ': '#ebe7de',
    'anexo': '#e4dcd2', 'garaje': '#dcdcdc', 'patio': '#eee8dc', 'deck': '#d8c19c',
    'agua': '#a6d6e8', 'agua_b': '#4f9fbf', 'muro': '#3b3834', 'vent': '#5fa8cf',
    'camino': '#d9d2c2', 'texto': '#2e2b27', 'sub': '#6b655c', 'porche': '#e9dfcb',
    'mueble': '#fbf9f4', 'mueble_b': '#8a8173', 'cama': '#f4efe6', 'huesp': '#dfe9f1',
}

out = []
def px(v): return round(v * S, 1)
def P(x, y): return px(x - X0), px(y - Y0)
def add(s): out.append(s)

def rect(x0, y0, x1, y1, fill, stroke=None, sw=0, extra=''):
    x, y = P(x0, y0)
    st = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ''
    add(f'<rect x="{x}" y="{y}" width="{px(x1 - x0)}" height="{px(y1 - y0)}" fill="{fill}"{st} {extra}/>')

def text(x, y, s, size=11, weight='normal', color=None, anchor='middle', italic=False, rot=False):
    if SIN_TEXTO:
        return
    X, Y = P(x, y)
    st = ' font-style="italic"' if italic else ''
    tr = f' transform="rotate(-90 {X} {Y})"' if rot else ''
    add(f'<text x="{X}" y="{Y}" font-size="{size}" font-weight="{weight}" fill="{color or C["texto"]}" text-anchor="{anchor}"{st}{tr}>{s}</text>')

def room(x0, y0, x1, y1, name, fill, dims=True, size=11, sub=None, lx=None, ly=None):
    """Estancia con su rótulo centrado (o en lx, ly). Con mobiliario, sin rótulo."""
    rect(x0, y0, x1, y1, fill, C['muro'], 2.4)
    if not name:
        return
    lines = name.split('\n')
    extra = []
    if sub: extra.append(sub)
    if dims: extra.append(f'{x1 - x0:g} × {y1 - y0:g} m'.replace('.', ','))
    cx = (x0 + x1) / 2 if lx is None else lx
    cy = (y0 + y1) / 2 if ly is None else ly
    lh = 0.85
    start = cy - (len(lines) + len(extra) - 1) * lh / 2 + 0.25
    for i, l in enumerate(lines):
        text(cx, start + i * lh, l, size, 'bold')
    for j, e in enumerate(extra):
        text(cx, start + (len(lines) + j) * lh, e, size - 2, color=C['sub'])

# aberturas: 'v' = muro vertical en x (de y0 a y1), 'h' = muro horizontal en y (de x0 a x1)
def opening(kind, at, a, b, fill, style='door', d=1, inv=False):
    """d = lado hacia el que abre la hoja: +1 este/sur, -1 oeste/norte. inv = bisagra en b en vez de en a."""
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
        elif inv:
            hx, hy = P(b, at); ex, ey = P(b, at + d * r); fx, fy = P(a, at)
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

# mobiliario (solo con --mobiliario)
def mueble(x0, y0, x1, y1, rx=0, fill=None, stroke=None, sw=1, extra=''):
    rect(x0, y0, x1, y1, fill or C['mueble'], stroke or C['mueble_b'], sw, f'rx="{rx}" {extra}')

def linea(xa, ya, xb, yb, color=None, sw=0.8, dash=None):
    (a, b), (c_, d) = P(xa, ya), P(xb, yb)
    ds = f' stroke-dasharray="{dash}"' if dash else ''
    add(f'<line x1="{a}" y1="{b}" x2="{c_}" y2="{d}" stroke="{color or C["mueble_b"]}" stroke-width="{sw}"{ds}/>')

def circulo(cx, cy, r, fill=None, stroke=None, sw=1):
    X, Y = P(cx, cy)
    add(f'<circle cx="{X}" cy="{Y}" r="{px(r)}" fill="{fill or C["mueble"]}" stroke="{stroke or C["mueble_b"]}" stroke-width="{sw}"/>')

def cama(x0, y0, x1, y1, cabecero):
    """Cama con almohadas en el lado del cabecero ('n', 's', 'e', 'o')."""
    mueble(x0, y0, x1, y1, 3, C['cama'])
    w, h = x1 - x0, y1 - y0
    if cabecero in 'ns':
        yy = y0 + 0.12 if cabecero == 'n' else y1 - 0.62
        n = 2 if w > 1.3 else 1
        for i in range(n):
            a = x0 + 0.12 + i * (w - 0.24) / n
            mueble(a + 0.05, yy, a + (w - 0.24) / n - 0.05, yy + 0.5, 3)
        fy = y0 + 0.75 if cabecero == 'n' else y1 - 0.75
        linea(x0, fy, x1, fy)
    else:
        xx = x0 + 0.12 if cabecero == 'o' else x1 - 0.62
        n = 2 if h > 1.3 else 1
        for i in range(n):
            a = y0 + 0.12 + i * (h - 0.24) / n
            mueble(xx, a + 0.05, xx + 0.5, a + (h - 0.24) / n - 0.05, 3)
        fx = x0 + 0.75 if cabecero == 'o' else x1 - 0.75
        linea(fx, y0, fx, y1)

def silla(cx, cy, s=0.45):
    mueble(cx - s / 2, cy - s / 2, cx + s / 2, cy + s / 2, 2)

def sillon(x0, y0, x1, y1, fill=None):
    mueble(x0, y0, x1, y1, 5, fill)
    mueble(x0 + 0.15, y0 + 0.15, x1 - 0.15, y1 - 0.15, 4, fill)

def inodoro(cx, cy, pared):
    """Cisterna contra la pared indicada ('n', 's', 'e', 'o')."""
    if pared in 'ns':
        t = cy - 0.35 if pared == 'n' else cy + 0.15
        mueble(cx - 0.25, t, cx + 0.25, t + 0.2, 1)
        X, Y = P(cx, cy + (0.1 if pared == 'n' else -0.1))
        add(f'<ellipse cx="{X}" cy="{Y}" rx="{px(0.2)}" ry="{px(0.27)}" fill="{C["mueble"]}" stroke="{C["mueble_b"]}" stroke-width="1"/>')
    else:
        t = cx - 0.35 if pared == 'o' else cx + 0.15
        mueble(t, cy - 0.25, t + 0.2, cy + 0.25, 1)
        X, Y = P(cx + (0.1 if pared == 'o' else -0.1), cy)
        add(f'<ellipse cx="{X}" cy="{Y}" rx="{px(0.27)}" ry="{px(0.2)}" fill="{C["mueble"]}" stroke="{C["mueble_b"]}" stroke-width="1"/>')

def lavabo(x0, y0, x1, y1, n=1):
    mueble(x0, y0, x1, y1, 1)
    horiz = (x1 - x0) >= (y1 - y0)
    for i in range(n):
        if horiz:
            cx, cy = x0 + (i + 0.5) * (x1 - x0) / n, (y0 + y1) / 2
        else:
            cx, cy = (x0 + x1) / 2, y0 + (i + 0.5) * (y1 - y0) / n
        X, Y = P(cx, cy)
        add(f'<ellipse cx="{X}" cy="{Y}" rx="{px(0.2)}" ry="{px(0.15)}" fill="#ffffff" stroke="{C["mueble_b"]}" stroke-width="0.8"/>')

def ducha(x0, y0, x1, y1):
    mueble(x0, y0, x1, y1, 0, '#eef6fa', C['vent'], 1.4)
    linea(x0, y0, x1, y1, '#b9d6e6', 0.6)
    linea(x0, y1, x1, y0, '#b9d6e6', 0.6)
    circulo((x0 + x1) / 2, (y0 + y1) / 2, 0.08, '#ffffff', C['vent'])

def estante(x0, y0, x1, y1, lomos=True):
    """Estantería: rectángulo con los lomos de los libros marcados."""
    mueble(x0, y0, x1, y1, 0, '#efe6d6')
    if not lomos:
        return
    if (x1 - x0) >= (y1 - y0):
        x = x0 + 0.25
        while x < x1 - 0.1:
            linea(x, y0 + 0.08, x, y1 - 0.08, '#b8a98f', 0.6); x += 0.25
    else:
        y = y0 + 0.25
        while y < y1 - 0.1:
            linea(x0 + 0.08, y, x1 - 0.08, y, '#b8a98f', 0.6); y += 0.25

def armario(x0, y0, x1, y1):
    """Armario: rectángulo con la barra de colgar en discontinua."""
    mueble(x0, y0, x1, y1)
    if (x1 - x0) >= (y1 - y0):
        linea(x0 + 0.1, (y0 + y1) / 2, x1 - 0.1, (y0 + y1) / 2, dash='3 2')
    else:
        linea((x0 + x1) / 2, y0 + 0.1, (x0 + x1) / 2, y1 - 0.1, dash='3 2')

def coche(x0, y0, x1, y1):
    mueble(x0, y0, x1, y1, 8, '#f3f3f3', '#7d7d7d', 1.2)
    w, h = x1 - x0, y1 - y0
    mueble(x0 + 0.2, y0 + h * 0.28, x1 - 0.2, y0 + h * 0.45, 3, '#d7e3ea', '#7d7d7d', 0.8)
    mueble(x0 + 0.2, y0 + h * 0.7, x1 - 0.2, y0 + h * 0.8, 3, '#d7e3ea', '#7d7d7d', 0.8)

def alfombra(x0, y0, x1, y1):
    rect(x0, y0, x1, y1, '#efe3cc', '#d6c7aa', 1, 'fill-opacity="0.55" stroke-dasharray="4 3"')


# ================================================================== geometría (m)
# Ala oeste (servicio): habitaciones x 21..26, corredor lateral 26..27,5 · y 0..20; pasillo oeste y 20..21,5
# Patio x 27,5..42 · Ala este: galería x 42..44, habitaciones 44..49 · Base de la U y 21,5..27,5
# Anexo oeste (bodega + yesos) x 11..20 · Garaje x 0..9 · Bloque este (estudio + biblioteca) x 52..63
YB, YS = 21.5, 27.5         # base de la U: norte y sur

# ------------------------------------------------------------------ exterior
add(f'<rect width="{W}" height="{H}" fill="{C["bg"]}"/>')
rect(X0, Y0, X1, -3, C['bosque'])
random.seed(7)
for i in range(200):
    tx, ty = random.uniform(X0, X1), random.uniform(Y0 + 0.3, -3.6)
    X, Y = P(tx, ty)
    add(f'<circle cx="{X}" cy="{Y}" r="{px(random.uniform(0.7, 1.4))}" fill="{random.choice([C["arbol"], C["arbol2"]])}" opacity="0.85"/>')
text(35, -5.6, 'B O S Q U E', 16, 'bold', '#3f5a31')

# caminos de grava
for r in [(34.9, 29.5, 36.1, 32.5), (1.5, 31.2, 36.1, 32.5), (0.5, 23.5, 8.5, 25.0), (1.5, 25.0, 3.0, 32.5),
          (63, 23.3, 70, 24.2),                      # sendero hacia la casa de Claire
          (9.6, 12, 10.4, 20.2)]:                    # sendero de la casa de huéspedes a la pasarela
    rect(*r, C['camino'])
text(18, 33.7, 'camino de entrada (grava)', 10, color=C['sub'], italic=True)


# patio, terraza, piscina
rect(27.5, 0, 42, YB, C['patio'])
rect(27.5, 16, 42, YB, C['deck'])
yy = 16.5
while yy < YB:
    (xa, ya), (xb, _) = P(27.5, yy), P(42, yy)
    add(f'<line x1="{xa}" y1="{ya}" x2="{xb}" y2="{ya}" stroke="#c7ae86" stroke-width="0.6"/>')
    yy += 0.5
rect(32.75, 3, 36.75, 13, C['agua'], C['agua_b'], 2, 'rx="6"')
text(34.75, 7.8, 'PISCINA', 11, 'bold', '#1f5f79')
text(34.75, 8.7, '4 × 10 m', 9, color='#1f5f79')
rect(39.2, 16.2, 41.5, 18.5, C['agua'], C['agua_b'], 2, 'rx="10"')
text(40.35, 17.5, 'jacuzzi', 8, 'bold', '#1f5f79')
for yy in (4.0, 6.5, 9.0, 11.5):                         # tumbonas de 2 × 0,7 m
    rect(29.4, yy, 31.4, yy + 0.7, '#ffffff', '#9c8f7a', 1, 'rx="3"')
    rect(38.1, yy, 40.1, yy + 0.7, '#ffffff', '#9c8f7a', 1, 'rx="3"')
rect(31.5, 18.5, 33.5, 19.5, '#c9b089', '#8c7656', 1, 'rx="3"')   # mesa del desayuno, 2 × 1 m
text(32.5, 19.25, 'mesa', 8, color='#5a4a35')
text(34.75, 1.5, 'PATIO INTERIOR', 12, 'bold', C['sub'])
text(34.75, 2.4, 'abierto al bosque', 9, color=C['sub'], italic=True)
text(34.75, 17.2, 'TERRAZA', 10, 'bold', '#6b5537')

# ------------------------------------------------------------------ estancias
serv, circ, soc, priv, anexo, huesp = C['serv'], C['circ'], C['soc'], C['priv'], C['anexo'], C['huesp']
# casa de huéspedes (Vera), 10 × 8: franja norte con cuarto auxiliar, baño y dormitorio; franja sur con sala y cocina.
# El dormitorio de Vera se abre a la sala frente al hueco reservado para la cama hospitalaria de Jude:
# con la puerta abierta, Vera la ve desde su cama.
text(5.5, 3.3, 'CASA DE HUÉSPEDES · Vera · 10 × 8 m', 9, 'bold', C['sub'])
room(0.5, 4, 3.5, 8, 'Cuarto\nauxiliar', huesp, size=7, ly=5.6)
room(3.5, 4, 6, 8, 'Baño', huesp, size=8, ly=5.8)
room(6, 4, 10.5, 8, 'Dormitorio', huesp, size=9, lx=8.25, ly=5.9)
room(0.5, 8, 10.5, 12, 'Sala y cocina', huesp, size=9, lx=3.6, ly=10.0)
rect(7.0, 9.75, 8.0, 11.95, 'none', C['sub'], 1, 'stroke-dasharray="4 3"')    # hueco de la cama de Jude
text(7.5, 11.0, 'Jude', 6, color=C['sub'], italic=True)
# ala oeste (servicio): tres habitaciones iguales de 5 × 4,5 con baño de 2 × 2 en la esquina noreste
for r, nombre in [(0, 'Hab. Dana'), (4.5, 'Hab. Sophie'), (9, 'Hab. Rachel')]:
    room(21, r, 26, r + 4.5, nombre, serv, lx=22.9, ly=r + 3.35, size=9)
    room(24, r, 26, r + 2, '' if MOB else 'Baño', serv, dims=False, size=8)
room(21, 13.5, 26, 15.5, 'C. técnico', serv, size=9)
room(21, 15.5, 26, 18, 'Lavandería', serv, size=9)
room(21, 18, 26, 20, 'Despensa', serv, size=9)
room(26, 0, 27.5, 20, '', circ)
text(26.95, 10, 'CORREDOR LATERAL', 9, 'bold', C['sub'], rot=True)
# anexo oeste, pasillo, pasarela, garaje
room(11, 15, 15, 20, 'Bodega', anexo, sub='medio vacía', size=10)
room(15, 15, 20, 20, 'Sala de\nyesos', anexo, sub='sin ventanas', size=10)
room(11, 20, 29, 21.5, '', circ)
text(18, 21.0, 'PASILLO OESTE', 9, 'bold', C['sub'])
rect(9, 20.2, 11, 21.3, '#f0ede6', C['muro'], 1, 'stroke-dasharray="4 3"')
text(10, 19.7, 'pasarela', 8, color=C['sub'], italic=True)
room(0, 17, 9, 23.5, 'Garaje', C['garaje'], sub='3 vehículos')
# base: cocina, comedor, corredor amplio, aseo, vestíbulo, ropero, porche
room(21, YB, 27.5, YS, 'Cocina', serv, sub='abierta')
room(27.5, YB, 32.5, YS, 'Comedor', soc)
room(32.5, YB, 38.5, 25, 'Corredor amplio', soc, size=10)
room(32.5, 25, 34, YS, 'Aseo', soc, dims=False, size=7)
room(34, 25, 37, YS, 'Vestíbulo', soc, size=9, ly=25.9)
room(37, 25, 38.5, YS, 'Rop.', soc, dims=False, size=7)
rect(34, YS, 37, 29.5, C['porche'], C['muro'], 1.2, 'stroke-dasharray="5 3"')
text(35.5, 28.8, 'Porche', 9, 'bold')
# salón en L: cuerpo 10,5 × 6 bajo el ala este + bahía 3,5 × 2,5 que entra en la terraza
pts = [(38.5, 19), (42, 19), (42, YB), (49, YB), (49, YS), (38.5, YS)]
add('<polygon points="' + ' '.join('%s,%s' % P(x, y) for x, y in pts) + f'" fill="{soc}" stroke="{C["muro"]}" stroke-width="2.4"/>')
text(45.5, 24.2, 'Salón', 12, 'bold')
text(45.5, 25.1, 'sala principal · ~72 m²', 9, color=C['sub'])
text(45.5, 25.9, '10,5 × 6 m + bahía 3,5 × 2,5 m', 8, color=C['sub'])
text(40.25, 20.3, 'bahía', 8, color=C['sub'], italic=True)
# ala este (Marcie)
room(42, 0, 49, 6, 'Habitación\nprincipal', priv, size=11)
room(49, 0, 53, 3.5, 'Baño\nprincipal', priv, size=9)
room(49, 3.5, 53, 6, 'Vestidor', priv, size=9)
room(42, 6, 44, YB, '', circ)
rect(42.4, 6.5, 43.6, 21, 'none', '#b6ad9b', 1, 'stroke-dasharray="3 3"')
text(43.25, 13.8, 'GALERÍA · luz cenital', 9, 'bold', C['sub'], rot=True)
room(44, 6, 49, 12, 'Invitados 1', priv, size=10, lx=47.0)
room(44, 12, 46, 15.5, 'Ropa\nblanca', priv, size=7, dims=False, ly=14.6)
room(46, 12, 49, 13.75, 'Baño inv. 1', priv, dims=False, size=7)     # baño privado de invitados 1
room(46, 13.75, 49, 15.5, 'Baño inv. 2', priv, dims=False, size=7)   # baño privado de invitados 2
room(44, 15.5, 49, YB, 'Invitados 2', priv, size=10, lx=47.0)
# bloque este
room(49, 23, 63, 24.5, '', circ)
text(58, 24.0, 'CORREDOR ESTE', 8, 'bold', C['sub'])
room(52, 18, 56, 23, 'Estudio', priv, size=10)
room(56, 18, 63, 23, 'Biblioteca', priv, size=11)

# ------------------------------------------------------------------ mobiliario
# Medidas reales estándar (m): cama doble 1,6 × 2,05 · cama grande 2 × 2,1 · mesilla 0,45 × 0,4 · armario 0,6 de fondo
# silla 0,45 · sillón 0,85 · sofá 0,95 de fondo · encimera 0,65 · lavadora 0,6 × 0,6 · inodoro 0,4 × 0,7
# lavabo 0,45 × 0,55 · estantería de libros 0,35-0,4 · coche 1,85 × 4,7 · cama hospitalaria 1 × 2,2 · camilla 0,7 × 1,9
if MOB:
    alfombra(45.9, 1.3, 48.95, 4.3)                  # habitación principal
    alfombra(28.4, 22.4, 31.6, 26.6)                 # comedor
    alfombra(43.0, 22.4, 48.2, 26.3)                 # salón
    # casa de huéspedes: dormitorio de Vera (cama doble con el cabecero al norte, mirando a la puerta y a la sala)
    cama(6.7, 4.05, 8.3, 6.1, 'n')
    mueble(6.2, 4.05, 6.65, 4.45); mueble(8.35, 4.05, 8.8, 4.45)
    armario(9.9, 4.3, 10.45, 6.8)
    sillon(9.0, 6.95, 9.85, 7.8)
    # baño completo: bañera (1,7 × 0,8) en el lateral derecho (pared este, esquina sureste) con el lado largo libre:
    # delante queda un hueco de 1,6 × 2,3 m, al que da la puerta, para acercar la grúa de pacientes o la silla.
    # Ducha a ras de suelo (1,45 × 1,55) bajo la ventana; inodoro contra la pared norte, junto a la ducha,
    # y lavabo en la pared oeste, entre la ducha y la puerta
    mueble(5.15, 6.25, 5.95, 7.95, 3, '#ffffff'); mueble(5.25, 6.35, 5.85, 7.85, 3, '#eef6fa')
    ducha(3.55, 4.05, 5.0, 5.6)
    inodoro(5.55, 4.4, 'n'); lavabo(3.55, 5.8, 4.0, 6.35)
    # cuarto auxiliar: sofá cama, escritorio bajo la ventana norte, estantería
    mueble(0.55, 4.5, 1.45, 6.5, 4, '#e7dcc8')
    mueble(1.8, 4.05, 3.0, 4.55); silla(2.4, 4.95)
    estante(3.0, 5.4, 3.45, 7.0, False)
    # sala y cocina americana: encimera en L con placa y fregadero, nevera, mesa para cuatro, sofá, televisor
    mueble(0.55, 8.9, 1.2, 11.95); mueble(1.2, 11.3, 3.2, 11.95)
    mueble(0.6, 9.9, 1.15, 10.6, 0, '#e8e8e8')
    for (cx, cy) in [(0.75, 10.05), (1.0, 10.05), (0.75, 10.45), (1.0, 10.45)]:
        circulo(cx, cy, 0.09, '#ffffff')
    lavabo(1.9, 11.4, 2.7, 11.9)
    mueble(0.55, 8.05, 1.3, 8.85, 1, '#f0f0f0')
    mueble(2.3, 9.4, 3.5, 10.2, 2, '#efe3cc')
    for (cx, cy) in [(2.6, 9.0), (3.2, 9.0), (2.6, 10.6), (3.2, 10.6)]:
        silla(cx, cy)
    mueble(3.8, 11.05, 5.8, 11.95, 4, '#e7dcc8')
    mueble(4.3, 9.9, 5.3, 10.4, 2, '#efe3cc')
    mueble(4.8, 8.05, 6.0, 8.45); linea(4.9, 8.25, 5.9, 8.25, '#3b3834', 2)
    silla(6.45, 10.9)                                                       # silla junto al hueco de la cama de Jude
    mueble(10.05, 9.0, 10.45, 10.0, 2)                                      # banco junto a la entrada
    # habitaciones del personal
    for r in (0, 4.5, 9):
        cama(21.05, r + 1.3, 23.1, r + 2.9, 'o')
        mueble(21.05, r + 0.8, 21.45, r + 1.25); mueble(21.05, r + 2.95, 21.45, r + 3.4)
        armario(21.5, r + 3.85, 23.9, r + 4.45)
        sillon(23.15, r + 0.1, 23.9, r + 0.85)
        mueble(24.1, r + 3.95, 25.0, r + 4.45); silla(24.55, r + 3.55)
        ducha(25.05, r + 0.05, 25.95, r + 0.95)
        inodoro(24.35, r + 0.5, 'o')
        lavabo(24.05, r + 1.25, 24.5, r + 1.8)
    # cuarto técnico, lavandería, despensa
    mueble(21.2, 14.85, 23.6, 15.45); circulo(24.6, 14.2, 0.3)
    lavabo(21.05, 15.6, 21.65, 16.3); mueble(21.05, 16.3, 21.65, 17.3)
    for i in range(3):
        mueble(21.8 + i * 0.65, 17.35, 22.4 + i * 0.65, 17.95, 2)
        circulo(22.1 + i * 0.65, 17.65, 0.2, '#ffffff')
    mueble(22.5, 16.0, 23.7, 16.35, 6)
    estante(21.05, 18.05, 21.5, 19.95, False); estante(21.5, 18.05, 25.0, 18.5, False); estante(21.5, 19.55, 25.0, 19.95, False)
    # bodega (medio vacía): botelleros con botellas tumbadas de 0,3 × 0,08 y mesa de cata
    mueble(11.05, 15.05, 14.95, 15.65, 0, '#efe6d6'); mueble(11.05, 15.65, 11.65, 19.95, 0, '#efe6d6')
    x = 11.75
    while x < 14.9:
        if int((x - 11.75) / 0.8) % 2 == 0:
            mueble(x, 15.2, x + 0.08, 15.5, 0, '#7b3b3b', '#5b2a2a', 0.5)
        x += 0.1
    y = 15.75
    while y < 19.9:
        if int((y - 15.75) / 0.8) % 2 == 0 and y < 18.2:
            mueble(11.2, y, 11.5, y + 0.08, 0, '#7b3b3b', '#5b2a2a', 0.5)
        y += 0.1
    circulo(13.3, 17.6, 0.4); silla(12.5, 17.6); silla(14.1, 17.6)
    # habitación de yesos
    mueble(15.6, 15.5, 16.3, 17.4, 3, '#ffffff')                                        # camilla
    for cy in (15.8, 17.1):
        circulo(15.95, cy, 0.1, '#dcdcdc')
    mueble(18.9, 15.4, 19.9, 17.6, 2, '#ffffff'); linea(19.4, 15.4, 19.4, 17.6)         # cama hospitalaria
    mueble(18.8, 15.3, 20.0, 15.5, 0, '#dcdcdc'); mueble(18.8, 17.5, 20.0, 17.7, 0, '#dcdcdc')
    estante(16.5, 15.05, 18.7, 15.5, False)
    mueble(15.1, 19.35, 16.3, 19.95, 1); circulo(15.7, 18.9, 0.2)                     # mesa de trabajo y taburete
    mueble(17.0, 16.5, 17.6, 16.95, 1)                                                  # carro auxiliar
    circulo(19.5, 19.4, 0.22, '#e3e3e3', '#7d7d7d'); circulo(19.65, 19.25, 0.05, '#7d7d7d', '#7d7d7d')
    # pasillo oeste: mesa con ruedas
    mueble(25.5, 20.95, 26.3, 21.45, 1)
    # garaje: tres vehículos de 1,85 × 4,7
    for x in (0.6, 3.6, 6.6):
        coche(x, 17.9, x + 1.85, 22.6)
    # cocina: encimera en L con placa y fregadero, nevera, columnas, isla, mesa del personal
    mueble(21.05, 23.3, 21.7, 27.45); mueble(21.7, 26.8, 26.4, 27.45)
    mueble(21.1, 24.4, 21.65, 25.2, 0, '#e8e8e8')
    for (cx, cy) in [(21.25, 24.6), (21.5, 24.6), (21.25, 25.0), (21.5, 25.0)]:
        circulo(cx, cy, 0.09, '#ffffff')
    lavabo(23.4, 26.85, 24.2, 27.35)
    mueble(21.05, 21.55, 21.8, 22.45, 1, '#f0f0f0'); mueble(21.9, 21.55, 23.3, 22.2)
    mueble(22.7, 23.8, 24.3, 24.7, 2)
    for cx in (23.1, 23.9):
        circulo(cx, 25.15, 0.2)
    mueble(25.8, 22.9, 26.6, 24.1, 2, '#efe3cc')
    for (cx, cy) in [(25.4, 23.2), (25.4, 23.8), (27.0, 23.2), (27.0, 23.8)]:
        silla(cx, cy)
    # comedor: mesa de 1 × 3 m para diez, aparador, vitrina
    mueble(29.5, 23.0, 30.5, 26.0, 3, '#efe3cc')
    for cy in (23.45, 24.15, 24.85, 25.55):
        silla(29.22, cy); silla(30.78, cy)
    silla(30.0, 22.72); silla(30.0, 26.28)
    mueble(30.6, 27.0, 32.2, 27.45); mueble(32.0, 24.8, 32.45, 26.4)
    # corredor amplio: mesa redonda de recibir, banco, plantas
    circulo(35.5, 23.2, 0.5, '#efe3cc'); circulo(35.5, 23.2, 0.15, '#c9dcb8', '#7fa06a')
    mueble(37.0, 24.55, 38.3, 24.95, 2)
    circulo(32.9, 21.9, 0.22, '#c9dcb8', '#7fa06a'); circulo(38.1, 21.9, 0.22, '#c9dcb8', '#7fa06a')
    # aseo, vestíbulo, ropero
    inodoro(32.85, 26.9, 'o'); lavabo(32.9, 25.05, 33.5, 25.45)
    mueble(36.55, 26.35, 36.95, 27.35, 2)
    armario(37.85, 25.2, 38.45, 27.3)
    # salón: sofá en L frente al televisor, mesa baja, sillón; mesa de juego; sillones en la bahía
    mueble(45.3, 21.55, 47.1, 22.0); linea(45.4, 21.75, 47.0, 21.75, '#3b3834', 2)
    mueble(43.25, 25.0, 46.9, 25.95, 4, '#e7dcc8'); mueble(43.25, 22.9, 44.2, 25.0, 4, '#e7dcc8')
    mueble(44.8, 23.3, 46.0, 24.1, 3, '#efe3cc')
    sillon(46.6, 22.6, 47.45, 23.45)
    circulo(40.4, 25.6, 0.5, '#efe3cc')
    for (cx, cy) in [(40.4, 24.8), (40.4, 26.4), (39.6, 25.6), (41.2, 25.6)]:
        silla(cx, cy)
    sillon(39.0, 19.6, 39.85, 20.45); sillon(40.9, 19.6, 41.75, 20.45); circulo(40.37, 20.0, 0.2)
    circulo(48.6, 27.0, 0.22, '#c9dcb8', '#7fa06a'); circulo(38.9, 27.0, 0.22, '#c9dcb8', '#7fa06a')
    # habitación principal: cama grande (cabecero al este, mira al patio), banco, sillones junto al ventanal, cómoda
    cama(46.85, 1.8, 48.95, 3.8, 'e')
    mueble(48.5, 1.25, 48.95, 1.7); mueble(48.5, 3.9, 48.95, 4.35)
    mueble(46.3, 2.1, 46.75, 3.5, 2)
    sillon(42.1, 1.2, 42.95, 2.05); sillon(42.1, 2.9, 42.95, 3.75); circulo(42.5, 2.47, 0.2)
    mueble(44.5, 5.5, 45.9, 5.95)
    # baño principal: bañera exenta bajo la ventana norte (vista al bosque), ducha de 2 × 1,4 (caben tres personas),
    # doble lavabo, inodoro
    mueble(51.1, 0.2, 52.8, 1.05, 8, '#ffffff'); mueble(51.2, 0.3, 52.7, 0.95, 7, '#eef6fa')
    ducha(49.05, 2.05, 51.05, 3.45)
    lavabo(49.1, 0.05, 50.8, 0.6, 2)
    inodoro(52.6, 2.7, 'e')
    # vestidor: armarios en U y puf
    armario(52.35, 3.55, 52.95, 5.95); armario(49.05, 5.35, 52.35, 5.95); armario(49.8, 3.55, 51.1, 4.15)
    circulo(50.8, 4.75, 0.25)
    # invitados 1
    cama(45.9, 6.05, 47.5, 8.1, 'n')
    mueble(45.4, 6.05, 45.85, 6.45); mueble(47.55, 6.05, 48.0, 6.45)
    mueble(46.0, 8.3, 47.4, 8.7, 2)
    armario(44.2, 11.4, 46.2, 12.0)
    mueble(48.45, 10.4, 48.95, 11.4); silla(48.0, 10.9)
    sillon(44.2, 9.9, 45.05, 10.75)
    # cuarto de ropa blanca (2 × 3,5): estanterías en tres paredes
    estante(45.55, 12.05, 45.95, 15.45, False); estante(44.4, 12.05, 45.55, 12.45, False); estante(44.4, 15.05, 45.55, 15.45, False)
    # baños privados de invitados (3 × 1,75 cada uno): ducha al fondo, inodoro, lavabo
    ducha(48.05, 12.05, 48.95, 13.25); inodoro(46.35, 13.3, 'o'); lavabo(47.2, 13.25, 47.9, 13.7)
    ducha(48.05, 14.25, 48.95, 15.45); inodoro(46.35, 14.2, 'o'); lavabo(47.2, 13.8, 47.9, 14.25)
    # invitados 2
    cama(45.9, 19.45, 47.5, 21.45, 's')
    mueble(45.4, 21.05, 45.85, 21.45); mueble(47.55, 21.05, 48.0, 21.45)
    mueble(46.0, 18.9, 47.4, 19.3, 2)
    armario(44.2, 15.55, 46.2, 16.15)
    mueble(48.45, 16.2, 48.95, 17.2); silla(48.0, 16.7)
    sillon(44.2, 16.6, 45.05, 17.45)
    # estudio: escritorio 1,6 × 0,75 con silla y dos de visita, estantería, sillón
    mueble(53.2, 19.6, 54.8, 20.35, 2, '#efe3cc')
    silla(54.0, 19.2, 0.55); silla(53.6, 20.8); silla(54.4, 20.8)
    estante(55.6, 18.2, 55.95, 22.8)
    sillon(52.1, 21.8, 52.95, 22.65)
    # biblioteca: estanterías de 0,4 m, dos sillones de cuero junto a la ventana norte, mesa de lectura, sofá
    estante(56.05, 18.5, 56.45, 22.95); estante(56.45, 22.55, 58.8, 22.95); estante(60.0, 22.55, 62.95, 22.95)
    estante(56.45, 18.05, 56.95, 18.45); estante(62.05, 18.05, 62.95, 18.45)
    sillon(58.3, 18.6, 59.2, 19.5, '#c9a27e'); sillon(60.2, 18.6, 61.1, 19.5, '#c9a27e'); circulo(59.7, 19.05, 0.2)
    mueble(57.8, 20.6, 59.4, 21.4, 2, '#efe3cc')
    for (cx, cy) in [(58.2, 20.2), (59.0, 20.2), (58.2, 21.8), (59.0, 21.8)]:
        silla(cx, cy)
    mueble(62.05, 19.8, 62.95, 21.8, 4, '#c9a27e'); mueble(61.2, 20.3, 61.7, 21.3, 2, '#efe3cc')
    # terraza: seis sillas alrededor de la mesa del desayuno
    for (cx, cy) in [(32.0, 18.05), (33.0, 18.05), (32.0, 19.95), (33.0, 19.95), (31.05, 19.0), (33.95, 19.0)]:
        silla(cx, cy)

# ------------------------------------------------------------------ puertas y aberturas
opening('h', 12, 9.3, 10.2, huesp, d=-1)                       # casa de huéspedes: entrada (sur)
opening('h', 8, 7.05, 7.95, huesp, d=-1)                       # sala -> dormitorio (alineada con la cama de Vera)
opening('h', 8, 3.65, 4.55, huesp, d=-1)                       # sala -> baño (0,9 m, para la grúa)
opening('h', 8, 2.3, 3.1, huesp, d=-1)                         # sala -> cuarto auxiliar
window('h', 4, 6.6, 8.4); window('v', 10.5, 4.8, 7.2)          # dormitorio: bosque y este
window('h', 4, 3.9, 4.8)                                       # baño: sobre la ducha
window('h', 4, 1.8, 3.0); window('v', 0.5, 5.0, 7.0)           # cuarto auxiliar
window('v', 0.5, 11.0, 11.8); window('h', 12, 4.0, 8.5); window('v', 10.5, 8.7, 9.9)   # sala y cocina
for r in (0, 4.5, 9):
    opening('v', 26, r + 2.8, r + 3.6, serv, d=-1)             # corredor lateral -> habitación
    opening('h', r + 2, 24.3, 25.0, serv)                      # habitación -> su baño
opening('v', 26, 14.1, 14.9, serv, d=-1)                       # cuarto técnico
opening('v', 26, 16.3, 17.1, serv, d=-1)                       # lavandería
opening('v', 26, 18.6, 19.4, serv, d=-1)                       # despensa
opening('h', 20, 26.1, 27.4, circ, 'open')                     # corredor lateral -> pasillo oeste
opening('h', 20, 13.4, 14.2, anexo, d=-1)                      # bodega
opening('h', 20, 17.5, 18.4, anexo, d=-1)                      # habitación de yesos
opening('v', 11, 20.3, 21.2, circ, 'open')                     # pasillo -> pasarela
opening('v', 9, 20.3, 21.2, C['garaje'], 'open')               # pasarela -> garaje
opening('h', 20.2, 9.6, 10.4, '#f0ede6', 'open')               # pasarela -> sendero de la casa de huéspedes
opening('h', 23.5, 0.5, 8.5, C['camino'], 'open')              # portón del garaje
opening('h', YB, 23.5, 24.4, serv)                             # pasillo -> cocina
opening('h', YB, 27.8, 28.7, soc)                              # pasillo -> comedor (puerta 3)
opening('v', 29, 20.3, 21.2, circ)                             # pasillo -> terraza (puerta 4)
opening('v', 27.5, 22.3, 26.7, soc, 'open')                    # cocina abierta al comedor
opening('v', 32.5, 22.3, 24.2, soc, 'open')                    # comedor <-> corredor amplio
opening('v', 38.5, 22.0, 24.5, soc, 'open')                    # corredor amplio <-> salón
opening('h', 25, 34.3, 36.7, soc, 'open')                      # vestíbulo -> corredor amplio
opening('v', 34, 25.6, 26.3, soc, d=-1)                        # aseo
opening('v', 37, 25.6, 26.3, soc)                              # ropero
opening('h', YS, 34.6, 35.5, C['porche'], d=-1)                # puerta principal doble, 2 hojas de 0,9 m
opening('h', YS, 35.5, 36.4, C['porche'], d=-1, inv=True)
opening('h', YB, 38.7, 41.8, soc, 'open')                      # bahía abierta al salón
opening('h', YB, 42.2, 43.8, soc, 'open')                      # galería -> salón
opening('h', 6, 42.4, 43.3, priv, d=-1)                        # galería -> habitación principal
opening('v', 49, 4.4, 5.2, priv)                               # habitación -> vestidor
opening('h', 3.5, 51.3, 52.0, priv, d=-1)                      # vestidor -> baño principal
opening('v', 44, 8.5, 9.3, priv)                               # galería -> invitados 1
opening('v', 44, 13.3, 14.1, priv)                             # galería -> ropa blanca
opening('h', 12, 46.4, 47.1, priv)                             # invitados 1 -> su baño
opening('h', 15.5, 46.4, 47.1, priv, d=-1)                     # invitados 2 -> su baño
opening('v', 44, 18.2, 19.0, priv)                             # galería -> invitados 2
opening('v', 49, 23.1, 24.4, circ, 'open')                     # salón -> corredor este
opening('h', 23, 53.3, 54.1, priv, d=-1)                       # estudio
opening('h', 23, 59.0, 59.8, priv, d=-1)                       # biblioteca
opening('v', 63, 23.2, 24.3, C['camino'])                      # puerta lateral

# ventanas
window('h', 0, 21.8, 23.6)                                     # habitación de Dana, al norte
for r in (0, 4.5, 9):
    window('v', 21, r + 1.2, r + 3.2)                          # habitaciones del personal al jardín oeste
window('v', 21, 16.0, 17.2)                                    # lavandería
for (a, b) in [(1, 6), (7, 12), (13, 18)]:
    window('v', 27.5, a, b)                                    # corredor lateral al patio
window('h', 0, 43.5, 47.5); window('v', 42, 1, 5)              # habitación principal
window('h', 0, 51.0, 52.9); window('v', 53, 0.8, 2.2)          # baño principal: ventanal norte sobre la bañera
for (a, b) in [(7.5, 10.5), (12.4, 13.3), (14.2, 15.1), (17.5, 20.5)]:
    window('v', 49, a, b)                                      # invitados 1, sus dos baños, invitados 2
for (a, b) in [(7, 11), (12.5, 16.5), (17.5, 20.5)]:
    window('v', 42, a, b)                                      # galería al patio
window('h', 18, 57, 62); window('v', 63, 19, 22)               # biblioteca
window('h', 18, 53, 55); window('v', 52, 19, 21.5)             # estudio
window('h', YS, 40, 47.5); window('v', 49, 25.5, 27)           # salón
window('h', YS, 28.5, 31.5); window('h', YS, 22, 26); window('v', 21, 22.5, 26.5)   # comedor / cocina
window('h', YB, 29.5, 32.2)                                    # ventanal norte del comedor
window('h', YB, 33, 38)                                        # vidriera corredera del corredor amplio
window('h', 19, 38.8, 41.7); window('v', 38.5, 19.2, 21.3)     # bahía del salón

# ------------------------------------------------------------------ rótulos exteriores
text(-7, 18.5, '← jardín oeste', 10, 'bold', C['sub'])
text(73.5, 23.5, 'casa de Claire →', 10, 'bold', C['sub'])
text(66.5, 22.6, 'puerta lateral', 8, color=C['sub'], italic=True)
text(58, 27, 'jardín', 9, color=C['sub'], italic=True)
text(38.5, 30.8, 'entrada', 9, color=C['sub'], italic=True)

# norte
nx, ny = P(76, 3)
add(f'<g transform="translate({nx},{ny})"><polygon points="0,-22 8,8 0,2 -8,8" fill="{C["muro"]}"/>'
    f'<text y="24" font-size="13" font-weight="bold" text-anchor="middle" fill="{C["muro"]}">N</text></g>')

# ------------------------------------------------------------------ leyenda
SIN_TEXTO = False
ly = 37
text(X0 + 2, ly, 'La mansión — planta con mobiliario' if MOB else 'La mansión — planta única', 20, 'bold', anchor='start')
text(X0 + 2, ly + 1.4, ('Muros y mobiliario a escala real · ' if MOB else 'Escala real · ') + 'medidas en metros', 11, color=C['sub'], anchor='start')
bx, by = X0 + 2, ly + 4
for i in range(4):
    rect(bx + i * 2.5, by, bx + (i + 1) * 2.5, by + 0.5, C['muro'] if i % 2 == 0 else '#ffffff', C['muro'], 1)
for i, lbl in enumerate(['0', '2,5', '5', '7,5', '10 m']):
    text(bx + i * 2.5, by + 1.6, lbl, 10)
zonas = [('serv', 'Servicio'), ('soc', 'Zona social'), ('priv', 'Zona privada'), ('circ', 'Circulación'),
         ('anexo', 'Anexo (bodega · yesos)'), ('garaje', 'Garaje')]
for i, (k, lbl) in enumerate(zonas):
    zx = 20 + (i % 3) * 14
    zy = ly - 0.8 + (i // 3) * 2
    rect(zx, zy, zx + 1.6, zy + 1, C[k], C['muro'], 1)
    text(zx + 2.1, zy + 0.8, lbl, 11, anchor='start')
sx, sy = 64, ly - 0.8
opening('h', sy + 0.5, sx, sx + 0.9, C['bg'])
rect(sx - 0.4, sy + 0.35, sx, sy + 0.65, C['muro'])
text(sx + 2.1, sy + 0.8, 'Puerta', 11, anchor='start')
rect(sx - 0.2, sy + 2.3, sx + 1.6, sy + 2.6, C['muro'])
window('h', sy + 2.45, sx - 0.2, sx + 1.6)
text(sx + 2.1, sy + 2.8, 'Ventana / ventanal', 11, anchor='start')
(xa, ya), (xb, _) = P(sx - 0.2, sy + 4.3), P(sx + 1.6, sy + 4.3)
add(f'<line x1="{xa}" y1="{ya}" x2="{xb}" y2="{ya}" stroke="{C["muro"]}" stroke-width="1" stroke-dasharray="3 3"/>')
text(sx + 2.1, sy + 4.6, 'Abertura sin puerta', 11, anchor='start')

# leyenda del mobiliario: cada símbolo dibujado a la misma escala real que en el plano
if MOB:
    fy = ly + 8.2
    text(X0 + 2, fy, 'Mobiliario', 14, 'bold', anchor='start')
    linea(X0 + 2, fy + 0.5, X1 - 2, fy + 0.5, '#c8c0b0', 1)

    def ley_bano(x, y):
        mueble(x, y + 0.6, x + 1.7, y + 1.45, 8, '#ffffff'); mueble(x + 0.1, y + 0.7, x + 1.6, y + 1.35, 7, '#eef6fa')
    def ley_placa(x, y):
        mueble(x, y + 0.7, x + 1.6, y + 1.35)
        mueble(x + 0.4, y + 0.75, x + 1.2, y + 1.3, 0, '#e8e8e8')
        for cx in (x + 0.6, x + 1.0):
            for cy in (y + 0.9, y + 1.15):
                circulo(cx, cy, 0.09, '#ffffff')
    def ley_lavadora(x, y):
        mueble(x, y + 0.7, x + 0.6, y + 1.3, 2); circulo(x + 0.3, y + 1.0, 0.2, '#ffffff')
    def ley_tv(x, y):
        mueble(x, y + 0.8, x + 1.8, y + 1.25); linea(x + 0.1, y + 1.0, x + 1.7, y + 1.0, '#3b3834', 2)
    def ley_coche(x, y):
        mueble(x, y + 0.1, x + 4.7, y + 1.95, 8, '#f3f3f3', '#7d7d7d', 1.2)
        mueble(x + 1.3, y + 0.3, x + 2.1, y + 1.75, 3, '#d7e3ea', '#7d7d7d', 0.8)
        mueble(x + 3.3, y + 0.3, x + 3.75, y + 1.75, 3, '#d7e3ea', '#7d7d7d', 0.8)
    def ley_camilla(x, y):
        mueble(x, y + 0.65, x + 1.9, y + 1.35, 3, '#ffffff')
        for cx in (x + 0.3, x + 1.6):
            circulo(cx, y + 1.0, 0.1, '#dcdcdc')
    def ley_hospital(x, y):
        mueble(x + 0.1, y + 0.5, x + 2.3, y + 1.5, 2, '#ffffff'); linea(x + 0.1, y + 1.0, x + 2.3, y + 1.0)
        mueble(x, y + 0.4, x + 0.2, y + 1.6, 0, '#dcdcdc'); mueble(x + 2.2, y + 0.4, x + 2.4, y + 1.6, 0, '#dcdcdc')
    def ley_botellero(x, y):
        mueble(x, y + 0.7, x + 2.0, y + 1.3, 0, '#efe6d6')
        for i in range(8):
            mueble(x + 0.1 + i * 0.1, y + 0.85, x + 0.18 + i * 0.1, y + 1.15, 0, '#7b3b3b', '#5b2a2a', 0.5)
    def ley_cubo(x, y):
        circulo(x + 0.3, y + 1.0, 0.22, '#e3e3e3', '#7d7d7d'); circulo(x + 0.45, y + 0.85, 0.05, '#7d7d7d', '#7d7d7d')
    def ley_carro(x, y):
        mueble(x, y + 0.75, x + 0.8, y + 1.25, 1)
        for cx in (x + 0.1, x + 0.7):
            circulo(cx, y + 1.3, 0.05, '#7d7d7d', '#7d7d7d')

    items = [
        ('Cama (doble / grande)', lambda x, y: cama(x, y + 0.05, x + 1.6, y + 2.1, 'n')),
        ('Mesilla, cómoda, banco', lambda x, y: mueble(x, y + 0.8, x + 1.4, y + 1.25, 2)),
        ('Armario (barra de colgar)', lambda x, y: armario(x, y + 0.7, x + 2.0, y + 1.3)),
        ('Sofá', lambda x, y: mueble(x, y + 0.55, x + 2.2, y + 1.5, 4, '#e7dcc8')),
        ('Sillón', lambda x, y: sillon(x, y + 0.6, x + 0.85, y + 1.45)),
        ('Silla · taburete', lambda x, y: (silla(x + 0.25, y + 1.0), circulo(x + 0.95, y + 1.0, 0.2))),
        ('Mesa', lambda x, y: mueble(x, y + 0.6, x + 1.6, y + 1.4, 2, '#efe3cc')),
        ('Mesa redonda', lambda x, y: circulo(x + 0.5, y + 1.0, 0.5, '#efe3cc')),
        ('Alfombra', lambda x, y: alfombra(x, y + 0.4, x + 2.2, y + 1.7)),
        ('Estantería de libros', lambda x, y: estante(x, y + 0.8, x + 2.2, y + 1.2)),
        ('Estantería (almacén)', lambda x, y: estante(x, y + 0.75, x + 2.2, y + 1.25, False)),
        ('Televisor sobre mueble', ley_tv),
        ('Planta', lambda x, y: circulo(x + 0.3, y + 1.0, 0.25, '#c9dcb8', '#7fa06a')),
        ('Ducha de cristal', lambda x, y: ducha(x, y + 0.5, x + 1.0, y + 1.5)),
        ('Inodoro', lambda x, y: inodoro(x + 0.3, y + 1.0, 'n')),
        ('Lavabo · fregadero', lambda x, y: lavabo(x, y + 0.75, x + 0.9, y + 1.3)),
        ('Bañera', ley_bano),
        ('Encimera con placa', ley_placa),
        ('Nevera · columna', lambda x, y: mueble(x, y + 0.6, x + 0.75, y + 1.5, 1, '#f0f0f0')),
        ('Lavadora · secadora', ley_lavadora),
        ('Calentador de agua', lambda x, y: circulo(x + 0.3, y + 1.0, 0.3)),
        ('Carro con ruedas', ley_carro),
        ('Botellero con botellas', ley_botellero),
        ('Camilla', ley_camilla),
        ('Cama hospitalaria', ley_hospital),
        ('Cubo con grifo', ley_cubo),
        ('Vehículo', ley_coche),
        ('Previsto (cama de Jude)', lambda x, y: rect(x, y + 0.5, x + 2.2, y + 1.5, 'none', C['sub'], 1, 'stroke-dasharray="4 3"')),
    ]
    col_w, row_h, cols = 11.0, 2.6, 8
    for i, (lbl, dibujo) in enumerate(items):
        cx = X0 + 2 + (i % cols) * col_w
        cy = fy + 1.0 + (i // cols) * row_h
        dibujo(cx, cy)
        ancho = 4.9 if lbl == 'Vehículo' else 2.6
        text(cx + ancho, cy + 1.3, lbl, 11, anchor='start')

svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
       f'font-family="Helvetica, Arial, sans-serif">\n<title>La mansión — planta{" con mobiliario" if MOB else ""}</title>\n' + '\n'.join(out) + '\n</svg>\n')
args = [a for a in sys.argv[1:] if not a.startswith('--')]
nombre = 'plano-mansion-mobiliario.svg' if MOB else 'plano-mansion.svg'
destino = args[0] if args else os.path.join(os.path.dirname(os.path.abspath(__file__)), nombre)
open(destino, 'w').write(svg)
print('escrito', destino)
