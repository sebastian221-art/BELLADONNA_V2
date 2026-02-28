# 🔬 BELL STRUCTURE ANALYZER v2.0

**Fecha:** 2026-02-23 14:31

---

## 📊 RESUMEN EJECUTIVO

```
Total archivos:     160
Total clases:       116
Total funciones:    167
Total líneas:      42909
Módulos:             20
Huérfanos:           52
```

---

## 🗂️ MÓDULOS DE BELL

| Módulo | Archivos | Descripción |
|--------|----------|-------------|
| `analisis` | 2 | — |
| `aprendizaje` | 5 | Motor de aprendizaje |
| `base_datos` | 3 | Conexión SQLite |
| `bucles` | 6 | Bucles autónomos |
| `config` | 1 | Configuración |
| `consejeras` | 19 | Las 7 consejeras (mente de Bell) |
| `core` | 5 | Núcleo fundamental de Bell |
| `demos` | 16 | — |
| `generacion` | 4 | Genera respuestas naturales |
| `grounding` | 20 | Sistema de anclaje 9D |
| `llm` | 2 | Integración con Groq/LLM |
| `matematicas` | 2 | — |
| `memoria` | 4 | Memoria persistente |
| `operaciones` | 2 | Operaciones de sistema |
| `planificacion` | 3 | — |
| `razonamiento` | 5 | Motor de pensamiento y decisiones |
| `red` | 3 | — |
| `scripts` | 5 | — |
| `traduccion` | 5 | Traduce español → lenguaje interno |
| `vocabulario` | 44 | Conceptos y palabras que Bell entiende |

---

## 🚀 PUNTO DE ENTRADA: main.py

### Imports internos:

- `aprendizaje.motor_aprendizaje`
- `base_datos`
- `bucles.gestor_bucles`
- `consejeras.echo.verificador_coherencia`
- `consejeras.gestor_consejeras`
- `generacion.generador_salida`
- `grounding`
- `grounding.calculadores`
- `llm.groq_wrapper`
- `llm.groq_wrapper`
- `memoria.gestor_memoria`
- `operaciones.shell_executor`
- `razonamiento.motor_razonamiento`
- `traduccion.traductor_entrada`
- `vocabulario.gestor_vocabulario`
- `vocabulario.semana10_bd`

### Clases definidas:

- `Belladonna`

---

## 🔗 DEPENDENCIAS ENTRE MÓDULOS

```
consejeras → core, razonamiento
demos → analisis, base_datos, consejeras, core, generacion, grounding, matematicas, operaciones, planificacion, razonamiento, red, traduccion, vocabulario
generacion → consejeras, llm, memoria, razonamiento, vocabulario
llm → config, vocabulario
razonamiento → core
root → aprendizaje, base_datos, bucles, consejeras, generacion, grounding, llm, memoria, operaciones, razonamiento, traduccion, vocabulario
traduccion → core, vocabulario
vocabulario → core
```

---

## 👥 CONSEJERAS (La mente de Bell)

**Gestor:** `consejeras\gestor_consejeras.py`

**Consejeras encontradas:**

- `consejeras\base_consejera.py`
- `consejeras\echo\logica.py`
- `consejeras\echo\verificador_coherencia.py`
- `consejeras\iris\vision.py`
- `consejeras\luna\intuicion.py`
- `consejeras\lyra\empatia.py`
- `consejeras\nova\ingeniera.py`
- `consejeras\sage\sintesis.py`
- `consejeras\vega\guardiana.py`
- `consejeras\vega\patrones.py`

---

## 🧠 RAZONAMIENTO (Donde va el clasificador)

### `razonamiento\__init__.py`
- Líneas: 18

### `razonamiento\evaluador_capacidades.py`
- Líneas: 150
- Clases:
  - `EvaluadorCapacidades`: __init__, evaluar_capacidad_accion, verificar_requisitos, calcular_confianza_total

### `razonamiento\generador_decisiones.py`
- Líneas: 112
- Clases:
  - `GeneradorDecisiones`: __init__, generar_decision_capacidad, generar_decision_saludo, generar_decision_agradecimiento, generar_decision_no_entendido

### `razonamiento\motor_razonamiento.py`
- Líneas: 700
- Clases:
  - `MotorRazonamiento`: __init__, razonar, _razonar_operacion, clasificar_intencion, construir_hechos (+12 más)
- Funciones:
  - `_clamp_certeza()`

### `razonamiento\tipos_decision.py`
- Líneas: 103
- Clases:
  - `TipoDecision`: 
  - `RazonRechazo`: 
  - `Decision`: __post_init__, es_ejecutable, es_rechazo, __repr__


---

## 💬 GENERACIÓN (Respuestas naturales)

### `generacion\__init__.py`
- Líneas: 12

### `generacion\generador_salida.py`
- Líneas: 848
- Clase: `GeneradorSalida`

### `generacion\prompts_naturales.py`
- Líneas: 963
- Clase: `PromptsNaturales`

### `generacion\templates_respuesta.py`
- Líneas: 114
- Clase: `TemplatesRespuesta`


---

## 🤖 LLM / GROQ

### `llm\__init__.py`
- Líneas: 26

### `llm\groq_wrapper.py`
- Líneas: 603
- Clase: `RespuestaGroq`
- Clase: `GroqWrapper`
  - Métodos: __init__, _inicializar_cliente, _obtener_gestor_vocabulario, embellecer_decision, _detectar_emocion, _obtener_tono_para_emocion, _obtener_conceptos_para_contexto, _construir_system_prompt_enriquecido
- Dependencias externas: json, groq, typing, datetime, dataclasses


---

## ⚠️ ARCHIVOS HUÉRFANOS

Estos archivos NO son importados por nadie:

- `Bell_Inventory.py`
- `analizar_para_clasificador.py`
- `bell_duplicate_analyzer.py`
- `consejeras\echo\logica.py`
- `consejeras\iris\vision.py`
- `consejeras\luna\intuicion.py`
- `consejeras\lyra\empatia.py`
- `consejeras\nova\ingeniera.py`
- `consejeras\sage\sintesis.py`
- `consejeras\vega\guardiana.py`
- `consejeras\vega\patrones.py`
- `demos\demo_fase2_consejo.py`
- `demos\demo_fase3_semana1.py`
- `demos\demo_fase3_semana3.py`
- `demos\demo_fase3_semana5.py`
- `demos\demo_fase3_semana6.py`
- `demos\demo_fase3_semana7.py`
- `demos\demo_fase3_semana8.py`
- `demos\demo_generador.py`
- `demos\demo_grounding_9d.py`
- `demos\demo_motor.py`
- `demos\demo_semana1_completo.py`
- `demos\demo_semana2_completo.py`
- `demos\demo_traductor.py`
- `demos\demo_vega.py`
- `demos\demo_vocabulario.py`
- `scripts\analizar_codigo_obsoleto.py`
- `scripts\cleanup_fase4a.py`
- `scripts\generar_expansion_1000.py`
- `scripts\validar_vocabulario.py`
- `scripts\ver_estructura_detallada.py`
- `traduccion\analizador_contexto.py`
- `vocabulario\expansion\acciones_digitales.py`
- `vocabulario\expansion\adjetivos_descriptivos.py`
- `vocabulario\expansion\comida_cocina.py`
- `vocabulario\expansion\conceptos_abstractos.py`
- `vocabulario\expansion\conectores_avanzados.py`
- `vocabulario\expansion\contexto_conversacional.py`
- `vocabulario\expansion\emociones_estados.py`
- `vocabulario\expansion\entretenimiento_ocio.py`
- `vocabulario\expansion\expresiones_comunes.py`
- `vocabulario\expansion\expresiones_lugar.py`
- `vocabulario\expansion\expresiones_tiempo.py`
- `vocabulario\expansion\naturaleza_ambiente.py`
- `vocabulario\expansion\numeros_cantidades.py`
- `vocabulario\expansion\objetos_comunes.py`
- `vocabulario\expansion\preguntas_respuestas.py`
- `vocabulario\expansion\profesiones_trabajo.py`
- `vocabulario\expansion\relaciones_sociales.py`
- `vocabulario\expansion\salud_cuerpo.py`
- `vocabulario\expansion\tecnologia_moderna.py`
- `vocabulario\expansion\verbos_cotidianos.py`

---

## 📋 GUÍA RÁPIDA PARA OBREROS

### ¿Dónde modifico para...?

| Tarea | Archivo |
|-------|---------|
| Agregar tipo de decisión | `razonamiento/tipos_decision.py` |
| Modificar el motor de razonamiento | `razonamiento/motor_razonamiento.py` |
| Agregar prompts para Groq | `generacion/prompts_naturales.py` |
| Modificar generación de respuestas | `generacion/generador_salida.py` |
| Agregar conceptos | `vocabulario/expansion/*.py` |
| Configurar Groq | `llm/groq_wrapper.py` |

### NO TOCAR (a menos que se indique):

- `core/*` — Estructuras fundamentales
- `consejeras/*` — Sistema de consejeras
- `main.py` — Punto de entrada

---

*Reporte generado automáticamente por bell_structure_analyzer_v2.py*