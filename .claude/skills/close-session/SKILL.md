---
name: close-session
description: Cierre completo de sesión de roleplay. Actualiza scene_log.md, state.md, characters.md y el transcript de conversación con un resumen exhaustivo de la sesión.
---

# Skill: close-session

Cierre completo de sesión de roleplay. Actualiza todos los archivos de continuidad con un resumen exhaustivo de lo ocurrido durante la sesión actual.

## Pasos a seguir

1. **Leer los archivos actuales** antes de modificar nada:
   - `world.md` (convenciones del mundo, tecnología, ubicaciones, composición de la ciudad)
   - `state.md`
   - `scene_log.md`
   - `characters.md`
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

4. **Actualizar `state.md`**:
   - Ubicación actual de cada personaje relevante
   - Estado físico actualizado (yesos, amputaciones, prótesis, vendajes)
   - Estado emocional o relacional si cambió significativamente
   - Sección "Pendiente / Próximos pasos" con los 2-4 hilos más inmediatos

5. **Actualizar `world.md`** si durante la sesión se estableció algo nuevo y permanente sobre el mundo:
   - Nueva ubicación descrita con detalle (edificio, zona, ruta dentro del área de Mark)
   - Nueva convención social, tecnológica o de infraestructura no documentada previamente
   - Decisión de Mark que cambia la configuración permanente del área o la ciudad (composición, reglas, espacios)

6. **Actualizar `characters.md`** si:
   - Apareció un personaje nuevo (añadir su ficha completa)
   - Cambió algo permanente de un personaje existente (física, relación con Mark, etc.)

7. **Guardar el transcript de la sesión**:
   - Identificar el archivo de la sesión actual: el que corresponde al día de hoy (`sesion_NN_YYYY-MM-DD.md` con la fecha actual). Si hay varios del mismo día, usar el de mayor `NN`.
   - Si no existe archivo para la sesión actual, crear `conversaciones/sesion_NN_YYYY-MM-DD.md` con `NN = max(NN existente) + 1` y la fecha de hoy.
   - Añadir al final del archivo de sesión todos los intercambios de la sesión que no estén ya guardados (un checkpoint previo puede haber escrito parte), respetando el formato existente (separadores `---`, negrita para diálogos, cursiva para descripciones).
   - Actualizar el índice `conversacion_completa.md`: añadir o actualizar la fila de la sesión en la tabla con la fecha y un resumen de una línea.

8. **Confirmar al usuario** con un resumen de una sola línea por archivo modificado, indicando qué cambió. Ejemplo:

   > `world.md` — añadida descripción del bar central de la ciudad
   > `scene_log.md` — añadidas escenas 17 y 18 (baño de Mark, yesos a Megan)
   > `state.md` — Megan ahora en el baño, yesos pendientes de aplicar
   > `characters.md` — sin cambios
   > `conversaciones/sesion_02_2026-04-30.md` — transcript completo guardado
   > `conversacion_completa.md` — sesión 02 añadida al índice

9. **Terminar el roleplay** NO continuar con el roleplay.

## Notas

- Si hay dudas sobre un detalle, omitirlo antes que inventarlo. No inventar hechos. Solo registrar lo que ocurrió en la conversación.
- Si el contexto estaba comprimido y algún detalle no es claro, indicarlo explícitamente en el archivo con una nota entre corchetes: `[detalle incierto — verificar]`
- El tono de los registros es neutro y factual, no narrativo.
- Para crear el archivo de una sesión nueva: revisar el número más alto existente en `conversaciones/` y sumar 1.
