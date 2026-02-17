# 🎯 Guía Completa: Conectar TikTok con Streamer.bot para GTA V

## ⚠️ IMPORTANTE: TikTok en Streamer.bot

**TikTok NO es una plataforma nativa de Streamer.bot**, pero podemos integrarlo usando métodos alternativos:

### Opciones de Integración

#### Opción 1: TikTok Live Studio + OBS Websocket (RECOMENDADO)
#### Opción 2: API de TikTok + Webhooks personalizados
#### Opción 3: Extensiones de terceros

---

## 🔧 OPCIÓN 1: Integración con OBS + Overlay (MÁS FÁCIL)

### Paso 1: Configurar el Dashboard como Overlay

1. **Abrir OBS Studio**
2. **Agregar Browser Source**:
   - Nombre: `GTA Control Panel`
   - URL: `http://localhost:3000`
   - Ancho: 1920
   - Alto: 1080
   - ✅ Marcar "Shutdown source when not visible"
   - ✅ Marcar "Refresh browser when scene becomes active"

3. **Hacer el overlay interactivo**:
   - Clic derecho en la fuente → **Interact**
   - Ahora puedes hacer clic en los botones durante el stream

### Paso 2: Usar Hotkeys para Comandos Rápidos

Crea hotkeys en OBS para ejecutar comandos comunes:

1. **Configuración → Hotkeys**
2. Agregar scripts de Python/AutoHotkey que llamen a la API:

```python
# hotkey_curar.py
import requests
requests.get('http://localhost:3000/ejecutar/curar')
```

3. Asignar teclas (F1, F2, F3, etc.)

---

## 🔧 OPCIÓN 2: Streamer.bot con HTTP Requests

Aunque TikTok no es nativo, puedes usar Streamer.bot para crear un panel de control manual.

### Paso 1: Instalar Streamer.bot

1. Descargar de: https://streamer.bot/
2. Instalar y abrir

### Paso 2: Crear Acciones en Streamer.bot

#### Acción Base: Ejecutar Comando GTA

1. **Actions** → **Add**
2. Nombre: `GTA_Ejecutar_Comando`
3. **Add Sub-Action** → **Core** → **Fetch URL**

**Configuración:**
```
Method: GET
URL: http://localhost:3000/ejecutar/%accion%
```

4. **Add Sub-Action** → **Core** → **Log Message**
```
Message: ✅ Comando ejecutado: %accion%
```

#### Crear Comandos Específicos

Para cada comando que quieras, crea una acción:

**Ejemplo: Curar**
1. Nombre: `GTA_Curar`
2. **Set Argument**:
   - Name: `accion`
   - Value: `curar`
3. **Execute Method** → `GTA_Ejecutar_Comando`

**Ejemplo: Spawn T20**
1. Nombre: `GTA_SpawnT20`
2. **Set Argument**:
   - Name: `accion`
   - Value: `veh_t20`
3. **Execute Method** → `GTA_Ejecutar_Comando`

### Paso 3: Asignar Hotkeys

1. En cada acción, ve a **Triggers**
2. **Add** → **Hotkey**
3. Presiona la combinación de teclas deseada
4. Ahora puedes ejecutar comandos con hotkeys durante el stream

---

## 🔧 OPCIÓN 3: Integración con TikTok Live Studio (AVANZADO)

### Requisitos
- TikTok Live Studio instalado
- Node.js instalado
- Conocimientos básicos de programación

### Paso 1: Instalar TikTok Live Connector

```bash
npm install -g tiktok-live-connector
```

### Paso 2: Crear Script de Escucha

Crea un archivo `tiktok_listener.js`:

```javascript
const { WebcastPushConnection } = require('tiktok-live-connector');
const axios = require('axios');

// Tu nombre de usuario de TikTok
const tiktokUsername = 'TU_USUARIO_TIKTOK';

// Conectar a TikTok Live
const tiktokLiveConnection = new WebcastPushConnection(tiktokUsername);

// Mapeo de regalos a comandos
const giftCommands = {
    'Rose': 'curar',
    'Heart': 'blindaje',
    'Diamond': 'veh_t20',
    'Castle': 'atk_zombies_10',
    'Rocket': 'veh_hydra',
    'Yacht': 'atk_marines',
    'Lion': 'atk_juggernaut'
};

// Escuchar regalos
tiktokLiveConnection.on('gift', data => {
    const giftName = data.giftName;
    const username = data.uniqueId;
    const command = giftCommands[giftName];
    
    if (command) {
        console.log(`🎁 ${username} envió ${giftName} → Ejecutando: ${command}`);
        
        // Enviar comando al dashboard
        axios.get(`http://localhost:3000/ejecutar/${command}`)
            .then(() => console.log('✅ Comando ejecutado'))
            .catch(err => console.error('❌ Error:', err.message));
    }
});

// Escuchar comentarios con comandos
tiktokLiveConnection.on('chat', data => {
    const message = data.comment.toLowerCase();
    const username = data.uniqueId;
    
    // Comandos de chat
    if (message.startsWith('!')) {
        const cmd = message.substring(1);
        const commandMap = {
            'auto': 'rnd_veh',
            'clima': 'cl_rnd',
            'curar': 'curar',
            'armas': 'armas',
            'caos': 'atk_rnd'
        };
        
        if (commandMap[cmd]) {
            console.log(`💬 ${username}: ${message} → ${commandMap[cmd]}`);
            axios.get(`http://localhost:3000/ejecutar/${commandMap[cmd]}`);
        }
    }
});

// Conectar
tiktokLiveConnection.connect()
    .then(state => {
        console.log('🔴 Conectado a TikTok Live!');
        console.log(`📺 Stream: ${state.roomId}`);
    })
    .catch(err => {
        console.error('❌ Error conectando:', err);
    });
```

### Paso 3: Ejecutar el Script

```bash
node tiktok_listener.js
```

**Mantén este script corriendo mientras haces stream en TikTok.**

---

## 🎮 OPCIÓN 4: Panel de Control Web (MÁS SIMPLE)

Si no quieres complicarte con integraciones, usa el dashboard directamente:

### Durante el Stream:

1. **Abre el dashboard**: `http://localhost:3000`
2. **Colócalo en una segunda pantalla** o en una ventana pequeña
3. **Haz clic en los botones** cuando los espectadores pidan comandos
4. **Usa OBS para mostrar el dashboard** como overlay

### Ventajas:
- ✅ No requiere configuración compleja
- ✅ Control total sobre qué comandos ejecutar
- ✅ Puedes ver el estado en tiempo real
- ✅ Funciona con cualquier plataforma (TikTok, Twitch, YouTube)

---

## 📱 OPCIÓN 5: Control desde Móvil

### Paso 1: Hacer el Dashboard Accesible en Red Local

1. Edita [`config.json`](../dashboard/config.json):
```json
{
  "server": {
    "port": 3000,
    "host": "0.0.0.0"
  }
}
```

2. Reinicia el dashboard

3. Encuentra tu IP local:
```bash
ipconfig  # Windows
ifconfig  # Linux/Mac
```

4. Desde tu móvil, abre:
```
http://TU_IP_LOCAL:3000
```

### Paso 2: Usar Durante el Stream

- Coloca tu móvil al lado
- Ejecuta comandos con un toque
- Perfecto para streams móviles de TikTok

---

## 🔍 Verificar que Todo Funciona

### Test 1: Dashboard Funcionando

```bash
# Abrir en navegador
http://localhost:3000
```

Deberías ver el panel de control con todos los botones.

### Test 2: API Respondiendo

```bash
# En PowerShell/CMD
curl http://localhost:3000/api/status
```

Deberías ver:
```json
{
  "status": "online",
  "version": "7.0.0",
  "uptime": 123.45,
  "commandsThisMinute": 0
}
```

### Test 3: Comando Ejecutándose

1. Abre GTA V con el script de Python cargado
2. En el navegador, haz clic en "❤️ CURAR"
3. Tu personaje debería curarse instantáneamente

### Test 4: Archivo de Comando Creándose

Verifica que se cree el archivo:
```
H:\Games\Grand Theft Auto V\comando_gta.json
```

---

## 🛠️ Solución de Problemas

### Problema: Los comandos no se ejecutan en el juego

**Diagnóstico:**

1. **Verificar que el dashboard esté corriendo**:
   ```bash
   # Deberías ver esto en la consola:
   🎮 GTA V DASHBOARD PILLAR V7 - INICIADO
   🌐 URL: http://0.0.0.0:3000
   ```

2. **Verificar que el archivo se cree**:
   - Navega a: `H:\Games\Grand Theft Auto V\`
   - Haz clic en un botón del dashboard
   - Debería aparecer `comando_gta.json`

3. **Verificar que el script de Python esté cargado**:
   - Abre GTA V
   - Presiona `Insert` para abrir la consola de ScriptHookVDotNet
   - Deberías ver: `escucha_dashboard.py` en la lista

**Soluciones:**

#### Si el archivo NO se crea:
```javascript
// Verifica la ruta en config.json
{
  "paths": {
    "commandFile": "./comando_gta.json"  // Ruta relativa al dashboard
  }
}
```

Cambia a ruta absoluta:
```json
{
  "paths": {
    "commandFile": "H:\\Games\\Grand Theft Auto V\\comando_gta.json"
  }
}
```

#### Si el archivo se crea pero no se ejecuta:
1. Verifica que [`escucha_dashboard.py`](../scripts/escucha_dashboard.py) tenga la ruta correcta:
```python
ARCHIVO_RUTA = "H:\\Games\\Grand Theft Auto V\\comando_gta.json"
```

2. Recarga el script en GTA V:
   - Presiona `Insert`
   - Escribe: `reload escucha_dashboard`

#### Si el script no se carga:
1. Verifica que ScriptHookVDotNet esté instalado
2. Coloca [`escucha_dashboard.py`](../scripts/escucha_dashboard.py) en:
   ```
   H:\Games\Grand Theft Auto V\scripts\
   ```

---

## 📊 Monitoreo en Tiempo Real

### Ver Estado del Sistema

```bash
# En navegador
http://localhost:3000/api/status
```

### Ver Logs del Dashboard

El dashboard muestra logs en la consola de Node.js:
```
[2024-01-15T10:30:45.123Z] Comando ejecutado: curar (Prioridad: 1)
[TikTok] Usuario123 envió: Rosa (Prioridad: 1)
```

### Ver Logs de GTA V

Revisa el archivo:
```
H:\Games\Grand Theft Auto V\ScriptHookVDotNet.log
```

---

## 🎨 Personalización

### Cambiar Comandos Asignados

Edita [`app.js`](../dashboard/app.js) para modificar los comandos disponibles.

### Agregar Nuevos Comandos

1. Agrega el comando en [`app.js`](../dashboard/app.js) en la sección correspondiente
2. Implementa la lógica en [`escucha_dashboard.py`](../scripts/escucha_dashboard.py)
3. Reinicia ambos servicios

### Cambiar Colores/Diseño

Edita los estilos CSS en [`app.js`](../dashboard/app.js) (líneas 281-413).

---

## 📝 Resumen de Opciones

| Opción | Dificultad | Integración TikTok | Recomendado |
|--------|------------|-------------------|-------------|
| Dashboard + OBS | ⭐ Fácil | Manual | ✅ SÍ |
| Streamer.bot + Hotkeys | ⭐⭐ Media | Manual | ✅ SÍ |
| TikTok Live Connector | ⭐⭐⭐ Difícil | Automática | ⚠️ Avanzado |
| Control desde Móvil | ⭐ Fácil | Manual | ✅ SÍ |

---

## 🔗 Enlaces Útiles

- [Streamer.bot](https://streamer.bot/)
- [TikTok Live Connector](https://github.com/zerodytrash/TikTok-Live-Connector)
- [OBS Studio](https://obsproject.com/)
- [ScriptHookVDotNet](http://www.dev-c.com/gtav/scripthookv/)

---

## ❓ Preguntas Frecuentes

### ¿Puedo usar esto con Twitch/YouTube?

Sí, el sistema funciona con cualquier plataforma. Para Twitch/YouTube, Streamer.bot tiene integración nativa.

### ¿Es seguro?

Sí, todo funciona localmente. No se expone nada a internet.

### ¿Afecta el rendimiento del juego?

No, el impacto es mínimo. El script de Python es muy ligero.

### ¿Puedo usar esto en modo online?

⚠️ **NO RECOMENDADO**. Usar mods en GTA Online puede resultar en ban.

---

**¿Necesitas ayuda?** Revisa la sección de [Troubleshooting](../docs/TROUBLESHOOTING.md)
