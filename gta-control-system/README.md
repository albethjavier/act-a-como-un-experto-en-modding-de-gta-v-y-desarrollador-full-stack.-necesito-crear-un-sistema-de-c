# 🎮 GTA V Remote Control System - PILLAR V8

Sistema completo de control remoto para GTA V con integración para TikTok Live, Twitch y YouTube. Permite que los espectadores controlen el juego mediante regalos, comandos de chat y más.

## ✨ Características

- 🎁 **200+ comandos** organizados en 9 categorías
- 🌐 **Dashboard web** con interfaz moderna
- 🎯 **Sistema de prioridad** para gestionar múltiples comandos
- 🔄 **Limpieza automática** para prevenir crashes
- 🎬 **Efectos cinematográficos** (fade in/out)
- 📱 **Responsive** - funciona en móvil
- 🔒 **Seguro** - todo funciona localmente
- 🎮 **Integración TikTok** automática con regalos
- ⚡ **Rate limiting** anti-spam
- 🛡️ **Manejo robusto de errores**
- ⚙️ **Polling automático** - NO requiere presionar F9
- 📢 **Notificaciones visuales** en pantalla
- 🔫 **100+ armas** con sistema mejorado

## 📋 Requisitos

### Software Necesario

- ✅ GTA V (modo historia)
- ✅ [ScriptHookV](http://www.dev-c.com/nativedb/)
- ✅ [ScriptHookVDotNet](http://www.dev-c.com/gtav/scripthookv/)
- ✅ [Node.js](https://nodejs.org/) 16+
- ✅ [Python para .NET](https://ironpython.net/) (incluido en ScriptHookVDotNet)

### Opcional (para streaming)

- 🎥 [OBS Studio](https://obsproject.com/)
- 📺 [Streamer.bot](https://streamer.bot/) (para Twitch/YouTube)
- 🎁 TikTok Live Bridge (incluido en este proyecto)

## 🚀 Instalación Rápida

### Paso 1: Instalar Dependencias de GTA V

1. **ScriptHookV**:
   - Descarga de: http://www.dev-c.com/nativedb/
   - Extrae `ScriptHookV.dll` en la carpeta de GTA V

2. **ScriptHookVDotNet**:
   - Descarga de: http://www.dev-c.com/gtav/scripthookv/
   - Extrae `ScriptHookVDotNet.asi` y `ScriptHookVDotNet2.dll` en la carpeta de GTA V

3. **Crear carpeta scripts**:
   ```
   H:\Games\Grand Theft Auto V\scripts\
   ```

4. **Copiar el script de Python**:
   - Copia `scripts/escucha_dashboard.py` a la carpeta `scripts` de GTA V

### Paso 2: Configurar el Dashboard

```bash
cd gta-control-system/dashboard
npm install
```

**Editar [`config.json`](dashboard/config.json)** con la ruta correcta de tu instalación de GTA V:

```json
{
  "paths": {
    "commandFile": "H:\\Games\\Grand Theft Auto V\\comando_gta.json",
    "queueFile": "H:\\Games\\Grand Theft Auto V\\cola_espera.json"
  }
}
```

### Paso 3: Iniciar el Sistema

1. **Iniciar el dashboard**:
   ```bash
   cd dashboard
   node app.js
   ```

2. **Abrir GTA V** (modo historia)

3. **Cargar el script en GTA V**:
   
   **Opción A - Usando C# (Recomendado)**: (más estable)
   - Presiona `F4` para abrir la consola de ScriptHookVDotNet
   - Escribe: `load escucha_dashboard`
   - Presiona Enter
   - Deberías ver: `[INFO] Script 'escucha_dashboard' loaded successfully`
   
   **Opción B - Usando Python**:
   - Los scripts .py se cargan automáticamente desde la carpeta `scripts/`
   - Asegúrate de que IronPython esté instalado correctamente
   - NO uses el comando `load` para archivos .py

4. **Abrir el dashboard**:
   ```
   http://localhost:3000
   ```

5. **¡Probar!** Haz clic en cualquier botón y verás el efecto en 1-2 segundos

> **⚠️ IMPORTANTE V8**: Ya NO necesitas presionar F9 ni ninguna tecla. El sistema es completamente automático.

## 📚 Documentación

### 🆕 Novedades V8

- 🚀 [Cambios y Mejoras V8](CAMBIOS_V8.md) - **¡LEE ESTO PRIMERO!**
  - Sistema automático (sin F9)
  - Modo Dios mejorado
  - 100+ armas
  - Notificaciones visuales

### Guías de Inicio

- 📖 [Guía de Instalación Completa](INSTALL.md)
- ⚡ [Inicio Rápido](QUICK_START.md)
- 🔍 [Diagnóstico Rápido](DIAGNOSTICO_RAPIDO.md)
- 🛠️ [Solución de Problemas](docs/TROUBLESHOOTING.md)

### Integración con Plataformas

- 🎁 [TikTok Live Bridge](tiktok-bridge/README.md) - Integración automática
- 🎮 [Streamer.bot Setup](streamerbot/TIKTOK_STREAMERBOT_SETUP.md) - Guía completa
- 📺 [Configuración de Regalos](streamerbot/tiktok_gifts.json)

### Referencia

- 📋 [Lista de Comandos](dashboard/LISTA_COMANDOS.md)
- 🇪🇸 [README en Español](dashboard/README_ES.md)
- 🧪 [Prueba Rápida](dashboard/PRUEBA_RAPIDA.md)
- 📖 [Documentación de Comandos](docs/COMMANDS.md)

## 🎯 Categorías de Comandos

### 🧹 Sistema y Limpieza
- Limpiar mapa, reset, reparar vehículo, forzar sol

### 💀 Ataques y Oleadas
- Zombies, payasos, policías, bomberos, pandillas, marines, aliens, juggernaut

### 🛡️ Jugador (Superpoderes)
- Curar, blindaje, invencibilidad, invisibilidad, super salto, velocidad, armas

### 🌍 Clima y Tiempo
- 12 tipos de clima + 3 horarios del día

### 🏎️ Vehículos Deportivos
- T20, Zentorno, Adder, Vagner, Emerus, Krieger, y más

### 🚜 Pesados y Especiales
- Tractores, limusinas, tanques, Batmóvil, DeLorean, Oppressor MK2

### ✈️ Aire y Mar
- Jets, helicópteros, submarinos, yates

### 👮 Nivel de Búsqueda
- 0 a 5 estrellas

### 📍 Teleport Seguro
- 14 ubicaciones icónicas del mapa

## 🎁 Integración con TikTok

### Opción 1: TikTok Live Bridge (Automático)

El método más fácil y automático:

```bash
cd gta-control-system/tiktok-bridge
npm install
node tiktok_listener.js TU_USUARIO_TIKTOK
```

**Características:**
- ✅ Detecta regalos automáticamente
- ✅ Comandos de chat (!auto, !clima, etc.)
- ✅ Eventos automáticos (seguidores, likes)
- ✅ Estadísticas en tiempo real
- ✅ Sistema de combos para regalos caros

Ver: [Guía completa del TikTok Bridge](tiktok-bridge/README.md)

### Opción 2: Manual con OBS

1. Agrega el dashboard como Browser Source en OBS
2. Haz clic en los botones durante el stream
3. Los espectadores ven el panel

Ver: [Guía de Streamer.bot](streamerbot/TIKTOK_STREAMERBOT_SETUP.md)

## 🎮 Uso Básico

### Dashboard Web

1. Abre `http://localhost:3000`
2. Haz clic en cualquier botón
3. El comando se ejecuta instantáneamente en el juego

### API REST

```bash
# Ejecutar comando
curl http://localhost:3000/ejecutar/curar

# Con prioridad
curl http://localhost:3000/ejecutar/curar?prioridad=5

# Ver estado
curl http://localhost:3000/api/status
```

### Desde TikTok Live

Los espectadores envían regalos:
- 🌹 Rosa (1 moneda) → Curación
- 💎 Diamante (100 monedas) → T20
- 🦁 León (40,000 monedas) → Combo legendario

O usan comandos de chat:
- `!auto` → Vehículo aleatorio
- `!clima` → Clima aleatorio
- `!curar` → Curación

## 🛠️ Configuración Avanzada

### Ajustar Rate Limiting

Edita [`config.json`](dashboard/config.json):

```json
{
  "security": {
    "rateLimitMs": 500,
    "maxCommandsPerMinute": 60
  }
}
```

### Personalizar Comandos

Edita [`app.js`](dashboard/app.js) para agregar o modificar comandos.

### Crear Combos Personalizados

En el TikTok Bridge, edita `GIFT_COMMANDS`:

```javascript
'MiCombo': { 
    combo: ['comando1', 'comando2', 'comando3'], 
    priority: 10, 
    desc: 'Mi combo épico' 
}
```

## 📊 Monitoreo

### Dashboard

```
http://localhost:3000
```

### API Status

```
http://localhost:3000/api/status
```

Respuesta:
```json
{
  "status": "online",
  "version": "7.0.0",
  "uptime": 123.45,
  "commandsThisMinute": 12,
  "totalCommands": 200
}
```

### Logs

- **Dashboard**: Consola de Node.js
- **GTA V**: `ScriptHookVDotNet.log`
- **TikTok Bridge**: Consola con estadísticas

## 🔧 Solución de Problemas

### Los comandos no se ejecutan

1. **Verifica que el dashboard esté corriendo**:
   ```bash
   curl http://localhost:3000/api/status
   ```

2. **Verifica que el archivo se cree**:
   ```
   H:\Games\Grand Theft Auto V\comando_gta.json
   ```

3. **Verifica que el script esté cargado**:
   - Presiona `Insert` en GTA V
   - Busca `escucha_dashboard.py`

4. **Verifica la ruta en [`config.json`](dashboard/config.json)**

Ver: [Guía de Diagnóstico Completa](DIAGNOSTICO_RAPIDO.md)

### El juego se crashea

- Usa "♻️ LIMPIAR MAPA" regularmente
- Reduce la frecuencia de comandos
- Verifica `ScriptHookVDotNet.log` para errores

### TikTok no conecta

- Verifica que estés en vivo
- Verifica el nombre de usuario
- Verifica tu conexión a internet

Ver: [Troubleshooting Completo](docs/TROUBLESHOOTING.md)

## 🎨 Personalización

### Cambiar Colores del Dashboard

Edita los estilos CSS en [`app.js`](dashboard/app.js) (líneas 281-413).

### Agregar Nuevos Comandos

1. Agrega el comando en [`app.js`](dashboard/app.js)
2. Implementa la lógica en [`escucha_dashboard.py`](scripts/escucha_dashboard.py)
3. Reinicia ambos servicios

### Mapear Regalos Diferentes

Edita [`tiktok_listener.js`](tiktok-bridge/tiktok_listener.js) en `GIFT_COMMANDS`.

## 📁 Estructura del Proyecto

```
gta-control-system/
├── dashboard/              # Dashboard web
│   ├── app.js             # Servidor Node.js
│   ├── config.json        # Configuración
│   ├── package.json       # Dependencias
│   └── start.bat          # Script de inicio
├── scripts/               # Scripts de Python para GTA V
│   ├── escucha_dashboard.py  # Script principal
│   └── gestor_prioridad.py   # Gestor de cola
├── tiktok-bridge/         # Puente TikTok Live
│   ├── tiktok_listener.js # Listener de TikTok
│   ├── package.json       # Dependencias
│   ├── start.bat          # Script de inicio
│   └── README.md          # Documentación
├── streamerbot/           # Configuración Streamer.bot
│   ├── SETUP_GUIDE.md     # Guía de setup
│   └── tiktok_gifts.json  # Mapeo de regalos
├── docs/                  # Documentación
│   ├── COMMANDS.md        # Lista de comandos
│   └── TROUBLESHOOTING.md # Solución de problemas
├── INSTALL.md             # Guía de instalación
├── QUICK_START.md         # Inicio rápido
├── DIAGNOSTICO_RAPIDO.md  # Diagnóstico
└── README.md              # Este archivo
```

## 🔒 Seguridad

- ✅ Todo funciona localmente
- ✅ No se expone nada a internet
- ✅ Rate limiting anti-spam
- ✅ Validación de comandos
- ✅ Manejo de errores robusto

## ⚠️ Advertencias

- ⚠️ **NO usar en GTA Online** - Riesgo de ban permanente
- ⚠️ Solo para modo historia
- ⚠️ Usa "Limpiar Mapa" regularmente para prevenir crashes
- ⚠️ Algunos comandos pueden causar inestabilidad si se usan en exceso

## 🤝 Contribuir

¿Encontraste un bug? ¿Tienes una sugerencia?

1. Abre un issue
2. Describe el problema o sugerencia
3. Incluye logs si es relevante

## 📝 Changelog

### V7.0.0 (Actual)
- ✅ Integración completa con TikTok Live
- ✅ Sistema de combos para regalos
- ✅ Comandos de chat
- ✅ Eventos automáticos (seguidores, likes)
- ✅ Estadísticas en tiempo real
- ✅ Mejoras en teleport y vehicle swap
- ✅ Fade effects cinematográficos
- ✅ Limpieza automática de entidades
- ✅ 200+ comandos organizados

## 📄 Licencia

MIT License - Úsalo libremente, modifícalo, compártelo.

## 🔗 Enlaces Útiles

- [ScriptHookV](http://www.dev-c.com/nativedb/)
- [ScriptHookVDotNet](http://www.dev-c.com/gtav/scripthookv/)
- [Node.js](https://nodejs.org/)
- [TikTok Live Connector](https://github.com/zerodytrash/TikTok-Live-Connector)
- [Streamer.bot](https://streamer.bot/)
- [OBS Studio](https://obsproject.com/)

## ❓ FAQ

### ¿Funciona con Twitch/YouTube?

Sí, usa Streamer.bot para esas plataformas. Ver [guía de Streamer.bot](streamerbot/TIKTOK_STREAMERBOT_SETUP.md).

### ¿Puedo usar esto en GTA Online?

⚠️ **NO RECOMENDADO**. Usar mods en GTA Online puede resultar en ban permanente.

### ¿Afecta el rendimiento?

No, el impacto es mínimo. El sistema está optimizado.

### ¿Es seguro?

Sí, todo funciona localmente. No se expone nada a internet.

### ¿Puedo personalizar los comandos?

Sí, puedes agregar, modificar o eliminar comandos editando los archivos correspondientes.

### ¿Necesito Streamer.bot para TikTok?

No, el TikTok Bridge incluido reemplaza la necesidad de Streamer.bot para TikTok.

---

**¿Necesitas ayuda?** Consulta la [guía de diagnóstico](DIAGNOSTICO_RAPIDO.md) o la [documentación completa](docs/TROUBLESHOOTING.md)

**¡Disfruta del caos controlado en GTA V! 🎮🔥**
