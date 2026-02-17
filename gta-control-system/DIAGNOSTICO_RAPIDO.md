# 🔍 Diagnóstico Rápido - Sistema de Control GTA V

Esta guía te ayudará a verificar que todo esté funcionando correctamente.

## ✅ Checklist de Verificación

### 1. Dashboard Funcionando

```bash
cd gta-control-system/dashboard
node app.js
```

**Deberías ver:**
```
╔════════════════════════════════════════════════════════╗
║   🎮 GTA V DASHBOARD PILLAR V7 - INICIADO            ║
╠════════════════════════════════════════════════════════╣
║   🌐 URL: http://0.0.0.0:3000                         ║
║   📁 Archivo de comando: H:\Games\Grand Theft Auto...║
║   ⚡ Rate Limit: 500ms entre comandos                 ║
║   🎯 Comandos disponibles: 200+                       ║
╚════════════════════════════════════════════════════════╝
```

**Test:**
1. Abre `http://localhost:3000` en tu navegador
2. Deberías ver el panel de control con botones

✅ **Funciona** | ❌ **No funciona** → Ver [Problema 1](#problema-1-dashboard-no-inicia)

---

### 2. API Respondiendo

Abre en tu navegador:
```
http://localhost:3000/api/status
```

**Deberías ver:**
```json
{
  "status": "online",
  "version": "7.0.0",
  "uptime": 123.45,
  "commandsThisMinute": 0,
  "features": {
    "priorityQueue": true,
    "autoCleanup": true,
    "fadeEffects": true,
    "debugMode": true
  },
  "totalCommands": 200
}
```

✅ **Funciona** | ❌ **No funciona** → Ver [Problema 2](#problema-2-api-no-responde)

---

### 3. Archivo de Comando Creándose

1. Haz clic en cualquier botón del dashboard (ej: "❤️ CURAR")
2. Navega a: `H:\Games\Grand Theft Auto V\`
3. Debería aparecer el archivo `comando_gta.json`

**Contenido esperado:**
```json
{
  "accion": "curar",
  "timestamp": 1234567890,
  "prioridad": 1
}
```

✅ **Se crea** | ❌ **No se crea** → Ver [Problema 3](#problema-3-archivo-no-se-crea)

---

### 4. Script de Python Cargado en GTA V

1. Abre GTA V
2. Presiona `Insert` para abrir la consola de ScriptHookVDotNet
3. Deberías ver en la lista: `escucha_dashboard.py`

**Comandos útiles en la consola:**
```
list                    # Ver scripts cargados
reload escucha_dashboard # Recargar el script
```

✅ **Cargado** | ❌ **No cargado** → Ver [Problema 4](#problema-4-script-no-se-carga)

---

### 5. Comando Ejecutándose en el Juego

**Test completo:**

1. ✅ Dashboard corriendo
2. ✅ GTA V abierto (modo historia)
3. ✅ Script de Python cargado
4. Haz clic en "❤️ CURAR" en el dashboard
5. Tu personaje debería curarse instantáneamente

✅ **Funciona** | ❌ **No funciona** → Ver [Problema 5](#problema-5-comandos-no-se-ejecutan)

---

## 🛠️ Solución de Problemas

### Problema 1: Dashboard No Inicia

**Error: "Cannot find module 'express'"**

**Solución:**
```bash
cd gta-control-system/dashboard
npm install
```

**Error: "Port 3000 already in use"**

**Solución:**
1. Cierra cualquier otra aplicación usando el puerto 3000
2. O cambia el puerto en [`config.json`](dashboard/config.json):
```json
{
  "server": {
    "port": 3001
  }
}
```

---

### Problema 2: API No Responde

**Causa:** El dashboard no está corriendo

**Solución:**
```bash
cd gta-control-system/dashboard
node app.js
```

Mantén esta ventana abierta mientras usas el sistema.

---

### Problema 3: Archivo No Se Crea

**Diagnóstico:**

1. Verifica la ruta en [`config.json`](dashboard/config.json):
```json
{
  "paths": {
    "commandFile": "H:\\Games\\Grand Theft Auto V\\comando_gta.json"
  }
}
```

2. **Ajusta la ruta** a donde tienes instalado GTA V:
   - Steam: `C:\\Program Files (x86)\\Steam\\steamapps\\common\\Grand Theft Auto V\\comando_gta.json`
   - Epic Games: `C:\\Program Files\\Epic Games\\GTAV\\comando_gta.json`
   - Rockstar: `C:\\Program Files\\Rockstar Games\\Grand Theft Auto V\\comando_gta.json`

3. **Usa doble barra invertida** (`\\`) en Windows

4. **Reinicia el dashboard** después de cambiar la configuración

**Test manual:**

Crea el archivo manualmente para verificar permisos:
```bash
# En PowerShell, desde la carpeta de GTA V
echo '{"accion":"test","timestamp":123,"prioridad":1}' > comando_gta.json
```

Si no puedes crear el archivo, verifica permisos de escritura en la carpeta.

---

### Problema 4: Script No Se Carga

**Causa 1: ScriptHookVDotNet no instalado**

**Solución:**
1. Descarga ScriptHookVDotNet: http://www.dev-c.com/gtav/scripthookv/
2. Extrae `ScriptHookVDotNet.asi` y `ScriptHookVDotNet2.dll` en la carpeta de GTA V
3. Reinicia GTA V

**Causa 2: Script en ubicación incorrecta**

**Solución:**
1. Crea la carpeta `scripts` en la raíz de GTA V si no existe:
   ```
   H:\Games\Grand Theft Auto V\scripts\
   ```
2. Copia [`escucha_dashboard.py`](scripts/escucha_dashboard.py) a esa carpeta
3. Reinicia GTA V

**Causa 3: Ruta incorrecta en el script**

**Solución:**
1. Abre [`escucha_dashboard.py`](scripts/escucha_dashboard.py)
2. Verifica la línea 24:
```python
ARCHIVO_RUTA = "H:\\Games\\Grand Theft Auto V\\comando_gta.json"
```
3. Ajusta a tu ruta de instalación
4. Guarda y recarga el script en GTA V

---

### Problema 5: Comandos No Se Ejecutan

**Diagnóstico paso a paso:**

#### Paso 1: Verificar que el archivo se crea
```bash
# Haz clic en un botón del dashboard
# Luego verifica:
dir "H:\Games\Grand Theft Auto V\comando_gta.json"
```

✅ **Se crea** → Continúa al Paso 2
❌ **No se crea** → Ver [Problema 3](#problema-3-archivo-no-se-crea)

#### Paso 2: Verificar que el script lee el archivo

1. Abre GTA V
2. Presiona `Insert` para abrir la consola
3. Escribe: `reload escucha_dashboard`
4. Haz clic en un botón del dashboard
5. Verifica que el archivo `comando_gta.json` desaparezca

✅ **Desaparece** → El script está leyendo
❌ **No desaparece** → El script no está leyendo

**Si no desaparece:**
- Verifica que la ruta en el script sea correcta
- Verifica que el script esté cargado (`list` en la consola)
- Revisa `ScriptHookVDotNet.log` para errores

#### Paso 3: Verificar que el comando se ejecuta

1. Haz clic en "❤️ CURAR"
2. Tu personaje debería curarse

✅ **Se cura** → ¡Todo funciona!
❌ **No se cura** → Verifica que estés en modo historia (no online)

---

## 🔍 Logs y Debugging

### Ver Logs del Dashboard

El dashboard muestra logs en tiempo real:
```
[2024-01-15T10:30:45.123Z] Comando ejecutado: curar (Prioridad: 1)
```

Para ver más detalles, activa `debugMode` en [`config.json`](dashboard/config.json):
```json
{
  "features": {
    "debugMode": true
  }
}
```

### Ver Logs de GTA V

Revisa el archivo:
```
H:\Games\Grand Theft Auto V\ScriptHookVDotNet.log
```

Busca errores relacionados con `escucha_dashboard.py`.

### Test Manual del Script

Crea manualmente el archivo de comando:

```bash
# En PowerShell
cd "H:\Games\Grand Theft Auto V"
echo '{"accion":"curar","timestamp":1234567890,"prioridad":1}' > comando_gta.json
```

Si el script funciona, el archivo desaparecerá y tu personaje se curará.

---

## 📊 Test de Integración Completa

### Test 1: Dashboard → Archivo

```bash
# 1. Inicia el dashboard
cd gta-control-system/dashboard
node app.js

# 2. En otro terminal, monitorea el archivo
cd "H:\Games\Grand Theft Auto V"
while ($true) { if (Test-Path comando_gta.json) { Get-Content comando_gta.json; Start-Sleep -Seconds 1 } }
```

Haz clic en un botón del dashboard. Deberías ver el contenido del archivo.

### Test 2: Archivo → GTA V

```bash
# 1. Abre GTA V con el script cargado
# 2. En PowerShell, crea el archivo manualmente
cd "H:\Games\Grand Theft Auto V"
echo '{"accion":"curar","timestamp":1234567890,"prioridad":1}' > comando_gta.json
```

Tu personaje debería curarse y el archivo desaparecer.

### Test 3: Dashboard → GTA V (Completo)

1. ✅ Dashboard corriendo
2. ✅ GTA V abierto (modo historia)
3. ✅ Script cargado
4. Haz clic en "❤️ CURAR"
5. ✅ Personaje se cura

---

## 🎯 Comandos de Prueba Recomendados

Prueba estos comandos en orden para verificar diferentes funcionalidades:

1. **❤️ CURAR** - Test básico de salud
2. **🛡️ BLINDAJE** - Test de armadura
3. **☀️ SOLEADO** - Test de clima
4. **🏎️ T20** - Test de spawn de vehículo
5. **📍 MAZE BANK** - Test de teleport
6. **⭐ 1 ESTRELLA** - Test de nivel de búsqueda
7. **♻️ LIMPIAR MAPA** - Test de limpieza

Si todos funcionan, ¡el sistema está perfecto!

---

## 🚀 Integración con TikTok

Una vez que todo funcione localmente, puedes integrar con TikTok:

### Opción 1: TikTok Live Bridge (Automático)

```bash
cd gta-control-system/tiktok-bridge
npm install
node tiktok_listener.js TU_USUARIO_TIKTOK
```

Ver: [README del TikTok Bridge](tiktok-bridge/README.md)

### Opción 2: Manual con OBS

1. Agrega el dashboard como Browser Source en OBS
2. Haz clic en los botones durante el stream
3. Los espectadores ven el panel y tú ejecutas comandos

Ver: [Guía de Streamer.bot](streamerbot/TIKTOK_STREAMERBOT_SETUP.md)

---

## 📝 Checklist Final

Antes de hacer stream, verifica:

- [ ] Dashboard corriendo en `http://localhost:3000`
- [ ] API responde en `/api/status`
- [ ] Archivo de comando se crea correctamente
- [ ] Script de Python cargado en GTA V
- [ ] Comandos se ejecutan en el juego
- [ ] TikTok Bridge conectado (si usas integración automática)
- [ ] GTA V en modo historia (NO online)
- [ ] Tienes un plan de qué comandos usar para cada regalo

---

## ❓ Preguntas Frecuentes

### ¿Por qué el archivo desaparece tan rápido?

Es normal. El script de Python lo lee y lo borra inmediatamente para evitar ejecutar el mismo comando dos veces.

### ¿Puedo ver el archivo antes de que desaparezca?

Sí, desactiva la eliminación automática temporalmente:

En [`escucha_dashboard.py`](scripts/escucha_dashboard.py), comenta la línea:
```python
# File.Delete(ARCHIVO_RUTA)  # Comentar para debugging
```

**Recuerda descomentarla después** o los comandos se ejecutarán en bucle.

### ¿Qué hago si el juego se crashea?

1. Reduce la frecuencia de comandos
2. Usa el comando "♻️ LIMPIAR MAPA" regularmente
3. Verifica que no haya demasiadas entidades spawneadas
4. Revisa `ScriptHookVDotNet.log` para errores

### ¿Puedo usar esto en GTA Online?

⚠️ **NO RECOMENDADO**. Usar mods en GTA Online puede resultar en ban permanente.

---

**¿Aún tienes problemas?** Consulta la [guía de troubleshooting completa](docs/TROUBLESHOOTING.md)
