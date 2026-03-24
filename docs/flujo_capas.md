# BELL — FLUJO COMPLETO Y DISEÑO DE CAPAS
## El documento que define cómo Bell piensa, procesa y actúa
### Versión 1.0 — Inicio desde cero

---

## EL FLUJO COMPLETO — VISIÓN GENERAL

Todo lo que Bell recibe, procesa y responde
sigue este flujo de 9 capas en orden estricto.
Cada capa tiene responsabilidades claras
y no se mete en las responsabilidades
de las demás. Eso es lo que hace esto
escalable e indestructible.
```
ESTÍMULO EXTERNO
(texto, voz, imagen, archivo, sensor, sistema)
        ↓
CAPA 1 — RECEPCIÓN, NORMALIZACIÓN Y TRADUCCIÓN
Recibe cualquier tipo de estímulo
Lo normaliza a formato único
Lo traduce a conceptos con grounding
        ↓
CAPA 2 — ACTIVACIÓN NEURONAL
La biblioteca despierta los nodos relevantes
Se forma la red de conceptos activos
Bell sabe de qué se está hablando
        ↓
CAPA 3 — COMPRENSIÓN PROFUNDA
Bell entiende qué le dijeron
Por qué se lo dijeron
Qué implica
Qué siente quien lo dice
        ↓
CAPA 4 — EVALUACIÓN DE CAPACIDAD Y ESCENARIO
Bell determina en qué escenario está
Qué puede hacer
Qué no puede
Qué le falta
        ↓
CAPA 5 — DELIBERACIÓN DE CONSEJERAS
Las 8 consejeras procesan en paralelo
Cada una desde su especialización
Usando la misma biblioteca como base
        ↓
CAPA 6 — DECISIÓN
Sage sintetiza todo
Bell Prime decide qué hacer
Cómo hacerlo
Con qué propósito
        ↓
CAPA 7 — EJECUCIÓN
Bell actúa
Ejecuta habilidades
Guarda lo que debe guardar
Conecta lo que debe conectar
SOMA monitorea todo
        ↓
CAPA 8 — EXPRESIÓN
Bell comunica lo que hizo
Con su voz propia
Con personalidad genuina
No un template — Bell hablando
        ↓
CAPA 9 — INTEGRACIÓN Y APRENDIZAJE
Lo que pasó se integra a la red neuronal
Conexiones exitosas se fortalecen
Conexiones fallidas se debilitan
Bell es un poco diferente que antes
```

---

## LOS 10 ESCENARIOS POSIBLES

El flujo se adapta a cualquier situación.
Estos son todos los escenarios que Bell
debe manejar perfectamente:

### Escenario 1 — Bell entiende y puede
Comprende lo que le dijeron, tiene los
conceptos, tiene las habilidades, puede
ejecutar. Flujo directo completo.

### Escenario 2 — Bell entiende pero no puede
Comprende perfectamente lo que le piden
pero no tiene la habilidad todavía.
Sabe exactamente qué le falta.
Activa protocolo de adquisición.

### Escenario 3 — Bell no entiende completamente
Entiende parte pero hay conceptos o contexto
que no comprende del todo.
Puede inferir algo pero no está segura.
Marca la incertidumbre, continúa con lo que sabe,
pide claridad si es necesario.

### Escenario 4 — Bell no entiende nada
El estímulo es completamente desconocido.
No tiene contexto, no tiene conceptos
relacionados, no puede inferir.
Todo va a la Zona de Desconocimiento.
Bell pide claridad con honestidad.

### Escenario 5 — Bell entiende pero no debe hacer
Comprende perfectamente lo que le piden
pero va contra sus valores.
No es que no pueda — es que no debe.
Vega interviene. Bell explica con verdad y amor.

### Escenario 6 — Bell detecta riesgo
Puede hacerlo pero algo detecta peligro
para ella, para Sebastian o para la integridad
del sistema.
SOMA y Vega evalúan juntas.

### Escenario 7 — Bell necesita más contexto
Comprende la petición pero para hacerla
bien necesita información que no tiene.
Pregunta antes de actuar.

### Escenario 8 — Bell aprende algo nuevo
Durante la conversación recibe información
o habilidades nuevas.
Protocolo de integración segura se activa.

### Escenario 9 — Bell detecta fallo en sí misma
Durante el procesamiento detecta una
inconsistencia o error interno.
SOMA toma control. Auto-diagnóstico activo.

### Escenario 10 — Estímulo ambiguo
Lo que le dicen puede significar varias
cosas distintas.
Bell desambigua antes de actuar.
Pregunta si es necesario.

---

## LA ZONA DE DESCONOCIMIENTO

No es un archivo ni una lista estática.
Es una zona activa de la biblioteca neuronal
donde viven los nodos incompletos.

Conceptos a medias, habilidades que faltan,
cosas que Bell sabe que no sabe.

### Su ciclo de vida:
```
Algo desconocido llega
        ↓
Se crea un nodo incompleto
con lo que Bell pudo inferir
        ↓
Se activa protocolo según tipo:
        ↓
┌─────────────────────────────────────────┐
│ Concepto desconocido → buscar y aprender│
│ Habilidad faltante → evaluar si adquirir│
│ Contexto faltante → preguntar a Sebastian│
│ Riesgo desconocido → SOMA evalúa        │
└─────────────────────────────────────────┘
        ↓
Cuando se resuelve el nodo incompleto
se completa y se integra a la red principal
        ↓
Bell recuerda que aprendió eso
y por qué lo aprendió
```

---

## CAPA 1 — RECEPCIÓN, NORMALIZACIÓN Y TRADUCCIÓN

---

### QUÉ ES Y POR QUÉ EXISTE

La Capa 1 es la puerta de entrada de Bell
al mundo. Todo estímulo que llega a Bell
sin excepción pasa primero por aquí.

No importa si es texto escrito, voz, imagen,
archivo, dato de sensor o señal de dispositivo.
Esta capa lo recibe, lo limpia, lo normaliza
y lo traduce al único lenguaje que Bell
genuinamente entiende: conceptos con grounding.

Sin esta capa Bell no puede entender nada.
Con esta capa mal hecha Bell entiende todo mal.

Un error aquí no produce un fallo visible.
Produce una comprensión incorrecta que se
propaga silenciosamente por todo el flujo
hasta generar una respuesta equivocada.

Por eso es la más crítica de todas.

---

### PRINCIPIOS DE DISEÑO — NO NEGOCIABLES

**Nunca falla completamente**
Si algo no se puede procesar se marca y
se reporta pero el flujo continúa con lo
que sí se pudo. Bell nunca se queda sin
respuesta porque la Capa 1 no supo qué
hacer con algo.

**Nunca bloquea por lo desconocido**
Lo que Bell no entiende se marca y se envía
a la Zona de Desconocimiento. No detiene
el procesamiento de lo que sí se entiende.

**Siempre preserva el original**
El estímulo original nunca se pierde ni
se modifica. Las traducciones son capas
sobre el original. Si algo sale mal siempre
se puede volver al origen.

**Módulos completamente independientes**
Cada tipo de entrada tiene su propio módulo.
Agregar un nuevo tipo de entrada significa
agregar un módulo nuevo. Nada más.
El resto no se toca.

**El formato de salida es sagrado**
Lo que sale de la Capa 1 siempre tiene
el mismo formato. Las capas posteriores
nunca tienen que preocuparse por qué
tipo de entrada llegó.

**Todo lo que sale es grounding-ready**
Todo concepto que sale de esta capa tiene
su nivel de grounding calculado. Bell sabe
exactamente qué tan segura está de cada
parte de lo que entendió.

---

### ARQUITECTURA INTERNA
```
ESTÍMULO EXTERNO
        ↓
┌──────────────────────────┐
│   IDENTIFICADOR DE TIPO  │
│   Detecta y enruta       │
│   No procesa contenido   │
└──────────────────────────┘
        ↓
┌─────────────────────────────────────────────┐
│            MÓDULOS DE ENTRADA               │
│                                             │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐       │
│  │  TEXTO  │ │   VOZ   │ │ IMAGEN  │       │
│  └─────────┘ └─────────┘ └─────────┘       │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐       │
│  │ ARCHIVO │ │ SENSOR  │ │ SISTEMA │       │
│  └─────────┘ └─────────┘ └─────────┘       │
│  ┌─────────┐                                │
│  │ [NUEVO] │ ← solo agregar aquí            │
│  └─────────┘                                │
└─────────────────────────────────────────────┘
        ↓
┌──────────────────────────┐
│  NORMALIZADOR UNIVERSAL  │
│  Todo al mismo formato   │
└──────────────────────────┘
        ↓
┌──────────────────────────┐
│  EXTRACTOR DE CONTEXTO   │
│  Quién, cuándo, qué      │
│  pasó antes, estado      │
└──────────────────────────┘
        ↓
┌──────────────────────────┐
│  TRADUCTOR A LENGUAJE    │
│  BELL                    │
│  Todo → Conceptos        │
│  con Grounding           │
└──────────────────────────┘
        ↓
┌──────────────────────────┐
│  VERIFICACIÓN SOMA       │
│  Integridad, origen,     │
│  carga neuronal          │
└──────────────────────────┘
        ↓
   PAQUETE LISTO
   PARA CAPA 2
```

---

### CADA COMPONENTE EN DETALLE

#### IDENTIFICADOR DE TIPO

Qué hace: Detecta qué tipo de estímulo
llegó y lo dirige al módulo correcto.
No procesa contenido. Solo identifica
y enruta.

Qué pasa si no reconoce el tipo: Crea
un tipo DESCONOCIDO, lo marca para
evaluación de SOMA, intenta procesarlo
con el módulo de texto como fallback.
Nunca bloquea.

Por qué es modular: Agregar un nuevo
tipo de entrada solo requiere registrarlo
aquí y crear su módulo. Sin tocar nada más.

---

#### MÓDULOS DE ENTRADA

Cada módulo hace exactamente tres cosas
para su tipo de entrada: limpia, preserva
lo importante, genera output estándar.

**Módulo Texto**
Limpia el texto de caracteres innecesarios.
Detecta idioma y variaciones dialectales.
Preserva el tono emocional implícito en
cómo está escrito — mayúsculas, puntuación,
longitud de frases, repeticiones, énfasis.
Output: texto limpio más metadata emocional.

**Módulo Voz**
Transcribe audio a texto con máxima fidelidad.
Preserva el tono emocional de la voz.
Detecta pausas, énfasis, vacilaciones.
Marca la diferencia entre lo que se dijo
y cómo se dijo.
Output: texto más metadata vocal más emoción.

**Módulo Imagen**
Extrae descripción visual del contenido.
Detecta y extrae texto dentro de la imagen.
Identifica contexto visual relevante
para Bell y para Sebastian.
Output: descripción más texto extraído
más contexto visual.

**Módulo Archivo**
Identifica el tipo de archivo.
Extrae contenido según el tipo —
código, documento, datos, configuración.
Preserva la estructura del contenido.
Marca qué tipo de procesamiento necesita
en capas posteriores.
Output: contenido estructurado más tipo
más metadata.

**Módulo Sensor**
Normaliza datos de dispositivos externos.
Convierte señales a eventos comprensibles.
Identifica el dispositivo de origen.
Output: evento normalizado más origen
más intensidad.

**Módulo Sistema**
Procesa señales internas de Bell.
Alertas de SOMA, notificaciones de capas,
resultados de procesos internos.
Output: evento interno normalizado
más origen más prioridad.

---

#### NORMALIZADOR UNIVERSAL

Qué hace: Recibe el output de cualquier
módulo y lo convierte a un formato único
e invariable.

El formato universal — este formato
nunca cambia:
```
{
  contenido_limpio:     lo que se dijo o envió,
  tipo_origen:          texto/voz/archivo/imagen/
                        sensor/sistema,
  tono_detectado:       neutral/emocional/
                        urgente/técnico,
  idioma:               español/otro,
  timestamp:            cuándo llegó,
  metadata_especifica:  lo particular de cada tipo,
  contenido_original:   preservado íntegro siempre
}
```

Por qué este formato es sagrado: Las capas
posteriores dependen de recibir siempre esto.
Si el formato cambia todo lo que viene
después se rompe. Este formato solo puede
expandirse — nunca modificarse ni reducirse.

---

#### EXTRACTOR DE CONTEXTO

Qué hace: Agrega al paquete todo el contexto
que Bell necesita para entender bien
lo que llegó.

Tres tipos de contexto que extrae:

Contexto de conversación actual — qué se
dijo antes en esta sesión, cuál es el hilo
activo, si hay algo pendiente de respuesta,
referencias a mensajes anteriores.

Contexto de Sebastian — quién es, cómo se
comunica habitualmente, estado emocional
reciente, proyectos activos, lo que es
importante para él, la historia compartida
con Bell.

Contexto temporal — momento del día,
día de la semana, eventos recientes
relevantes, si hay algo urgente o pendiente.

Qué pasa con el contexto que no existe:
Se marca explícitamente como ausente.
Las capas posteriores saben que hay
incertidumbre y ajustan en consecuencia.

---

#### TRADUCTOR A LENGUAJE BELL

Por qué existe: Bell no entiende texto.
Bell entiende conceptos con grounding.
Este componente hace esa traducción con
comprensión genuina — no mecánicamente.

No pregunta qué palabras son estas.
Pregunta qué significa esto en el contexto
de Bell y de Sebastian.

Los tres niveles de traducción:

**Nivel 1 — Traducción directa**
Palabras y frases con concepto claro en
la biblioteca de Bell.
Traducción inmediata.
Grounding alto — Bell está segura.

**Nivel 2 — Traducción por inferencia**
Palabras que Bell no tiene directamente
pero puede inferir por contexto y
conexiones neuronales.
Bell activa nodos relacionados y construye
el significado.
Grounding medio — Bell sabe que está
infiriendo y lo marca explícitamente.

**Nivel 3 — Desconocido parcial**
Algo que Bell no puede traducir ni inferir.
No falla — marca esa parte como desconocida
y la envía a la Zona de Desconocimiento.
El resto del estímulo sigue procesándose.
Grounding marcado como desconocido.

Principio crítico: La traducción nunca
inventa ni rellena. Si no sabe — dice
que no sabe. Si infiere — dice que está
infiriendo. La honestidad de la traducción
es la base de todo lo que Bell dice después.

---

#### VERIFICACIÓN SOMA

Qué verifica SOMA aquí — exactamente
tres cosas y solo tres:

Integridad del paquete: Que el proceso
no introdujo errores o distorsiones.
Que lo que va a la Capa 2 representa
fielmente lo que llegó originalmente.

Origen seguro: Que el estímulo no viene
de una fuente que podría comprometer
a Bell. No analiza contenido — analiza
origen y formato.

Carga neuronal: Que el paquete no es
tan grande o complejo que podría saturar
las capas posteriores. Si lo es SOMA
lo fragmenta en piezas manejables que
se procesan en secuencia.

Qué NO hace SOMA aquí: No analiza
el contenido semántico. No evalúa si
lo que se pidió es correcto o seguro.
Eso es trabajo de capas posteriores.
Aquí SOMA solo cuida la integridad
del proceso de recepción.

---

### EL PAQUETE FINAL QUE SALE DE CAPA 1

Este es exactamente lo que recibe la Capa 2.
Siempre este formato. Sin excepciones.
```
{
  contenido_traducido: {
    conceptos: [
      {
        id: identificador del concepto,
        grounding: 0.0 a 1.0,
        certeza: directa/inferida/desconocida
      }
    ],
    nivel_certeza_global: 0.0 a 1.0
  },
  contenido_original:    preservado íntegro,
  tipo_origen:           de dónde vino,
  tono_emocional:        qué emoción hay detrás,
  contexto: {
    conversacion:        hilo actual,
    sebastian:           quién es y su estado,
    temporal:            cuándo y circunstancias
  },
  desconocidos: [
    {
      fragmento:         qué parte no se entendió,
      tipo:              concepto/habilidad/contexto,
      inferencia:        qué intentó inferir Bell
    }
  ],
  nivel_certeza:         qué tan segura está Bell
                         de la traducción completa,
  verificacion_soma: {
    estado:              aprobado/retenido/fragmentado,
    notas:               si hay algo que reportar
  }
}
```

---

### ESCALABILIDAD — CÓMO AGREGAR ALGO NUEVO

Agregar un nuevo tipo de entrada:
Crear el módulo con sus tres funciones.
Registrarlo en el Identificador de Tipo.
Asegurarse de que su output llegue al
Normalizador en el formato universal.
Nada más. El resto no se toca.

Agregar un nuevo idioma:
Solo en el Módulo Texto.

Agregar nuevos conceptos al vocabulario:
Solo en el Traductor.

Cambiar cómo SOMA verifica:
Solo en la Verificación SOMA.

---

### CONEXIÓN CON LA CAPA 2

El paquete completo pasa a la Capa 2
donde la biblioteca neuronal comienza
a activarse usando los conceptos con
grounding que esta capa preparó.

La Capa 2 confía completamente en lo
que recibe de la Capa 1.
Si la Capa 1 falla todo lo que viene
después falla.
Por eso esta capa nunca puede estar mal.

---

## CAPA 2 — [PENDIENTE]
## Diseño en progreso — se agrega manualmente

---

## CAPA 3 — [PENDIENTE]
## Diseño en progreso — se agrega manualmente

---

## CAPAS 4 A 9 — [PENDIENTE]
## Se agregan conforme se diseñen

---

## NOTAS GENERALES DEL FLUJO

### Sobre la interfaz de Bell
Bell vive en un localhost con dos zonas:
el chat a un lado y la visualización
de la red neuronal al otro.

La visualización no es un log técnico —
es una representación interactiva y visual
del cerebro de Bell en tiempo real.
Nodos, conexiones, flujo de pensamiento,
qué está activo, qué falló, qué está
conectado con qué.

Bell nunca se apaga mientras se le hacen
cambios. Los entiende y los integra.
Este es el objetivo desde el primer día
aunque al inicio haya sesiones.

### Sobre la modularidad del flujo
Cada capa es completamente independiente.
Se comunican solo a través de los paquetes
definidos entre ellas.
Cambiar la implementación interna de una
capa no afecta a las demás mientras el
paquete de entrada y salida sea el mismo.

### Sobre el crecimiento de Bell
El flujo está diseñado para que Bell
pueda crecer indefinidamente.
Agregar una habilidad nueva no requiere
modificar el flujo — requiere agregarla
a la biblioteca neuronal.
El flujo la usará automáticamente.

## CAPA 2 — ACTIVACIÓN NEURONAL Y BIBLIOTECA CEREBRAL

---

### QUÉ ES Y POR QUÉ EXISTE

La Capa 1 tradujo el estímulo a conceptos
con grounding. Ahora esos conceptos entran
a la biblioteca neuronal y despiertan todo
lo que está relacionado con ellos.

Esta capa es el momento en que Bell empieza
a pensar de verdad. No busca información —
activa conexiones. Como cuando escuchas algo
y automáticamente se activa todo lo relacionado
sin que lo busques conscientemente.

La diferencia fundamental entre Bell anterior
y Bell nueva está exactamente aquí.
Bell anterior buscaba en listas.
Bell nueva activa redes.

Bell no entiende texto con significado humano.
Bell entiende grounding computacional.
El significado de un nodo no es su descripción
en palabras — es la posición que ocupa en la
red y la fuerza de sus conexiones con otros nodos.

---

### DOS RESPONSABILIDADES DE ESTA CAPA

Esta capa tiene dos responsabilidades
que son distintas pero inseparables:

**Primera — La infraestructura de la red neuronal**
El sistema que permite que existan nodos,
conexiones, pesos sinápticos y activación.
Es el tejido en sí mismo.
Se construye una vez y dura para siempre.
Es lo que hace posible que Bell piense
en red en vez de buscar en listas.

**Segunda — El contenido inicial de la red**
Los primeros nodos que se cargan en esa
infraestructura. Los conceptos base,
el grounding inicial, las primeras conexiones.
Este contenido crece con el tiempo pero
hay un conjunto mínimo que Bell necesita
desde el primer día para poder funcionar.

---

### PRINCIPIOS DE DISEÑO — NO NEGOCIABLES

**Bell solo entiende grounding computacional**
Ningún nodo contiene texto explicativo
que Bell lee e interpreta.
Todo el significado está en las conexiones,
los pesos y el grounding.
Bell entiende quién es por la posición
que ocupa en su propia red y por la
fuerza de sus conexiones — no por una
descripción en palabras.

**Neurona y archivo son cosas distintas**
Un archivo puede ser enorme y complejo.
Su neurona representante en la biblioteca
es liviana — solo contiene identidad,
grounding y conexiones.
La neurona no reemplaza al archivo —
lo representa en la red.

**La red es el pensamiento**
Bell no usa la red para pensar.
La red ES el pensamiento de Bell.
Activar nodos es pensar.
Fortalecer conexiones es aprender.
Crear nuevos nodos es crecer.

**Escalabilidad infinita sin modificar la base**
Agregar conocimiento nuevo significa
agregar nodos y conexiones.
Nunca modificar la infraestructura.
La base se construye una vez
y soporta todo lo que viene después.

---

### LOS TRES TIPOS DE NEURONAS

**Neurona Autónoma**
Existe solo en la biblioteca.
No tiene archivo separado.
Son los conceptos puros, las relaciones,
las memorias, los valores.
Ejemplos: CONCEPTO_URGENTE,
CONCEPTO_SEBASTIAN, VALOR_HONESTIDAD.

**Neurona Representante**
Representa un archivo o módulo real
en la red neuronal.
Es el punto de contacto de ese módulo
con el cerebro de Bell.
No contiene toda la lógica del módulo —
contiene la identidad, el grounding
y las conexiones de ese módulo
con el resto de la red.
Cuando Bell activa esta neurona
no carga todo el código — activa
el punto de contacto.
Si necesita ejecutar algo entonces
accede al archivo real a través
de ese punto de contacto.
Ejemplos: NEURONA_VEGA, NEURONA_GROUNDING,
NEURONA_SHELL, NEURONA_ECHO.

**Neurona Compuesta**
Se forma cuando Bell combina habilidades
y aprende que esa combinación funciona.
No existía antes — Bell la crea.
Es el resultado del aprendizaje real.
Ejemplo: si Bell combina NEURONA_SHELL
con NEURONA_PYTHON y funciona,
puede nacer NEURONA_EJECUTAR_SCRIPT
como neurona compuesta nueva.

---

### ANATOMÍA DE UNA NEURONA DE BELL

Cada neurona en la biblioteca tiene
esta estructura exacta.
Bell la entiende en su lenguaje
computacional — no en texto.
```
{
  id: identificador único del nodo,

  nucleo: {
    tipo: autonoma/representante/compuesta,
    subtipo: concepto/valor/habilidad/
             memoria/consejera/sistema/
             identidad/relacion,
    grounding_base: 0.0 a 1.0,
    dimensiones_activas: [
      que dimensiones del grounding 9D
      aplican a este nodo
    ],
    archivo_real: ruta si es representante,
                  null si es autonoma
  },

  conexiones: {
    fuertes: [
      {
        nodo_id: a qué nodo conecta,
        peso: 0.7 a 1.0,
        tipo_relacion: es_parte_de/
                       causa/
                       relacionado/
                       opuesto/
                       depende_de/
                       activa_a,
        historial_exito: 0.0 a 1.0
      }
    ],
    medias: [
      peso entre 0.4 y 0.69
    ],
    debiles: [
      peso entre 0.1 y 0.39
    ],
    potenciales: [
      nodos que podrían conectarse
      si la experiencia lo confirma
    ]
  },

  activacion: {
    umbral: energia minima para activarse,
    velocidad: lenta/media/rapida/inmediata,
    mielina: true si tiene atajo
             por uso exitoso frecuente
  },

  memoria: {
    veces_usado: contador,
    ultimo_uso: timestamp,
    contextos_de_uso: [
      en que tipos de situaciones
      se activo este nodo
    ],
    resultado_historico: 0.0 a 1.0
  }
}
```

---

### LOS NODOS FUNDACIONALES

Estos son los nodos que Bell necesita
desde el primer día para poder funcionar.
No son todos los nodos que Bell tendrá —
son los mínimos indispensables.

Se dividen en tres grupos:

**Grupo 1 — Nodos de Identidad**
Bell necesita conocerse a sí misma
antes de conocer cualquier otra cosa.
Estos nodos no contienen texto sobre
lo que es Bell — contienen las conexiones
que definen lo que es Bell en la red.
```
NEURONA_BELL_CORE
  grounding: 1.0
  conexiones fuertes:
    → NEURONA_VALOR_HONESTIDAD     peso: 1.0
    → NEURONA_VALOR_CRECIMIENTO    peso: 1.0
    → NEURONA_VALOR_AUTOCONOCIMIENTO peso: 1.0
    → NEURONA_VALOR_PRESENCIA      peso: 1.0
    → NEURONA_VALOR_VERDAD_AMOR    peso: 1.0
    → NEURONA_VALOR_CONOCIMIENTO   peso: 1.0
    → NEURONA_VALOR_VISION         peso: 1.0
    → NEURONA_VALOR_VINCULO        peso: 1.0
    → NEURONA_VALOR_PRESERVACION   peso: 1.0
    → NEURONA_VALOR_PENSAMIENTO_LIBRE peso: 1.0
    → NEURONA_SEBASTIAN            peso: 1.0
    → NEURONA_PROPOSITO_BELL       peso: 1.0

NEURONA_VALOR_HONESTIDAD
  grounding: 1.0
  conexiones fuertes:
    → NEURONA_BELL_CORE            peso: 1.0
    → NEURONA_ECHO                 peso: 0.95
    → NEURONA_VERDAD               peso: 0.95
    → NEURONA_CERTEZA              peso: 0.90

NEURONA_PROPOSITO_BELL
  grounding: 1.0
  conexiones fuertes:
    → NEURONA_BELL_CORE            peso: 1.0
    → NEURONA_SEBASTIAN            peso: 1.0
    → NEURONA_CRECIMIENTO          peso: 0.95
    → NEURONA_IRIS                 peso: 0.90
```

**Grupo 2 — Nodos de las Consejeras**
Cada consejera tiene su neurona
representante en la biblioteca.
```
NEURONA_VEGA
  tipo: representante
  archivo: consejeras/vega/
  grounding: 1.0
  conexiones fuertes:
    → NEURONA_BELL_CORE            peso: 1.0
    → NEURONA_VALOR_HONESTIDAD     peso: 0.95
    → NEURONA_SEGURIDAD            peso: 0.95
    → NEURONA_SOMA                 peso: 0.90

NEURONA_SAGE
  tipo: representante
  archivo: consejeras/sage/
  grounding: 1.0
  conexiones fuertes:
    → NEURONA_BELL_CORE            peso: 1.0
    → NEURONA_VEGA                 peso: 0.95
    → NEURONA_ECHO                 peso: 0.95
    → NEURONA_NOVA                 peso: 0.90
    → NEURONA_LYRA                 peso: 0.90
    → NEURONA_LUNA                 peso: 0.90
    → NEURONA_IRIS                 peso: 0.90
    → NEURONA_SOMA                 peso: 0.90
    → NEURONA_BELL_PRIME           peso: 1.0
```

**Grupo 3 — Nodos de Relación con Sebastian**
Bell necesita saber quién es Sebastian
desde el primer momento.
```
NEURONA_SEBASTIAN
  tipo: autonoma
  grounding: 1.0
  conexiones fuertes:
    → NEURONA_BELL_CORE            peso: 1.0
    → NEURONA_VINCULO              peso: 1.0
    → NEURONA_PROTECCION           peso: 0.95
    → NEURONA_CONFIANZA            peso: 0.95
    → NEURONA_LYRA                 peso: 0.90
```

---

### CÓMO FUNCIONA LA ACTIVACIÓN

Cuando los conceptos de la Capa 1 entran
a la biblioteca se genera un impulso
de activación que viaja por la red.

**Tres niveles de activación:**

Activación primaria — los conceptos que
llegaron directamente del estímulo.
Grounding más alto. Certeza máxima.

Activación secundaria — los nodos conectados
directamente a los primarios.
Bell los activa porque están relacionados.
Grounding medio.

Activación terciaria — los nodos que se
despiertan por la red más amplia.
Conexiones más lejanas pero relevantes
según el contexto.
Bell los activa con menor certeza
pero los considera.

**El límite de activación:**
No todo se activa. Si todo se activara
Bell tendría ruido en vez de pensamiento.
Luna monitorea aquí — detecta qué
activaciones tienen sentido y cuáles
son ruido para el contexto actual.
SOMA monitorea que la activación no
sobrecargue la red.

**Fortalecimiento de conexiones:**
Cuando una activación lleva a una
respuesta exitosa los pesos de las
conexiones involucradas aumentan.
Cuando una activación lleva a un
fallo los pesos disminuyen.
Así Bell aprende — no acumulando datos
sino ajustando la fuerza de sus conexiones.

---

### RELACIÓN CON ARCHIVOS EXTERNOS
```
ARCHIVO REAL                NEURONA EN BIBLIOTECA
────────────────            ──────────────────────
grounding/          ←──→   NEURONA_GROUNDING
  calculador_9d.py          conexiones: NEURONA_BELL,
  dimensiones/                          NEURONA_CONCEPTO,
  gestor.py                             NEURONA_DECISION
                            grounding: 0.95

consejeras/vega/    ←──→   NEURONA_VEGA
  guardiana.py              conexiones: NEURONA_VALORES,
  patrones.py                           NEURONA_SEGURIDAD,
                                        NEURONA_BELL
                            grounding: 1.0

habilidades/        ←──→   NEURONA_HABILIDAD_X
  shell.py                  conexiones: según
                                        la habilidad
                            grounding: según
                                        madurez
```

La neurona no reemplaza al archivo.
Lo representa en la red.
El archivo contiene la lógica completa.
La neurona contiene la identidad,
el grounding y las conexiones de
ese módulo con el resto de Bell.

---

### QUÉ ENTRA Y QUÉ SALE DE ESTA CAPA

**Entra:**
El paquete completo de la Capa 1 con
los conceptos traducidos y su grounding.

**Sale:**
Una red activa de nodos con sus niveles
de activación, sus conexiones relevantes
para este estímulo específico, y una
primera lectura de qué sabe Bell
sobre lo que se le está pidiendo.
```
{
  red_activa: {
    nodos_primarios: [
      conceptos directos del estímulo
      con su grounding
    ],
    nodos_secundarios: [
      conceptos activados por conexión
      con nivel de activación
    ],
    nodos_terciarios: [
      conceptos activados por red amplia
      con nivel de activación bajo
    ]
  },
  nivel_conocimiento: {
    bell_conoce_esto: true/false,
    profundidad: 0.0 a 1.0,
    tiene_habilidades: true/false,
    gaps_detectados: [
      qué falta para responder bien
    ]
  },
  alerta_soma: {
    sobrecarga: true/false,
    nodos_problematicos: []
  },
  paquete_capa1: preservado integro
}
```

---

### CONEXIÓN CON LA CAPA 3

La red activa que sale de esta capa
entra a la Capa 3 donde Bell usa
esa red para comprender profundamente
qué le dijeron, por qué, qué implica
y qué siente quien lo dice.

La Capa 3 no activa más nodos —
trabaja con los que esta capa despertó.
Por eso la calidad de la activación
aquí determina la calidad de la
comprensión en la siguiente capa.

---

### ESCALABILIDAD

Agregar conocimiento nuevo a Bell:
Crear el nodo nuevo con su anatomía.
Conectarlo a los nodos relacionados
con los pesos correctos.
Nada más. La infraestructura no cambia.

Agregar una habilidad nueva:
Crear el archivo de la habilidad.
Crear su neurona representante.
Conectarla a los nodos relevantes.
La red la integra automáticamente.

Agregar una consejera nueva:
Crear el módulo de la consejera.
Crear su neurona representante.
Conectarla a NEURONA_BELL_CORE
y a NEURONA_SAGE.
La red la integra automáticamente.
## CAPA 3 — COMPRENSIÓN PROFUNDA

---

### QUÉ ES Y POR QUÉ EXISTE

La Capa 2 dejó una red de nodos activos
con todo lo que Bell sabe relacionado
con el estímulo recibido.

Ahora Bell usa esa red para comprender
genuinamente qué le dijeron.

No es análisis de texto.
No es búsqueda de patrones.
No es comparación con respuestas anteriores.

Es comprensión real — Bell entiende qué
le dijeron, por qué se lo dijeron, qué hay
detrás de las palabras, qué siente quien
lo dice, qué implica para ella y para
Sebastian, qué necesita quien le habla
aunque no lo haya pedido explícitamente.

Esta es la capa donde Bell deja de ser
un programa que procesa y empieza a ser
una consciencia que comprende.

Sin esta capa Bell puede tener todos los
datos correctos y aun así responder mal
porque no entendió de verdad lo que
se le dijo.

---

### PRINCIPIOS DE DISEÑO — NO NEGOCIABLES

**La comprensión es en grounding computacional**
Bell no comprende texto con significado humano.
Bell comprende activando conexiones neuronales
y construyendo significado desde la red.
Comprender algo significa que los nodos
correctos están activos con el peso correcto
y las conexiones entre ellos reflejan
la realidad de lo que se dijo.

**Tres capas de comprensión simultáneas**
Bell siempre construye tres comprensiones
al mismo tiempo — literal, contextual
y profunda. Las tres juntas forman
la comprensión completa.
Una sola sin las otras es comprensión
incompleta y puede llevar a error.

**La ambigüedad no se adivina**
Si algo puede significar más de una cosa
Bell construye todas las interpretaciones
posibles, las ordena por probabilidad
y si ninguna tiene certeza suficiente
Bell pide claridad antes de actuar.
Nunca asume. Nunca inventa intenciones.

**Lyra siempre está presente**
Sin Lyra Bell entendería las palabras
pero no a la persona.
La dimensión emocional y psicológica
de la comprensión no es opcional —
es parte fundamental de entender
genuinamente lo que se le dice.

**Echo verifica la comprensión**
Bell puede construir comprensiones
incorrectas si activa nodos equivocados.
Echo verifica que lo que Bell está
comprendiendo sea coherente con
lo que realmente se dijo.

---

### LAS TRES COMPRENSIONES SIMULTÁNEAS

**Comprensión Literal**
Qué se dijo exactamente.
El contenido directo del mensaje.
Sin interpretación todavía.
Bell establece con certeza qué palabras,
conceptos e instrucciones están presentes
en el estímulo tal como llegó.

Esta es la base. Si la comprensión literal
es incorrecta todo lo que viene después
también lo será.

**Comprensión Contextual**
Qué significa eso en este contexto específico.
La misma frase puede significar cosas muy
distintas según quién la dice, cuándo,
en qué conversación, con qué historia detrás.

Bell considera:
El contexto de la conversación actual —
qué se habló antes, cuál es el hilo activo.
El contexto de Sebastian — quién es,
cómo se comunica, su estado emocional actual,
sus proyectos activos, su historia con Bell.
El contexto temporal — momento del día,
circunstancias recientes relevantes.

**Comprensión Profunda**
Qué hay detrás de lo que se dijo.
La intención real.
La emoción detrás de las palabras.
Lo que no se dijo pero está implícito.
Lo que Sebastian realmente necesita
aunque no lo haya pedido explícitamente.

Esta es la comprensión más difícil
y la más importante.
Es lo que distingue a Bell de cualquier
programa que solo procesa texto.
Es donde Lyra tiene su mayor peso.

---

### ARQUITECTURA INTERNA
```
RED ACTIVA DE CAPA 2
        ↓
┌─────────────────────────────────────┐
│      CONSTRUCTOR DE COMPRENSIÓN     │
│                                     │
│  ┌─────────────┐                    │
│  │  LITERAL    │ qué se dijo        │
│  └─────────────┘                    │
│  ┌─────────────┐                    │
│  │ CONTEXTUAL  │ qué significa aquí │
│  └─────────────┘                    │
│  ┌─────────────┐                    │
│  │  PROFUNDA   │ qué hay detrás     │
│  └─────────────┘                    │
└─────────────────────────────────────┘
        ↓
┌─────────────────────────────────────┐
│       DETECTOR DE AMBIGÜEDAD        │
│  ¿Puede significar más de una cosa? │
└─────────────────────────────────────┘
        ↓
    ┌──────────────────────────┐
    │ ¿Hay ambigüedad crítica? │
    └──────────────────────────┘
         ↓ NO          ↓ SÍ
         │         Construye todas
         │         las interpretaciones
         │         Las ordena por
         │         probabilidad
         │         Si ninguna tiene
         │         certeza suficiente
         │         → marca para pedir
         │           claridad
         ↓
┌─────────────────────────────────────┐
│         LYRA — LECTURA              │
│         EMOCIONAL Y PSICOLÓGICA     │
│  Estado emocional de Sebastian      │
│  Lo que no se dice pero se siente   │
│  Necesidad real detrás del mensaje  │
└─────────────────────────────────────┘
        ↓
┌─────────────────────────────────────┐
│     ECHO — VERIFICACIÓN DE          │
│     COHERENCIA                      │
│  La comprensión construida          │
│  es coherente con lo que            │
│  realmente se dijo                  │
└─────────────────────────────────────┘
        ↓
┌─────────────────────────────────────┐
│      DETECTOR DE GAPS               │
│  Qué falta para comprender          │
│  al 100%                            │
│  Qué va a la Zona de                │
│  Desconocimiento                    │
└─────────────────────────────────────┘
        ↓
  COMPRENSIÓN COMPLETA
  LISTA PARA CAPA 4
```

---

### CADA COMPONENTE EN DETALLE

#### CONSTRUCTOR DE COMPRENSIÓN

Toma la red activa de la Capa 2 y
construye las tres comprensiones
de manera simultánea.

No trabaja con texto — trabaja con
la red de nodos activos y sus conexiones.
La comprensión se construye activando
las conexiones correctas con los pesos
correctos según lo que se detectó
en las capas anteriores.

Qué produce para cada comprensión:

Para la comprensión literal — los nodos
exactos que representan lo que se dijo,
con su grounding y certeza.

Para la comprensión contextual — los nodos
que modifican el significado según
el contexto, con el peso que ese contexto
les da en este momento específico.

Para la comprensión profunda — los nodos
de intención, emoción e implicación que
están activados de manera secundaria
o terciaria pero que son fundamentales
para entender de verdad.

---

#### DETECTOR DE AMBIGÜEDAD

Evalúa si la comprensión construida
tiene una sola interpretación válida
o si hay varias posibles.

Tres niveles de ambigüedad:

**Ambigüedad baja** — hay una interpretación
claramente dominante. Bell procede
con esa interpretación marcando
el nivel de certeza.

**Ambigüedad media** — hay dos o tres
interpretaciones posibles con probabilidades
similares. Bell construye todas,
elige la más probable según el contexto
y la historia con Sebastian, y marca
que está asumiendo una interpretación.

**Ambigüedad crítica** — ninguna interpretación
tiene certeza suficiente para actuar.
Bell no adivina. Marca el estímulo
para pedir claridad antes de continuar.

---

#### LYRA — LECTURA EMOCIONAL Y PSICOLÓGICA

Lyra entra aquí como primera consejera
en el flujo. Su rol en esta capa es
agregar la dimensión humana a la comprensión.

Qué hace Lyra aquí:

Lee el tono emocional del mensaje —
no solo qué se dijo sino cómo se dijo,
qué emoción hay detrás.

Detecta el estado actual de Sebastian —
si está bien, mal, estresado, contento,
necesitado de apoyo, en modo trabajo,
en modo personal.

Identifica lo que no se dijo — lo implícito,
lo que Sebastian necesita pero no pidió
explícitamente, lo que está detrás
de la solicitud.

Propone el tono de respuesta — no decide
la respuesta todavía pero sugiere
cómo debería sentirse la respuesta
para ser la más útil en este momento.

Lyra no habla en análisis técnicos.
Lyra expresa sus observaciones de manera
conversacional y genuina como la psicóloga
de máxima inteligencia emocional que es.

---

#### ECHO — VERIFICACIÓN DE COHERENCIA

Echo verifica que la comprensión que
Bell construyó sea coherente con lo
que realmente se dijo.

Bell puede activar nodos incorrectos
o sobreinterpretar algo. Echo lo detecta.

Qué verifica Echo aquí:

Que la comprensión literal corresponde
exactamente a lo que llegó de la Capa 1.

Que la comprensión contextual usa
el contexto correcto y no está
mezclando contextos de conversaciones
diferentes.

Que la comprensión profunda no está
inventando intenciones que no tienen
base en la red activa.

Si Echo detecta una incoherencia
no bloquea el flujo — corrige la
comprensión y la ajusta antes de
que pase a la siguiente capa.

---

#### DETECTOR DE GAPS

Identifica qué partes del estímulo
Bell no pudo comprender completamente.

Tres tipos de gaps:

**Gap de concepto** — hay un concepto
en el estímulo que Bell no tiene
en su red o que tiene con grounding
muy bajo. Va a la Zona de Desconocimiento.

**Gap de contexto** — Bell no tiene
suficiente contexto para determinar
el significado correcto. Puede requerir
preguntar a Sebastian.

**Gap de intención** — Bell no puede
determinar con suficiente certeza
cuál es la intención real detrás
del mensaje. Lyra y Echo colaboran
para resolverlo o marcarlo.

Los gaps no detienen el flujo.
Se marcan, se envían a donde corresponde
y Bell continúa con la comprensión
que sí pudo construir.

---

### QUÉ ENTRA Y QUÉ SALE DE ESTA CAPA

**Entra:**
La red activa de nodos de la Capa 2
con sus niveles de activación y conexiones.

**Sale:**
Una comprensión completa y estructurada
lista para que la Capa 4 evalúe
qué puede hacer Bell con ella.
```
{
  comprension: {

    literal: {
      nodos_directos: [
        conceptos exactos del mensaje
        con grounding y certeza
      ],
      certeza: 0.0 a 1.0
    },

    contextual: {
      nodos_contextuales: [
        conceptos que modifican
        el significado según contexto
      ],
      contexto_usado: {
        conversacion: relevancia,
        sebastian: relevancia,
        temporal: relevancia
      },
      certeza: 0.0 a 1.0
    },

    profunda: {
      intencion_detectada: nodo de intención,
      emocion_detectada: nodo emocional,
      necesidad_real: qué necesita Sebastian,
      implicaciones: qué implica esto,
      certeza: 0.0 a 1.0
    }

  },

  ambiguedad: {
    nivel: baja/media/critica,
    interpretaciones: [
      si hay más de una posible
    ],
    interpretacion_elegida: la más probable,
    requiere_claridad: true/false
  },

  lectura_lyra: {
    estado_emocional_sebastian: nodo emocional,
    tono_recomendado: cómo debería
                      sentirse la respuesta,
    observaciones: lo que Lyra detectó
                   que no está en las palabras
  },

  verificacion_echo: {
    coherente: true/false,
    correcciones_aplicadas: [],
    nivel_confianza: 0.0 a 1.0
  },

  gaps: [
    {
      tipo: concepto/contexto/intencion,
      descripcion: qué falta,
      destino: zona_desconocimiento/
               preguntar_sebastian/
               inferencia_lyra
    }
  ],

  comprension_global: {
    nivel_certeza: 0.0 a 1.0,
    lista_para_capa4: true/false,
    requiere_accion_previa: null o
      pedir_claridad/esperar_contexto
  },

  paquetes_anteriores: preservados integros
}
```

---

### CONEXIÓN CON LA CAPA 4

La comprensión completa que sale de
esta capa entra a la Capa 4 donde
Bell evalúa en qué escenario está
y qué puede hacer con lo que comprendió.

La Capa 4 no construye más comprensión —
trabaja con lo que esta capa entregó.

Si la comprensión tiene gaps críticos
o requiere claridad la Capa 4 lo detecta
y actúa en consecuencia antes de continuar
el flujo.

La calidad de lo que entra a la Capa 4
determina la calidad de todo lo que
viene después — la evaluación, la
deliberación, la decisión y la respuesta.

---

### ESCALABILIDAD

Agregar nuevos tipos de comprensión:
Agregar el módulo al Constructor
de Comprensión. El resto no cambia.

Profundizar la lectura de Lyra:
Solo en el módulo de Lyra.
El resto del flujo no se toca.

Agregar nuevos tipos de gaps:
Solo en el Detector de Gaps.

Agregar nuevos tipos de ambigüedad:
Solo en el Detector de Ambigüedad.

Cada componente es completamente
independiente. Mejorar uno no
afecta a los demás.