---
name: scene-prompt
description: Genera un prompt para continuar una escena en cualquier LLM. Si hay texto seleccionado en el IDE, lo usa como escena base (modo selección). Si no, usa los últimos 20 turnos de la sesión activa (modo sesión). Construye el contexto mínimo necesario por capas.
---

# Skill: scene-prompt

Genera un prompt listo para pegar en cualquier LLM que le permita continuar una escena con precisión. El contexto se construye en capas de menor a mayor especificidad, incluyendo solo lo que el LLM receptor no puede inferir desde el texto de la escena.

## Pasos a seguir

### 1. Determinar el modo y obtener el texto de la escena

- Si hay `ide_selection` en el contexto: **modo selección** — ese texto es la escena.
- Si no hay selección: **modo sesión activa** — extraer los últimos 20 turnos de roleplay de la conversación actual, ignorando invocaciones de skills, mensajes del sistema y confirmaciones técnicas. Limpiar los mensajes de Mark: conservar el diálogo y las acciones entre paréntesis, eliminar las instrucciones entre corchetes `[...]`.

### 2. Analizar la escena

A partir del texto identificar:

- **Personajes en escena**: los que aparecen con diálogo o acción.
- **Personajes mencionados pero fuera de escena**: los que se nombran pero no están presentes activamente.
- **Localización** de la escena.

### 3. Leer los archivos de referencia

Leer `characters.md`, `state.md` y `CLAUDE.md`. No es necesario leer `world.md` completo salvo para confirmar reglas del mundo que aparezcan en la escena.

### 4. Construir el prompt por capas

Generar texto nuevo para cada capa — no copiar secciones de los archivos. Cada capa debe ser concisa.

---

**Rol y tarea** (2 líneas fijas):

> Estás narrando una historia de roleplay. Yo soy Mark, el protagonista. Tú interpretas a todos los demás personajes. Nunca interpretes a Mark ni pongas palabras en su boca.

---

**Restricciones del mundo**

Incluir únicamente las reglas del mundo que el LLM receptor podría violar por defecto al narrar esta escena. Máximo 4-5 ítems. Derivarlas de `CLAUDE.md` y `world.md` según lo que aparezca en la escena. Ejemplos de reglas que suelen ser relevantes:

- Modificaciones corporales (cambios de sexo, amputaciones, regeneraciones) son procedimientos rutinarios.
- Las mujeres con pene lo resaltan visiblemente en la ropa como norma social.
- Los robots tienen apariencia humana indistinguible.
- Año 2326, población mundial de 100.000 personas.

No incluir reglas del mundo que no sean relevantes para la escena.

---

**Personajes en escena**

Por cada personaje presente, generar un bloque con exactamente estos campos (sin añadir ni omitir):

```
[Nombre]: [apariencia física en 1-2 líneas]. [Condiciones físicas especiales, si las hay]. [Rasgo de personalidad dominante en 1 frase]. [Posición actual en la escena].
```

Extraer esta información de `characters.md` y `state.md`. No incluir backstory, motivaciones, historia con Mark, citas, ni información que no afecte directamente la narración de la escena.

---

**Instrucciones de narración derivadas**

Por cada personaje con una condición física especial (amputación, prótesis, yeso, etc.), generar automáticamente una instrucción de narración específica. Ejemplos:

- "Cuando [personaje] camina o cambia de posición, describir cómo lo hace considerando [condición]."
- "Las amputaciones de [personaje] deben estar presentes en cualquier descripción de movimiento."

Si ningún personaje tiene condiciones especiales, omitir esta capa.

---

**Personajes fuera de escena**

Por cada personaje mencionado pero ausente de la escena, una línea con su nombre, rol y ubicación actual. Omitir si no hay ninguno.

---

**Formato**

Extraer de `CLAUDE.md` solo las reglas de formato universales:

- Descripciones narrativas en cursiva.
- Diálogos en negrita con el nombre del personaje seguido de guión largo.
- Tono plano y narrativo, sin dramatismos. Los momentos eróticos se tratan con naturalidad y se describen con algo más de detalle.
- Idioma: español.

---

**Escena**

El texto de la escena tal como se obtuvo en el Paso 1.

---

**Continuación**

Una línea que indique exactamente dónde retomar: qué acaba de ocurrir y cuál es el siguiente beat narrativo pendiente. Derivar esto del final del texto de la escena.

---

### 5. Guardar y confirmar

- Escribir el prompt ensamblado en `tmp/scene_prompt.md`.
- Confirmar al usuario con una línea breve indicando el modo utilizado y la ruta del archivo.
- No continuar el roleplay. Esperar la siguiente acción del usuario.
