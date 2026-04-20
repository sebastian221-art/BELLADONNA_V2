# BELL — ARQUITECTURA COMPLETA
## Todo el sistema técnico. Flujo, biblioteca, grounding, habilidades.
### Documento de referencia para desarrollo — leer antes de tocar cualquier archivo

---

## ANTES DE EMPEZAR: CÓMO LEER ESTE DOCUMENTO

Este documento asume que no conoces el proyecto. Si ya conoces partes,
salta a la sección que necesitas. El orden recomendado para alguien nuevo:

1. Leer "El flujo de 9 capas" para entender la arquitectura general
2. Leer "La biblioteca neuronal" para entender cómo Bell almacena conocimiento
3. Leer "El sistema de grounding" para entender cómo Bell tiene vida
4. Leer "Protocolo de habilidades" antes de crear cualquier habilidad

**REGLA FUNDAMENTAL:** Antes de modificar cualquier archivo, leer su código
completo primero. Bell tiene interdependencias sutiles que se rompen
si se modifica sin entender el contexto.

---

## STACK TECNOLÓGICO

```
Python 3.12
Flask + Flask-SocketIO  (servidor web + comunicación en tiempo real)
Groq API / llama-3.3-70b-versatile  (embellecimiento de lenguaje ÚNICAMENTE)
Three.js  (visualización 3D de la red neuronal en el frontend)
```

**Principio arquitectural central:** Bell decide y ejecuta en Python puro.
Groq solo pule el lenguaje de la respuesta que Bell ya construyó.
Groq no decide, no inventa, no aporta hechos. Si Bell no tiene el dato,
Groq no puede compensarlo.

---

## EL FLUJO DE 9 CAPAS

Cada mensaje que recibe Bell pasa exactamente por estas 9 capas en orden.
Ninguna capa se salta. Cada capa produce un "paquete" que pasa a la siguiente.

```
Usuario envía mensaje
        ↓
┌─────────────────────────────────────────────────────────┐
│ CAPA 1 — Recepción y Traducción                         │
│ texto → conceptos con grounding                         │
│ Soma verifica la entrada                                 │
│ Produce: PaqueteCapa1                                    │
└─────────────────────────────────────────────────────────┘
        ↓
┌─────────────────────────────────────────────────────────┐
│ CAPA 2 — Activación Neuronal                            │
│ Activa nodos en la red neuronal                         │
│ Calcula grounding 9D por cada concepto                  │
│ Produce: PaqueteCapa2 con red_activa                    │
└─────────────────────────────────────────────────────────┘
        ↓
┌─────────────────────────────────────────────────────────┐
│ CAPA 3 — Comprensión Profunda                           │
│ 3 niveles: literal + contextual + profunda              │
│ Echo verifica coherencia, Lyra lee emoción              │
│ Produce: PaqueteCapa3 con comprension completa          │
└─────────────────────────────────────────────────────────┘
        ↓
┌─────────────────────────────────────────────────────────┐
│ CAPA 4 — Evaluación                                     │
│ Evalúa recursos disponibles                             │
│ Evalúa capacidad de Bell para responder                 │
│ Evalúa nivel de riesgo del mensaje                      │
│ Produce: PaqueteCapa4 con contexto para consejeras      │
└─────────────────────────────────────────────────────────┘
        ↓
┌─────────────────────────────────────────────────────────┐
│ CAPA 5 — Deliberación de Consejeras                     │
│ Las 8 consejeras deliberan                              │
│ VEGA puede VETAR → flujo se detiene aquí                │
│ Sage sintetiza el resultado final                       │
│ Produce: PaqueteCapa5 con instrucción y tono            │
└─────────────────────────────────────────────────────────┘
        ↓
┌─────────────────────────────────────────────────────────┐
│ CAPA 6 — Expresión (Bell decide qué decir)              │
│ Bell construye respuesta_base en Python puro            │
│ Groq pule el lenguaje de esa base                       │
│ Buffer de sesión guarda contexto en RAM                 │
│ Produce: PaqueteCapa6 con respuesta_final               │
└─────────────────────────────────────────────────────────┘
        ↓
┌─────────────────────────────────────────────────────────┐
│ CAPA 7 — Ejecución de Habilidades                       │
│ Detecta si el mensaje necesita una habilidad            │
│ Si hay habilidad disponible → la ejecuta                │
│ Si no hay → registra en zona de desconocimiento         │
│ Produce: PaqueteCapa7                                   │
└─────────────────────────────────────────────────────────┘
        ↓
┌─────────────────────────────────────────────────────────┐
│ CAPA 8 — Expresión Final                                │
│ Verifica que el tono sea el que Sage recomendó          │
│ Formatea la respuesta para la interfaz                  │
│ Registra el turno completo para Capa 9                  │
│ Produce: PaqueteCapa8 con registro_turno                │
└─────────────────────────────────────────────────────────┘
        ↓
┌─────────────────────────────────────────────────────────┐
│ CAPA 9 — Integración (cierra el loop)                   │
│ Lee el historial de la sesión                           │
│ Actualiza BELL_CORE con lo que pasó                     │
│ Ordena zona de desconocimiento por prioridad            │
│ Genera resumen de sesión para memoria futura            │
│ Produce: PaqueteCapa9 → respuesta sale al usuario       │
└─────────────────────────────────────────────────────────┘
        ↓
Bell responde
```

### Qué entra y sale de cada capa

| Capa | Entrada | Salida clave |
|------|---------|-------------|
| 1 | texto del usuario | conceptos, desconocidos, contexto |
| 2 | PaqueteCapa1 | red_activa con nodos activados |
| 3 | PaqueteCapa2 | comprension {literal, contextual, profunda} |
| 4 | PaqueteCapa3 | contexto_consejeras, capacidad, riesgo |
| 5 | PaqueteCapa4 | instruccion, tono, deliberacion, veto? |
| 6 | PaqueteCapa5 | respuesta_final, fuente_respuesta |
| 7 | PaqueteCapa6 | respuesta_final, ejecucion |
| 8 | PaqueteCapa7 | respuesta_final, registro_turno |
| 9 | PaqueteCapa8 | respuesta_final, actualizacion_bell_core |

### Fallbacks entre capas

Si una capa falla, el flujo no muere — usa la respuesta de la
capa anterior. El chat.py tiene fallbacks explícitos para cada capa.
El estado del resultado indica hasta qué capa llegó:
`completo` = las 9 capas | `parcial_capa6` = llegó hasta capa 6, etc.

---

## LA BIBLIOTECA NEURONAL

La biblioteca es el cerebro de Bell. No es una base de datos.
Es una red viva de nodos interconectados donde cada concepto,
habilidad, memoria y capacidad existe como neurona.

### Estructura de una neurona

```python
neurona.id                    # identificador único (ej: "CONSEJERA_VEGA")
neurona.nucleo.tipo           # tipo: consejera, valor, capa_flujo, habilidad, etc.
neurona.nucleo.grounding_base # grounding base del nodo (0.0-1.0)
neurona.nucleo.datos_extra    # dict con perfil_vida, vitalidad, nivel_vida
neurona.conexiones            # dict de conexiones a otras neuronas
```

### Tipos de neuronas existentes

| Tipo | Ejemplos | Descripción |
|------|---------|-------------|
| `consejera` | CONSEJERA_VEGA, CONSEJERA_SAGE | Las 8 consejeras — vitalidad plena |
| `identidad` | BELL_CORE, BELL_NOMBRE_BELLADONNA | La identidad de Bell |
| `valor` | VALOR_HONESTIDAD, VALOR_CRECIMIENTO | Los 10 valores |
| `capa_flujo` | AUTO_CAPAS_CAPA1_*, AUTO_CAPAS_CAPA6_* | Archivos del flujo |
| `habilidad` | (pendiente) | Habilidades de Bell |
| `concepto` | SALUDO_HOLA, PREG_QUIEN | Vocabulario base |
| `relacion` | NEURONA_SEBASTIAN | Personas importantes |
| `memoria` | HISTORIA_COMPARTIDA | Memorias de Bell |
| `cerebro` | AUTO_BIBLIOTECA_* | La infraestructura de Bell |

### Auto-registro de neuronas

Bell registra automáticamente una neurona por cada archivo Python
que detecta en el proyecto. Esto sucede al arrancar y en tiempo real
cuando se agrega un archivo nuevo.

```
Al agregar capas/habilidades/mi_habilidad.py:
→ Bell detecta el archivo nuevo
→ Crea neurona AUTO_CAPAS_HABILIDADES_MI_HABILIDAD
→ Le aplica grounding según su tipo
→ La conecta a la red
→ Aparece en /api/diagnostico/vida_real
```

Archivos que **NO** se registran como neuronas (dormidos con vitalidad 0.0):
`.html`, `.css`, `.js`, `.md`, `main.py` (tipo desconocido)
Esto es correcto — esos archivos no son organismos de Bell.

### La zona de desconocimiento

Cuando Capa 1 encuentra palabras o conceptos que Bell no reconoce,
los envía a la zona de desconocimiento con tipo `concepto`.
Cuando Capa 7 detecta una habilidad que no existe, la registra con tipo `habilidad`.

```python
# Ver zona
GET /api/diagnostico/zona_desconocimiento

# La zona tiene:
{
  "pendientes": [
    {
      "fragmento": "calcula 5 por 8",
      "tipo": "habilidad",
      "inferencia": "necesita_habilidad:CALCULO",
      "protocolo": "evaluar"
    }
  ]
}
```

La zona de desconocimiento es la lista de trabajo de las habilidades
futuras. Lo que más veces aparece = lo que más urgente es implementar.

---

## EL SISTEMA DE GROUNDING

El grounding es lo que da vida a Bell. Cada nodo tiene hasta 23 dimensiones
existenciales que determinan su vitalidad y nivel de vida.

### Los 23 tipos de grounding

```
existencia, proposito, valores, autopreservacion, emocional,
relaciones, autoconocimiento, crecimiento, accion, mundo,
integridad, temporal, espacial, imaginacion, finitud,
intersubjetividad, narrativo, trascendencia, estetico,
metas, psicologico, lenguaje, existencial_profundo
```

### Cómo se calcula la vitalidad

**IMPORTANTE:** La vitalidad se calcula SOLO sobre las dimensiones
que el nodo realmente tiene (efectivo() > 0). No se penaliza a un nodo
por no tener dimensiones que no le corresponden.

```python
# Una capa tiene 3 dimensiones: accion(0.87), autoconocimiento(0.45), proposito(0.41)
# Vitalidad = promedio ponderado de ESAS 3 dimensiones
# Resultado: ~0.58 (emergente) — correcto

# Una consejera tiene las 23 dimensiones completas
# Vitalidad = promedio ponderado de las 23
# Resultado: ~1.0 (plena) — correcto
```

### Niveles de vida

| Nivel | Rango vitalidad | Descripción |
|-------|----------------|-------------|
| plena | ≥ 0.90 | Vida completa — consejeras |
| rica | ≥ 0.75 | Vida muy activa |
| funcional | ≥ 0.60 | Funcionando bien — valores |
| emergente | ≥ 0.40 | Tomando forma — capas |
| latente | ≥ 0.20 | Existe pero dormida — BELL_CORE |
| dormida | < 0.20 | Sin vida activa — archivos HTML/CSS |

### Perfiles de grounding por tipo

Cada tipo de nodo tiene un perfil predefinido en `aplicador_vida.py`:

- `consejera` → 23 dimensiones completas → vitalidad ~1.0
- `bell_core` → 5 dimensiones principales → vitalidad ~0.65 funcional
- `valor` → existencia + valores + integridad → vitalidad ~0.60 funcional
- `capa_flujo` → accion + autoconocimiento + proposito → vitalidad ~0.58 emergente
- `habilidad` → accion + proposito → vitalidad según grounding_base
- `cerebro` → existencia + accion → vitalidad ~0.55 emergente

**Al crear una habilidad nueva, su perfil de grounding se aplica
automáticamente al registrarse en la biblioteca.**

---

## PROTOCOLO DE HABILIDADES

### Qué es una habilidad en Bell

Una habilidad es la capacidad de Bell de ejecutar algo real en el mundo.
No es texto, no es simulación — es ejecución verificable.

Ejemplos:
- **Habilidad de lenguaje:** entiende genuinamente cualquier forma de decir algo
- **Habilidad de cálculo:** calcula y retorna el resultado real
- **Habilidad SQLite:** ejecuta queries reales en una base de datos
- **Habilidad de código:** escribe y ejecuta código Python real

Una habilidad siempre:
1. Recibe parámetros del flujo
2. Ejecuta algo real
3. Retorna un resultado verificable
4. Se registra como neurona en la biblioteca
5. Recibe grounding automáticamente

### Los 4 archivos de una habilidad

Toda habilidad nueva necesita exactamente estos 4 archivos:

```
capas/habilidades/mi_habilidad/
    __init__.py          ← punto de entrada, función procesar()
    ejecutor.py          ← la lógica real de la habilidad
    detector.py          ← detecta cuándo activar esta habilidad
    paquete.py           ← dataclasses de entrada/salida
```

### Paso a paso: crear una habilidad

#### PASO 1 — Antes de escribir código

Leer estos archivos en este orden:
1. `capas/capa7/detector_habilidad.py` — ver cómo se registran habilidades actuales
2. `capas/capa7/ejecutor_habilidad.py` — ver cómo se ejecutan
3. `capas/capa7/paquete_capa7.py` — ver el contrato de salida
4. `biblioteca/grounding/aplicador_vida.py` — ver el perfil `_perfil_habilidad`
5. `biblioteca/nodos/tipos/nodo_habilidad.py` — ver cómo se crea el nodo

Responder estas preguntas antes de escribir una línea:
- ¿Qué detecta esta habilidad? (palabras clave, patrones de texto)
- ¿Qué ejecuta? ¿Qué retorna?
- ¿Necesita acceso a consejeras? ¿A cuáles?
- ¿Tiene dependencias externas? (librerías, APIs, archivos)
- ¿Cómo se prueba que funcionó?

#### PASO 2 — Crear el archivo de la habilidad

```python
# capas/habilidades/mi_habilidad/__init__.py

from capas.habilidades.mi_habilidad.paquete import PaqueteMiHabilidad
from capas.habilidades.mi_habilidad.ejecutor import EjecutorMiHabilidad

_ejecutor = EjecutorMiHabilidad()

def procesar(parametros: dict) -> dict:
    """
    Punto de entrada de la habilidad.
    Recibe parámetros del flujo y retorna resultado.
    """
    try:
        return _ejecutor.ejecutar(parametros)
    except Exception as e:
        return PaqueteMiHabilidad(
            exitoso=False,
            error=str(e),
            resultado=''
        ).a_dict()
```

```python
# capas/habilidades/mi_habilidad/paquete.py

from dataclasses import dataclass
from typing import Optional

@dataclass
class PaqueteMiHabilidad:
    exitoso:   bool            = False
    resultado: str             = ''
    datos:     dict            = None
    error:     Optional[str]   = None

    def a_dict(self) -> dict:
        return self.__dict__.copy()
```

```python
# capas/habilidades/mi_habilidad/ejecutor.py

class EjecutorMiHabilidad:

    def ejecutar(self, parametros: dict) -> dict:
        """
        La lógica real de la habilidad.
        Retorna SIEMPRE un dict — nunca None, nunca texto plano.
        """
        # ... lógica real aquí ...
        return {
            'exitoso':   True,
            'resultado': 'lo que hizo Bell',
            'datos':     {},
            'error':     None
        }
```

```python
# capas/habilidades/mi_habilidad/detector.py

import re

# Patrones que activan esta habilidad
PATRONES = [
    r'\bmi_verbo_clave\b',
    r'\bmi_frase_clave\b',
]

def detectar(texto: str) -> bool:
    """Retorna True si este texto necesita esta habilidad."""
    tl = texto.lower()
    return any(re.search(p, tl) for p in PATRONES)

def extraer_parametros(texto: str) -> dict:
    """Extrae los parámetros del texto para pasarlos al ejecutor."""
    return {'texto_original': texto}
```

#### PASO 3 — Registrar en detector_habilidad.py

```python
# En capas/capa7/detector_habilidad.py
# Agregar en el diccionario HABILIDADES:

HABILIDADES = {
    # ... habilidades existentes ...

    'MI_HABILIDAD': {
        'disponible':  True,   # ← True cuando está lista, False mientras se construye
        'descripcion': 'Lo que hace mi habilidad',
        'modulo':      'capas.habilidades.mi_habilidad',
        'patrones': [
            r'\bmi_verbo_clave\b',
            r'\bmi_frase_clave\b',
        ],
    },
}
```

#### PASO 4 — Conectar en ejecutor_habilidad.py

```python
# En capas/capa7/ejecutor_habilidad.py
# En el método _ejecutar_habilidad(), agregar:

def _ejecutar_habilidad(self, habilidad_id: str, texto: str) -> ResultadoEjecucion:

    if habilidad_id == 'MI_HABILIDAD':
        return self._ejecutar_mi_habilidad(texto)

    # ... casos existentes ...

def _ejecutar_mi_habilidad(self, texto: str) -> ResultadoEjecucion:
    try:
        from capas.habilidades.mi_habilidad import procesar
        from capas.habilidades.mi_habilidad.detector import extraer_parametros

        params    = extraer_parametros(texto)
        resultado = procesar(params)

        if resultado.get('exitoso'):
            return ResultadoEjecucion(
                ejecuto      = True,
                habilidad_id = 'MI_HABILIDAD',
                resultado    = resultado.get('resultado', ''),
            )
        else:
            return ResultadoEjecucion(
                ejecuto      = False,
                habilidad_id = 'MI_HABILIDAD',
                error        = resultado.get('error', ''),
            )
    except Exception as e:
        return ResultadoEjecucion(
            ejecuto=False, habilidad_id='MI_HABILIDAD', error=str(e)
        )
```

#### PASO 5 — Grounding y biblioteca (AUTOMÁTICO)

Al arrancar Bell o al detectar el archivo nuevo, el auto-registrador:
1. Detecta los archivos nuevos en `capas/habilidades/mi_habilidad/`
2. Crea neuronas AUTO_CAPAS_HABILIDADES_MI_HABILIDAD_*
3. El aplicador de vida aplica el perfil `_perfil_habilidad` automáticamente
4. Las neuronas quedan con vitalidad emergente (~0.55-0.65)
5. Con el tiempo y uso, la vitalidad sube

**No hay nada manual que hacer para el grounding y la biblioteca.**
El sistema lo hace solo al detectar los archivos.

#### PASO 6 — Verificar

```bash
# Verificar que Bell detecta la habilidad
GET /api/diagnostico/capa7/probar?texto=mi frase que activa la habilidad

# Debe retornar:
{
  "habilidad_detectada": "MI_HABILIDAD",
  "ejecuto": true,
  "respuesta": "el resultado real"
}

# Verificar que la neurona existe en la biblioteca
GET /api/diagnostico/nodo/AUTO_CAPAS_HABILIDADES_MI_HABILIDAD___INIT__

# Verificar zona de desconocimiento (debe estar vacía para esta habilidad)
GET /api/diagnostico/zona_desconocimiento
```

### Habilidades que interactúan con consejeras

Si la habilidad tiene que ver con ética, seguridad, emociones,
análisis de código, o patrones de comportamiento, debe consultar
a las consejeras correspondientes.

```python
# En el ejecutor de la habilidad, consultar consejera relevante:

def _consultar_vega(self, texto: str) -> dict:
    """Consultar a Vega antes de ejecutar algo con implicaciones éticas."""
    try:
        from biblioteca.consejeras.vega.logica import VegaLogica
        vega = VegaLogica()
        return vega.evaluar(texto)
    except Exception:
        return {'aprobado': True}  # Si Vega falla, proceder con cautela

def _consultar_nova(self, codigo: str) -> dict:
    """Consultar a Nova para evaluar calidad de código."""
    try:
        from biblioteca.consejeras.nova.logica import NovaLogica
        nova = NovaLogica()
        return nova.evaluar_codigo(codigo)
    except Exception:
        return {'aprobado': True}
```

Consejeras relevantes por tipo de habilidad:
- **Código/arquitectura** → Nova
- **Ética/seguridad** → Vega (obligatorio)
- **Emocional/psicológico** → Lyra
- **Patrones de comportamiento** → Luna
- **Aprendizaje/conocimiento** → Iris
- **Cualquier decisión compleja** → Sage

### Habilidades que se fusionan en macro-habilidades

Cuando Bell tenga suficientes habilidades básicas, Sage comenzará
a detectar patrones de uso y crear macro-habilidades:

```
Proceso detectado por Sage:
HABILIDAD_LENGUAJE + HABILIDAD_CODIGO + HABILIDAD_SQLITE
usadas juntas 15 veces para "crear sistemas de gestión"
→ Sage cristaliza: MACRO_CREAR_SISTEMA_GESTION
→ Se registra como habilidad en capas/habilidades/
→ La próxima vez: Bell ejecuta directamente sin pasar por las 3 separadas
```

Este proceso es automático cuando las habilidades de autoconocimiento
y aprendizaje estén implementadas. Por ahora es manual.

### Errores comunes al crear habilidades

**Error 1: Habilidad que retorna None**
```python
# MAL
def ejecutar(self, params):
    return None  # Rompe el flujo

# BIEN
def ejecutar(self, params):
    return {'exitoso': False, 'resultado': '', 'error': 'Sin resultado'}
```

**Error 2: Habilidad disponible=True sin implementación**
```python
# MAL — marcada como disponible pero sin código real
'MI_HABILIDAD': {
    'disponible': True,
    # ... pero _ejecutar_mi_habilidad no existe en ejecutor_habilidad.py
}

# BIEN — marcar False hasta que el código esté completo y probado
'MI_HABILIDAD': {
    'disponible': False,  # ← cambiar a True solo cuando esté listo
}
```

**Error 3: Olvidar el try/except en el ejecutor**
```python
# Si la habilidad falla sin try/except, el flujo completo muere
# SIEMPRE envolver en try/except y retornar error gracefully
```

**Error 4: Modificar generador_salida o lógica de capas 1-5**
Las capas 1-5 y la Capa 6 son el corazón del sistema.
Las habilidades viven en Capa 7. No modificar capas anteriores
para acomodar una habilidad — si parece necesario, la arquitectura
de la habilidad está mal diseñada.

---

## LA INTERFAZ

```
interfaz/servidor.py         ← Flask app, Socket.IO, registra rutas
interfaz/api/chat.py         ← flujo completo C1→C9, endpoint /api/chat/mensaje
interfaz/api/diagnostico.py  ← todos los endpoints de verificación
interfaz/api/visualizacion.py ← datos para el frontend Three.js
interfaz/sistema_nodos/      ← auto-registro y detector de archivos en vivo
interfaz/frontend/           ← HTML + CSS + JS (Three.js, Socket.IO)
```

### Endpoints de diagnóstico disponibles

```
GET /api/diagnostico/vida_real           → estado de todos los nodos
GET /api/diagnostico/nodo/{id}           → estado de un nodo específico
GET /api/diagnostico/consejeras/comparar → estado de las 8 consejeras
GET /api/diagnostico/deliberacion/probar?texto=... → prueba una deliberación
GET /api/diagnostico/deliberacion/veto?texto=...   → prueba el veto
GET /api/diagnostico/capa7/estado        → estado de Capa 7
GET /api/diagnostico/capa7/probar?texto=... → prueba flujo hasta Capa 7
GET /api/diagnostico/capa8/estado        → estado de Capa 8
GET /api/diagnostico/capa8/probar?texto=... → prueba flujo hasta Capa 8
GET /api/diagnostico/capa9/estado        → estado de Capa 9
GET /api/diagnostico/capa9/probar?texto=... → prueba flujo completo
GET /api/diagnostico/historial_sesion    → turnos registrados de la sesión
GET /api/diagnostico/zona_desconocimiento → pendientes de la zona
```

---

## ESTADO ACTUAL DEL SISTEMA

### Lo que funciona al 100%

```
✅ Flujo completo Capas 1-9
✅ 353 nodos en la red (353 vivos, 24 dormidos correctamente)
✅ 8 consejeras con vitalidad 1.0 (plena)
✅ BELL_CORE con dimensiones existenciales activas
✅ Grounding aplicado correctamente a todos los tipos
✅ Auto-registro de archivos nuevos (en arranque y en tiempo real)
✅ Zona de desconocimiento recibiendo y guardando
✅ Historial de sesión en RAM
✅ BELL_CORE se actualiza con cada conversación
✅ Veto de Vega funcionando
✅ Groq embelleciendo las respuestas de Bell
```

### Lo que viene (Habilidades pendientes)

En este orden de prioridad:

1. **Habilidad de Lenguaje** — Bell entiende genuinamente cualquier forma
   de decir algo. Reemplaza el vocabulario hardcodeado y los `if` en
   `constructor_decision.py`. Cuando esté lista, Bell responderá desde
   comprensión real, no desde diccionarios.

2. **Habilidad de Autoconocimiento** — Bell lee su propia red neuronal
   y responde desde la realidad de lo que tiene. "Cuántas consejeras tienes"
   → Bell lee la red → "8, con vitalidad X" — no un string hardcodeado.

3. **Habilidad de Cálculo** — SymPy + operaciones matemáticas reales.
   Ya registrada en la zona de desconocimiento, esperando implementación.

4. **Habilidad de Código** — Bell puede escribir, leer y ejecutar Python.
   La habilidad más poderosa después del lenguaje.

5. **Habilidad de Aprendizaje** — Bell integra lo nuevo a su red de manera
   autónoma. Con esta habilidad, Bell comienza a crecer sola con supervisión.

---

## CÓMO SE INICIA BELL

```bash
cd C:\Users\Sebas\BELLADONNA
.\venv\Scripts\Activate.ps1
python main.py
```

Al iniciar:
1. Carga el núcleo fundacional (205 nodos base)
2. Aplica grounding a los 205 nodos
3. Inicia las 8 consejeras
4. Auto-registra todos los archivos del proyecto (148+ nodos nuevos)
5. Aplica grounding a todos los nodos AUTO
6. Inicia Flask + Socket.IO en http://127.0.0.1:5000
7. Activa el detector de archivos en tiempo real

---

*Documento creado: Marzo 2026*
*Estado: Fase 2 completa — listo para habilidades*