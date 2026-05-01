---
name: checkpoint
description: Guardado rápido mid-sesión de roleplay. Actualiza scene_log.md, state.md y el transcript de conversación sin hacer un cierre completo.
---

# Skill: checkpoint

Guardado rápido mid-sesión. Registra el estado actual sin hacer un cierre completo, para proteger la continuidad ante la compresión de contexto en sesiones largas.

## Cuándo usarlo

- Al terminar una escena importante antes de seguir con la siguiente
- Cuando la sesión lleva muchos mensajes y se acerca la compresión de contexto
- En cualquier pausa natural (cambio de día narrativo, salto de escenario)

## Pasos a seguir

1. **Revisar la conversación reciente** desde el último checkpoint o desde el inicio de la sesión. Consultar `world.md` si hay dudas sobre convenciones del mundo (tecnología, normas sociales, ubicaciones, composición de la ciudad) al escribir los registros. Actualizarlo si durante los intercambios revisados se estableció algún detalle nuevo y permanente del mundo no documentado allí (nueva ubicación, nueva convención, decisión de Mark que cambie la configuración del área).

2. **Añadir entradas nuevas a `scene_log.md`**:
   - Solo las escenas ocurridas desde el último guardado
   - Formato idéntico al existente: título breve + párrafo de resumen
   - Actualizar la nota al final del archivo con el momento actual exacto y el próximo paso pendiente

3. **Actualizar solo las secciones de `state.md` que hayan cambiado**:
   - Ubicación de personajes si se movieron
   - Estado físico si cambió (nuevos yesos, prótesis quitadas, etc.)
   - No reescribir lo que no cambió

4. **Añadir el transcript reciente al archivo de sesión activo** en `conversaciones/`:
   - Identificar el archivo de la sesión actual: el que corresponde al día de hoy (`sesion_NN_YYYY-MM-DD.md` con la fecha actual). Si hay varios del mismo día, usar el de mayor `NN`.
   - Si no existe archivo para la sesión actual (es el primer guardado de una sesión nueva): crear `conversaciones/sesion_NN_YYYY-MM-DD.md` con `NN = max(NN existente) + 1` y la fecha de hoy. No actualizar `conversacion_completa.md` aquí; eso queda para `/close-session`.
   - Añadir al final del archivo los intercambios ocurridos desde el último checkpoint, respetando el formato existente (separadores `---`, negrita para diálogos, cursiva para descripciones).
   - No duplicar contenido ya guardado.

5. **`characters.md` — toque ligero**:
   - Si apareció un personaje nuevo: añadir su ficha completa, incluyendo las secciones **Voz / Tics de habla**, **Citas memorables** y **Momentos con Mark**.
   - Si hubo un cambio permanente en un personaje existente: actualizar los campos descriptivos.
   - Si en lo recién ocurrido apareció una **cita memorable** clara o un **tic de habla** nuevo y evidente, añadirlo (1 línea cada uno). Si no es evidente, dejarlo para `/close-session`.
   - **No** añadir entradas a "Momentos con Mark" en checkpoints — eso queda para el cierre, cuando ya existe la referencia a la escena en `scene_log.md`.

6. **Confirmar al usuario** con un mensaje breve de una línea:

   > Checkpoint guardado — [descripción de una frase de lo registrado]

7. **Roleplay** NO continuar con el roleplay, esperar a la siguiente interacción del usuario para retomar el roleplay.

## Notas

- Velocidad sobre completitud: es un guardado rápido, no un cierre formal.
- Si hay dudas sobre un detalle, omitirlo antes que inventarlo. No inventar hechos. Solo registrar lo que ocurrió en la conversación.
- El tono de los registros es neutro y factual, no narrativo.
- El skill `/close-session` sigue siendo necesario al terminar la sesión; este es un seguro intermedio.
