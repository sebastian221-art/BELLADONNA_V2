# 🏗️ ARQUITECTURA DE BELLADONNA - MAPA COMPLETO
*Generado automáticamente por Bell_Inventory.py*

---

## 📊 RESUMEN EJECUTIVO

- **Total de archivos**: 200
- **Código activo**: 124 archivos
- **Código legacy**: 12 archivos
- **Tests**: 45 archivos
- **Módulos principales**: 19

### 🏥 Estado de Salud

⚠️  **23 archivos obsoletos detectados**
⚠️  **14 archivos huérfanos** (nadie los importa)

---

## 📦 MÓDULOS PRINCIPALES

### VOCABULARIO

- **Archivos**: 23
- **Clases**: 1
- **Funciones**: 31
- **Líneas de código**: 5838
- **Depende de**: core, vocabulario

**Archivos clave:**
- `__init__.py` - Paquete de Vocabulario de Belladonna.
- `gestor_vocabulario.py` - Gestor de Vocabulario de Belladonna.
- `semana10_bd.py` - Vocabulario de Bases de Datos - Semana 10 (Fase 3 FINAL).
- `semana1_acciones.py` - Conceptos de Acciones - Semana 1.
- `semana1_cognitivos.py` - Conceptos Cognitivos - Semana 1.

### GROUNDING

- **Archivos**: 20
- **Clases**: 20
- **Funciones**: 7
- **Líneas de código**: 2208
- **Depende de**: grounding

**Archivos clave:**
- `__init__.py` - Módulo Grounding - Sistema de Grounding 9D para Belladonna
- `base_dimension.py` - Clase base abstracta para todas las dimensiones de grounding
- `__init__.py` - Calculadores de Grounding.
- `calculador_9d.py` - Calculador de Grounding 9D.
- `extension_calculador.py` - Extensión de Grounding para ConceptoAnclado.

### CONSEJERAS

- **Archivos**: 18
- **Clases**: 10
- **Funciones**: 0
- **Líneas de código**: 1057
- **Depende de**: consejeras, core, razonamiento

**Archivos clave:**
- `__init__.py` - Sistema de Consejeras de Belladonna.
- `base_consejera.py` - Clase Base para Consejeras - Definición abstracta.
- `__init__.py`
- `logica.py` - Echo - Consejera Lógica.
- `gestor_consejeras.py` - Gestor de Consejeras - Coordina todas las consejeras de Bell

### APRENDIZAJE

- **Archivos**: 5
- **Clases**: 9
- **Funciones**: 0
- **Líneas de código**: 981
- **Depende de**: aprendizaje

**Archivos clave:**
- `__init__.py` - Paquete de Aprendizaje Básico - Fase 2.
- `ajustador_grounding.py` - Ajustador de Grounding - Modifica grounding de conceptos.
- `aplicador_insights.py` - Aplicador de Insights - Convierte insights en acciones.
- `estrategias.py` - Estrategias de Aprendizaje - Define cómo ajustar grounding.
- `motor_aprendizaje.py` - Motor de Aprendizaje - Coordina el sistema de aprendizaje.

### LLM

- **Archivos**: 5
- **Clases**: 4
- **Funciones**: 1
- **Líneas de código**: 875
- **Depende de**: llm

**Archivos clave:**
- `__init__.py` - Módulo LLM - Fase 4A Semana 1-2
- `dataset_bell.py`
- `generador_respuestas.py` - Generador de Respuestas Híbrido - OPTIMIZADO 100%
- `gestor_llm.py` - Gestor de LLM Local - ESPAÑOL - Fase 4A
- `verificador_coherencia.py` - Verificador de Coherencia - MEJORADO 100%

### BUCLES

- **Archivos**: 6
- **Clases**: 5
- **Funciones**: 0
- **Líneas de código**: 763
- **Depende de**: bucles

**Archivos clave:**
- `__init__.py` - Paquete de Bucles Autónomos - Fase 2.
- `base_bucle.py` - Bucle Base - Clase abstracta para bucles autónomos.
- `bucle_corto.py` - Bucle Corto - Revisión rápida de conceptos recientes.
- `bucle_largo.py` - Bucle Largo - Consolidación de aprendizaje.
- `bucle_medio.py` - Bucle Medio - Análisis de patrones conversacionales.

### PLANIFICACION

- **Archivos**: 3
- **Clases**: 6
- **Funciones**: 0
- **Líneas de código**: 672

**Archivos clave:**
- `__init__.py` - Módulo de Planificación Multi-Paso.
- `ejecutor_planes.py` - Ejecutor de Planes Multi-Paso.
- `motor_planificacion.py` - Motor de Planificación Multi-Paso.

### BASE_DATOS

- **Archivos**: 3
- **Clases**: 3
- **Funciones**: 0
- **Líneas de código**: 671

**Archivos clave:**
- `__init__.py` - Módulo de Bases de Datos SQLite.
- `cliente_sqlite.py` - Cliente SQLite para manejo de bases de datos.
- `gestor_bd.py` - Gestor avanzado de bases de datos SQLite.

### MEMORIA

- **Archivos**: 4
- **Clases**: 9
- **Funciones**: 0
- **Líneas de código**: 623
- **Depende de**: memoria

**Archivos clave:**
- `__init__.py` - Paquete de Memoria Persistente - Fase 2.
- `almacen.py` - Almacén de Memoria - Persistencia en JSON.
- `gestor_memoria.py` - Gestor de Memoria - Interfaz principal para memoria persiste
- `tipos_memoria.py` - Tipos y Enums para el Sistema de Memoria.

### RAZONAMIENTO

- **Archivos**: 5
- **Clases**: 6
- **Funciones**: 0
- **Líneas de código**: 336
- **Depende de**: core, razonamiento

**Archivos clave:**
- `__init__.py` - Paquete de Razonamiento - El cerebro de Bell.
- `evaluador_capacidades.py` - Evaluador de Capacidades - ¿Bell PUEDE hacer algo?
- `generador_decisiones.py` - Generador de Decisiones - Crea objetos Decision.
- `motor_razonamiento.py` - Motor de Razonamiento - El cerebro de Bell.
- `tipos_decision.py` - Tipos de Decisiones que Bell puede tomar.

### GENERACION

- **Archivos**: 3
- **Clases**: 2
- **Funciones**: 0
- **Líneas de código**: 305
- **Depende de**: generacion, razonamiento

**Archivos clave:**
- `__init__.py` - Paquete de Generación - Decisiones → Español.
- `generador_salida.py` - Generador de Salida - Decision → Español Natural.
- `templates_respuesta.py` - Templates de Respuesta - Convertir Decisiones a Español.

### CORE

- **Archivos**: 5
- **Clases**: 6
- **Funciones**: 2
- **Líneas de código**: 262
- **Depende de**: core

**Archivos clave:**
- `__init__.py`
- `capacidades_bell.py` - Define qué puede hacer Bell en la realidad.
- `concepto_anclado.py` - ConceptoAnclado: La unidad fundamental del conocimiento de B
- `principios.py` - Principios Fundamentales de Belladonna.
- `tipos.py` - Tipos y enums fundamentales de Belladonna.

### OPERACIONES

- **Archivos**: 2
- **Clases**: 2
- **Funciones**: 0
- **Líneas de código**: 225

**Archivos clave:**
- `__init__.py` - Módulo de operaciones del sistema.
- `shell_executor.py` - Ejecutor de comandos shell con seguridad.

### TRADUCCION

- **Archivos**: 3
- **Clases**: 2
- **Funciones**: 0
- **Líneas de código**: 190
- **Depende de**: core, traduccion, vocabulario

**Archivos clave:**
- `__init__.py` - Paquete de Traducción - Español → Conceptos.
- `analizador_español.py` - Analizador de Español - Semana 2.
- `traductor_entrada.py` - Traductor de Entrada - Español → ConceptosAnclados.

---

## 🧬 JERARQUÍA DE CLASES

### Heredan de `ABC`

- BaseBucle (bucles\base_bucle.py)
- Consejera (consejeras\base_consejera.py)
- DimensionGrounding (grounding\base_dimension.py)
- EstrategiaAprendizaje (aprendizaje\estrategias.py)

### Heredan de `BaseBucle`

- BucleCorto (bucles\bucle_corto.py)
- BucleLargo (bucles\bucle_largo.py)
- BucleMedio (bucles\bucle_medio.py)
- BucleTest (tests\test_bucles.py)

### Heredan de `Consejera`

- Echo (consejeras\echo\logica.py)
- Iris (consejeras\iris\vision.py)
- Luna (consejeras\luna\intuicion.py)
- Lyra (consejeras\lyra\empatia.py)
- Nova (consejeras\nova\ingeniera.py)
- Sage (consejeras\sage\sintesis.py)
- Vega (consejeras\vega\guardiana.py)

### Heredan de `DimensionGrounding`

- GroundingCausal (grounding\dimensiones\causal.py)
- GroundingComputacional (grounding\dimensiones\computacional.py)
- GroundingContextual (grounding\dimensiones\contextual.py)
- GroundingMetacognitivo (grounding\dimensiones\metacognitivo.py)
- GroundingPragmatico (grounding\dimensiones\pragmatico.py)
- GroundingPredictivo (grounding\dimensiones\predictivo.py)
- GroundingSemantico (grounding\dimensiones\semantico.py)
- GroundingSocial (grounding\dimensiones\social.py)
- GroundingTemporal (grounding\dimensiones\temporal.py)

### Heredan de `EstrategiaAprendizaje`

- EstrategiaComposite (aprendizaje\estrategias.py)
- EstrategiaConservadora (aprendizaje\estrategias.py)
- EstrategiaExitoFallido (aprendizaje\estrategias.py)
- EstrategiaInsights (aprendizaje\estrategias.py)
- EstrategiaUsoFrecuente (aprendizaje\estrategias.py)

---

## ⚠️  CÓDIGO OBSOLETO DETECTADO

Los siguientes archivos pueden estar obsoletos:

- `_legacy\extension_grounding.py` - *Carpeta _legacy*
- `_legacy\grounding_causal.py` - *Carpeta _legacy*
- `_legacy\grounding_contextual.py` - *Carpeta _legacy*
- `_legacy\grounding_metacognitivo.py` - *Carpeta _legacy*
- `_legacy\grounding_pragmatico.py` - *Carpeta _legacy*
- `_legacy\grounding_predictivo.py` - *Carpeta _legacy*
- `_legacy\grounding_semantico.py` - *Carpeta _legacy*
- `_legacy\grounding_social.py` - *Carpeta _legacy*
- `_legacy\grounding_temporal.py` - *Carpeta _legacy*
- `_legacy\integracion_grounding_bell.py` - *Carpeta _legacy*
- `_legacy\reporte_grounding.py` - *Carpeta _legacy*
- `aprendizaje\__init__.py` - *Sin clases ni funciones públicas*
- `base_datos\__init__.py` - *Sin clases ni funciones públicas*
- `bucles\__init__.py` - *Sin clases ni funciones públicas*
- `consejeras\__init__.py` - *Sin clases ni funciones públicas*
- `grounding\calculadores\__init__.py` - *Sin clases ni funciones públicas*
- `grounding\reportes\__init__.py` - *Sin clases ni funciones públicas*
- `limpiar_legacy.py` - *Carpeta _legacy*
- `llm\__init__.py` - *Sin clases ni funciones públicas*
- `memoria\__init__.py` - *Sin clases ni funciones públicas*

---

## 📚 DEPENDENCIAS EXTERNAS

Librerías más usadas:

- **typing** - usado en 65 archivos
- **dataclasses** - usado en 23 archivos
- **pathlib** - usado en 21 archivos
- **datetime** - usado en 13 archivos
- **sys** - usado en 12 archivos
- **os** - usado en 7 archivos
- **collections** - usado en 6 archivos
- **json** - usado en 6 archivos
- **enum** - usado en 5 archivos
- **ast** - usado en 4 archivos
- **abc** - usado en 4 archivos
- **argparse** - usado en 3 archivos
- **time** - usado en 3 archivos
- **subprocess** - usado en 3 archivos
- **transformers** - usado en 3 archivos

---

## 💡 RECOMENDACIONES PARA FASE 4A

### 1. Limpieza de Código
- **CRÍTICO**: Mover 23 archivos obsoletos a carpeta `_archive/`

### 2. Módulos Activos
Los siguientes módulos están listos para Fase 4A:
- ✅ **aprendizaje** - 9 clases, 0 funciones
- ✅ **base_datos** - 3 clases, 0 funciones
- ✅ **bucles** - 5 clases, 0 funciones
- ✅ **consejeras** - 10 clases, 0 funciones
- ✅ **core** - 6 clases, 2 funciones
- ✅ **generacion** - 2 clases, 0 funciones
- ✅ **grounding** - 20 clases, 7 funciones
- ✅ **llm** - 4 clases, 1 funciones
- ✅ **memoria** - 9 clases, 0 funciones
- ✅ **operaciones** - 2 clases, 0 funciones
- ✅ **planificacion** - 6 clases, 0 funciones
- ✅ **razonamiento** - 6 clases, 0 funciones
- ✅ **traduccion** - 2 clases, 0 funciones
- ✅ **vocabulario** - 1 clases, 31 funciones

### 3. Puntos de Integración LLM
Módulos clave para conectar con Groq:
- `generacion/` - Generador de respuestas (ya existe)
- `razonamiento/` - Motor de decisiones (ya existe)
- `consejeras/sage/` - Filtro de coherencia (ya existe)

---

*Fin del reporte*