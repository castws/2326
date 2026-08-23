---
name: close-session
description: Cierre completo de sesión de roleplay. Actualiza scene_log.md, state.md, characters.md y el transcript de conversación con un resumen exhaustivo de la sesión.
---

# Skill: close-session

Cierre completo de sesión de roleplay. Actualiza todos los archivos de continuidad con un resumen exhaustivo de lo ocurrido durante la sesión actual.

## Pasos a seguir

1. **Leer los archivos actuales** antes de modificar nada:
   - `world.md` (convenciones del mundo, tecnología, moda, índice de escenarios y de reglas)
   - Las fichas `escenarios/<nombre>.md` de los lugares donde transcurrió la sesión, y `reglas/<nombre>.md` si la sesión tocó la composición de la población, las enfermedades del mundo o la app de citas
   - `state.md`
   - `scene_log.md` (ventana activa de escenas)
   - `characters.md` (índice) y las fichas `personajes/<nombre>.md` de los personajes que intervinieron en la sesión (ya estarán abiertas: intervenir exige haber abierto la ficha)
   - `conversacion_completa.md` (el índice)

2. **Revisar la conversación completa** de la sesión actual e identificar:
   - Todas las escenas que ocurrieron (en orden)
   - Cambios en la ubicación o estado físico de personajes
   - Nuevos personajes introducidos
   - Decisiones, acuerdos o promesas relevantes
   - El punto exacto donde terminó la historia

3. **Actualizar `scene_log.md`**:
   - Si la sesión continuó en un día ya iniciado, añadir las nuevas escenas bajo ese día
   - Si se inició un nuevo día narrativo, añadir una sección nueva
   - Cada escena debe tener un título breve y un párrafo de resumen con los hechos principales
   - Al final del archivo, actualizar o añadir la línea de estado final: **"La conversación termina aquí, [descripción precisa del momento]"** y **"Próximo paso pendiente: [lo que estaba a punto de ocurrir o quedó acordado]"**
   - **Consolidar la ventana (orden obligatorio, nunca invertir):** `scene_log.md` tiene dos niveles — **Nivel 1 verbatim** (el día narrativo actual, escena por escena) y **Nivel 2 condensado** (~3 días anteriores, un párrafo por medio día, sin diálogo ni detalle sensorial). Al consolidar:
     1. Todo día que salga de Nivel 1 se **copia verbatim e íntegro a `scene_log_archive.md`** en ese momento, en orden cronológico.
     2. **Solo después** se condensa a Nivel 2 la copia que se queda en `scene_log.md`.
     3. Todo día que salga de Nivel 2 se **borra** de `scene_log.md` — no se archiva nada, su verbatim ya está en el archivo desde el paso 1.
     - **Comprobación previa e innegociable:** nunca condensar un día que no esté ya copiado en el archivo. Verificarlo contando escenas antes de tocar nada; el archivo solo crece y **jamás recibe una versión resumida**.
     - Antes de mover un día, comprobar que `state.md` → "Hitos pasados" tiene su línea-resumen de ≤ 130 caracteres; si falta, añadirla. No sacar de Nivel 1 escenas a las que aún apunte un evento de "Eventos programados", un hilo de "Hilos latentes" o una entrada de "Sin cerrar".

4. **Actualizar `state.md`**:
   - **"Día actual":** ubicación de Marcie, su estado y el próximo momento a narrar.
   - **"Fichas a abrir":** los nombres exactos de quien vaya a estar en el primer beat de la próxima sesión, cada uno con su motivo en un paréntesis corto (`**Vera** (la levanta a las 8:30)`). Normalmente 0-2 nombres; **`ninguna` es un valor válido y correcto**. Es el único campo que decide qué se carga al arrancar: la ubicación de Marcie ya no decide nada. Escribirlo pensando en quién estará delante, no en quién es importante.
   - Estado físico actualizado (yesos, amputaciones, prótesis, vendajes) y estado relacional si cambió.
   - **`state.md` NO lleva bloques de personaje.** Su contenido es exactamente: `## Cronología` (Día actual · Eventos programados · Hilos latentes · Hitos pasados), `## Marcie` —única sin ficha propia— y `## Sin cerrar`. Nada más.
   - **Todo estado de personaje va al `## Estado actual` de su ficha**, esté donde esté y se cargue o no. Si alguien cambió de estado en la sesión, se edita su ficha; **nunca se crea un bloque en `state.md`**, ni siquiera para quien viva con Marcie: su ficha se abre en cuanto entra en escena, así que el bloque solo duplicaría peor lo que ya está cargado.
   - Lo único que puede tirar de un personaje hacia `state.md` es **una iniciativa suya** → va a "Hilos latentes" con su tarjeta de voz y mecánica, o **un plazo** → va a "Eventos programados".
   - **"Hitos pasados":** añadir la línea del día, **≤ 130 caracteres**.
   - **"Hilos latentes":** actualizar los disparos consumidos (poner el nuevo "Último: Día N" y recalcular el vencimiento) y añadir los hilos nuevos que hayan surgido.
   - **"Sin cerrar":** hilos abiertos que no son iniciativa de nadie y que solo mueve Marcie. Retirar los ya consumidos. No repetir aquí nada que ya esté en "Eventos programados" o "Hilos latentes".

5. **Actualizar el mundo** si durante la sesión se estableció algo nuevo y permanente. Cada tipo de cambio va a su archivo:
   - **Lugar nuevo descrito con detalle** (edificio, local, zona, casa): crear su ficha `escenarios/<nombre-kebab>.md` con el formato habitual (campos de cabecera, secciones `##`, y una sección final **`## Reglas de continuidad`**) y añadir su línea al índice de escenarios de `world.md`.
   - **Detalle nuevo de un lugar ya documentado** (una estancia, un horario, un cambio permanente del sitio): editar **su** ficha en `escenarios/`, y solo actualizar la línea del índice si cambia la descripción breve.
   - **Nueva convención social, de moda, tecnológica o regla global** no documentada previamente: editar `world.md`.
   - **Cambios en la composición de la población, en las enfermedades del mundo o en la app de citas:** editar `reglas/poblacion-y-enfermedades.md` o `reglas/app-citas.md`.
   - Decisión de Mark que cambia la configuración permanente del área o la ciudad: registrarla en el archivo que corresponda según lo anterior.

6. **Actualizar las fichas de personajes (`personajes/<nombre>.md`) y el índice (`characters.md`)**:
   - **Formato:** las fichas siguen `reglas/plantilla-personaje.md` (leerla antes de crear o reorganizar una). **Nunca se añade un bloque `## Día N` a una ficha**, ni una segunda sección con un nombre que ya existe: lo ocurrido se **fusiona** en la sección canónica que le corresponde, y el detalle escena a escena se queda en `scene_log.md`. Si al terminar una ficha tiene dos secciones con el mismo nombre, hay que unirlas.
   - **Personaje nuevo:** crear `personajes/<nombre-kebab>.md` siguiendo la plantilla — nivel A (ficha breve) para figurantes y contactos de una escena, nivel B (ficha completa) para quien vaya a tener arco. Rellenar **todos** los campos físicos obligatorios, incluidos los negativos ("Sin pene", "Sin amputaciones"). Añadir su línea al índice, en el nivel que corresponda.
   - **Personaje existente que intervino:** editar **su** archivo en `personajes/`. Si cambió algo permanente (física, relación con Mark, etc.), actualizar los campos descriptivos en `## Apariencia` o `## Relaciones`. Enriquecer las tres secciones existentes:
     - **Voz / Tics de habla:** añadir muletillas, fórmulas o tonos nuevos detectados en esta sesión que no estuvieran ya capturados.
     - **Citas memorables:** añadir 1-3 líneas verbatim de la sesión que capturen la voz del personaje, con etiqueta corta de contexto entre paréntesis. Si la sección llega a 6-7 citas, sustituir las menos representativas en lugar de acumular indefinidamente.
     - **Momentos con Marcie:** añadir el o los hitos compartidos en esta sesión, cada uno con referencia a la escena recién registrada (formato `(Día N, escena M)`).
     - **Desbordamiento a historial:** si al terminar la ficha supera **~8 KB**, mover las entradas más antiguas de `## Momentos con Marcie` y `## Citas memorables` a `personajes/<nombre>-historial.md` (creándolo si no existe), en orden cronológico y verbatim. En la ficha se quedan las que siguen siendo operativas para narrarla hoy —orientativo ≤ 1,5 KB por sección— más el puntero `> Entradas anteriores (N) en [nombre]-historial.md`. Estos archivos no se cargan nunca al inicio.
   - El criterio es destilar, no transcribir: pocas líneas, alta señal. Si nada nuevo justifica añadir, no añadir.
   - **Mantener el índice (`characters.md`):** el roster tiene **dos grupos, `## Activos` y `## Archivados`**, y ninguno decide qué se carga. Lo que hay que mantener es:
     - La **ficha mínima** de quien haya cambiado de condición —**≤ 200 caracteres**, sin actualizaciones de estado en negrita.
     - El **`Dónde`** (sub-bullet `_Dónde:_`, **≤ 80 caracteres**) de quien haya cambiado de sitio o de rutina: ubicación habitual + horario solo si no es trivial. Es un dato de estado y se desincroniza si no se toca. `characters.md` es **canónico** para la ubicación; si la ficha del personaje dice otra cosa, corregir la ficha, no el índice.
     - Lo único que se mueve de grupo es **archivar** (deja de volver a escena) o **desarchivar** (Marcie lo reincorpora). Mover es solo mover la línea; la ficha no se corta ni se pega.
   - **Pregunta obligatoria, por cada personaje activo que haya intervenido en la sesión:** contestar por escrito **¿queda algo que este personaje haga por iniciativa propia?**
     - **Sí** → entrada en `state.md` → "Hilos latentes", con disparador explícito (cadencia + último disparo, condición, o fecha) y **tarjeta de voz y mecánica** suficiente para ejecutarlo sin abrir la ficha.
     - **No** → añadir su nombre a la línea agrupada `- **Sin iniciativa pendiente:** ...` al final de "Hilos latentes". Basta el nombre; solo se añade texto si hay una **restricción negativa** que evite un error al narrar (por ejemplo, que no tenga vía de comunicación).
     - **Invariante a comprobar antes de cerrar:** todo nombre de `## Activos` aparece o en una entrada de "Hilos latentes" o en la línea `Sin iniciativa pendiente`. Quien no esté en ninguna de las dos se queda mudo por omisión — nadie contestó por él.
     - Registrar una iniciativa como si fuera estado ("X y Z lo están intentando") es exactamente el fallo que deja mudo a un personaje durante semanas.

7. **Guardar el transcript de la sesión**:
   - Identificar el archivo de la sesión actual: el que corresponde al día de hoy (`sesion_NN_YYYY-MM-DD.md` con la fecha actual). Si hay varios del mismo día, usar el de mayor `NN`.
   - Si no existe archivo para la sesión actual, crear `conversaciones/sesion_NN_YYYY-MM-DD.md` con `NN = max(NN existente) + 1` y la fecha de hoy.
   - Añadir al final del archivo de sesión todos los intercambios de la sesión que no estén ya guardados (un checkpoint previo puede haber escrito parte), respetando el formato existente (separadores `---`, negrita para diálogos, cursiva para descripciones).
   - Actualizar el índice `conversacion_completa.md`: añadir o actualizar la fila de la sesión en la tabla con la fecha y un resumen de una línea.

8. **Verificar el presupuesto de contexto** antes de cerrar. Medir los archivos que se cargan al inicio y avisar de cualquier tope superado (ver `CLAUDE.md` → "Presupuesto de contexto"):

   ```bash
   wc -c world.md characters.md state.md scene_log.md CLAUDE.md
   wc -c personajes/*.md | grep -v historial | sort -n | tail -5
   ```

   Topes: `state.md` 20 KB · `scene_log.md` 55 KB · `characters.md` 8 KB · ficha individual 8 KB (salvo arco muy activo) · **carga total de inicio 175 KB**. El bloque fijo (`world` + `characters` + `state` + `scene_log` + `CLAUDE`) son ~119 KB; encima solo suman las fichas de "Fichas a abrir". Si algo se pasa, decir cuánto y por qué; no dejarlo pasar en silencio.

9. **Confirmar al usuario** con un resumen de una sola línea por archivo modificado, indicando qué cambió. Ejemplo:

   > `escenarios/bar-central.md` — ficha nueva del bar central + línea añadida al índice de `world.md`
   > `scene_log.md` — añadidas escenas 17 y 18 (baño de Mark, yesos a Megan)
   > `state.md` — Megan ahora en el baño, yesos pendientes de aplicar
   > `characters.md` — sin cambios
   > `conversaciones/sesion_02_2026-04-30.md` — transcript completo guardado
   > `conversacion_completa.md` — sesión 02 añadida al índice

10. Proponer un mensaje corto para hacer commit en git sobre la sesión que acaba de pasar.

11. **Terminar el roleplay** NO continuar con el roleplay.

## Notas

- Si hay dudas sobre un detalle, omitirlo antes que inventarlo. No inventar hechos. Solo registrar lo que ocurrió en la conversación.
- Si el contexto estaba comprimido y algún detalle no es claro, indicarlo explícitamente en el archivo con una nota entre corchetes: `[detalle incierto — verificar]`
- El tono de los registros es neutro y factual, no narrativo.
- Para crear el archivo de una sesión nueva: revisar el número más alto existente en `conversaciones/` y sumar 1.
