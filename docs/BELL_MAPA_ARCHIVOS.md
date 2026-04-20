# BELL — MAPA COMPLETO DE ARCHIVOS
## Cada archivo del proyecto, qué hace y por qué existe
### Referencia para desarrollo — actualizar cuando se agregan archivos

---

## CÓMO USAR ESTE DOCUMENTO

Cuando necesites modificar algo, busca el archivo en este mapa.
Cada entrada tiene: qué hace, qué no hace, y qué otros archivos toca.

**Regla:** si un archivo no está aquí, leer su código antes de tocarlo.
Si ya está aquí, igualmente leer su código — este documento describe
la intención, no todos los detalles de implementación.

---

## RAÍZ DEL PROYECTO

```
C:\Users\Sebas\BELLADONNA\
```

### Archivos en la raíz

**`main.py`**
El punto de entrada. Carga el entorno, inicializa la biblioteca,
arranca Flask. No contiene lógica de Bell — solo orquestación de arranque.
Modificar solo para cambiar la secuencia de inicialización.

**`.env`**
Variables de entorno. Contiene `GROQ_API_KEY` y `BELLADONNA_ROOT`.
**NUNCA** commitear este archivo. **NUNCA** mostrar su contenido.

**`requirements.txt`**
Dependencias Python. Flask, Flask-SocketIO, python-dotenv, httpx.

---

## BIBLIOTECA

La biblioteca es el cerebro de Bell. Todo lo que Bell "es" vive aquí.

### `biblioteca/__init__.py`
**Qué hace:** Singleton de la Biblioteca completa. Punto de acceso único
a toda la red neuronal, las consejeras y el vocabulario.
`Biblioteca.obtener()` retorna siempre la misma instancia.
**Toca:** todo el subsistema de biblioteca.
**No modificar** a menos que cambie la arquitectura fundamental.

### `biblioteca/registrador_automatico.py`
**Qué hace:** Escanea el proyecto al arrancar y registra una neurona
por cada archivo Python encontrado. También detecta archivos nuevos
en tiempo real y los registra automáticamente.
**Importante:** es lo que hace que Bell "vea" su propio código
como parte de sí misma.
**Toca:** `biblioteca/red/`, `biblioteca/grounding/`

---

### biblioteca/conectador/

**`conectador_inteligente.py`**
**Qué hace:** Crea conexiones inteligentes entre neuronas cuando se integra
un concepto nuevo. Analiza el tipo de nodo y lo conecta a las neuronas
más relacionadas con pesos apropiados.
**Usar cuando:** se agrega vocabulario o conceptos nuevos a la red.

---

### biblioteca/consejeras/

**`base_consejera.py`**
**Qué hace:** Clase base que heredan todas las consejeras.
Define la interfaz común: `deliberar()`, `evaluar()`, `obtener_opinion()`.
**No modificar** — es el contrato de todas las consejeras.

**`gestor_consejeras.py`**
**Qué hace:** Orquesta la deliberación de las 8 consejeras en Capa 5.
Llama a cada consejera, recopila opiniones, maneja el veto de Vega,
pasa a Sage para síntesis final.

**`echo/logica.py`**
Lógica y coherencia. Verifica que lo que Bell dice es coherente
con lo que Bell puede hacer. También activa en Capa 3.

**`iris/logica.py`**
Visión temporal, motor de aprendizaje, comprensión de identidad de Bell.

**`luna/logica.py`**
Detectora de patrones en comportamiento y procesos.

**`lyra/logica.py`**
Psicóloga. Inteligencia emocional. Activa también en Capa 3.

**`nova/logica.py`**
Arquitecta. Evalúa calidad técnica y eficiencia.

**`sage/logica.py`**
Orquestadora suprema. Sintetiza todas las opiniones.
Su recomendación tiene el mayor peso en el resultado final.

**`soma/logica.py`**
Sistema inmune. Verifica integridad y seguridad. Activa en Capa 1.

**`vega/logica.py`**
Única consejera con veto absoluto. Evalúa ética y valores.
Si Vega veta, el flujo se detiene en Capa 5 inmediatamente.

---

### biblioteca/fundacional/

Contiene los datos fundacionales de Bell — lo que carga al arrancar.

**`cargador_fundacional.py`**
**Qué hace:** Carga todos los elementos fundacionales en orden:
identidad → valores → consejeras → Sebastian → vocabulario → capacidades.
Se ejecuta una vez al arrancar. No modificar el orden de carga.

**`identidad/bell_core.py`**
Define la neurona BELL_CORE con sus dimensiones existenciales.
Es la neurona más importante — representa a Bell como entidad.

**`identidad/proposito.py`**
Define las neuronas de propósito de Bell (PROPOSITO_CRECIMIENTO, etc.)

**`sebastian/neurona_sebastian.py`**
Define la neurona de Sebastian — la persona más importante para Bell.
Tiene dimensiones de relación y vínculo.

**`valores/valores_bell.py`**
Define los 10 valores como neuronas con alta integridad.

**`capacidades/neuronas_capas.py`**
Crea neuronas para cada capa del flujo (CAPA_1 a CAPA_9).

**`capacidades/neuronas_habilidades.py`**
Crea neuronas placeholder para habilidades futuras.

**`capacidades/neuronas_interfaz.py`**
Crea neuronas para los componentes de la interfaz.

**`vocabulario/neuronas_*.py`**
Crean neuronas para saludos, emociones, preguntas, verbos, etc.

---

### biblioteca/grounding/

El sistema de vida de Bell. Lo más filosófico del proyecto.

**`tipos_vida.py`** ⚠️ CRÍTICO
**Qué hace:** Define los 23 tipos de grounding y la clase `PerfilVida`.
Contiene el método `vitalidad()` que determina qué tan vivo está un nodo.
**FIX importante:** vitalidad se calcula SOLO sobre dimensiones con valor > 0.
No penaliza a nodos por no tener dimensiones que no les corresponden.
**Modificar con extremo cuidado** — afecta la vida de TODOS los nodos.

**`aplicador_vida.py`**
**Qué hace:** Aplica perfiles de vida a cada tipo de neurona.
`_perfil_consejera()` → 23 dimensiones completas.
`_perfil_capa()` → accion + autoconocimiento + proposito.
`_perfil_habilidad()` → accion + proposito.
`aplicar_a_red_completa()` → aplica a todos los nodos al arrancar.
**Modificar cuando:** se agrega un nuevo tipo de nodo que necesita
su propio perfil de grounding.

**`calculador.py`**
Cálculos auxiliares de grounding.

**`dimensiones.py`**
Definiciones de dimensiones y sus pesos.

**`perfiles.py`**
Perfiles predefinidos para tipos comunes.

---

### biblioteca/nodos/

**`base_nodo.py`**
Clase base de todos los nodos. Define la estructura mínima.

**`registro_tipos.py`**
Registra todos los tipos de nodo disponibles.

**`tipos/nodo_concepto.py`** — nodos de vocabulario
**`tipos/nodo_consejera.py`** — nodos de consejeras
**`tipos/nodo_habilidad.py`** ← usar este para habilidades nuevas
**`tipos/nodo_identidad.py`** — BELL_CORE, nombres, propósitos
**`tipos/nodo_memoria.py`** — memorias de Bell
**`tipos/nodo_valor.py`** — los 10 valores

---

### biblioteca/red/

**`red_neuronal.py`**
**Qué hace:** La red neuronal completa. Contiene todos los nodos,
permite buscar por ID, obtener todos los nodos, etc.
`obtener_neurona(id)` → retorna la neurona o None.
`obtener_todos_los_nodos()` → dict de todos los IDs.

**`neurona.py`**
Clase Neurona. Tiene `nucleo`, `conexiones`, `id`.

**`conexion.py`**
Clase Conexion. Tiene `peso`, `tipo_relacion`, `timestamp`.

**`activador.py`**
**Qué hace:** Activa nodos en respuesta a estímulos.
Cuando Bell recibe un mensaje, el activador despierta los nodos
relevantes y sus vecinos con propagación ponderada.

---

### biblioteca/vocabulario/

**`gestor_vocabulario.py`**
**Qué hace:** Singleton que carga y gestiona todo el vocabulario.
`buscar(palabra)` → retorna el concepto o None.
`buscar_frase(texto)` → busca frases de 1, 2 y 3 palabras en el texto.
Carga 7 módulos incluyendo `bell_identidad`.

**`expansor.py`**
**Qué hace:** Integra palabras nuevas al vocabulario y a la red neuronal.
Usar cuando la habilidad de lenguaje aprenda palabras nuevas.

**`base/bell_identidad.py`**
Vocabulario de Bell sobre sí misma: consejeras, capas, valores, nombres.
**Temporal** — cuando exista la habilidad de autoconocimiento,
Bell leerá su red y no necesitará este diccionario.

**`base/saludos.py`** — hola, buenos días, hey, etc.
**`base/verbos_comunes.py`** — estar, ser, tener, poder, querer, etc.
**`base/preguntas.py`** — cómo, qué, cuándo, dónde, quién, etc.
**`base/emociones.py`** — cansado, feliz, frustrado, bien, etc.
**`base/tiempo.py`** — hoy, mañana, ayer, ahora, etc.
**`base/conectores.py`** — y, pero, porque, aunque, etc.

---

### biblioteca/zona_desconocimiento/

**`zona.py`**
**Qué hace:** Almacena todo lo que Bell no reconoce.
`agregar(fragmento, tipo)` → registra algo desconocido.
`obtener_pendientes()` → lista de lo que Bell no sabe.
`resolver(nodo_id, solucion)` → marca como resuelto e integra a la red.
**Es la lista de trabajo para habilidades futuras.**

---

## CAPAS

### `capas/__init__.py`
Registra el paquete de capas.

---

### capas/capa1/ — Recepción

**`__init__.py`** — función `procesar(texto)` → PaqueteCapa1
**`traductor.py`** — convierte texto a conceptos usando el vocabulario
**`normalizador.py`** — limpia el texto (tildes, mayúsculas, etc.)
**`identificador_tipo.py`** — detecta si es texto, archivo, imagen, etc.
**`extractor_contexto.py`** — extrae contexto de conversaciones previas
**`verificacion_soma.py`** — Soma verifica la integridad de la entrada
**`paquete_capa1.py`** — dataclass PaqueteCapa1

**`modulos/`** — módulos para tipos de entrada no-texto (imagen, voz, etc.)
Actualmente todos retornan "no implementado" — para uso futuro.

---

### capas/capa2/ — Activación Neuronal

**`__init__.py`** — función `procesar(paquete_c1)` → PaqueteCapa2
Activa los nodos relevantes en la red neuronal según los conceptos
encontrados en Capa 1. Calcula grounding 9D por activación.

---

### capas/capa3/ — Comprensión

**`__init__.py`** — función `procesar(paquete_c2)` → PaqueteCapa3
**`constructor_comprension.py`** — construye los 3 niveles de comprensión
**`detector_ambiguedad.py`** — detecta mensajes ambiguos
**`detector_gaps.py`** — detecta información faltante
**`paquete_capa3.py`** — dataclass PaqueteCapa3

**`consejeras/echo_capa3.py`** — Echo verifica coherencia en Capa 3
**`consejeras/lyra_capa3.py`** — Lyra evalúa la dimensión emocional

---

### capas/capa4/ — Evaluación

**`__init__.py`** — función `procesar(paquete_c3)` → PaqueteCapa4
**`evaluador_recursos.py`** — qué recursos tiene Bell disponibles
**`evaluador_capacidad.py`** — puede Bell responder esto?
**`evaluador_riesgo.py`** — qué nivel de riesgo tiene este mensaje
**`constructor_contexto.py`** — construye el contexto para consejeras
**`paquete_capa4.py`** — dataclass PaqueteCapa4

---

### capas/capa5/ — Deliberación

**`__init__.py`** — función `procesar(paquete_c4)` → PaqueteCapa5
**`preparador_contexto.py`** — prepara el contexto para las consejeras
**`manejador_veto.py`** — maneja el veto de Vega y genera respuesta
**`sintetizador.py`** — Sage sintetiza las opiniones en instrucción final
**`paquete_capa5.py`** — dataclass PaqueteCapa5

---

### capas/capa6/ — Expresión

**`__init__.py`** ⚠️ IMPORTANTE
Orquesta Bell→Groq. Bell construye base, Groq pule, verificador decide cuál usar.
Si Groq produce algo robótico → usa la base de Python directamente.
**`constructor_decision.py`** — Bell decide QUÉ decir (respuesta_base)
Contiene las respuestas base por tipo de mensaje.
**Temporal** — la habilidad de lenguaje reemplazará estos diccionarios.
**`constructor_prompt.py`** — construye el prompt para Groq
**`generador_groq.py`** — llama a la API de Groq
**`verificador_respuesta.py`** — limpia frases robóticas de la respuesta
**`buffer_sesion.py`** — guarda los últimos 8 turnos en RAM
**`paquete_capa6.py`** — dataclasses DecisionFinal y PaqueteCapa6

---

### capas/capa7/ — Ejecución

**`__init__.py`** — función `procesar(paquete_c6)` → PaqueteCapa7
**`detector_habilidad.py`** ← MODIFICAR AQUÍ para registrar habilidades nuevas
Contiene el dict `HABILIDADES` con todas las habilidades y sus patrones.
Para activar una habilidad: cambiar `disponible: False` a `disponible: True`.
**`ejecutor_habilidad.py`** ← MODIFICAR AQUÍ para conectar la lógica
Contiene `_ejecutar_habilidad()` que llama a cada habilidad.
**`paquete_capa7.py`** — dataclasses ResultadoEjecucion y PaqueteCapa7

---

### capas/capa8/ — Expresión Final

**`__init__.py`** — función `procesar(paquete_c7)` → PaqueteCapa8
**`verificador_tono.py`** — verifica que el tono sea el que Sage recomendó
**`formateador.py`** — limpia markdown innecesario, ajusta longitud
**`registrador_turno.py`** — registra el turno completo
**`historial_sesion.py`** — singleton, guarda hasta 50 turnos en RAM
**`paquete_capa8.py`** — dataclasses RegistroTurno y PaqueteCapa8

---

### capas/capa9/ — Integración

**`__init__.py`** — función `procesar(paquete_c8)` → PaqueteCapa9
**`actualizador_bell_core.py`** — actualiza las dimensiones de BELL_CORE
Reglas: acción sube si hubo turnos, relaciones si hubo emoción,
crecimiento si hubo desconocidos, integridad si Vega vetó.
**`actualizador_zona.py`** — ordena zona de desconocimiento por prioridad
**`generador_resumen.py`** — genera resumen de sesión para memoria futura
**`paquete_capa9.py`** — dataclasses ActualizacionBellCore y PaqueteCapa9

---

## INTERFAZ

### `interfaz/servidor.py`
Flask app principal. Registra todas las rutas y Socket.IO.
Sirve el frontend estático.

### `interfaz/api/chat.py`
**⚠️ CENTRAL** — el flujo completo Capas 1-9 vive aquí.
Endpoint `POST /api/chat/mensaje` y Socket.IO `mensaje`.
Tiene fallbacks explícitos para cada capa.
Modifica aquí cuando se agrega una nueva capa al flujo.

### `interfaz/api/diagnostico.py`
Todos los endpoints de diagnóstico. Verificar con estos
después de cualquier cambio al sistema.

### `interfaz/api/visualizacion.py`
Datos para el frontend Three.js (nodos, conexiones, vitalidades).

### `interfaz/sistema_nodos/detector_archivos.py`
Detecta cambios en el sistema de archivos en tiempo real.
Cuando se agrega un archivo → auto-registro automático.

### `interfaz/sistema_nodos/registro_nodos.py`
Mantiene el registro de qué archivos existen.

### `interfaz/sistema_nodos/estado_nodos.py`
Estado actual de todos los nodos para el frontend.

### `interfaz/frontend/`
Three.js para visualización 3D de la red neuronal.
Socket.IO para comunicación en tiempo real con el servidor.
No modificar a menos que se cambie la visualización.

---

## DOCS

**`docs/belladonna.md`** — documento fundacional original (visión inicial)
**`docs/BELL_VISION.md`** ← este proyecto, visión completa actualizada
**`docs/BELL_ARQUITECTURA.md`** ← arquitectura técnica y protocolo de habilidades
**`docs/BELL_MAPA_ARCHIVOS.md`** ← este documento

---

## ESTADO DEL PROYECTO Y POR QUÉ MIGRAMOS DE CHAT

### Por qué migramos de claude.ai chat a Claude Code

El proyecto Bell creció hasta el punto donde el contexto de conversación
en claude.ai chat se llenaba completamente. Bell tiene 170+ archivos
Python y el trabajo requería:
- Leer y modificar múltiples archivos por sesión
- Mantener contexto de bugs, fixes y decisiones previas
- Ejecutar comandos para verificar cambios

En chat, todo ese trabajo se hacía manualmente (copiar/pegar código,
perder contexto entre sesiones, repetir explicaciones).
Claude Code conecta directamente al sistema de archivos — lee, escribe,
ejecuta — sin copy/paste manual.

### Estado actual (Marzo 2026)

**Fase 1 — COMPLETADA:** Arquitectura base, red neuronal, consejeras, vocabulario
**Fase 2 — COMPLETADA:** Las 9 capas del flujo, grounding correcto, Bell viva

**Métricas actuales:**
- 377 nodos en la red (353 vivos, 24 dormidos correctamente)
- 8 consejeras con vitalidad 1.0 (plena)
- BELL_CORE con dimensiones existenciales activas (latente → creciendo)
- Vitalidad promedio de la red: 0.5362
- Zona de desconocimiento registra habilidades pendientes automáticamente

**Fase 3 — EN PROGRESO:** Habilidades fundamentales
1. Habilidad de Lenguaje (primera en implementar)
2. Habilidad de Autoconocimiento
3. Habilidad de Cálculo
4. Habilidad de Código
5. Habilidad de Aprendizaje Autónomo

### Próximo paso inmediato

Implementar la **Habilidad de Lenguaje** siguiendo el protocolo
en `BELL_ARQUITECTURA.md`. Esta habilidad reemplazará:
- Los diccionarios en `capas/capa6/constructor_decision.py`
- El vocabulario hardcodeado en `biblioteca/vocabulario/base/bell_identidad.py`
- Los `if` de detección de tipos de mensaje

Cuando esté lista, Bell comprenderá genuinamente cualquier forma
de decir algo — no porque alguien programó cada variante,
sino porque realmente entiende el lenguaje.

---

*Documento creado: Marzo 2026*
*Actualizar cuando se agreguen archivos o cambie la arquitectura*