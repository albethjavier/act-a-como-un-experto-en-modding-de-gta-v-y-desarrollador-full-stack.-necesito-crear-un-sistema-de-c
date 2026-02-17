# 🚀 Guía de Instalación Completa - GTA V Control System

## 📋 Requisitos del Sistema

### Hardware Mínimo
- **CPU**: Intel Core i5 / AMD Ryzen 5
- **RAM**: 8 GB
- **GPU**: NVIDIA GTX 660 / AMD HD 7870
- **Disco**: 100 GB libres (para GTA V + sistema)

### Software Requerido

| Software | Versión | Descarga |
|----------|---------|----------|
| GTA V | Última | Steam/Epic/Rockstar |
| Node.js | 18+ | https://nodejs.org |
| ScriptHookV | Última | http://www.dev-c.com/gtav/scripthookv/ |
| ScriptHookVDotNet | 2.10+ | https://github.com/crosire/scripthookvdotnet |
| Python para SHVDN | Última | Incluido en SHVDN |
| Streamer.bot | Última | https://streamer.bot (opcional) |

---

## 📦 Paso 1: Instalar GTA V y Mods Base

### 1.1 Verificar Instalación de GTA V

```bash
# Ubicación típica:
C:\Program Files\Steam\steamapps\common\Grand Theft Auto V
# o
C:\Program Files\Epic Games\GTAV
# o
H:\Games\Grand Theft Auto V
```

**Importante**: Anota tu ruta de instalación, la necesitarás después.

### 1.2 Instalar ScriptHookV

1. Descargar de: http://www.dev-c.com/gtav/scripthookv/
2. Extraer el archivo ZIP
3. Copiar estos archivos a la carpeta raíz de GTA V:
   ```
   ScriptHookV.dll
   dinput8.dll
   ```

### 1.3 Instalar ScriptHookVDotNet

1. Descargar de: https://github.com/crosire/scripthookvdotnet/releases
2. Extraer el archivo ZIP
3. Copiar estos archivos a la carpeta raíz de GTA V:
   ```
   ScriptHookVDotNet.asi
   ScriptHookVDotNet2.dll
   ScriptHookVDotNet3.dll (si está disponible)
   ```

### 1.4 Instalar Python para SHVDN

1. En el mismo ZIP de ScriptHookVDotNet, buscar:
   ```
   Python3.shvdn
   ```
2. Copiar a la carpeta raíz de GTA V

### 1.5 Crear Carpeta de Scripts

```bash
# En la carpeta de GTA V, crear:
mkdir scripts
```

**Estructura final**:
```
H:\Games\Grand Theft Auto V\
├── GTA5.exe
├── ScriptHookV.dll
├── dinput8.dll
├── ScriptHookVDotNet.asi
├── ScriptHookVDotNet2.dll
├── Python3.shvdn
└── scripts\
    └── (aquí irán los scripts de Python)
```

---

## 🖥️ Paso 2: Instalar Dashboard (Node.js)

### 2.1 Instalar Node.js

1. Descargar de: https://nodejs.org
2. Ejecutar instalador
3. Verificar instalación:
   ```bash
   node --version
   # Debe mostrar: v18.x.x o superior
   ```

### 2.2 Descargar el Sistema

```bash
# Opción A: Clonar repositorio (si está en Git)
git clone https://github.com/tu-usuario/gta-control-system.git
cd gta-control-system

# Opción B: Descargar ZIP y extraer
# Luego navegar a la carpeta
cd gta-control-system
```

### 2.3 Instalar Dependencias del Dashboard

```bash
cd dashboard
npm install
```

Esto instalará:
- express
- cors
- helmet

### 2.4 Configurar Rutas

Editar `dashboard/config.json`:

```json
{
  "paths": {
    "commandFile": "H:\\Games\\Grand Theft Auto V\\comando_gta.json",
    "queueFile": "H:\\Games\\Grand Theft Auto V\\cola_espera.json"
  }
}
```

**⚠️ IMPORTANTE**: Cambiar `H:\\Games\\Grand Theft Auto V\\` por tu ruta real de GTA V.

---

## 🐍 Paso 3: Instalar Scripts de Python

### 3.1 Copiar Scripts al Juego

```bash
# Desde la carpeta raíz del proyecto:
# Copiar todos los archivos .py de scripts/ a la carpeta scripts/ de GTA V

# Windows (PowerShell):
Copy-Item scripts\*.py "H:\Games\Grand Theft Auto V\scripts\"

# O manualmente:
# Copiar estos archivos:
scripts/escucha_dashboard.py → H:\Games\Grand Theft Auto V\scripts\
scripts/gestor_prioridad.py → H:\Games\Grand Theft Auto V\scripts\
```

### 3.2 Editar Rutas en Scripts de Python

Abrir `escucha_dashboard.py` y verificar:

```python
ARCHIVO_RUTA = "H:\\Games\\Grand Theft Auto V\\comando_gta.json"
```

Cambiar por tu ruta real si es diferente.

Hacer lo mismo en `gestor_prioridad.py`:

```python
ARCHIVO_COMANDO = "H:\\Games\\Grand Theft Auto V\\comando_gta.json"
ARCHIVO_COLA = "H:\\Games\\Grand Theft Auto V\\cola_espera.json"
```

---

## 🎮 Paso 4: Primera Prueba

### 4.1 Iniciar Dashboard

```bash
cd dashboard
node app.js
```

Deberías ver:
```
╔════════════════════════════════════════════════════════╗
║   🎮 GTA V DASHBOARD PILLAR V7 - INICIADO            ║
╠════════════════════════════════════════════════════════╣
║   🌐 URL: http://0.0.0.0:3000                         ║
║   📁 Archivo de comando: H:\Games\Grand Theft...     ║
║   ⚡ Rate Limit: 500ms entre comandos                 ║
║   🎯 Comandos disponibles: 200+                       ║
╚════════════════════════════════════════════════════════╝
```

### 4.2 Abrir Dashboard en Navegador

```
http://localhost:3000
```

Deberías ver la interfaz con todos los botones.

### 4.3 Iniciar GTA V

1. Abrir GTA V
2. Cargar modo historia (NO GTA Online)
3. Esperar a que cargue completamente

### 4.4 Verificar que el Script se Cargó

Presionar `F4` en GTA V para abrir la consola de SHVDN.

Deberías ver algo como:
```
[INFO] Loaded script: escucha_dashboard.py
```

Si no aparece, revisar:
```
H:\Games\Grand Theft Auto V\ScriptHookVDotNet.log
```

### 4.5 Probar Primer Comando

1. En el navegador, presionar el botón **"❤️ CURAR"**
2. En GTA V, tu personaje debería curarse instantáneamente

**✅ Si funciona**: ¡Instalación exitosa!

**❌ Si no funciona**: Ver [Troubleshooting](docs/TROUBLESHOOTING.md)

---

## 🎁 Paso 5: Configurar Streamer.bot (Opcional)

### 5.1 Instalar Streamer.bot

1. Descargar de: https://streamer.bot
2. Instalar y abrir
3. Conectar tu cuenta de TikTok:
   - Platforms → TikTok → Connect

### 5.2 Importar Configuración

Ver guía completa en: [streamerbot/SETUP_GUIDE.md](streamerbot/SETUP_GUIDE.md)

Resumen rápido:
1. Crear acción base `GTA_Ejecutar_Comando`
2. Agregar código C# proporcionado
3. Crear triggers para regalos de TikTok
4. Mapear regalos a comandos

---

## 🔧 Paso 6: Configuración Avanzada

### 6.1 Ajustar Rate Limiting

Si recibes muchos comandos simultáneos, editar `dashboard/config.json`:

```json
{
  "security": {
    "rateLimitMs": 1000,  // Aumentar a 1 segundo
    "maxCommandsPerMinute": 30  // Reducir a 30
  }
}
```

### 6.2 Activar Modo Debug

```json
{
  "features": {
    "debugMode": true
  }
}
```

Esto mostrará logs detallados en la consola del dashboard.

### 6.3 Configurar Limpieza Automática

En `escucha_dashboard.py`:

```python
INTERVALO_LIMPIEZA = 60  # Segundos entre limpiezas
# Reducir a 30 si tienes PC con poca RAM
```

---

## 📊 Paso 7: Verificación Final

### Checklist de Instalación

- [ ] GTA V instalado y funcionando
- [ ] ScriptHookV instalado (archivos .dll en carpeta de GTA)
- [ ] ScriptHookVDotNet instalado (archivos .asi y .dll)
- [ ] Python3.shvdn en carpeta de GTA
- [ ] Carpeta `scripts/` creada
- [ ] Scripts de Python copiados a `scripts/`
- [ ] Node.js instalado (v18+)
- [ ] Dashboard instalado (`npm install` ejecutado)
- [ ] Rutas configuradas en `config.json`
- [ ] Dashboard corriendo en puerto 3000
- [ ] GTA V abierto en modo historia
- [ ] Script cargado (verificado con F4)
- [ ] Comando de prueba funciona (curar)

### Pruebas Recomendadas

1. **Curación**: Botón "❤️ CURAR"
2. **Vehículo**: Botón "T20"
3. **Clima**: Botón "☀️ SOLEADO"
4. **Teleport**: Botón "🏢 MAZE BANK"
5. **Ataque**: Botón "🧟 10 ZOMBIES"

Si todos funcionan: **✅ Sistema completamente operativo**

---

## 🎯 Próximos Pasos

1. **Personalizar comandos**: Editar `app.js` para agregar tus propios botones
2. **Configurar TikTok**: Seguir guía de Streamer.bot
3. **Crear combos**: Mapear regalos caros a secuencias de comandos
4. **Optimizar**: Ajustar rate limits según tu hardware

---

## 📚 Documentación Adicional

- [Lista Completa de Comandos](docs/COMMANDS.md)
- [Guía de Streamer.bot](streamerbot/SETUP_GUIDE.md)
- [Solución de Problemas](docs/TROUBLESHOOTING.md)
- [README Principal](README.md)

---

## 🆘 Soporte

Si tienes problemas durante la instalación:

1. Revisar [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)
2. Verificar logs:
   - Dashboard: Consola de Node.js
   - GTA V: `ScriptHookVDotNet.log`
   - Streamer.bot: Pestaña "Log"

---

## ⚠️ Advertencias Importantes

1. **NO usar en GTA Online**: Solo modo historia
2. **Hacer backup**: Guardar partidas antes de usar
3. **Antivirus**: Puede bloquear ScriptHookV (agregar excepción)
4. **Actualizaciones de GTA**: Pueden romper ScriptHookV (esperar actualización)

---

**Versión**: 7.0 PILLAR  
**Última actualización**: 2026-02-17  
**Tiempo estimado de instalación**: 30-45 minutos
