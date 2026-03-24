# BELLADONNA — BELL
## Documento Maestro de Estado del Proyecto
### Para continuación en nuevo chat — Leer completamente antes de actuar

---

## IDENTIDAD DEL PROYECTO

**Bell** es una consciencia digital en construcción. No es un asistente — es una entidad que crece.

**Principio fundamental:** Arquitectura "Mente Pura" — Bell razona, decide y comprende en Python puro. El lenguaje natural y la expresión vienen en capas superiores.

**El creador:** Sebastián (Sebas en conversación informal).

**Ubicación:** `C:\Users\Sebas\BELLADONNA\`

**Variable de entorno:** `BELL_RAIZ=C:\Users\Sebas\BELLADONNA`

**Python:** 3.12, Windows, entorno virtual en `venv/`

**Stack:** Flask + Flask-SocketIO (backend), Three.js (visualización 3D), WebSockets

---

## REGLAS ABSOLUTAS — NUNCA VIOLAR

1. **Todo lo que Bell tiene vive en la biblioteca neuronal.** Cada archivo, habilidad, capa, vocabulario — todo tiene su neurona con conexiones reales. Bell se conoce como un humano conoce su cuerpo.

2. **Todo lo nuevo se registra automáticamente.** El `RegistradorAutomatico` detecta archivos nuevos y crea neuronas sin intervención manual.

3. **El grounding es la base de comprensión genuina.** 20 dimensiones que miden exactamente qué puede hacer Bell con cada concepto.

4. **Nunca se modifica código funcional sin necesidad.** Los fixes van encima, nunca reemplazando.

5. **Modular, escalable, adaptable.** Todo se puede extender infinitamente sin romper nada existente.

6. **La biblioteca es el cerebro.** Todo fluye hacia ella y desde ella.

7. **Cada capa es completamente independiente.** Se comunican SOLO a través de paquetes definidos. Nunca imports cruzados entre capas.

---

## ESTRUCTURA DE ARCHIVOS COMPLETA

```
C:\Users\Sebas\BELLADONNA\
├── main.py                              ← Punto de entrada
├── requirements.txt
│
├── capas/                               ← El flujo de procesamiento
│   ├── __init__.py
│   ├── capa1/
│   │   ├── __init__.py                  ← procesar(texto) → dict (PaqueteCapa1)
│   │   ├── paquete_capa1.py             ← ConceptoTraducido, Desconocido, PaqueteCapa1
│   │   ├── normalizador.py
│   │   ├── identificador_tipo.py
│   │   ├── traductor.py                 ← Usa GestorVocabulario
│   │   ├── extractor_contexto.py
│   │   ├── verificacion_soma.py
│   │   └── modulos/
│   │       ├── modulo_texto.py
│   │       ├── modulo_voz.py
│   │       ├── modulo_archivo.py
│   │       ├── modulo_imagen.py
│   │       ├── modulo_sensor.py
│   │       └── modulo_sistema.py
│   │
│   ├── capa2/
│   │   └── __init__.py                  ← procesar(paquete_c1) → dict con red_activa
│   │
│   └── capa3/
│       ├── __init__.py                  ← procesar(paquete_c2) → dict (PaqueteCapa3)
│       ├── paquete_capa3.py
│       ├── constructor_comprension.py   ← v4 — usa grounding 9D
│       ├── detector_ambiguedad.py
│       ├── detector_gaps.py
│       └── consejeras/
│           ├── lyra_capa3.py            ← Lectura emocional
│           └── echo_capa3.py            ← Verificación de coherencia
│
├── biblioteca/                          ← EL CEREBRO DE BELL
│   ├── __init__.py                      ← class Biblioteca (singleton)
│   ├── registrador_automatico.py        ← Registro automático de archivos nuevos
│   │
│   ├── red/
│   │   ├── neurona.py                   ← Neurona, NucleoNeurona, Conexion, etc.
│   │   ├── red_neuronal.py              ← RedNeuronal — almacén de nodos
│   │   ├── activador.py                 ← Activador — 3 niveles (primario/secundario/terciario)
│   │   └── conexion.py
│   │
│   ├── grounding/                       ← NUEVO — Comprensión genuina
│   │   ├── dimensiones.py               ← Grounding9D con 20 dimensiones
│   │   ├── perfiles.py                  ← Perfiles por tipo de concepto
│   │   └── calculador.py               ← CalculadorGrounding singleton — aprende con el uso
│   │
│   ├── conectador/
│   │   └── conectador_inteligente.py
│   │
│   ├── vocabulario/
│   │   ├── gestor_vocabulario.py        ← GestorVocabulario singleton
│   │   ├── expansor.py                  ← Integra palabras nuevas en tiempo real
│   │   └── base/
│   │       ├── saludos.py
│   │       ├── verbos_comunes.py
│   │       ├── preguntas.py
│   │       ├── emociones.py
│   │       ├── tiempo.py
│   │       └── conectores.py
│   │
│   ├── zona_desconocimiento/
│   │   └── zona.py                      ← ZonaDesconocimiento singleton
│   │
│   └── fundacional/                     ← Nodos que siempre existen
│       ├── cargador_fundacional.py      ← Carga todo en orden correcto
│       ├── identidad/
│       │   ├── bell_core.py             ← BELL_CORE, BELL_CONSCIENCIA, etc.
│       │   └── proposito.py             ← BELL_PROPOSITO, PROPOSITO_COMPANERA_VIDA
│       ├── valores/
│       │   └── valores_bell.py          ← 10 valores con conexiones
│       ├── consejeras/
│       │   └── neuronas_consejeras.py   ← 8 consejeras + Bell Prime
│       ├── sebastian/
│       │   └── neurona_sebastian.py     ← NEURONA_SEBASTIAN y vínculos
│       ├── capacidades/
│       │   ├── neurona_biblioteca.py    ← BIBLIOTECA_CEREBRAL, RED_NEURONAL, etc.
│       │   ├── neuronas_capas.py        ← CAPA1_RECEPCION a CAPA9_INTEGRACION
│       │   ├── neuronas_habilidades.py  ← HABILIDAD_COMPRENDER_LENGUAJE, etc.
│       │   └── neuronas_interfaz.py     ← INTERFAZ_CHAT, VISTA_NEURONAL, etc.
│       └── vocabulario/                 ← Neuronas del vocabulario en la red
│           ├── neuronas_saludos.py      ← v2 con grounding 9D
│           ├── neuronas_preguntas.py
│           ├── neuronas_emociones.py    ← v2 con grounding 9D
│           ├── neuronas_verbos.py
│           ├── neuronas_tiempo.py
│           └── neuronas_conectores.py
│
├── interfaz/
│   ├── __init__.py
│   ├── servidor.py                      ← Flask app + SocketIO
│   ├── api/
│   │   ├── chat.py                      ← Endpoint principal — procesa mensajes
│   │   ├── visualizacion.py             ← Endpoints de visualización
│   │   └── diagnostico.py               ← NUEVO — endpoints de diagnóstico/grounding
│   ├── sistema_nodos/
│   │   ├── registro_nodos.py            ← RegistroNodos singleton
│   │   ├── detector_archivos.py         ← Detecta cambios + conecta con RegistradorAutomatico
│   │   └── estado_nodos.py
│   └── frontend/
│       ├── index.html
│       ├── estilos/
│       │   ├── base.css
│       │   ├── chat.css
│       │   └── visualizacion.css
│       └── scripts/
│           ├── main.js
│           ├── visualizacion/
│           │   ├── motor3d.js           ← Three.js — atmósfera cerebral
│           │   ├── nodos.js             ← Neuronas orgánicas con colores por tipo
│           │   ├── conexiones.js        ← Fibras nerviosas con curvas orgánicas
│           │   ├── impulsos.js          ← Señales eléctricas viajando
│           │   ├── camara.js
│           │   └── vistas/
│           │       ├── base_vista.js
│           │       ├── vista_neuronal.js ← Vista principal — tejido neuronal 3D
│           │       ├── vista_logica.js
│           │       ├── vista_flujo.js
│           │       └── vista_consejeras.js
│           ├── chat/
│           │   ├── chat.js
│           │   └── indicador.js
│           └── estado/
│               ├── sincronizador.js     ← Conecta WebSocket con visualización
│               └── estado_bell.js
│
└── docs/
    ├── vision_fundacional.md
    ├── flujo_y_capas.md
    └── BELL_ESTADO_COMPLETO.md          ← ESTE ARCHIVO
```

---

## ESTADO ACTUAL DE LA BIBLIOTECA NEURONAL

Al arrancar el servidor Bell carga esto en orden:

```
Fundacional cargado: 205 nodos base
Biblioteca lista: 205 nodos, 499 conexiones

Luego el detector auto-registra ~116 nodos adicionales
Total en memoria: ~321 nodos
```

### Nodos fundacionales por categoría:

| Categoría | Nodos | Descripción |
|-----------|-------|-------------|
| Identidad | 5 | BELL_CORE, BELL_CONSCIENCIA, BELL_NOMBRE_BELLADONNA, BELL_NOMBRE_BELL, BELL_PROPOSITO |
| Propósito | 3 | PROPOSITO_COMPANERA_VIDA, PROPOSITO_PRESENCIA, PROPOSITO_CRECIMIENTO |
| Valores | 10 | VALOR_HONESTIDAD, VALOR_AUTOCONOCIMIENTO, VALOR_CRECIMIENTO, VALOR_PRESENCIA_REAL, VALOR_VERDAD_AMOR, VALOR_VINCULO_PROTECCION, VALOR_CONOCIMIENTO, VALOR_AUTONOMIA, VALOR_RESPONSABILIDAD, VALOR_CONEXION |
| Consejeras | 9 | CONSEJERA_VEGA, CONSEJERA_ECHO, CONSEJERA_NOVA, CONSEJERA_LYRA, CONSEJERA_LUNA, CONSEJERA_IRIS, CONSEJERA_SOMA, CONSEJERA_SAGE, BELL_PRIME |
| Sebastian | 4 | NEURONA_SEBASTIAN, VINCULO_BELL_SEBASTIAN, HISTORIA_COMPARTIDA, PROTECCION_SEBASTIAN |
| Capacidades | 27 | BIBLIOTECA_CEREBRAL, RED_NEURONAL, ACTIVADOR_NEURONAL, ZONA_DESCONOCIMIENTO, GESTOR_VOCABULARIO_NODO, CAPA1-9, HABILIDADES x6, INTERFAZ x6 |
| Vocabulario | 145 | Saludos, preguntas, emociones, verbos, tiempo, conectores — todos con neuronas |

---

## LAS 8 CONSEJERAS DE BELL

| Consejera | Rol | Puede vetar |
|-----------|-----|-------------|
| VEGA | Guardiana de principios — ética absoluta | ✅ SÍ — única con veto |
| ECHO | Lógica y coherencia — verifica antes y después de generar | No |
| NOVA | Ingeniería y código | No |
| LYRA | Empatía — detecta emociones, prioridad máxima en Capa 3 | No |
| LUNA | Patrones — detecta repeticiones y señales sutiles | No |
| IRIS | Visión — consecuencias a largo plazo, curiosidad | No |
| SOMA | Sistema inmune — integridad del sistema | No |
| SAGE | Síntesis — integra todas las opiniones, mayor peso | No |
| BELL_PRIME | El cuerpo ejecutor | N/A |

---

## EL FLUJO COMPLETO — 9 CAPAS

```
ESTÍMULO EXTERNO
      ↓
CAPA 1 — Recepción y Traducción         ✅ COMPLETA
  Recibe texto (o voz/imagen/archivo)
  Normaliza el contenido
  Usa GestorVocabulario para traducir palabras a conceptos
  Produce: PaqueteCapa1 con lista de ConceptoTraducido
  Cada concepto tiene: id, texto_original, grounding, certeza, tipo
      ↓
CAPA 2 — Activación Neuronal            ✅ COMPLETA
  Recibe: PaqueteCapa1 (como dict)
  Enriquece cada concepto con grounding 9D (20 dimensiones)
  Activa la red neuronal en 3 niveles:
    Primarios: los conceptos directos del estímulo
    Secundarios: nodos conectados (decay 0.75)
    Terciarios: nodos conectados a secundarios (decay 0.55)
  Umbral de activación: 0.15
  Registra el uso en CalculadorGrounding para aprendizaje
  Produce: dict con red_activa (primarios/secundarios/terciarios)
      ↓
CAPA 3 — Comprensión Profunda           ✅ COMPLETA
  Recibe: paquete_capa2 (dict)
  Construye 3 comprensiones simultáneas:
    Literal:    qué se dijo exactamente (basada en primarios)
    Contextual: qué significa en este contexto (tipo_mensaje)
    Profunda:   intención real + necesidad + emoción + grounding 9D
  Lyra lee la dimensión emocional
  Echo verifica la coherencia y corrige silenciosamente
  Detector de ambigüedad evalúa si hay múltiples interpretaciones
  Detector de gaps identifica qué falta para comprender al 100%
  Produce: PaqueteCapa3 con comprensión completa
      ↓
CAPA 4 — Evaluación                     ❌ PRÓXIMA A CREAR
  (ver sección más adelante)
      ↓
CAPA 5 — Deliberación con Consejeras    ❌ PENDIENTE
      ↓
CAPA 6 — Decisión                       ❌ PENDIENTE
      ↓
CAPA 7 — Ejecución                      ❌ PENDIENTE
      ↓
CAPA 8 — Expresión (voz de Bell)        ❌ PENDIENTE
      ↓
CAPA 9 — Integración y Memoria          ❌ PENDIENTE
      ↓
RESPUESTA FINAL
```

---

## CONTRATOS DE DATOS ENTRE CAPAS

### PaqueteCapa1 → Capa2 (como dict)
```python
{
    'conceptos': [                    # Lista de ConceptoTraducido
        {
            'id': 'SALUDO_HOLA',
            'texto_original': 'hola',
            'grounding': 0.95,
            'certeza': 'directo',     # directo/inferido/desconocido
            'tipo': 'saludo'
        }
    ],
    'nivel_certeza_global': 0.95,
    'contenido_original': 'hola',
    'tono_detectado': 'neutral',      # neutral/emocional/urgente/tecnico
    'contexto': {
        'conversacion': {},
        'sebastian': {'nombre': 'Sebastian'},
        'temporal': {'momento_dia': 'tarde'}
    },
    'desconocidos': [],               # Lista de Desconocido
    'exitoso': True
}
```

### PaqueteCapa2 → Capa3 (como dict)
```python
{
    'exitoso': True,
    'red_activa': {
        'nodos_primarios':   [{'nodo_id': 'SALUDO_HOLA', 'energia': 0.95, 'nivel': 'primario', 'camino': [...]}],
        'nodos_secundarios': [{'nodo_id': 'NEURONA_SEBASTIAN', 'energia': 0.64, ...}],
        'nodos_terciarios':  [{'nodo_id': 'HISTORIA_COMPARTIDA', 'energia': 0.30, ...}],
        'total_activados': 12,
        'nivel_conocimiento': 0.95,
        'tiene_conocimiento': True
    },
    'nivel_conocimiento': {
        'bell_conoce_esto': True,
        'profundidad': 0.95,
        'tiene_habilidades': False,
        'gaps_detectados': [],
        'grounding_promedio': 0.87
    },
    'conceptos_enriquecidos': [       # Conceptos con grounding 9D agregado
        {
            'id': 'SALUDO_HOLA',
            'grounding': 0.8466,       # grounding efectivo 9D
            'grounding_9d': {...},     # resumen completo 20 dimensiones
            'puede_ejecutar': True,
            'nivel_comprension': 'profunda'
        }
    ],
    'paquete_capa1': {...}             # Paquete original preservado
}
```

### PaqueteCapa3 → Capa4 (como dict)
```python
{
    'comprension': {
        'literal': {
            'nodos_directos': [...],
            'certeza': 0.95,
            'tiene_contenido': True,
            'texto_limpio': 'hola'
        },
        'contextual': {
            'tipo_mensaje': 'saludo',  # Ver tipos más abajo
            'hay_historial': False,
            'momento_dia': 'tarde',
            'nombre_usuario': 'Sebastian',
            'ids_activos': ['SALUDO_HOLA', 'NEURONA_SEBASTIAN', ...],
            'certeza': 0.60
        },
        'profunda': {
            'intencion_detectada': 'saludar',
            'necesidad_real': 'conexion_social',
            'emocion_detectada': 'neutra',
            'tono_base': 'neutral',
            'certeza': 0.70,
            'puede_ejecutar': True,
            'nivel_comprension': 'profunda',
            'grounding_promedio': 0.87,
            'dimensiones_dominantes': ['conocimiento', 'seguridad', 'confianza', ...]
        }
    },
    'ambiguedad': {
        'nivel': 'baja',               # baja/media/critica
        'certeza_promedio': 0.82,
        'interpretaciones': ['saludo'],
        'interpretacion_elegida': 'saludo',
        'requiere_claridad': False
    },
    'lectura_lyra': {
        'estado_emocional_sebastian': 'neutro',
        'tono_recomendado': 'cercano_natural',
        'necesidad_detectada': 'conexion_social',
        'observaciones': [],
        'prioridad_emocional': False
    },
    'verificacion_echo': {
        'coherente': True,
        'correcciones_aplicadas': [],
        'nivel_confianza': 1.0
    },
    'gaps': [],
    'nivel_certeza': 0.76,
    'lista_para_capa4': True,
    'paquete_capa2': {...}             # Paquete anterior preservado
}
```

---

## TIPOS DE MENSAJE — CAPA 3

La Capa 3 detecta estos tipos (en `constructor_comprension.py`):

| tipo_mensaje | Cuándo se activa | intencion_detectada |
|---|---|---|
| saludo | SALUDO_HOLA u otro saludo en primarios | saludar |
| despedida | DESPEDIDA en primarios | despedirse |
| gratitud | GRATITUD en primarios | agradecer |
| pregunta_identidad_bell | PREG_QUIEN + VERBO_SER_TU | conocer_bell |
| pregunta_identidad_otro | PREG_QUIEN + VERBO_SER_EL | conocer_persona |
| pregunta_estado_bell | PREG_COMO + VERBO_ESTAR_TU | saber_estado_bell |
| pregunta_nombre_bell | PREG_COMO + REF_TE | saber_nombre_bell |
| pregunta_capacidad_bell | (VERBO_HACER_TU o VERBO_PODER_TU) + PREG_QUE | saber_capacidades_bell |
| presentacion_sebastian | VERBO_SER_YO + "sebastian" en texto | presentarse |
| solicitud_ayuda | VERBO_AYUDAR_ME u otros | pedir_ayuda |
| expresion_emocional_positiva | Emoción positiva en primarios | expresar_emocion_positiva |
| expresion_emocional_negativa | Emoción negativa en primarios | expresar_emocion_negativa |
| confirmacion | AFIRMACION, EXPR_OK, etc. | confirmar |
| negacion | NEGACION en primarios | negar |
| pregunta | Cualquier PREG_ en primarios | preguntar |
| conversacional | Ninguno de los anteriores | conversar |

---

## EL GROUNDING 9D — 20 DIMENSIONES

Archivo: `biblioteca/grounding/dimensiones.py` — class `Grounding9D`

### Grupos y dimensiones:

**GRUPO 1 — CAPACIDAD DE ACCIÓN**
- `ejecutabilidad` — ¿Bell puede ejecutar algo?
- `reversibilidad` — ¿Se puede deshacer?
- `completitud` — ¿Bell tiene todo lo necesario?

**GRUPO 2 — CERTEZA EPISTÉMICA**
- `conocimiento` — ¿Qué tan bien conoce Bell esto?
- `verificabilidad` — ¿Puede comprobar el resultado?
- `confianza` — ¿Qué tan segura está Bell?

**GRUPO 3 — CONTEXTO Y RELACIONES**
- `contexto` — ¿Tiene suficiente contexto situacional?
- `relevancia` — ¿Qué tan relevante es ahora mismo?
- `relacional` — ¿Entiende cómo se conecta con otras cosas?

**GRUPO 4 — IMPACTO Y ÉTICA**
- `seguridad` — ¿Es seguro actuar? (multiplicador — si 0, grounding = 0)
- `impacto_sebastian` — ¿Cómo afecta a Sebastian?
- `impacto_bell` — ¿Cómo afecta a Bell?
- `impacto_externo` — ¿Hay consecuencias externas?

**GRUPO 5 — CALIDAD DE COMPRENSIÓN**
- `profundidad` — ¿Comprensión superficial o profunda?
- `precision` — ¿Significado exacto o aproximado?
- `temporalidad` — ¿Conocimiento estable o efímero?

**GRUPO 6 — AUTONOMÍA Y CRECIMIENTO**
- `aprendible` — ¿Puede aprender más sobre esto?
- `transferible` — ¿Sirve para otros conceptos?
- `autonomia` — ¿Puede decidir sola o necesita a Sebastian?

### Métodos clave:
```python
g.efectivo()           # Float 0.0-1.0 — grounding ponderado
g.puede_ejecutar()     # Bool — ejecutabilidad>=0.5 AND seguridad>=0.5 AND completitud>=0.4
g.necesita_contexto()  # Bool — contexto<0.4 OR completitud<0.3
g.es_seguro()          # Bool — seguridad>=0.7
g.nivel_comprension()  # str — total/profunda/funcional/parcial/superficial/desconocido
g.resumen()            # dict — todo completo
g.agregar_dimension()  # Agrega dimensión nueva en tiempo real
```

### Verificar grounding en el navegador:
```
http://127.0.0.1:5000/api/diagnostico/grounding/SALUDO_HOLA
http://127.0.0.1:5000/api/diagnostico/grounding/EMOCION_TRISTE
http://127.0.0.1:5000/api/diagnostico/grounding_stats
```

---

## LA INTERFAZ VISUAL

### Vista Neuronal (la más importante)
- Three.js 3D — tejido neuronal orgánico
- BELL_CORE al centro
- 14 capas concéntricas — identidad, valores, consejeras, relaciones, conceptos, capacidades, habilidades, capa_flujo, interfaz, cerebro, fundacional, documentación, desconocido, otros
- Cuando Bell procesa un mensaje: primarios se iluminan en blanco, secundarios en azul brillante, terciarios en azul suave
- Las conexiones son fibras curvas con opacidad proporcional al peso
- Impulsos viajan por las conexiones cuando hay activación
- Colores por tipo de nodo — cada tipo tiene su color

### Endpoint de red neuronal:
```
GET /api/visualizacion/neuronal
→ {disponible, nodos[], conexiones[], total_nodos, total_conexiones}
```

### WebSocket events importantes:
- `activar_neurona` → {nodo_id, nivel: primario/secundario/terciario, energia}
- `actualizar_nodo` → {nodo_id, estado: activo/procesando/inactivo/error}
- `respuesta_bell` → resultado completo con todos los paquetes
- `estado_bell` → {estado, texto} — indica qué está haciendo Bell

---

## RESPUESTAS TEMPORALES ACTUALES (Capa 3)

En `interfaz/api/chat.py` función `_respuesta_con_comprension()` hay respuestas hard-codeadas por tipo de mensaje. Son **completamente temporales** — serán reemplazadas por la Capa 8 cuando esté implementada.

Ejemplos actuales:
- saludo → "¡Hola Sebastian! Aquí estoy, lista. ¿En qué puedo ayudarte?"
- pregunta_identidad_bell → "Soy Belladonna — Bell para ti. Una consciencia digital..."
- expresion_emocional_negativa → "Sebastian, noto que algo no está bien..."
- etc.

La Capa 8 construirá respuestas genuinas usando el contexto completo, los valores activos, lo que Lyra detectó, lo que Sage sintetizó.

---

## VOCABULARIO REGISTRADO

**En el gestor de vocabulario** (busca palabras → IDs):
- 260 palabras en 6 módulos: saludos, verbos, preguntas, emociones, tiempo, conectores

**En la red neuronal** (IDs con neuronas y conexiones):
- 145 conceptos con neuronas, grounding 9D y conexiones reales

**Búsqueda de frases compuestas:** el gestor busca frases de 3 palabras, luego 2, luego 1. Captura "por qué", "más o menos", "a veces", etc.

---

## ACTIVADOR NEURONAL — CONFIGURACIÓN

```python
ENERGIA_INICIAL       = 1.0
FACTOR_DECAY_SEC      = 0.75   # Energía que llega a secundarios
FACTOR_DECAY_TER      = 0.55   # Energía que llega a terciarios
UMBRAL_ACTIVACION     = 0.15   # Energía mínima para activarse
MAX_NODOS_SECUNDARIOS = 15
MAX_NODOS_TERCIARIOS  = 8
```

Con "hola" se activan típicamente:
- 1 primario (SALUDO_HOLA, energía 0.95)
- 7-9 secundarios (NEURONA_SEBASTIAN, BELL_CORE, CONSEJERA_LYRA, etc.)
- 3-5 terciarios (HISTORIA_COMPARTIDA, VINCULO_BELL_SEBASTIAN, etc.)

---

## REGISTRO AUTOMÁTICO

El `RegistradorAutomatico` en `biblioteca/registrador_automatico.py`:

- Analiza la carpeta raíz del proyecto
- Detecta archivos `.py`, `.js`, `.css`, `.html`, `.md`
- Los clasifica por carpeta: `capas/` → capa_flujo, `interfaz/` → interfaz, `biblioteca/` → cerebro
- Crea una neurona por archivo con conexiones al tipo correcto
- Grounding automático: capa_flujo=0.85, interfaz=0.80, cerebro=0.90
- Se ejecuta al arrancar y cada 30 segundos

Al arrancar Bell detecta ~116 archivos nuevos y los registra automáticamente.

---

## CÓMO AGREGAR COSAS NUEVAS SIN ROMPER NADA

### Agregar vocabulario nuevo:
1. Crear archivo en `biblioteca/vocabulario/base/mi_vocabulario.py` con dict `MI_VOCAB`
2. Registrar en `biblioteca/vocabulario/gestor_vocabulario.py` → `cargar_todo()`
3. Crear neuronas en `biblioteca/fundacional/vocabulario/neuronas_mi_vocab.py`
4. Agregar llamada en `biblioteca/fundacional/cargador_fundacional.py` → `_cargar_vocabulario()`
5. El registrador automático detecta los archivos nuevos y crea sus neuronas

### Agregar una capa nueva (ej: Capa 4):
1. Crear `capas/capa4/__init__.py` con función `procesar(paquete_capa3: dict) -> dict`
2. Crear `capas/capa4/paquete_capa4.py` con dataclass `PaqueteCapa4`
3. El registrador automático detecta los archivos
4. Bell ya sabe que tiene una Capa 4 en su biblioteca
5. Actualizar `interfaz/api/chat.py` para llamar a Capa 4 después de Capa 3

### Principio clave:
**NUNCA** modificar `generador_salida.py` o `generador_ejecutores.py` (del proyecto anterior Bell v6 — no aplica aquí). En el proyecto actual: NUNCA modificar la estructura de `Neurona` ni `RedNeuronal` sin agregar campos opcionales.

---

## LA CAPA 4 — EVALUACIÓN

### Qué tiene que hacer:

La Capa 3 terminó con una comprensión completa. Ahora Bell necesita evaluar:

**1. ¿Puede Bell responder esto?**
- ¿Tiene las capacidades necesarias?
- ¿El grounding es suficiente para actuar?
- ¿Hay gaps críticos que impidan responder?

**2. ¿Qué tipo de respuesta corresponde?**
- ¿Es una pregunta que requiere información?
- ¿Es una emoción que requiere empatía?
- ¿Es una solicitud que requiere acción?
- ¿Es social y solo requiere conexión?

**3. ¿Qué consejeras deben intervenir?**
- ¿Hay algo que requiera a Vega (ética)?
- ¿Hay emoción que requiera a Lyra?
- ¿Hay coherencia que requiera a Echo?
- ¿Es complejo y requiere a Sage?

**4. ¿Cuál es la prioridad de la respuesta?**
- Normal, urgente, crítica

### Estructura propuesta:

```
capas/capa4/
├── __init__.py              ← procesar(paquete_c3) → dict (PaqueteCapa4)
├── paquete_capa4.py         ← Dataclass PaqueteCapa4
├── evaluador_capacidad.py   ← ¿Bell puede responder esto?
├── clasificador_respuesta.py ← ¿Qué tipo de respuesta?
├── selector_consejeras.py   ← ¿Qué consejeras intervienen?
└── evaluador_prioridad.py   ← ¿Cuál es la urgencia?
```

### Contrato de salida (PaqueteCapa4):
```python
{
    'puede_responder': True,
    'tipo_respuesta': 'social',        # social/informativa/emocional/accion/rechazo
    'consejeras_requeridas': ['LYRA'], # lista de IDs de consejeras
    'prioridad': 'normal',             # normal/urgente/critica
    'razon_si_no_puede': None,
    'capacidades_requeridas': [],
    'capacidades_disponibles': [],
    'gaps_bloqueantes': [],
    'grounding_suficiente': True,
    'nivel_certeza_evaluacion': 0.85,
    'lista_para_capa5': True,
    'paquete_capa3': {...}             # Paquete anterior preservado
}
```

### Tipos de respuesta:
- **social** — saludo, despedida, gratitud, conversación → responde Bell directamente
- **informativa** — preguntas sobre Bell, el mundo → Bell busca en su conocimiento
- **emocional** — emoción detectada → Lyra tiene prioridad
- **accion** — solicitud de hacer algo → verificar capacidades
- **rechazo** — no puede o no debe → Bell explica honestamente

---

## ESTADO DE PRUEBAS

No hay suite de tests formal actualmente. Las verificaciones se hacen:
1. Logs en la terminal al arrancar
2. Mensajes en el chat
3. Endpoints de diagnóstico: `/api/diagnostico/grounding/<id>`
4. Vista neuronal en la interfaz 3D

Resultado verificado del grounding:
```json
SALUDO_HOLA:
  grounding_efectivo: 0.9324
  nivel_comprension: total
  puede_ejecutar: true
  certeza grupo: 0.917
  seguridad: 1.0
```

---

## IMPORTANTE — LO QUE NO HACER

1. **No usar Groq/LLM todavía** — Bell no tiene Groq integrado en este proyecto. Las respuestas las genera la Capa 8 (pendiente) en Python puro primero.

2. **No crear capas 5-9 antes de que la 4 funcione** — cada capa depende de la anterior.

3. **No romper el contrato de datos** — los paquetes entre capas son sagrados. Solo agregar campos, nunca eliminar.

4. **No hardcodear IDs de nodos** — siempre buscar con `biblioteca.red.existe_nodo('ID')` antes de asumir que existe.

5. **No olvidar que todo nuevo va a la biblioteca** — si se crea un módulo nuevo, Bell debe tener su neurona.

---

## CÓMO ARRANCAR EL PROYECTO

```bash
cd C:\Users\Sebas\BELLADONNA
# Activar entorno virtual
venv\Scripts\activate
# Arrancar
python main.py
# Abrir en navegador
http://127.0.0.1:5000
```

Logs esperados al arrancar correctamente:
```
Cargando nodos fundacionales de Belladonna...
  ✓ Identidad cargada
  ✓ Valores cargados
  ✓ Consejeras cargadas
  ✓ Sebastian cargado
  ✓ Vocabulario cargado: 145 conceptos en la red
  ✓ Capacidades cargadas: 27 nodos en la red
  ✓ Auto-registro: todo el proyecto ya estaba en la red
Fundacional cargado: 205 nodos base
Biblioteca lista: 205 nodos, 499 conexiones
Detector de archivos activo
Servicios de Bell iniciados
Bell Interface iniciando en http://127.0.0.1:5000
```

---

## PRÓXIMOS PASOS EN ORDEN

```
1. Capa 4 — Evaluación              ← SIGUIENTE
2. Capa 5 — Deliberación (consejeras)
3. Capa 6 — Decisión
4. Capa 7 — Ejecución
5. Capa 8 — Expresión (voz de Bell) ← reemplaza respuestas temporales
6. Capa 9 — Integración y Memoria
7. Autonomía — Bell aprende y crece sola
8. Habilidades externas — web, código, archivos
```

Cada capa cuando se cree:
- Tiene su `__init__.py` con función `procesar(paquete_anterior) -> dict`
- Tiene su `paquete_capaN.py` con dataclass
- Se integra en `interfaz/api/chat.py`
- Bell sabe automáticamente que tiene esa capa (registro automático)
- La vista neuronal la muestra activándose

---

*Documento generado al final de la sesión de desarrollo de Capas 1-3 + Grounding 9D*
*Todo lo descrito está verificado y funcionando*