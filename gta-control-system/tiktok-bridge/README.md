# 🎁 TikTok Live Bridge para GTA V

Este puente conecta automáticamente TikTok Live con tu sistema de control de GTA V, permitiendo que los regalos y comandos de chat ejecuten acciones en el juego en tiempo real.

## 🚀 Instalación Rápida

### Paso 1: Instalar Node.js

Si no tienes Node.js instalado:

1. Descarga desde: https://nodejs.org/
2. Instala la versión LTS (recomendada)
3. Reinicia tu computadora

### Paso 2: Instalar Dependencias

```bash
cd gta-control-system/tiktok-bridge
npm install
```

### Paso 3: Iniciar el Bridge

**Opción A: Usando el script (Windows)**
```bash
start.bat
```

**Opción B: Manualmente**
```bash
node tiktok_listener.js TU_USUARIO_TIKTOK
```

Reemplaza `TU_USUARIO_TIKTOK` con tu nombre de usuario real de TikTok.

## 📋 Requisitos Previos

- ✅ Node.js 16+ instalado
- ✅ Dashboard de GTA V corriendo en `http://localhost:3000`
- ✅ GTA V con scripts de Python cargados
- ✅ Estar en vivo en TikTok

## 🎮 Cómo Funciona

1. **Inicias el bridge** con tu nombre de usuario de TikTok
2. **El bridge se conecta** a tu stream en vivo
3. **Escucha eventos**:
   - 🎁 Regalos
   - 💬 Comandos de chat
   - 👤 Nuevos seguidores
   - 📤 Compartir stream
   - ❤️ Likes (cada 100)
4. **Envía comandos** al dashboard de GTA V
5. **El dashboard ejecuta** las acciones en el juego

## 🎁 Regalos Mapeados

### Regalos Básicos (1-50 monedas)

| Regalo | Comando | Descripción |
|--------|---------|-------------|
| Rosa | `curar` | Curación completa |
| Corazón | `blindaje` | Armadura completa |
| Dedo Arriba | `fix_veh` | Reparar vehículo |
| Helado | `cl_rnd` | Clima aleatorio |
| Donut | `t_dia` | Cambiar a mediodía |
| Arcoíris | `cl_clear` | Clima despejado |

### Regalos Medios (100-500 monedas)

| Regalo | Comando | Descripción |
|--------|---------|-------------|
| Diamante | `veh_t20` | Superdeportivo T20 |
| Corona | `veh_zentorno` | Lamborghini Zentorno |
| Trofeo | `veh_adder` | Bugatti Adder |
| Castillo | `atk_zombies_10` | 10 zombies |
| Cohete | `atk_police_15` | Asalto policial |
| Ferrari | `veh_rhino` | Tanque militar |

### Regalos Caros (1000-5000 monedas)

| Regalo | Comando | Descripción |
|--------|---------|-------------|
| Yate | `atk_marines` | Ataque de marines |
| Avión | `veh_hydra` | Jet militar Hydra |
| Mansión | `atk_aliens` | Invasión alienígena |
| Planeta | `atk_juggernaut` | Juggernaut con minigun |
| Galaxia | `w_5` | 5 estrellas de policía |
| Universo | `limpiar_todo` | Limpiar todo el mapa |

### Regalos Legendarios (40000+ monedas) - COMBOS

| Regalo | Comandos | Descripción |
|--------|----------|-------------|
| León | `atk_juggernaut` + `inv_on` + `armas` + `veh_khanjali` | Combo legendario |
| Dragón | `w_5` + `atk_marines` + `atk_police_15` | Caos total |
| Fénix | `limpiar_todo` + `curar` + `inv_on` + `veh_hydra` | Renacimiento |

## 💬 Comandos de Chat

Los espectadores pueden usar estos comandos en el chat:

| Comando | Acción |
|---------|--------|
| `!auto` | Vehículo aleatorio |
| `!clima` | Clima aleatorio |
| `!curar` | Curación |
| `!armas` | Todas las armas |
| `!tp` | Teleport a Maze Bank |
| `!caos` | Ataque aleatorio |
| `!limpiar` | Limpiar mapa |
| `!tanque` | Spawn tanque |
| `!jet` | Spawn jet |
| `!zombies` | 10 zombies |
| `!dios` | Modo dios ON |
| `!mortal` | Modo dios OFF |

## 🎯 Eventos Automáticos

- **Nuevo seguidor** → Clima aleatorio
- **Compartir stream** → Vehículo aleatorio
- **100 likes** → Curación

## 📊 Monitoreo

El bridge muestra en tiempo real:

```
✅ [10:30:45] Usuario123 → Rosa → curar
🎁 Usuario456 envió 5x Diamante
💬 Usuario789: !auto → rnd_veh
👤 ¡Usuario000 te siguió! → Clima aleatorio
```

### Ver Estadísticas

Presiona `Ctrl+C` para ver las estadísticas completas:

```
╔════════════════════════════════════════╗
║         ESTADÍSTICAS                   ║
╠════════════════════════════════════════╣
║ 🎁 Regalos recibidos: 45              ║
║ ⚡ Comandos ejecutados: 52            ║
║ 💬 Comandos de chat: 12               ║
║ ❌ Errores: 0                         ║
║ ⏱️  Tiempo activo: 15m 30s            ║
╚════════════════════════════════════════╝
```

## 🛠️ Solución de Problemas

### Error: "No se puede conectar al dashboard"

**Solución:**
1. Verifica que el dashboard esté corriendo:
   ```bash
   cd gta-control-system/dashboard
   node app.js
   ```
2. Abre `http://localhost:3000` en tu navegador
3. Deberías ver el panel de control

### Error: "Error al conectar a TikTok Live"

**Posibles causas:**

1. **No estás en vivo**: Debes estar transmitiendo en TikTok
2. **Usuario incorrecto**: Verifica que el nombre de usuario sea correcto
3. **Conexión a internet**: Verifica tu conexión

### Error: "tiktok-live-connector no encontrado"

**Solución:**
```bash
npm install
```

### Los comandos no se ejecutan en el juego

**Diagnóstico:**

1. **Verifica que el dashboard esté corriendo**
2. **Verifica que GTA V esté abierto** con el script de Python cargado
3. **Verifica la ruta del archivo** en [`config.json`](../dashboard/config.json):
   ```json
   {
     "paths": {
       "commandFile": "H:\\Games\\Grand Theft Auto V\\comando_gta.json"
     }
   }
   ```

## 🎨 Personalización

### Agregar Nuevos Regalos

Edita [`tiktok_listener.js`](tiktok_listener.js) y agrega en `GIFT_COMMANDS`:

```javascript
const GIFT_COMMANDS = {
    // ... regalos existentes ...
    'NuevoRegalo': { cmd: 'comando_gta', priority: 3, desc: 'Descripción' }
};
```

### Agregar Nuevos Comandos de Chat

Edita `CHAT_COMMANDS`:

```javascript
const CHAT_COMMANDS = {
    // ... comandos existentes ...
    '!nuevo': 'comando_gta'
};
```

### Cambiar Prioridades

Mayor prioridad = se ejecuta primero en la cola:

```javascript
'Regalo': { cmd: 'comando', priority: 10, desc: 'Alta prioridad' }
```

### Crear Combos Personalizados

```javascript
'MiCombo': { 
    combo: ['comando1', 'comando2', 'comando3'], 
    priority: 10, 
    desc: 'Mi combo épico' 
}
```

Los comandos se ejecutan con 2 segundos de delay entre cada uno.

## 📝 Notas Importantes

- ⚠️ **Solo funciona cuando estás en vivo** en TikTok
- ⚠️ Los nombres de regalos pueden variar según región/idioma
- ⚠️ Algunos regalos pueden tener nombres diferentes
- ✅ El sistema es completamente local y seguro
- ✅ No se expone nada a internet
- ✅ Funciona con cualquier versión de GTA V (modo historia)

## 🔗 Enlaces Útiles

- [TikTok Live Connector](https://github.com/zerodytrash/TikTok-Live-Connector)
- [Dashboard GTA V](../dashboard/README_ES.md)
- [Guía de Comandos](../dashboard/LISTA_COMANDOS.md)
- [Troubleshooting](../docs/TROUBLESHOOTING.md)

## 💡 Consejos

1. **Prueba primero sin stream**: Usa el dashboard manualmente para verificar que todo funcione
2. **Configura los regalos**: Ajusta el mapeo según los regalos disponibles en tu región
3. **Usa combos para regalos caros**: Crea secuencias épicas para regalos de alto valor
4. **Monitorea los logs**: Mantén visible la consola del bridge para ver qué está pasando
5. **Ten un moderador**: Alguien que pueda ayudarte a gestionar el chat mientras juegas

## ❓ Preguntas Frecuentes

### ¿Funciona con Twitch/YouTube?

No, este bridge es específico para TikTok. Para Twitch/YouTube, usa Streamer.bot directamente.

### ¿Puedo usar esto en GTA Online?

⚠️ **NO RECOMENDADO**. Usar mods en GTA Online puede resultar en ban permanente.

### ¿Afecta el rendimiento?

No, el impacto es mínimo. El bridge consume muy pocos recursos.

### ¿Necesito Streamer.bot?

No, este bridge reemplaza la necesidad de Streamer.bot para TikTok.

### ¿Puedo ver qué regalos están disponibles en mi región?

Sí, visita: https://streamtoearn.io/gifts?region=TU_CODIGO_PAIS

---

**¿Necesitas ayuda?** Abre un issue o consulta la [guía de troubleshooting](../docs/TROUBLESHOOTING.md)
