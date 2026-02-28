# 📅 SEMANA 1 - FASE 4A: PREPARACIÓN Y LIMPIEZA (ACTUALIZADA)

**Fecha inicio**: 16 de Febrero, 2026  
**Objetivos**: Limpiar código obsoleto, configurar Groq con .env, verificar todo  
**Duración**: 5-7 días

---

## 🎯 CAMBIOS IMPORTANTES

### ✅ Ahora usamos `.env` en vez de variables de sistema
- **Más seguro**: No expones tu API key en variables globales
- **Más portable**: El archivo .env viaja con el proyecto
- **Más fácil**: Solo copias y pegas tu key

### ✅ Verificador de Echo fusionado
- Combina verificación original de Bell
- Agrega verificación de Groq
- Un solo archivo: `verificador_coherencia_v2.py`

---

## 📋 CHECKLIST ACTUALIZADO

### DÍA 1: Limpieza
- [ ] Ejecutar `python scripts/cleanup_fase4a.py`
- [ ] Verificar limpieza exitosa

### DÍA 2: Configurar Groq (.env)
- [ ] Crear cuenta en https://console.groq.com
- [ ] Obtener API Key
- [ ] Copiar `.env.example` → `.env`
- [ ] Pegar API Key en `.env`

### DÍA 3: Tests
- [ ] Ejecutar `python test_semana1.py`
- [ ] Verificar que todos los tests pasen

### DÍA 4-5: Pruebas Manuales
- [ ] Probar Groq (si tests pasaron)
- [ ] Probar Echo
- [ ] Revisar logs

---

## 🔧 INSTRUCCIONES PASO A PASO

### PASO 1: Ejecutar Limpieza

```bash
cd C:\Users\Sebas\BELLADONNA
python scripts\cleanup_fase4a.py
```

**Resultado esperado:**
```
✅ Eliminada carpeta expresion/
✅ Archivada carpeta _legacy/ → _archive/_legacy/
✅ Desactivado llm/gestor_llm.py (.old)
...
RESUMEN DE LIMPIEZA
✅ Cambios realizados: 8
❌ Errores encontrados: 0
```

---

### PASO 2: Configurar .env (NUEVO)

#### 2.1. Obtener API Key de Groq

1. Ve a https://console.groq.com
2. Crea cuenta (gratis)
3. Navega a "API Keys"
4. Crea una nueva key
5. **Copia la key** (solo se muestra una vez)

#### 2.2. Crear archivo .env

**Opción A: Copiar desde ejemplo**
```bash
cd C:\Users\Sebas\BELLADONNA
copy .env.example .env
```

**Opción B: Crear manualmente**

Crea un archivo llamado `.env` en la raíz con este contenido:

```bash
# CONFIGURACIÓN DE GROQ - FASE 4A
GROQ_API_KEY=gsk_AQUI_TU_KEY_REAL

# Configuración del modelo
GROQ_MODEL=llama-3.2-90b-text-preview
GROQ_TEMPERATURE=0.3
GROQ_MAX_TOKENS=500
GROQ_TIMEOUT=10

# Rutas de archivos
BELL_WHITELIST_PATH=data/BELL_WHITELIST.json
GROQ_CONFIG_PATH=config/groq_config.json

# Logging
ENABLE_LOGGING=true
LOG_PATH=logs/fase4a/groq_interactions.jsonl
```

**⚠️ IMPORTANTE:**
- Reemplaza `gsk_AQUI_TU_KEY_REAL` con tu key real de Groq
- NO subas `.env` a GitHub (ya está en .gitignore)
- `.env.example` es solo plantilla (sin keys reales)

#### 2.3. Verificar Configuración

```bash
python config/config_manager.py
```

**Resultado esperado:**
```
==============================================================
CONFIGURACIÓN ACTUAL - FASE 4A
==============================================================
Proyecto root: C:\Users\Sebas\BELLADONNA
Archivo .env: C:\Users\Sebas\BELLADONNA\.env

Groq:
  API Key: ✅ Configurada
  Modelo: llama-3.2-90b-text-preview
  Temperatura: 0.3
  Max Tokens: 500

✅ Configuración válida!
```

---

### PASO 3: Ejecutar Tests Completos

```bash
python test_semana1.py
```

**Este test verifica:**
- ✅ Estructura de carpetas
- ✅ Archivos creados
- ✅ Archivo .env configurado
- ✅ ConfigManager funciona
- ✅ Groq wrapper se importa
- ✅ Verificador Echo funciona
- ✅ Whitelist es válida
- ✅ Flujo completo Bell → Groq → Echo

**Resultado esperado:**
```
================================================================================
 TEST SUITE - SEMANA 1 FASE 4A
================================================================================

📁 TESTS DE ESTRUCTURA
--------------------------------------------------------------------------------
  ✅ Carpeta existe: config
  ✅ Carpeta existe: data
  ✅ Carpeta existe: logs/fase4a
  ...

⚙️  TESTS DE CONFIGURACIÓN
--------------------------------------------------------------------------------
  ✅ .env.example existe
  ✅ .env configurado
  ✅ GROQ_API_KEY está configurada
  ...

🧪 TESTS DE MÓDULOS
--------------------------------------------------------------------------------
  ✅ GroqWrapper importado
  ✅ VerificadorCoherenciaEcho importado
  ✅ Verificador aprueba texto válido
  ✅ Verificador detecta basura
  ...

🔗 TESTS DE INTEGRACIÓN
--------------------------------------------------------------------------------
  ✅ Flujo completo funciona: Bell → Groq → Echo → User

================================================================================
 RESUMEN DE TESTS
================================================================================
Total de tests: 20
✅ Pasados: 20
❌ Fallidos: 0

🎉 ¡TODOS LOS TESTS PASARON!
✅ Semana 1 está COMPLETA y lista para usar
```

---

### PASO 4: Pruebas Manuales (Opcional)

Si todos los tests pasaron, puedes probar manualmente:

#### Test de Groq

```bash
python llm/groq_wrapper.py
```

**Resultado:**
```
🧪 Probando GroqWrapper...

📤 Enviando a Groq:
{
  "tipo": "CAPACIDAD",
  "capacidad": true,
  ...
}

📥 Respuesta de Groq:
Texto: He leído el archivo test.txt (1 KB)...
Tokens: 45
Latencia: 342ms

✅ Test exitoso!
```

#### Test de Echo

```bash
python consejeras/echo/verificador_coherencia_v2.py
```

**Resultado:**
```
🧪 Testing VerificadorCoherenciaEcho FUSIONADO...

==========================================================
✅ Test 1: Basura del LLM
==========================================================
Original: La lógica de los números primos...
Coherente: False
Confianza: 0.0
Acción: BLOQUEAR
Fallback: ¡Hola! ¿En qué puedo ayudarte?

==========================================================
✅ Test 2: Respuesta válida
==========================================================
Original: ¡Hola! ¿En qué puedo ayudarte?
Coherente: True
Confianza: 1.0
Acción: PERMITIR
```

---

## 📊 VERIFICACIÓN DE ÉXITO

Al final de la Semana 1, debes tener:

### ✅ Archivos Creados
- [x] `scripts/cleanup_fase4a.py`
- [x] `llm/groq_wrapper.py`
- [x] `consejeras/echo/verificador_coherencia_v2.py`
- [x] `data/BELL_WHITELIST.json`
- [x] `config/groq_config.json`
- [x] `config/config_manager.py`
- [x] `.env.example`
- [x] `.env` (con tu API key)
- [x] `test_semana1.py`

### ✅ Tests Pasados
```bash
python test_semana1.py
# Resultado: 20/20 tests pasados
```

---

## 🚨 SOLUCIÓN DE PROBLEMAS

### Error: "GROQ_API_KEY no configurada"

**Causa**: No creaste el archivo `.env` o tiene el valor de ejemplo.

**Solución:**
```bash
# 1. Verifica que .env existe
dir .env

# 2. Abre .env y verifica que tiene tu key real
notepad .env

# 3. Debe verse así:
GROQ_API_KEY=gsk_TuKeyRealAqui123456789
```

### Error: "No se puede leer .env"

**Causa**: Archivo `.env` tiene formato incorrecto.

**Solución:**
- Verifica que cada línea sea `KEY=VALUE`
- No uses espacios alrededor del `=`
- No uses comillas extras

**Correcto:**
```
GROQ_API_KEY=gsk_123
```

**Incorrecto:**
```
GROQ_API_KEY = "gsk_123"   ❌ (espacios y comillas)
```

### Error: "Groq SDK no instalado"

**Solución:**
```bash
pip install groq --break-system-packages
```

---

## 📈 PRÓXIMOS PASOS (SEMANA 2)

Una vez que `test_semana1.py` pase todos los tests:

1. **Integrar con main.py**
   - Modificar `generacion/generador_salida.py`
   - Agregar flujo: Bell → Groq → Echo

2. **Logging completo**
   - Guardar todas las interacciones
   - Monitorear alucinaciones detectadas

3. **Tests de integración**
   - Probar con casos reales
   - Verificar latencia

---

**✅ ¡Listo para Semana 1!**  
**Comando final**: `python test_semana1.py`  
**Siguiente**: Semana 2 - Integración