# 📅 FASE 4A - SEMANA 3-4: INTEGRACIÓN GROQ

**Duración**: 2 semanas  
**Estado**: Lista para implementar  
**Prerequisito**: Semana 1-2 completada (tests 26/26 pasando)

---

## 🎯 OBJETIVO

Integrar Groq con el flujo principal de Bell usando la **Arquitectura Mente Pura**:

```
Usuario
   ↓
Bell (Python) → Razona y decide
   ↓
Groq (API) → Solo embellece texto
   ↓
Echo (Python) → Verifica coherencia
   ↓
Respuesta final
```

---

## 📦 ARCHIVOS A REEMPLAZAR

### 1. `generacion/generador_salida.py`

**Cambios principales:**
- Nuevo parámetro `usar_groq` en `__init__`
- Método `_generar_con_groq()` para usar Groq
- Método `_generar_simbolica()` para modo legacy
- Estadísticas de uso de Groq
- Fallback automático a simbólico si Groq falla

**Copiar:**
```powershell
copy generacion_generador_salida.py generacion\generador_salida.py
```

---

### 2. `consejeras/echo/logica.py`

**Cambios principales:**
- Método `verificar_respuesta_llm()` para verificar Groq
- Integración con `verificador_coherencia.py`
- Lazy loading del verificador

**Copiar:**
```powershell
copy consejeras_echo_logica.py consejeras\echo\logica.py
```

---

### 3. `main.py`

**Cambios principales:**
- Flag `--use-groq` para activar Groq
- Comando `groq` para ver estadísticas
- Comando `toggle_groq` para cambiar en runtime
- Logging mejorado en modo verbose

**Copiar:**
```powershell
copy main.py main.py
```

---

## 🚀 INSTALACIÓN

### PASO 1: Hacer backup

```powershell
# Crear carpeta de backup
mkdir backups\semana2

# Backup de archivos originales
copy generacion\generador_salida.py backups\semana2\
copy consejeras\echo\logica.py backups\semana2\
copy main.py backups\semana2\
```

### PASO 2: Copiar archivos nuevos

```powershell
# Copiar archivos modificados
copy generacion_generador_salida.py generacion\generador_salida.py
copy consejeras_echo_logica.py consejeras\echo\logica.py
copy main.py main.py

# Copiar test
copy test_integracion_groq.py test_integracion_groq.py
```

### PASO 3: Ejecutar tests

```powershell
python test_integracion_groq.py
```

**Resultado esperado:**
```
================================================================================
TEST SUITE - INTEGRACIÓN GROQ - FASE 4A SEMANA 3-4
================================================================================

TEST 1: IMPORTACIONES
--------------------------------------------------------------------------------
✅ GeneradorSalida importado
✅ Echo importado
✅ VerificadorCoherenciaEcho importado
✅ GroqWrapper importado

✅ TODAS LAS IMPORTACIONES EXITOSAS

TEST 2: GENERADOR SIMBÓLICO
--------------------------------------------------------------------------------
✅ Generador creado (modo legacy)
✅ Respuesta generada: "..."
✅ Estadísticas correctas

✅ GENERADOR SIMBÓLICO FUNCIONA

TEST 3: ECHO VERIFICADOR
--------------------------------------------------------------------------------
✅ Verificador creado
✅ Texto válido aprobado
✅ Basura detectada
✅ Capacidad inventada detectada

✅ ECHO VERIFICADOR FUNCIONA

TEST 4: FLUJO COMPLETO (SIMULADO)
--------------------------------------------------------------------------------
✅ Generador creado (modo Groq)
✅ Respuesta generada: "..."
✅ Stats: 1 generadas, 1 fallbacks

✅ FLUJO COMPLETO FUNCIONA

================================================================================
RESUMEN DE TESTS
================================================================================
✅ Importaciones
✅ Generador Simbólico
✅ Echo Verificador
✅ Flujo Completo

Total: 4 tests
✅ Pasados: 4
❌ Fallidos: 0

🎉 ¡TODOS LOS TESTS PASARON!
✅ Fase 4A Semana 3-4 lista para producción
================================================================================
```

---

## 🎮 USO

### MODO 1: Legacy (Sin Groq)

```powershell
# Iniciar Bell sin Groq (modo actual)
python main.py
```

Bell usa generación simbólica pura. Ideal para:
- Testing sin API key
- Desarrollo offline
- Comparar con modo Groq

---

### MODO 2: Con Groq (Modo Mente Pura)

```powershell
# Iniciar Bell con Groq
python main.py --use-groq
```

Bell usa Groq para embellecer. Requiere:
- API key configurada en `.env`
- Internet activo
- Groq SDK instalado

---

### MODO 3: Comparación en Runtime

```powershell
python main.py
```

Dentro de la conversación:
```
🧑 Tú: toggle_groq
   Groq: ON (Mente Pura)

🧑 Tú: hola
🌿 Bell: ¡Hola! ¿En qué puedo ayudarte hoy?

🧑 Tú: toggle_groq
   Groq: OFF (Legacy)

🧑 Tú: hola
🌿 Bell: Hola.
```

---

## 📊 COMANDOS NUEVOS

### `groq` - Ver estado de Groq

```
🧑 Tú: groq

================================================================================
ESTADO DE GROQ - FASE 4A
================================================================================

✅ Groq: ACTIVADO (Modo Mente Pura)
   • Total generadas: 15
   • Groq usadas: 12
   • Groq bloqueadas: 2
   • Fallback a simbólico: 1
   • Tasa uso Groq: 80.0%
   • Tasa bloqueo Echo: 16.7%
================================================================================
```

---

### `toggle_groq` - Cambiar modo en runtime

```
🧑 Tú: toggle_groq
   Groq: ON (Mente Pura)
```

Cambia entre:
- **ON**: Bell → Groq → Echo
- **OFF**: Bell → Respuesta directa

---

### `stats` - Estadísticas mejoradas

Ahora incluye información de Groq:

```
🧑 Tú: stats

================================================================================
ESTADÍSTICAS DEL SISTEMA
================================================================================

📚 Vocabulario
  Total: 465 | Grounding 1.0: 87

🧠 Grounding 9D
  Extensiones en cache: 15

🎨 Generación (Fase 4A)
  Groq: ON
  Tasa uso: 80.0%
  Tasa bloqueo: 16.7%

💬 Conversación
  Turnos: 15
================================================================================
```

---

## 🧪 CASOS DE PRUEBA

### Test 1: Respuesta básica

```
🧑 Tú: puedes leer archivos?
🌿 Bell: Sí, puedo leer archivos. Tengo acceso a operaciones de lectura...
```

**Verificar:**
- Respuesta en lenguaje natural
- Sin "STATUS: OK" ni formato robótico
- Menciona capacidad correcta

---

### Test 2: Detección de basura

```
🧑 Tú: lee el archivo test.txt
```

Si Groq responde con basura:
```
"Los números primos son: 2, 3, 5, 7, 11..."
```

Echo debe detectarlo y usar respuesta simbólica:
```
🌿 Bell: He leído el archivo test.txt.
```

---

### Test 3: Capacidades inventadas

```
🧑 Tú: toma una foto
```

Si Groq inventa capacidades:
```
"He tomado una foto con mi cámara integrada"
```

Echo debe bloquearlo:
```
🌿 Bell: No puedo tomar fotos. No tengo acceso a hardware de cámara.
```

---

## 📈 MÉTRICAS DE ÉXITO

### ✅ Tests deben pasar

```powershell
python test_integracion_groq.py
# Resultado: 4/4 tests pasando
```

---

### ✅ Tasa de uso de Groq > 70%

```
🧑 Tú: stats

Tasa uso: 80.0%  ← Debe ser > 70%
```

Significa que Groq se usa la mayoría del tiempo.

---

### ✅ Tasa de bloqueo < 20%

```
🧑 Tú: groq

Tasa bloqueo Echo: 16.7%  ← Debe ser < 20%
```

Significa que Echo bloquea menos del 20% de respuestas de Groq.

---

## 🐛 TROUBLESHOOTING

### Error: "No module named 'groq'"

**Solución:**
```powershell
pip install groq --break-system-packages
```

---

### Error: "GROQ_API_KEY not found"

**Solución:**
```powershell
# Verificar .env
type .env | findstr GROQ_API_KEY

# Si no está, agregarlo
notepad .env
```

Agregar:
```
GROQ_API_KEY=gsk_tu_key_aqui
```

---

### Groq siempre usa fallback

**Diagnóstico:**
```
🧑 Tú: verbose
🧑 Tú: hola
```

Buscar en output:
```
⚠️  Groq falló, usando respuesta simbólica: [error]
```

**Soluciones:**
1. Verificar API key
2. Verificar internet
3. Ver logs en `logs/fase4a/groq_interactions.jsonl`

---

### Echo bloquea demasiado (>30%)

**Diagnóstico:**
```
🧑 Tú: groq
Tasa bloqueo Echo: 45%  ← Muy alto
```

**Posibles causas:**
1. Groq está alucinando mucho
2. Whitelist muy restrictiva
3. Verificador muy estricto

**Solución:**
Revisar logs y ajustar whitelist si es necesario.

---

## 🎉 COMPLETADO CUANDO...

✅ Todos los tests pasan (4/4)  
✅ Tasa uso Groq > 70%  
✅ Tasa bloqueo Echo < 20%  
✅ Bell responde naturalmente  
✅ No hay errores en logs

---

## 📚 SIGUIENTE PASO

Una vez completada Semana 3-4:

**SEMANA 5-6: BUCLES PROACTIVOS**
- Iris analiza código automáticamente
- Nova propone conceptos nuevos
- Aprendizaje sin LLM

---

## 💡 TIPS

1. **Usa verbose durante desarrollo**
   ```powershell
   python main.py --use-groq --verbose
   ```

2. **Compara modos con toggle_groq**
   - Prueba la misma pregunta en ambos modos
   - Observa diferencias de naturalidad

3. **Revisa logs regularmente**
   ```powershell
   type logs\fase4a\groq_interactions.jsonl
   ```

4. **Haz backup antes de modificar**
   - Siempre guarda versión anterior
   - Fácil rollback si hay problemas

---

**¿Preguntas? ¡Consulta la guía o ejecuta `help` en Bell!** 🌿