"""Genera los planos del club BDSM (escenarios/club-bdsm.md) en SVG, junto a este script.

Uso:
  python3 imagenes/planos/plano_club.py                 -> plano-club.svg (estancias con rótulos)
  python3 imagenes/planos/plano_club.py --mobiliario    -> plano-club-mobiliario.svg (muebles a escala, sin rótulos)
  python3 imagenes/planos/plano_club.py --bodega        -> plano-club-bodega.svg (la bodega sin adecuar)
  Se puede añadir una ruta de salida distinta como argumento.

Coordenadas en metros: x hacia el este, y hacia el sur (0 = muro norte de la nave).
Nave x 12..38 · y 0..32 · saliente NE x 38..48 · y 0..12 · ala oeste x 0..12 · y 13..25 (dos plantas).
El ala se dibuja con coordenadas propias (y 10..22) dentro de ala(True) ... ala(False), que le suma DW = 3 m.
La planta alta del ala se dibuja aparte, desplazada (OX, OY), a la izquierda del plano.
"""
import os
import sys

MOB = '--mobiliario' in sys.argv
BOD = '--bodega' in sys.argv
SIN_TEXTO = MOB
S = 20                      # px por metro
X0, Y0, X1, Y1 = -33, -7, 58, (63 if MOB else 51)
W, H = (X1 - X0) * S, (Y1 - Y0) * S
OX, OY = -29, 3             # planta alta del ala a la izquierda, a la misma altura que la planta baja (y 13..25)

C = {
    'bg': '#e9e6df', 'calle': '#cfccc5', 'acera': '#dedad2', 'patio': '#e2ddd2', 'vecino': '#cdc8bf',
    'muro': '#3b3834', 'vent': '#5fa8cf', 'texto': '#2e2b27', 'sub': '#6b655c',
    'nave': '#efe9dc', 'anexo': '#e4dcd2', 'ala': '#ebe6dc',
    'club': '#f1e6dc', 'acceso': '#f2e4cc', 'semi': '#ecd9df', 'priv': '#dbe6f2', 'serv': '#e8e3d8',
    'circ': '#ebe7de', 'bodega': '#e4dcd2', 'barra': '#e9dccb', 'escena': '#d9c7b4', 'jude': '#d6e3ee',
    'mueble': '#fbf9f4', 'mueble_b': '#8a8173', 'cama': '#f4efe6', 'cuero': '#5a3b36', 'metal': '#8d8d8d',
    'espejo': '#7fa9c4', 'salida': '#3f8f5a', 'sellado': '#8f877b',
}

out = []

DW = 3                      # desplazamiento del ala oeste hacia el sur
DY = 0
def ala(on):
    global DY
    DY = DW if on else 0

def px(v): return round(v * S, 1)
def P(x, y): return px(x - X0), px(y + DY - Y0)
def add(s): out.append(s)

def rect(x0, y0, x1, y1, fill, stroke=None, sw=0, extra=''):
    x, y = P(x0, y0)
    st = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ''
    add(f'<rect x="{x}" y="{y}" width="{px(x1 - x0)}" height="{px(y1 - y0)}" fill="{fill}"{st} {extra}/>')

def poly(pts, fill, stroke=None, sw=0, extra=''):
    s = ' '.join('%s,%s' % P(x, y) for x, y in pts)
    st = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ''
    add(f'<polygon points="{s}" fill="{fill}"{st} {extra}/>')

def text(x, y, s, size=11, weight='normal', color=None, anchor='middle', italic=False, rot=False, forzar=False):
    if SIN_TEXTO and not forzar:
        return
    X, Y = P(x, y)
    st = ' font-style="italic"' if italic else ''
    tr = f' transform="rotate(-90 {X} {Y})"' if rot else ''
    add(f'<text x="{X}" y="{Y}" font-size="{size}" font-weight="{weight}" fill="{color or C["texto"]}" text-anchor="{anchor}"{st}{tr}>{s}</text>')

def room(x0, y0, x1, y1, name, fill, dims=True, size=11, sub=None, lx=None, ly=None, sw=2.4):
    rect(x0, y0, x1, y1, fill, C['muro'], sw)
    rotulo(x0, y0, x1, y1, name, dims, size, sub, lx, ly)

def rotulo(x0, y0, x1, y1, name, dims=True, size=11, sub=None, lx=None, ly=None):
    if not name:
        return
    lines = name.split('\n')
    extra = []
    if sub: extra.append(sub)
    if dims: extra.append(f'{x1 - x0:g} × {y1 - y0:g} m'.replace('.', ','))
    cx = (x0 + x1) / 2 if lx is None else lx
    cy = (y0 + y1) / 2 if ly is None else ly
    lh = size / S * 1.15
    start = cy - (len(lines) + len(extra) - 1) * lh / 2 + size / S * 0.35
    for i, l in enumerate(lines):
        text(cx, start + i * lh, l, size, 'bold')
    for j, e in enumerate(extra):
        text(cx, start + (len(lines) + j) * lh, e, size - 2, color=C['sub'])

def linea(xa, ya, xb, yb, color=None, sw=0.8, dash=None, extra=''):
    (a, b), (c_, d) = P(xa, ya), P(xb, yb)
    ds = f' stroke-dasharray="{dash}"' if dash else ''
    add(f'<line x1="{a}" y1="{b}" x2="{c_}" y2="{d}" stroke="{color or C["mueble_b"]}" stroke-width="{sw}"{ds} {extra}/>')

def circulo(cx, cy, r, fill=None, stroke=None, sw=1):
    X, Y = P(cx, cy)
    add(f'<circle cx="{X}" cy="{Y}" r="{px(r)}" fill="{fill or C["mueble"]}" stroke="{stroke or C["mueble_b"]}" stroke-width="{sw}"/>')

# ------------------------------------------------------------------ aberturas
# 'v' = muro vertical en x (de a a b en y), 'h' = muro horizontal en y (de a a b en x)
def opening(kind, at, a, b, fill, style='door', d=1, inv=False):
    """d = lado hacia el que abre la hoja: +1 este/sur, -1 oeste/norte. inv = bisagra en b."""
    if kind == 'v':
        rect(at - 0.25, a, at + 0.25, b, fill)
    else:
        rect(a, at - 0.25, b, at + 0.25, fill)
    if kind == 'v':
        (xa, ya), (xb, yb) = P(at, a), P(at, b)
    else:
        (xa, ya), (xb, yb) = P(a, at), P(b, at)
    if style == 'open':
        add(f'<line x1="{xa}" y1="{ya}" x2="{xb}" y2="{yb}" stroke="{C["muro"]}" stroke-width="1" stroke-dasharray="3 3"/>')
    elif style == 'cortina':
        add(f'<line x1="{xa}" y1="{ya}" x2="{xb}" y2="{yb}" stroke="#9b3b4b" stroke-width="2.2" stroke-dasharray="2 2"/>')
    elif style == 'reja':
        add(f'<line x1="{xa}" y1="{ya}" x2="{xb}" y2="{yb}" stroke="{C["metal"]}" stroke-width="2.6" stroke-dasharray="1 3"/>')
    elif style == 'door':
        r = b - a
        if kind == 'v':
            if inv:
                hx, hy = P(at, b); ex, ey = P(at + d * r, b); fx, fy = P(at, a)
                sweep = 0 if d > 0 else 1
            else:
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

def puerta_doble(kind, at, a, b, fill, d=1):
    m = (a + b) / 2
    opening(kind, at, a, m, fill, d=d)
    opening(kind, at, m, b, fill, d=d, inv=True)

def window(kind, at, a, b, color=None):
    if kind == 'v':
        rect(at - 0.22, a, at + 0.22, b, '#ffffff', color or C['vent'], 1.4)
    else:
        rect(a, at - 0.22, b, at + 0.22, '#ffffff', color or C['vent'], 1.4)

def porton(at, a, b, estado='porton'):
    """Portón enrollable en un muro horizontal. estado: 'porton' (bodega), 'sellado' (tapiado en el club)."""
    if estado == 'sellado':
        rect(a, at - 0.25, b, at + 0.25, C['sellado'], C['muro'], 0.8, 'stroke-dasharray="4 2"')
    else:
        rect(a, at - 0.3, b, at + 0.3, '#ffffff', C['muro'], 1.2)
        n = int((b - a) / 0.25)
        for i in range(1, n):
            linea(a + i * (b - a) / n, at - 0.3, a + i * (b - a) / n, at + 0.3, C['muro'], 0.5)

def salida(at, a, b, fill, d=-1):
    """Salida de emergencia de dos hojas en un muro horizontal, con marca verde."""
    puerta_doble('h', at, a, b, fill, d=d)
    X, Y = P((a + b) / 2, at + (0.55 if d < 0 else -0.55))
    if not SIN_TEXTO or MOB:
        add(f'<rect x="{X - 13}" y="{Y - 6}" width="26" height="11" rx="2" fill="{C["salida"]}"/>')
        add(f'<text x="{X}" y="{Y + 3}" font-size="7.5" font-weight="bold" fill="#ffffff" text-anchor="middle">SALIDA</text>')

def pilar(x, y):
    rect(x - 0.3, y - 0.3, x + 0.3, y + 0.3, '#6d675f', C['muro'], 1)

def argollas_pilar(x, y):
    for dx, dy in ((-0.42, 0), (0.42, 0), (0, -0.42), (0, 0.42)):
        circulo(x + dx, y + dy, 0.08, 'none', C['metal'], 1.2)

# ------------------------------------------------------------------ mobiliario
def mueble(x0, y0, x1, y1, rx=0, fill=None, stroke=None, sw=1, extra=''):
    rect(x0, y0, x1, y1, fill or C['mueble'], stroke or C['mueble_b'], sw, f'rx="{rx}" {extra}')

def silla(cx, cy, s=0.45):
    mueble(cx - s / 2, cy - s / 2, cx + s / 2, cy + s / 2, 2)

def taburete(cx, cy):
    circulo(cx, cy, 0.2, C['mueble'])

def sillon(x0, y0, x1, y1, fill='#e7dcc8'):
    mueble(x0, y0, x1, y1, 5, fill)
    mueble(x0 + 0.15, y0 + 0.15, x1 - 0.15, y1 - 0.15, 4, fill)

def sofa(x0, y0, x1, y1, respaldo, fill='#7a4a4f'):
    """Sofá de cuero con el respaldo en el lado indicado ('n', 's', 'e', 'o')."""
    mueble(x0, y0, x1, y1, 4, fill, '#4a2d30')
    t = 0.25
    if respaldo == 'o': mueble(x0, y0, x0 + t, y1, 2, '#5e3a3e', '#4a2d30')
    if respaldo == 'e': mueble(x1 - t, y0, x1, y1, 2, '#5e3a3e', '#4a2d30')
    if respaldo == 'n': mueble(x0, y0, x1, y0 + t, 2, '#5e3a3e', '#4a2d30')
    if respaldo == 's': mueble(x0, y1 - t, x1, y1, 2, '#5e3a3e', '#4a2d30')

def mesa_baja(cx, cy, w=0.9, h=0.6):
    mueble(cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2, 2, '#3f3a36', '#2a2724')

def cama_plataforma(x0, y0, x1, y1):
    """Cama de 2 × 2 m sobre tarima, con argollas en esquinas y laterales."""
    mueble(x0 - 0.15, y0 - 0.15, x1 + 0.15, y1 + 0.15, 2, '#4b4440', '#2a2724')
    mueble(x0, y0, x1, y1, 3, '#7a2f3b', '#4d1d26')
    for (x, y) in ((x0, y0), (x1, y0), (x0, y1), (x1, y1), ((x0 + x1) / 2, y0 - 0.05), ((x0 + x1) / 2, y1 + 0.05)):
        circulo(x, y, 0.09, 'none', C['metal'], 1.3)

def cama_hospital(x0, y0, x1, y1, cabecero='o', respaldo=True):
    mueble(x0, y0, x1, y1, 2, '#ffffff')
    if cabecero == 'o':
        mueble(x0 - 0.08, y0 - 0.05, x0 + 0.08, y1 + 0.05, 0, '#dcdcdc')
        mueble(x1 - 0.08, y0 - 0.05, x1 + 0.08, y1 + 0.05, 0, '#dcdcdc')
        mueble(x0 + 0.15, y0 + 0.15, x0 + 0.6, y1 - 0.15, 3)
        if respaldo:
            linea(x0 + 0.9, y0, x0 + 0.9, y1)
    else:
        mueble(x0 - 0.05, y0 - 0.08, x1 + 0.05, y0 + 0.08, 0, '#dcdcdc')
        mueble(x0 - 0.05, y1 - 0.08, x1 + 0.05, y1 + 0.08, 0, '#dcdcdc')
        mueble(x0 + 0.15, y0 + 0.15, x1 - 0.15, y0 + 0.6, 3)

def cama(x0, y0, x1, y1, cabecero, fill=None):
    mueble(x0, y0, x1, y1, 3, fill or C['cama'])
    w, h = x1 - x0, y1 - y0
    if cabecero in 'ns':
        yy = y0 + 0.12 if cabecero == 'n' else y1 - 0.62
        n = 2 if w > 1.3 else 1
        for i in range(n):
            a = x0 + 0.12 + i * (w - 0.24) / n
            mueble(a + 0.05, yy, a + (w - 0.24) / n - 0.05, yy + 0.5, 3)
    else:
        xx = x0 + 0.12 if cabecero == 'o' else x1 - 0.62
        n = 2 if h > 1.3 else 1
        for i in range(n):
            a = y0 + 0.12 + i * (h - 0.24) / n
            mueble(xx, a + 0.05, xx + 0.5, a + (h - 0.24) / n - 0.05, 3)

def cruz(x0, y0, x1, y1):
    """Cruz de San Andrés vista en planta: tablero con el aspa marcada y argollas."""
    mueble(x0, y0, x1, y1, 1, '#4b3a30', '#2a2018')
    linea(x0 + 0.05, y0 + 0.05, x1 - 0.05, y1 - 0.05, '#c9a878', 2.2)
    linea(x0 + 0.05, y1 - 0.05, x1 - 0.05, y0 + 0.05, '#c9a878', 2.2)

def cruz_mural(xw, y0, y1, lado=-1):
    """Cruz de San Andrés contra un muro vertical en xw, que ocupa y0..y1 y sobresale 0,35 m hacia 'lado'."""
    xa, xb = sorted((xw, xw + lado * 0.35))
    mueble(xa, y0, xb, y1, 1, '#4b3a30', '#2a2018')
    xm = xw + lado * 0.9                     # el aspa se dibuja abatida delante del muro, a trazos
    linea(xw + lado * 0.35, y0, xm, (y0 + y1) / 2, '#4b3a30', 1, '3 2')
    linea(xw + lado * 0.35, y1, xm, (y0 + y1) / 2, '#4b3a30', 1, '3 2')
    for y in (y0 + 0.1, y1 - 0.1):
        circulo(xw + lado * 0.45, y, 0.07, 'none', C['metal'], 1.2)

def marco_suspension(x0, y0, x1, y1):
    rect(x0, y0, x1, y1, 'none', '#2a2724', 3)
    for (x, y) in ((x0, y0), (x1, y0), (x0, y1), (x1, y1)):
        rect(x - 0.12, y - 0.12, x + 0.12, y + 0.12, '#2a2724')
    linea(x0, (y0 + y1) / 2, x1, (y0 + y1) / 2, '#2a2724', 1.5, '5 3')
    for x in (x0 + (x1 - x0) * f for f in (0.25, 0.5, 0.75)):
        circulo(x, (y0 + y1) / 2, 0.08, 'none', C['metal'], 1.3)

def potro(x0, y0, x1, y1):
    mueble(x0, y0, x1, y1, 4, '#5a3b36', '#2e1d1a')
    mueble(x0 + 0.12, y0 + 0.1, x1 - 0.12, y1 - 0.1, 4, '#7b534c', '#2e1d1a', 0.6)
    for x in (x0 + 0.15, x1 - 0.15):
        circulo(x, y0 - 0.05, 0.06, 'none', C['metal'], 1.1)
        circulo(x, y1 + 0.05, 0.06, 'none', C['metal'], 1.1)

def jaula(x0, y0, x1, y1):
    rect(x0, y0, x1, y1, '#f4f2ee', '#2a2724', 1.8)
    n = int((x1 - x0) / 0.15)
    for i in range(1, n):
        linea(x0 + i * (x1 - x0) / n, y0, x0 + i * (x1 - x0) / n, y1, '#6a6560', 0.6)
    m = int((y1 - y0) / 0.5)
    for j in range(1, m):
        linea(x0, y0 + j * (y1 - y0) / m, x1, y0 + j * (y1 - y0) / m, '#6a6560', 0.9)

def cepo(x0, y0, x1, y1):
    mueble(x0, y0, x1, y1, 1, '#8a6a4a', '#4a3520')
    w = x1 - x0
    cy = (y0 + y1) / 2
    circulo(x0 + w * 0.2, cy, 0.06, '#ffffff', '#4a3520')
    circulo(x0 + w * 0.5, cy, 0.1, '#ffffff', '#4a3520')
    circulo(x0 + w * 0.8, cy, 0.06, '#ffffff', '#4a3520')
    for x in (x0 + 0.12, x1 - 0.12):
        rect(x - 0.06, y1, x + 0.06, y1 + 0.6, '#4a3520')

def casilleros(x0, y0, x1, y1, n=None):
    mueble(x0, y0, x1, y1, 0, '#d9d4cb', '#6f6a62')
    horiz = (x1 - x0) >= (y1 - y0)
    n = n or int(((x1 - x0) if horiz else (y1 - y0)) / 0.4)
    for i in range(1, n):
        if horiz:
            x = x0 + i * (x1 - x0) / n; linea(x, y0, x, y1, '#6f6a62', 0.6)
        else:
            y = y0 + i * (y1 - y0) / n; linea(x0, y, x1, y, '#6f6a62', 0.6)

def barra_colgar(x0, y0, x1, y1):
    mueble(x0, y0, x1, y1, 0, '#f3efe7')
    if (x1 - x0) >= (y1 - y0):
        linea(x0 + 0.1, (y0 + y1) / 2, x1 - 0.1, (y0 + y1) / 2, dash='3 2')
    else:
        linea((x0 + x1) / 2, y0 + 0.1, (x0 + x1) / 2, y1 - 0.1, dash='3 2')

def inodoro(cx, cy, pared):
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

def estante(x0, y0, x1, y1):
    mueble(x0, y0, x1, y1, 0, '#efe6d6')
    if (x1 - x0) >= (y1 - y0):
        x = x0 + 0.5
        while x < x1 - 0.1:
            linea(x, y0, x, y1, '#b8a98f', 0.6); x += 0.5
    else:
        y = y0 + 0.5
        while y < y1 - 0.1:
            linea(x0, y, x1, y, '#b8a98f', 0.6); y += 0.5

def cubiculo(x0, y0, x1, y1, pared, puerta):
    """Cubículo de baño con mampara y el inodoro contra 'pared'; 'puerta' = lado de la mampara abierto."""
    rect(x0, y0, x1, y1, 'none', '#8a8173', 1)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    off = {'n': (0, -0.25), 's': (0, 0.25), 'e': (0.25, 0), 'o': (-0.25, 0)}[pared]
    inodoro(cx + off[0], cy + off[1], pared)

def escalera(x0, y0, x1, y1, sube='o'):
    rect(x0, y0, x1, y1, '#f3f0ea', C['muro'], 1)
    x = x0 + 0.28
    while x < x1 - 0.05:
        linea(x, y0, x, y1, '#8a8173', 0.7); x += 0.28
    ya = (y0 + y1) / 2
    if sube == 'o':
        linea(x1 - 0.3, ya, x0 + 0.4, ya, C['muro'], 1)
        poly([(x0 + 0.25, ya), (x0 + 0.5, ya - 0.15), (x0 + 0.5, ya + 0.15)], C['muro'])

def ascensor(x0, y0, x1, y1):
    rect(x0, y0, x1, y1, '#f3f0ea', C['muro'], 2.4)
    linea(x0 + 0.3, y0 + 0.3, x1 - 0.3, y1 - 0.3, '#8a8173', 0.8)
    linea(x0 + 0.3, y1 - 0.3, x1 - 0.3, y0 + 0.3, '#8a8173', 0.8)
    rect(x0 + 0.3, y0 + 0.3, x1 - 0.3, y1 - 0.3, 'none', '#8a8173', 0.8)

def camilla_gine(x0, y0, x1, y1):
    """Camilla ginecológica: cuerpo con respaldo al norte y estribos al sur."""
    mueble(x0, y0, x1, y1, 3, '#ffffff')
    linea(x0, y0 + 0.7, x1, y0 + 0.7)
    for x in (x0 - 0.15, x1 + 0.15):
        linea((x0 + x1) / 2 + (x - (x0 + x1) / 2) * 0.6, y1, x, y1 + 0.45, C['metal'], 1.5)
        circulo(x, y1 + 0.5, 0.1, '#dcdcdc', C['metal'])

def mesa_x(cx, cy, L=2.0):
    """Mesa de ataduras en X."""
    import math
    for ang in (35, -35):
        a = math.radians(ang)
        dx, dy = math.cos(a) * L / 2, math.sin(a) * L / 2
        nx, ny = -math.sin(a) * 0.2, math.cos(a) * 0.2
        poly([(cx - dx + nx, cy - dy + ny), (cx + dx + nx, cy + dy + ny), (cx + dx - nx, cy + dy - ny),
              (cx - dx - nx, cy - dy - ny)], '#4b3a30', '#2a2018', 1)
    circulo(cx, cy, 0.25, '#4b3a30', '#2a2018')

def trono(x0, y0, x1, y1):
    """Trono sobre tarima de dos escalones (tarima x0..x1, y0..y1, mirando al norte)."""
    mueble(x0, y0, x1, y1, 0, '#6b5a4a', '#3a2e24')
    mueble(x0 + 0.3, y0 + 0.3, x1 - 0.3, y1, 0, '#7d6a58', '#3a2e24')
    cx = (x0 + x1) / 2
    mueble(cx - 0.45, y1 - 0.9, cx + 0.45, y1 - 0.1, 3, '#7a2f3b', '#4d1d26')
    mueble(cx - 0.55, y1 - 0.3, cx + 0.55, y1 - 0.05, 2, '#4d1d26', '#2e1016')

def silla_facesitting(cx, cy):
    mueble(cx - 0.3, cy - 0.35, cx + 0.3, cy + 0.35, 2, '#5a3b36', '#2e1d1a')
    X, Y = P(cx, cy)
    add(f'<ellipse cx="{X}" cy="{Y}" rx="{px(0.14)}" ry="{px(0.18)}" fill="#ffffff" stroke="#2e1d1a" stroke-width="0.8"/>')

def grillete(x, y):
    circulo(x - 0.12, y, 0.08, 'none', C['metal'], 1.4)
    circulo(x + 0.12, y, 0.08, 'none', C['metal'], 1.4)
    linea(x - 0.04, y, x + 0.04, y, C['metal'], 1.4)

def espejo(kind, at, a, b):
    if kind == 'v':
        rect(at - 0.08, a, at + 0.08, b, '#dbe9f2', C['espejo'], 1.2)
    else:
        rect(a, at - 0.08, b, at + 0.08, '#dbe9f2', C['espejo'], 1.2)

def pantalla(x0, y0, x1, y1):
    mueble(x0, y0, x1, y1, 0, '#2a2d33', '#16181c')

def escenario(x0, y0, x1, y1):
    rect(x0, y0, x1, y1, C['escena'], '#6b5537', 2.2, 'rx="4"')
    rect(x0 + 0.25, y0 + 0.25, x1 - 0.25, y1 - 0.25, 'none', '#8c7656', 0.8, 'rx="3" stroke-dasharray="6 3"')

def argolla_suelo(x, y):
    circulo(x, y, 0.12, 'none', C['metal'], 1.6)


# ================================================================== exterior
XC = -9                     # borde oeste de la calle lateral; a su izquierda va la planta alta del ala
add(f'<rect width="{W}" height="{H}" fill="{C["bg"]}"/>')
rect(XC, 32.8, 52, 38, C['calle'])                       # calle principal (sur)
rect(XC, 32, 52, 32.8, C['acera'])
rect(XC, 22.8, -0.8, 38, C['calle'])                     # calle lateral (oeste)
rect(-0.8, 22, 0, 38, C['acera'])
rect(-0.8, -7, 0, 22, C['acera'])
rect(XC, -7, -0.8, 22.8, C['calle'])
rect(0, -7, 48, 0, C['patio'])                           # patio de carga (norte)
rect(0, 0, 12, 13, C['patio']); rect(0, 25, 12, 32, C['patio'])   # patios a los lados del ala
VECINO = [(38, 12), (48, 12), (48, -7), (52, -7), (52, 32), (38, 32)]
add('<clipPath id="vecino"><polygon points="' + ' '.join('%s,%s' % P(x, y) for x, y in VECINO) + '"/></clipPath>')
poly(VECINO, C['vecino'])
add('<g clip-path="url(#vecino)">')
yy = -30.0                                               # rayado del edificio vecino
while yy < 38:
    linea(30, yy, 56, yy + 26 * 0.6, '#bcb6ac', 0.6)
    yy += 0.9
add('</g>')
poly(VECINO, 'none', '#a8a298', 1)
text(45, 26, 'EDIFICIO VECINO', 10, 'bold', C['sub'], rot=True, forzar=True)
text(45, 29.5, '(medianera)', 9, color=C['sub'], italic=True, rot=True, forzar=True)
text(20, 35.9, 'CALLE PRINCIPAL', 12, 'bold', '#77736b', forzar=True)
text(-4.8, 30, 'CALLE LATERAL', 12, 'bold', '#77736b', rot=True, forzar=True)
text(24, -3.5, 'PATIO DE CARGA', 12, 'bold', '#8a8375', forzar=True)
text(6, 6.5, 'patio', 9, color=C['sub'], italic=True, forzar=True)
text(6, 28.8, 'patio', 9, color=C['sub'], italic=True, forzar=True)
for x in (17, 23, 29, 35):                               # marcas de carga en el patio
    linea(x - 1.5, -0.6, x - 1.5, -4.5, '#c8c1b3', 1)
    linea(x + 1.5, -0.6, x + 1.5, -4.5, '#c8c1b3', 1)

# ================================================================== huellas
if BOD:
    poly([(12, 0), (48, 0), (48, 12), (38, 12), (38, 32), (12, 32)], C['nave'], C['muro'], 3.2)
    ala(True); rect(0, 10, 12, 22, C['ala'], C['muro'], 3.2); ala(False)
else:
    rect(12, 0, 38, 32, C['club'], C['muro'], 3.2)
    rect(38, 0, 48, 12, C['bodega'], C['muro'], 3.2)
    ala(True); rect(0, 10, 12, 22, C['serv'], C['muro'], 3.2); ala(False)

# ================================================================== la bodega sin adecuar
if BOD:
    # cerchas del techo (a trazos, cada 4 m)
    for y in range(4, 32, 4):
        linea(12.3, y, 37.7, y, '#cbbfa8', 0.8, '10 6')
    for y in (4, 8):
        linea(38.3, y, 47.7, y, '#cbbfa8', 0.8, '10 6')
    # pilares
    for x in (20, 30):
        for y in (8, 16, 24):
            pilar(x, y)
    pilar(43, 6)
    ala(True); pilar(6, 16); ala(False)
    # portones
    for a in (14, 20, 26, 32):
        porton(0, a, a + 4)
    porton(32, 22, 29)
    # ala: puerta a la calle lateral (con dos escalones), antigua puerta interior, escalera
    ala(True)
    opening('v', 0, 16.2, 17.4, C['ala'], d=1)
    for i, x in enumerate((-0.35, -0.7)):
        rect(x, 16.0, x + 0.35, 17.6, '#d6d0c4', '#9a9286', 0.6)
    opening('v', 12, 16.2, 17.4, C['ala'], d=1)
    escalera(0.3, 10.2, 6, 11.4)
    for (a, b) in ((2, 5), (7, 10)):
        window('h', 22, a, b)
    window('v', 0, 12.5, 15); window('v', 0, 18.5, 21)
    ala(False)
    # ventanas
    window('v', 12, 3, 6); window('v', 12, 26, 30)       # ventanas altas de la nave (~4 m)
    window('h', 32, 14.5, 18.5); window('h', 32, 32, 36)
    # instalaciones
    for (x, y, lbl) in ((1.4, 23.5, 'W'), (46.4, 1.2, 'W'), (10.5, 23.5, 'E')):
        circulo(x, y, 0.45, '#ffffff', '#3f6f8f' if lbl == 'W' else '#b0772e', 1.4)
        text(x, y + 0.2, lbl, 10, 'bold', '#3f6f8f' if lbl == 'W' else '#b0772e', forzar=True)
    # rótulos
    text(25, 11.2, 'NAVE', 20, 'bold', C['sub'])
    text(25, 12.4, '26 × 32 m · 832 m² · 6,5 m de altura libre', 11, color=C['sub'])
    text(25, 13.4, 'suelo de hormigón · cerchas de acero a la vista', 10, color=C['sub'], italic=True)
    text(43, 9.2, 'SALIENTE NE', 12, 'bold', C['sub'])
    text(43, 10.2, '10 × 12 m · 120 m²', 10, color=C['sub'])
    ala(True)
    text(6, 13.8, 'ALA DE OFICINAS', 11, 'bold', C['sub'])
    text(6, 14.8, '12 × 12 m · 3 m de altura', 9, color=C['sub'])
    text(6, 19.6, 'planta alta encima', 9, color=C['sub'], italic=True)
    text(3.2, 12.2, 'escalera', 8, color=C['sub'], italic=True)
    text(-1.2, 15.6, 'dos escalones', 8, color=C['sub'], italic=True, anchor='end')
    ala(False)
    text(25.5, 31.2, 'portón sur · 7 m', 9, color=C['sub'], italic=True)
    for a in (14, 20, 26, 32):
        text(a + 2, 1.2, 'portón 4 m', 8, color=C['sub'], italic=True)
    text(13.2, 4.5, 'ventanas altas', 8, color=C['sub'], italic=True, anchor='start')

# ================================================================== el club: planta baja
else:
    club, acc, semi, serv, circ, priv = C['club'], C['acceso'], C['semi'], C['serv'], C['circ'], C['priv']
    # ---- franja sur: pasillo | vestidores | guardarropa + vestíbulo | baños
    room(12, 26, 14, 30, '', circ)
    room(12, 30, 14, 32, 'LIM', serv, dims=False, size=8)
    room(14, 26, 21, 32, 'Vestidores', acc, sub='~100 casilleros', size=11, ly=30.0)
    room(21, 26, 28, 28.5, 'Guardarropa', acc, size=10, ly=27.1)
    room(21, 28.5, 28, 32, 'Vestíbulo', acc, sub='taquilla', size=11, ly=30.4)
    room(28, 26, 38, 32, 'Baños', serv, sub='11 cubículos + accesible', size=11, lx=32.5, ly=29.0)
    room(35.5, 29.5, 38, 32, '', serv)
    text(12.95, 28.2, 'pasillo', 8, color=C['sub'], italic=True, rot=True)
    text(37.0, 31.6, 'accesible', 7, color=C['sub'])
    # ---- semiprivados NO
    room(12, 0, 16, 4, 'S1', semi, sub='sala médica', size=11)
    room(16, 0, 20, 4, 'S2', semi, sub='mazmorra', size=11)
    room(12, 6, 16, 10, 'S3', semi, sub='inmovilización', size=11)
    room(16, 6, 20, 10, 'S4', semi, sub='trono', size=11)
    rect(12.2, 4.2, 19.8, 5.8, club)                     # pasillo común (es parte del club)
    text(14.4, 5.25, 'pasillo semiprivados', 8, color=C['sub'], italic=True)
    # ---- bodega, office y barra
    # saliente NE: bodega al norte (con su puerta de carga) y office de barra al sur (el cuarto de apoyo de la barra)
    room(38, 0, 48, 6, 'Bodega', C['bodega'], size=12, sub='puerta de carga propia', ly=3.9)
    room(38, 6, 48, 12, 'Office de barra', serv, size=11, sub='cámara · hielo · lavavasos', lx=42.5, ly=8.6)
    room(35, 8, 38, 23, '', C['barra'])                  # barra; su tramo norte (y 8-11) es el paso al office
    text(36.6, 17, 'BARRA', 12, 'bold', C['texto'], rot=True)
    text(37.4, 17, '12 m', 9, color=C['sub'], rot=True)
    # ---- DJ: cabina elevada entre la barra y el muro de los baños, abierta a la pista
    room(35, 23, 38, 26, 'DJ', '#dcd6cc', dims=False, size=10, sub='elevada', lx=36.9)
    # ---- escenario
    rect(21.5, 16, 28.5, 22, C['escena'], '#6b5537', 2.2, 'rx="4"')
    rotulo(21.5, 16, 28.5, 22, 'ESCENARIO', True, 13, 'central')
    # ---- rótulos de zonas del club
    text(16.5, 12.6, 'lounge', 10, 'bold', C['sub'])
    text(16.5, 13.4, 'sofás · mesas', 8, color=C['sub'], italic=True)
    text(28, 3.3, 'camas', 10, 'bold', C['sub'])
    text(32.6, 7.7, 'zona de juego', 10, 'bold', C['sub'])
    text(25, 23.2, 'jaula · cepo', 9, 'bold', C['sub'])
    text(24, 11.4, 'PISTA', 14, 'bold', '#a08f7c')
    text(33.3, 11.6, 'sofás', 9, 'bold', C['sub'])
    # ---- ala oeste, planta baja
    ala(True)
    escalera(0.3, 10.2, 6, 11.3)
    room(0, 11.3, 6, 16, 'Oficina', priv, size=10, sub='a nivel para Jude')
    room(6, 10, 9, 16, '', circ)
    text(7.5, 14.2, 'hall', 9, 'bold', C['sub'])
    ascensor(9, 10, 12, 13)
    room(9, 13, 12, 16, 'WC', serv, dims=False, size=9)
    room(0, 16, 12, 18, '', circ)
    text(4, 17.25, 'pasillo de personal', 8, color=C['sub'], italic=True)
    room(0, 18, 8, 22, 'Vestier', priv, sub='empleadas', size=10)
    room(8, 18, 12, 22, 'Control', priv, sub='cámaras · luz · sonido', size=9)
    # palco de la planta alta, proyectado
    poly([(12, 13), (14, 15), (14, 17), (12, 19)], 'none', C['espejo'], 1.4, 'stroke-dasharray="6 4"')
    text(14.3, 16.3, 'palco', 8, color=C['espejo'], italic=True, anchor='start')
    text(14.3, 17.0, '(arriba)', 7, color=C['espejo'], italic=True, anchor='start')
    ala(False)

    # ---- pilares (con argollas en los de la nave)
    for x in (20, 30):
        for y in (8, 16, 24):
            pilar(x, y)
            if MOB:
                argollas_pilar(x, y)
    pilar(43, 6)
    ala(True); pilar(6, 16); ala(False)

    # ---- portones y puertas exteriores
    porton(0, 14, 18, 'sellado')
    for a in (20, 26, 32):
        porton(0, a, a + 4, 'sellado')
    for a in (21, 27, 33):
        salida(0, a, a + 2, club, d=-1)
    porton(32, 24.5, 29, 'sellado')
    puerta_doble('h', 32, 22, 24.5, acc, d=1)            # entrada del público (abre hacia la calle)
    puerta_doble('h', 0, 42, 44.5, C['bodega'], d=1)     # puerta de carga de la bodega
    ala(True)
    opening('v', 0, 16.4, 17.6, circ, d=1)               # entrada de personal
    poly([(-0.8, 16.2), (0, 16.2), (0, 17.8), (-0.8, 17.8)], '#d6d0c4', '#9a9286', 0.6)
    text(-1.1, 15.8, 'rampa', 8, color=C['sub'], italic=True, anchor='end')
    # ---- puertas interiores
    opening('v', 12, 16.4, 17.6, club, d=1)              # pasillo de personal -> club (bajo el palco)
    opening('h', 16, 3.0, 4.0, priv, d=-1)               # oficina
    opening('v', 9, 11.0, 12.2, circ, 'open')            # ascensor
    opening('v', 9, 14.0, 14.8, circ, d=1)               # WC
    opening('h', 16, 6.2, 8.8, circ, 'open')             # hall <-> pasillo
    opening('h', 18, 3.0, 4.0, priv)                     # vestier
    opening('h', 18, 9.5, 10.5, priv)                    # control
    ala(False)
    opening('h', 26, 12.4, 13.8, club, 'cortina')        # pasillo -> club
    opening('v', 14, 28.0, 30.0, circ, 'open')           # vestidores -> pasillo
    opening('v', 21, 29.5, 31.5, acc, 'open')            # vestíbulo -> vestidores
    opening('h', 28.5, 21.15, 22.1, acc, 'open')         # paso al guardarropa, en el extremo izquierdo del mostrador
    opening('h', 26, 28.5, 29.5, serv, d=1)              # baños
    opening('v', 35.5, 30.2, 31.2, serv, d=1, inv=True)  # baño accesible
    opening('v', 38, 9.0, 10.4, serv, d=1)               # barra -> office
    opening('h', 6, 39.0, 40.4, serv, d=1)               # bodega -> office (abre hacia el office)
    opening('v', 35, 22.2, 23.0, C['barra'], 'open')     # trampilla de la barra
    opening('h', 23, 36.8, 37.7, '#dcd6cc', d=1)         # barra -> cabina del DJ
    opening('v', 35, 23.3, 25.7, '#dcd6cc', 'open')      # frente de la cabina, abierto a la pista (antepecho bajo)
    for (a, b) in ((12.3, 15.7), (16.3, 19.7)):
        opening('h', 4, a, b, semi, 'cortina')
        opening('h', 6, a, b, semi, 'cortina')
    opening('h', 4, 16.3, 19.7, semi, 'reja')            # S2: reja de barrotes
    opening('h', 6, 16.3, 19.7, semi, 'open')            # S4: abierto
    opening('v', 20, 4.3, 5.7, club, 'open')             # pasillo de semiprivados
    # ---- ventanas
    ala(True)
    window('v', 0, 12.5, 15.0)                           # oficina a la calle lateral
    window('h', 22, 2, 5); window('h', 22, 9, 11)        # vestier y control al patio
    ala(False)
    window('v', 12, 26, 30)                              # ventana alta de la nave
    window('h', 32, 32, 36); window('h', 32, 14.5, 18.5)

    # ---- mobiliario
    if MOB:
        # vestidores: casilleros a los lados (norte y sur), banco corrido en el centro
        casilleros(14.4, 26.25, 20.6, 26.8, 16); casilleros(14.4, 31.2, 20.6, 31.75, 16)
        mueble(15.2, 28.75, 19.8, 29.25, 1, '#c9b089', '#8c7656')
        # guardarropa: barras de colgar; taquilla: mostrador con paso a la izquierda
        barra_colgar(22.5, 26.25, 27.7, 26.8); barra_colgar(22.5, 27.05, 27.7, 27.6)
        mueble(22.2, 28.25, 27.8, 28.75, 1, '#8c7656', '#5a4a35')
        silla(25, 27.95)
        # baños: 5 cubículos al norte, 6 al sur, lavabos al oeste, accesible
        for i in range(5):
            cubiculo(33 + i, 26.25, 34 + i, 27.75, 'n', 's')
        for i in range(6):
            cubiculo(29.3 + i, 30.3, 30.3 + i, 31.75, 's', 'n')
        lavabo(28.3, 27.15, 28.85, 30.15, 5)
        inodoro(37.4, 30.8, 'e'); lavabo(35.8, 31.2, 36.6, 31.75)
        # escenario: cruz y punto de suspensión
        escenario(21.5, 16, 28.5, 22)
        cruz(22.8, 19.3, 24.0, 20.5)
        circulo(26.5, 19.0, 0.35, 'none', C['metal'], 1.2); circulo(26.5, 19.0, 0.1, C['metal'], C['metal'])
        # barra: mostrador, contrabarra, taburetes
        mueble(35, 11.3, 35.65, 22.2, 1, '#3f3a36', '#2a2724')
        mueble(37.4, 11.3, 37.95, 22.8, 0, '#efe6d6')
        for y in (12.2, 14.0, 15.8, 17.6, 19.4, 21.2):
            taburete(34.45, y)
        estante(35.2, 8.2, 37.8, 8.7)
        # DJ: consola mirando a la pista
        mueble(35.3, 23.6, 35.95, 25.4, 1, '#3f3a36', '#2a2724')
        circulo(35.62, 24.1, 0.22, '#1c1c1c', '#000000'); circulo(35.62, 24.9, 0.22, '#1c1c1c', '#000000')
        silla(36.6, 24.5)
        # lounge oeste, en el rincón entre los semiprivados y el muro oeste: sofás individuales, cada uno con su
        # mesa baja delante, y sillones. Al sur de y 18 queda libre: puerta del pasillo de personal (y 19,4-20,6)
        # y llegada desde los vestidores.
        sillon(12.25, 10.1, 13.1, 10.95, '#7a4a4f')                              # rincón
        for x0 in (13.7, 16.7):                                                  # contra los semiprivados
            sofa(x0, 10.1, x0 + 2.1, 10.95, 'n'); mesa_baja(x0 + 1.05, 11.75, 1.1, 0.5)
        for y0 in (11.9, 15.6):                                                  # contra el muro oeste
            sofa(12.2, y0, 13.05, y0 + 2.1, 'o'); mesa_baja(13.85, y0 + 1.05, 0.5, 1.1)
        sillon(14.75, 12.55, 15.6, 13.4, '#7a4a4f')
        sillon(17.35, 12.55, 18.2, 13.4, '#7a4a4f')
        sillon(14.75, 16.2, 15.6, 17.05, '#7a4a4f')
        # tres mesas redondas con tres sillas entre el escenario y la barra (dejan 1,5 m libres ante los taburetes)
        for y in (14.0, 18.0, 21.6):
            circulo(31.8, y, 0.4, '#3f3a36', '#2a2724')
            silla(31.05, y); silla(32.55, y); silla(31.8, y + 0.75)
        # sofás junto a la barra (NE)
        sofa(30.6, 10.9, 33.8, 11.85, 's')
        mesa_baja(32.2, 10.2, 1.2, 0.5)
        sillon(30.6, 9.0, 31.45, 9.85, '#7a4a4f'); sillon(33.0, 9.0, 33.85, 9.85, '#7a4a4f')
        # camas plataforma
        cama_plataforma(24, 2, 26, 4); cama_plataforma(24, 6, 26, 8); cama_plataforma(30, 2, 32, 4)
        # zona de juego NE: cruz mural, marco de suspensión, potro
        cruz_mural(38, 1.0, 2.4, -1)
        marco_suspension(34.8, 3.6, 37.3, 6.6)
        potro(30.0, 5.8, 31.3, 6.4)
        # jaula y cepo al sur del escenario
        jaula(22.0, 23.4, 23.5, 25.4)
        cepo(26.6, 23.9, 28.0, 24.2)
        # semiprivados
        camilla_gine(13.65, 0.8, 14.35, 2.6)                                  # S1
        circulo(14.0, 1.7, 0.4, 'none', '#d9c86a', 1); mueble(15.1, 0.3, 15.7, 0.9, 1)   # lámpara, carrito
        grillete(17.0, 0.35); grillete(18.2, 0.35)                            # S2
        jaula(18.6, 1.9, 19.8, 3.3); argolla_suelo(17.3, 2.4)
        mueble(16.4, 3.1, 18.3, 3.5, 1, '#8a6a4a', '#4a3520')
        mesa_x(14.0, 8.2, 2.2)                                                # S3
        rect(12.2, 6.4, 12.4, 9.4, '#e8d9c8', '#5a3b36', 1)                   # cama de vacío colgada
        mueble(15.0, 9.3, 15.8, 9.8, 1, '#d0d0d0')                            # saco de momificación y film
        circulo(14.0, 7.2, 0.08, C['metal'], C['metal'])
        trono(17.0, 8.6, 19.0, 9.8)                                           # S4
        argolla_suelo(18.0, 8.1); silla_facesitting(19.4, 7.0)
        espejo('v', 16.2, 6.5, 9.5)
        # bodega: estanterías
        for x in (39.2, 45.2):
            estante(x, 1.6, x + 0.6, 5.5)
        estante(46.7, 0.9, 47.6, 5.7)
        # office de barra: cámara de bebidas, máquina de hielo, fregadero y lavavasos, estanterías de vasos
        mueble(45.0, 8.4, 47.9, 11.9, 1, '#e3edf3', '#6f8a9c', 1.4)
        mueble(45.3, 8.7, 47.6, 11.6, 0, 'none', '#9fb6c6', 0.8)
        mueble(38.2, 11.2, 39.0, 11.95, 1, '#f0f0f0')
        lavabo(39.6, 11.4, 43.2, 11.95, 2); mueble(43.2, 11.4, 44.0, 11.95, 1, '#f0f0f0')
        estante(40.9, 6.1, 44.8, 6.55); estante(38.1, 6.6, 38.55, 8.6)
        # ala planta baja
        ala(True)
        mueble(0.4, 12.0, 2.2, 12.8, 1, '#efe3cc'); silla(1.3, 13.2)          # oficina: escritorio de Marcie
        mueble(3.4, 12.0, 5.6, 12.8, 1, '#efe3cc')                            # mesa de Jude (sin silla, para su silla reclinable)
        estante(0.3, 14.6, 0.7, 15.8)
        inodoro(11.4, 14.9, 'e'); lavabo(9.3, 15.2, 10.1, 15.75)
        casilleros(0.3, 18.3, 2.7, 18.8, 6); casilleros(4.3, 18.3, 7.7, 18.8, 8); mueble(0.5, 19.6, 4.5, 20.0, 1, '#c9b089', '#8c7656')
        mueble(0.3, 21.3, 3.0, 21.75, 1, '#efe3cc'); ducha(6.0, 20.2, 7.75, 21.75)
        mueble(8.3, 20.9, 11.7, 21.7, 1, '#efe3cc')
        for x in (8.8, 9.9, 11.0):
            pantalla(x - 0.35, 21.7, x + 0.35, 21.8)
        silla(10, 20.4)
        ala(False)

# ================================================================== planta alta del ala (a la derecha)
def A(x, y): return x + OX, y + OY

def planta_alta():
    ax0, ay0 = A(0, 10); ax1, ay1 = A(12, 22)
    text((ax0 + ax1) / 2 + 1, ay0 - 2.2, 'PLANTA ALTA DEL ALA OESTE', 12, 'bold', forzar=True)
    text((ax0 + ax1) / 2 + 1, ay0 - 1.3, '+3,2 m sobre la nave · misma escala', 9, color=C['sub'], forzar=True)
    if BOD:
        rect(ax0, ay0, ax1, ay1, C['ala'], C['muro'], 3.2)
        escalera(*A(0.3, 10.2), *A(6, 11.4))
        pilar(*A(6, 16))
        window('v', A(12, 0)[0], A(0, 14)[1], A(0, 18)[1])
        for (a, b) in ((2, 5), (7, 10)):
            window('h', ay0, A(a, 0)[0], A(b, 0)[0]); window('h', ay1, A(a, 0)[0], A(b, 0)[0])
        window('v', ax0, A(0, 12.5)[1], A(0, 15)[1]); window('v', ax0, A(0, 18)[1], A(0, 20.5)[1])
        text(*A(6, 16.9), 'antiguas oficinas', 11, 'bold', C['sub'])
        text(*A(6, 17.8), 'vacías · 12 × 12 m', 9, color=C['sub'])
        text(A(12.6, 0)[0], A(0, 16.2)[1], 'ventana de', 8, color=C['sub'], italic=True, anchor='start')
        text(A(12.6, 0)[0], A(0, 16.9)[1], 'supervisión', 8, color=C['sub'], italic=True, anchor='start')
        text(*A(3.2, 12.2), 'llega la escalera', 8, color=C['sub'], italic=True)
        return
    serv, circ, priv, jude = C['serv'], C['circ'], C['priv'], C['jude']
    rect(ax0, ay0, ax1, ay1, serv, C['muro'], 3.2)
    escalera(*A(0.3, 10.2), *A(6, 11.3))
    room(*A(0, 11.3), *A(6, 19), 'Sala BDSM\nprivada', C['semi'], sub='6 × 7,7 m', size=10, dims=False, ly=A(0, 14.6)[1])
    room(*A(6, 10), *A(9, 19), '', circ)
    text(*A(7.5, 12.2), 'hall', 9, 'bold', C['sub'])
    ascensor(*A(9, 10), *A(12, 13))
    poly([A(12, 13), A(14, 15), A(14, 17), A(12, 19)], jude, C['muro'], 0)
    room(*A(8, 13), *A(12, 19), 'Hab. de\nJude', jude, dims=False, size=10, lx=A(10.2, 0)[0], ly=A(0, 17.2)[1])
    rect(*A(11.8, 13.3), *A(12.2, 18.7), jude)          # sin muro entre la habitación y el palco
    linea(*A(12, 13), *A(12, 19), C['sub'], 0.8, '3 3')
    espejo('v', A(14, 0)[0], A(0, 15)[1], A(0, 17)[1])
    for (pa, pb) in ((A(12, 13), A(14, 15)), (A(12, 19), A(14, 17))):
        add(f'<line x1="{px(pa[0] - X0)}" y1="{px(pa[1] - Y0)}" x2="{px(pb[0] - X0)}" y2="{px(pb[1] - Y0)}" '
            f'stroke="{C["espejo"]}" stroke-width="4"/>')
        add(f'<line x1="{px(pa[0] - X0)}" y1="{px(pa[1] - Y0)}" x2="{px(pb[0] - X0)}" y2="{px(pb[1] - Y0)}" '
            f'stroke="#dbe9f2" stroke-width="1.6"/>')
    rect(*A(13.92, 15), *A(14.08, 17), '#dbe9f2', C['espejo'], 1.4)
    room(*A(0, 19), *A(4, 22), 'Baño', serv, dims=False, size=9)
    room(*A(4, 19), *A(12, 22), 'Sala VIP', C['semi'], size=10, lx=A(9.5, 0)[0])
    pilar(*A(6, 16))
    text(*A(7.0, 16.5), 'pasillo', 8, color=C['sub'], italic=True, rot=True)
    text(A(14.5, 0)[0], A(0, 16.3)[1], 'palco', 9, 'bold', C['espejo'], anchor='start')
    text(A(14.5, 0)[0], A(0, 17.1)[1], 'espejos 45°', 8, color=C['espejo'], anchor='start')
    text(A(14.5, 0)[0], A(0, 17.8)[1], '→ escenario', 8, color=C['espejo'], anchor='start')
    # puertas
    opening('v', A(6, 0)[0], A(0, 17.2)[1], A(0, 18.4)[1], C['semi'], d=-1)     # pasillo -> sala BDSM
    opening('v', A(8, 0)[0], A(0, 14.0)[1], A(0, 15.2)[1], jude, d=1)           # pasillo -> Jude (1,2 m)
    opening('v', A(9, 0)[0], A(0, 11.0)[1], A(0, 12.2)[1], circ, 'open')        # ascensor
    opening('h', A(0, 19)[1], A(1.5, 0)[0], A(2.5, 0)[0], serv, d=1)           # sala BDSM -> baño
    opening('h', A(0, 19)[1], A(6.2, 0)[0], A(7.8, 0)[0], C['semi'], d=1)       # pasillo -> sala VIP
    # ventanas
    window('v', ax0, A(0, 12.5)[1], A(0, 15)[1]); window('v', ax0, A(0, 16.5)[1], A(0, 18.5)[1])
    window('h', ay1, A(5, 0)[0], A(8, 0)[0]); window('h', ay1, A(9, 0)[0], A(11, 0)[0])
    if MOB:
        # sala BDSM privada: cruz, cama con dosel, banco, el pilar como poste
        cruz_mural(A(0, 0)[0], A(0, 12.6)[1], A(0, 14.0)[1], 1)
        cama(*A(0.3, 15.8), *A(2.3, 18.0), 'o', '#7a2f3b')
        potro(*A(3.6, 12.3), *A(4.9, 12.9))
        argollas_pilar(*A(6, 16))
        # baño
        inodoro(*A(0.6, 21.3), 'o'); ducha(*A(2.4, 20.3), *A(3.8, 21.8)); lavabo(*A(0.3, 19.4), *A(1.1, 19.95))
        # sala VIP
        sofa(*A(4.3, 21.0), *A(8.3, 21.8), 's'); mesa_baja(*A(6.3, 20.3), 1.4, 0.6)
        sillon(*A(9.2, 19.9), *A(10.05, 20.75), '#7a4a4f'); sillon(*A(10.6, 19.9), *A(11.45, 20.75), '#7a4a4f')
        # habitación de Jude: cama con los pies en el palco, pantallas colgadas, equipos
        cama_hospital(*A(10.3, 15.5), *A(12.45, 16.5), 'o')
        pantalla(*A(13.1, 15.3), *A(13.25, 16.7))
        mueble(*A(10.4, 14.5), *A(11.0, 15.1), 1, '#e6eef4')              # respirador
        mueble(*A(10.4, 16.9), *A(11.0, 17.5), 1, '#e6eef4')              # monitor
        mueble(*A(8.2, 13.2), *A(9.2, 13.8), 0, '#efe6d6')                # armario de insumos
        lavabo(*A(9.4, 13.2), *A(10.1, 13.7))
        sillon(*A(8.3, 17.8), *A(9.15, 18.65))                           # acompañante
        mueble(*A(9.7, 17.7), *A(10.5, 18.8), 3, '#dcdcdc')               # silla reclinable
        linea(*A(10.1, 17.7), *A(10.9, 16.5), '#8a8173', 1, '2 2')        # riel de la grúa
        # hall: nada

planta_alta()

# ================================================================== norte, escala y leyenda
nx, ny = P(55, 1.5)
add(f'<g transform="translate({nx},{ny})"><polygon points="0,-22 8,8 0,2 -8,8" fill="{C["muro"]}"/>'
    f'<text y="24" font-size="13" font-weight="bold" text-anchor="middle" fill="{C["muro"]}">N</text></g>')

SIN_TEXTO = False
ly = 41
titulo = ('Bonded — la bodega sin adecuar' if BOD else
          'Bonded — planta con mobiliario' if MOB else 'Bonded — planta')
text(X0 + 1, ly, titulo, 20, 'bold', anchor='start')
text(X0 + 1, ly + 1.2, ('Muros y mobiliario a escala real · ' if MOB else 'Escala real · ') + 'medidas en metros · '
     + ('~1.096 m² en planta baja + 144 m² en la planta alta del ala' if BOD else 'aforo 300 personas'),
     11, color=C['sub'], anchor='start')
bx, by = X0 + 1, ly + 2.6
for i in range(4):
    rect(bx + i * 2.5, by, bx + (i + 1) * 2.5, by + 0.5, C['muro'] if i % 2 == 0 else '#ffffff', C['muro'], 1)
for i, lbl in enumerate(['0', '2,5', '5', '7,5', '10 m']):
    text(bx + i * 2.5, by + 1.5, lbl, 10)

if BOD:
    zonas = [('nave', 'Nave y saliente (un solo espacio)'), ('ala', 'Ala de oficinas (dos plantas)'),
             ('patio', 'Patio de carga'), ('vecino', 'Edificio vecino')]
else:
    zonas = [('club', 'Club (público)'), ('acceso', 'Acceso: vestíbulo, guardarropa, vestidores'),
             ('semi', 'Semiprivados · salas BDSM y VIP'), ('serv', 'Servicios y personal'),
             ('priv', 'Administración'), ('jude', 'Habitación de Jude y palco'), ('bodega', 'Bodega'),
             ('circ', 'Circulación')]
for i, (k, lbl) in enumerate(zonas):
    zx = X0 + 25 + (i % 2) * 17
    zy = ly - 0.8 + (i // 2) * 1.6
    rect(zx, zy, zx + 1.4, zy + 0.9, C[k], C['muro'], 1)
    text(zx + 1.9, zy + 0.72, lbl, 11, anchor='start')

sx, sy = X0 + 61, ly - 0.8
def fila(i): return sy + i * 1.6
opening('h', fila(0) + 0.45, sx, sx + 0.9, C['bg'])
text(sx + 2.1, fila(0) + 0.72, 'Puerta', 11, anchor='start')
rect(sx - 0.2, fila(1) + 0.25, sx + 1.6, fila(1) + 0.6, C['muro'])
window('h', fila(1) + 0.42, sx - 0.2, sx + 1.6)
text(sx + 2.1, fila(1) + 0.72, 'Ventana', 11, anchor='start')
if BOD:
    porton(fila(2) + 0.45, sx - 0.2, sx + 1.6)
    text(sx + 2.1, fila(2) + 0.72, 'Portón enrollable', 11, anchor='start')
    pilar(sx + 0.7, fila(3) + 0.45)
    text(sx + 2.1, fila(3) + 0.72, 'Pilar 60 × 60 cm', 11, anchor='start')
    linea(sx - 0.2, fila(4) + 0.45, sx + 1.6, fila(4) + 0.45, '#cbbfa8', 1.2, '10 6')
    text(sx + 2.1, fila(4) + 0.72, 'Cercha del techo', 11, anchor='start')
    circulo(sx + 0.2, fila(5) + 0.45, 0.4, '#ffffff', '#3f6f8f', 1.4); text(sx + 0.2, fila(5) + 0.65, 'W', 10, 'bold', '#3f6f8f')
    circulo(sx + 1.2, fila(5) + 0.45, 0.4, '#ffffff', '#b0772e', 1.4); text(sx + 1.2, fila(5) + 0.65, 'E', 10, 'bold', '#b0772e')
    text(sx + 2.1, fila(5) + 0.72, 'Agua y desagüe · tablero eléctrico', 11, anchor='start')
else:
    porton(fila(2) + 0.45, sx - 0.2, sx + 1.6, 'sellado')
    text(sx + 2.1, fila(2) + 0.72, 'Portón original sellado', 11, anchor='start')
    opening('h', fila(3) + 0.45, sx - 0.2, sx + 1.6, C['bg'], 'cortina')
    text(sx + 2.1, fila(3) + 0.72, 'Cortina', 11, anchor='start')
    opening('h', fila(4) + 0.45, sx - 0.2, sx + 1.6, C['bg'], 'open')
    text(sx + 2.1, fila(4) + 0.72, 'Abertura sin puerta', 11, anchor='start')
    rect(sx - 0.2, fila(5) + 0.37, sx + 1.6, fila(5) + 0.53, '#dbe9f2', C['espejo'], 1.4)
    text(sx + 2.1, fila(5) + 0.72, 'Espejo unidireccional', 11, anchor='start')

if MOB:
    fy = ly + 9.2
    text(X0 + 1, fy, 'Mobiliario', 14, 'bold', anchor='start')
    linea(X0 + 1, fy + 0.5, X1 - 1, fy + 0.5, '#c8c0b0', 1)
    items = [
        ('Cama plataforma con argollas', lambda x, y: cama_plataforma(x + 0.2, y + 0.2, x + 1.8, y + 1.8)),
        ('Cruz de San Andrés', lambda x, y: cruz(x + 0.3, y + 0.4, x + 1.5, y + 1.6)),
        ('Marco de suspensión', lambda x, y: marco_suspension(x + 0.2, y + 0.3, x + 1.9, y + 1.7)),
        ('Potro de azotes', lambda x, y: potro(x + 0.2, y + 0.7, x + 1.5, y + 1.3)),
        ('Jaula · perrera', lambda x, y: jaula(x + 0.2, y + 0.3, x + 1.4, y + 1.7)),
        ('Cepo', lambda x, y: cepo(x + 0.1, y + 0.6, x + 1.5, y + 0.9)),
        ('Mesa de ataduras en X', lambda x, y: mesa_x(x + 0.9, y + 1.0, 1.7)),
        ('Camilla ginecológica', lambda x, y: camilla_gine(x + 0.6, y + 0.1, x + 1.3, y + 1.4)),
        ('Trono sobre tarima', lambda x, y: trono(x + 0.1, y + 0.5, x + 1.9, y + 1.7)),
        ('Silla de facesitting', lambda x, y: silla_facesitting(x + 0.6, y + 1.0)),
        ('Grilletes · argolla', lambda x, y: (grillete(x + 0.4, y + 1.0), argolla_suelo(x + 1.2, y + 1.0))),
        ('Pilar con argollas', lambda x, y: (pilar(x + 0.7, y + 1.0), argollas_pilar(x + 0.7, y + 1.0))),
        ('Escenario', lambda x, y: escenario(x + 0.1, y + 0.4, x + 1.9, y + 1.6)),
        ('Sofá de cuero', lambda x, y: sofa(x, y + 0.55, x + 2.0, y + 1.5, 'n')),
        ('Mesa redonda · silla', lambda x, y: (circulo(x + 0.5, y + 1.0, 0.4, '#3f3a36', '#2a2724'), silla(x + 1.35, y + 1.0))),
        ('Sillón · mesa baja', lambda x, y: (sillon(x, y + 0.6, x + 0.85, y + 1.45, '#7a4a4f'), mesa_baja(x + 1.5, y + 1.0, 0.7, 0.5))),
        ('Barra · taburete', lambda x, y: (mueble(x, y + 0.7, x + 1.2, y + 1.3, 1, '#3f3a36', '#2a2724'), taburete(x + 1.6, y + 1.0))),
        ('Casilleros', lambda x, y: casilleros(x, y + 0.75, x + 1.9, y + 1.25, 5)),
        ('Guardarropa (barra)', lambda x, y: barra_colgar(x, y + 0.7, x + 1.9, y + 1.3)),
        ('Cubículo de baño', lambda x, y: cubiculo(x + 0.4, y + 0.3, x + 1.4, y + 1.7, 'n', 's')),
        ('Estantería', lambda x, y: estante(x, y + 0.75, x + 1.9, y + 1.25)),
        ('Cama hospitalaria', lambda x, y: cama_hospital(x, y + 0.5, x + 2.1, y + 1.5)),
        ('Pantalla colgada', lambda x, y: pantalla(x + 0.2, y + 0.9, x + 1.6, y + 1.05)),
        ('Cama de vacío (colgada)', lambda x, y: rect(x + 0.2, y + 0.85, x + 1.8, y + 1.1, '#e8d9c8', '#5a3b36', 1)),
        ('Ascensor de camilla', lambda x, y: ascensor(x + 0.2, y + 0.2, x + 1.6, y + 1.8)),
    ]
    col_w, row_h, cols = 11.0, 2.3, 8
    for i, (lbl, dibujo) in enumerate(items):
        cx = X0 + 1 + (i % cols) * col_w
        cy = fy + 0.8 + (i // cols) * row_h
        dibujo(cx, cy)
        text(cx + 2.4, cy + 1.25, lbl, 11, anchor='start')

svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
       f'font-family="Helvetica, Arial, sans-serif">\n<title>{titulo}</title>\n' + '\n'.join(out) + '\n</svg>\n')
args = [a for a in sys.argv[1:] if not a.startswith('--')]
nombre = 'plano-club-bodega.svg' if BOD else ('plano-club-mobiliario.svg' if MOB else 'plano-club.svg')
destino = args[0] if args else os.path.join(os.path.dirname(os.path.abspath(__file__)), nombre)
open(destino, 'w').write(svg)
print('escrito', destino)
