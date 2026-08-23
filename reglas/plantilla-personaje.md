# Plantilla de fichas de personaje

Checklist para crear o actualizar una ficha en `personajes/<nombre>.md`.

**No se carga al inicio de sesión.** Se abre en dos momentos: cuando se crea un personaje nuevo
(incluidos los que crea Claire en vivo) y cuando se reorganiza una ficha existente al cerrar
sesión.

Dos niveles. El nivel se elige por la relevancia del personaje, no por el detalle que se le haya
descrito en una escena suelta:

- **Nivel A — ficha breve:** figurantes, contactos de una escena, personajes de fondo con nombre.
- **Nivel B — ficha completa:** quien tenga arco propio, presente o en marcha. Un personaje de
  nivel A se asciende a nivel B en el momento en que empieza a tenerlo.

El nivel de la ficha no tiene nada que ver con los grupos de `characters.md` (`Activos` /
`Archivados`), que solo dicen si el personaje puede volver a escena. Al crear una ficha, añadir
además su línea al índice: ficha mínima ≤ 200 caracteres + sub-bullet `_Dónde:_` ≤ 80 con su
ubicación habitual (y el horario si no es trivial).

---

## Regla de oro: los campos físicos no se omiten

El motivo de esta plantilla es que un dato físico que no está escrito se improvisa en escena, y
lo improvisado se contradice en la sesión siguiente. Por eso:

- **Todos los campos de `Genitales`, `Cuerpo` y `Condición física` se rellenan siempre**, también
  cuando la respuesta es negativa: "Sin pene", "Sin amputaciones ni aparatos".
- Un campo que no se sepa se **decide ahora** y se escribe. No se deja en blanco ni se pone
  "por determinar".
- Si un dato ya se narró en una escena, manda lo narrado: la ficha lo recoge, no lo cambia.

---

## Nivel A — ficha breve

Campos en negrita, sin encabezados `##`. Unas diez líneas.

```markdown
# <Nombre> _(descriptor corto entre paréntesis, si ayuda)_

**Tipo:** Robot (habitante de la ciudad / personal del Creston / de la mansión…)
**Edad aparente:** NN años
**Apariencia:** Piel, cabello (color y largo), ojos, complexión, altura aproximada. Ropa de la escena en que apareció.
**Genitales:** Vagina (forma de los labios) o pene (medidas en fláccido y erecto, cómo lo lleva en la ropa). Siempre explícito.
**Condición física:** Amputaciones, yesos, aparatos o prótesis — o "ninguna".
**Personalidad:** Dos o tres rasgos.
**Rol:** De qué conoce a Marcie y qué hace en la historia.

**Momentos con Marcie:**

- Qué pasó _(Día N, escena M)_.
```

---

## Nivel B — ficha completa

Cabecera de campos en negrita y después las diez secciones `##` **en este orden fijo**. Las
marcadas _(opcional)_ se omiten enteras si no aplican; las demás van siempre.

```markdown
# <Nombre>

**Nombre completo:** <Nombre Apellido>
**Tipo:** Robot (…)
**Edad aparente:** NN años
**Conocida:** Día N, <dónde>   ← o **Creada:** Día N, por Claire a petición de Marcie
```

### 1. `## Apariencia`

Cuatro subcampos obligatorios y uno de vestuario.

- **Rasgos:** tono de piel · color de ojos · cabello (color, largo, cómo lo lleva habitualmente) ·
  rasgos de cara · marcas visibles (pecas, tatuajes, piercings, cicatrices).
- **Cuerpo:** **altura en cm** · complexión · senos (tamaño, pezones) · caderas · cintura ·
  vello púbico.
- **Genitales:** siempre explícito, en positivo y en negativo.
  - **Con vagina:** **forma de los labios** — mayores (llenos, finos, recogidos) y menores
    (ocultos entre los mayores, asomando, prominentes, asimétricos) · color · clítoris ·
    y **"Sin pene"** escrito.
  - **Con pene:** **medidas en fláccido y en erecto**, en cm, con el formato ya usado en la
    historia — **longitud × circunferencia** (ver [Hobbs](../personajes/hobbs.md): "15 × 15;
    8,5 × 11,5 en reposo") · circuncidado o no · testículos · y **cómo lo resalta en la ropa**
    — obligatorio, es norma social del mundo (`CLAUDE.md` → "Mujeres con pene"): si va marcado
    bajo la tela, si asoma, si lleva capucha y de qué color.
  - Quien tiene los dos, o ninguno, se describe igual de explícito.
- **Condición física:** amputaciones con **nivel exacto** · yesos (articulación, posición en que
  la deja fijada, qué deja libre) · aparatos, prótesis, sondas, muletas o silla · o
  **"Ninguna"**. Para yesos de enfermedad de yoga o de mástil, seguir el checklist de
  `reglas/poblacion-y-enfermedades.md` → "Cómo describir a alguien enyesado por estas
  enfermedades"; no duplicarlo aquí.
- **Vestimenta habitual:** estilo general y prendas que suele elegir. **No la ropa de un día
  concreto:** la ropa es de escena, no de estado (`CLAUDE.md` → Consistencia temporal, regla 5).
  Si el personaje lleva algo permanente (capucha, arnés, jaula), eso sí va aquí.

### 2. `## Personalidad`

Cómo trata a la gente, qué la incomoda, qué hace cuando algo no le gusta.

### 3. `## Trabajo` _(opcional)_

Profesión, dónde y cuándo, y cómo le afecta su condición física.

### 4. `## Conocimiento`

Qué sabe y qué no sabe, en dos listas. Nadie salvo Claire conoce la tecnología real oculta
(`world.md` → "Percepción de los personajes sobre el mundo"); si el personaje es de la ciudad,
basta con dejarlo dicho en una línea.

### 5. `## Sexualidad / fetiches` _(opcional)_

Qué le atrae, qué rol adopta, qué límites tiene y a quién se lo ha contado.

### 6. `## Relaciones` _(opcional)_

Vínculos con otros personajes, cada uno enlazado a su ficha. Lo que cada parte sabe y lo que no.

### 7. `## Voz / Tics`

Muletillas, fórmulas y tono. Formulado como conducta reutilizable ("antepone el dato antes de
obedecer"), no como anécdota de una escena.

### 8. `## Citas memorables`

**Una sola sección en toda la ficha.** Lista de citas verbatim, cada una con etiqueta corta de
contexto: `_(qué estaba pasando — Día N)_`. Máximo 6-8. Al llegar al tope se **sustituyen** las
menos representativas; no se acumulan ni se abre una sección nueva por sesión.

### 9. `## Momentos con Marcie`

**Una sola sección en toda la ficha.** Lista cronológica, una línea por hito, con referencia
`(Día N, escena M)`. Hitos, no narración: el detalle escena a escena vive en `scene_log.md`.

### 10. `## Estado actual`

**Siempre la última sección.** Ubicación, estado físico vigente, hilos abiertos y disparadores
pendientes (condiciones del tipo "cuando pase X, el personaje hace Y").

---

## Regla anti-acumulación

**No se crean bloques `## Día N` en las fichas.** Una ficha describe cómo es el personaje ahora,
no el diario de lo que le pasó. Al cerrar sesión, lo ocurrido se reparte entre las secciones que
ya existen:

| Lo que ocurrió en la sesión | Dónde va |
| --- | --- |
| Una frase que capta su voz | `Citas memorables` (sustituyendo, si ya hay 8) |
| Un hito compartido con Marcie | `Momentos con Marcie` |
| Un cambio físico permanente | `Apariencia` → Condición física |
| Un vínculo nuevo o un cambio de vínculo | `Relaciones` |
| Un tic de habla nuevo | `Voz / Tics` |
| Dónde está y qué tiene pendiente | `Estado actual` |
| El detalle de qué pasó en cada escena | `scene_log.md`, no la ficha |

Si algo no encaja en ninguna sección, es señal de que pertenece a `scene_log.md` o a `state.md`.

---

## Al terminar una ficha, comprobar

1. Ninguna sección aparece dos veces.
2. No hay ningún `## Día N`.
3. `Genitales`, `Cuerpo` y `Condición física` están rellenos, incluidos los negativos.
4. `Estado actual` es la última sección y está al día.
5. La ropa descrita en `Vestimenta habitual` es un estilo, no el conjunto de un día concreto.

---

## Tope de tamaño y desbordamiento a historial

Una ficha vive para **narrar al personaje hoy**, no para acumular su historia. Las dos únicas secciones que crecen sin techo son `## Momentos con Marcie` y `## Citas memorables`.

- **Tope orientativo de la ficha: ~8 KB.** Al superarlo, mover las entradas **más antiguas** de esas dos secciones a `personajes/<nombre>-historial.md`, en orden cronológico y verbatim.
- En la ficha se quedan las que siguen siendo operativas (orientativo: **≤ 1,5 KB por sección**), más el puntero final `> Entradas anteriores (N) en [nombre]-historial.md`.
- **`-historial.md` no se carga nunca al inicio de sesión.** Se abre solo si hace falta un detalle antiguo concreto.
- Un personaje en arco muy activo puede quedar por encima de los 8 KB si lo que le sobra es contenido **operativo** (voz, mecánica, relaciones, ajustes vigentes) y no histórico. El tope que manda en ese caso es el de la carga total de inicio (`CLAUDE.md` → "Presupuesto de contexto").
