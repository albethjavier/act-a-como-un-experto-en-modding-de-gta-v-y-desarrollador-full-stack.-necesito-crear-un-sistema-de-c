# 🎮 GTA V Remote Control System - PILLAR V7

Sistema profesional de control remoto para GTA V con integración TikTok/Streamer.bot

## 🏗️ Arquitectura del Sistema

```
┌─────────────────┐
│  TikTok Live    │ (Regalos, Comandos, Eventos)
└────────┬────────┘
         │
┌────────▼────────┐
│  Streamer.bot   │ (Puente de Eventos)
└────────┬────────┘
         │
┌────────▼────────┐
│ Dashboard Web   │ (Node.js/Express - Puerto 3000)
│  + API REST     │
└────────┬────────┘
         │
┌────────▼────────┐
│ comando_gta.json│ (Archivo de Comunicación)
└────────┬────────┘
         │
┌────────▼────────┐
│ Priority Queue  │ (cola_espera.json - Sistema de Prioridad)
└────────┬────────┘
         │
┌────────▼────────────────────────┐
│  Motores de Ejecución (Python)  │
│  ├─ motor_vehiculos.py          │
│  ├─ motor_caos.py                │
│  └─ escucha_dashboard.py         │
└────────┬────────────────────────┘
         │
┌────────▼────────┐
│   GTA V Game    │ (ScriptHookVDotNet)
└─────────────────┘
```

## 🚀 Características Principales

### ✅ Mejoras Implementadas (V7)

1. **Sistema de Cola de Prioridad**: Los regalos caros de TikTok saltan al frente
2. **Motores Multihilo**: Separación de vehículos y caos para evitar saturación
3. **Anti-Crash**: Limpieza automática de entidades cada 60 segundos
4. **Teleport Seguro**: Sistema de congelación + carga de colisiones
5. **Vehicle Swap Perfecto**: Sin bugs de posición usando nativos directos
6. **Debounce Protection**: Previene spam de comandos
7. **Fade Effects**: Transiciones cinematográficas en cambios de vehículo
8. **Error Recovery**: Manejo robusto de archivos bloqueados

### 📊 Estadísticas del Sistema

- **+200 Comandos** organizados en 9 categorías
- **14 Ubicaciones de Teleport** con coordenadas corregidas
- **12 Tipos de Clima** con limpieza de partículas
- **50+ Vehículos** (Deportivos, Pesados, Aéreos, Marítimos)
- **12 Tipos de Ataques** con IA agresiva
- **15 Superpoderes** para el jugador

## 📁 Estructura de Archivos

```
gta-control-system/
├── dashboard/
│   ├── app.js                    # Servidor Express principal
│   ├── package.json              # Dependencias Node.js
│   ├── config.json               # Configuración de rutas
│   └── public/
│       └── index.html            # UI del dashboard (opcional)
├── scripts/
│   ├── escucha_dashboard.py      # Script principal SHVDN
│   ├── motor_vehiculos.py        # Motor de spawneo de vehículos
│   ├── motor_caos.py             # Motor de ataques y efectos
│   └── utils.py                  # Funciones compartidas
├── streamerbot/
│   ├── actions.json              # Configuración de Streamer.bot
│   ├── tiktok_gifts.json         # Mapeo de regalos TikTok
│   └── SETUP_GUIDE.md            # Guía de configuración
├── docs/
│   ├── COMMANDS.md               # Lista completa de comandos
│   ├── NATIVES.md                # Referencia de funciones nativas
│   └── TROUBLESHOOTING.md        # Solución de problemas
└── README.md                     # Este archivo
```

## 🔧 Instalación

### Requisitos Previos

1. **GTA V** instalado en: `H:\Games\Grand Theft Auto V\`
2. **ScriptHookV** + **ScriptHookVDotNet** (v2.10+)
3. **Python para SHVDN** (Python3.shvdn o Pytrainer)
4. **Node.js** (v18+) y **Bun** (opcional)
5. **Streamer.bot** (para integración TikTok)

### Paso 1: Instalar Dashboard

```bash
cd dashboard
npm install
# o con bun
bun install
```

### Paso 2: Copiar Scripts de Python

Copiar todos los archivos `.py` de `scripts/` a:
```
H:\Games\Grand Theft Auto V\scripts\
```

### Paso 3: Configurar Streamer.bot

Ver guía completa en: `streamerbot/SETUP_GUIDE.md`

## 🎯 Uso Rápido

### Iniciar Dashboard

```bash
cd dashboard
node app.js
# o con bun
bun app.js
```

Abrir navegador en: `http://localhost:3000`

### Iniciar GTA V

1. Abrir GTA V
2. Los scripts de Python se cargarán automáticamente
3. Presionar botones en el dashboard o recibir regalos en TikTok

## 🎁 Sistema de Prioridad (TikTok)

Los regalos se procesan según su valor en monedas:

| Regalo | Monedas | Prioridad | Comando Sugerido |
|--------|---------|-----------|------------------|
| Rosa | 1 | Baja | Curar, Reparar Auto |
| Corazón | 10 | Baja | Clima Random |
| Helado | 30 | Media | Vehículo Deportivo |
| Diamante | 100 | Media | Ataque de Zombies |
| Castillo | 500 | Alta | Tanque Rhino |
| León | 40,000 | Máxima | Juggernaut + Modo Dios |

## 🛡️ Seguridad y Estabilidad

### Protecciones Implementadas

- **Rate Limiting**: Máximo 1 comando cada 500ms
- **File Locking**: Manejo de archivos en uso
- **Entity Cleanup**: Limpieza automática cada 60s
- **Collision Loading**: Previene caídas al vacío
- **Error Recovery**: Try/catch en todas las operaciones críticas

### Comandos de Emergencia

- `limpiar_todo`: Elimina todos los NPCs y vehículos
- `suicidio`: Reset completo del jugador
- `w_0`: Eliminar estrellas de policía
- `inv_on`: Activar modo dios

## 📚 Documentación Adicional

- [Lista Completa de Comandos](docs/COMMANDS.md)
- [Referencia de Nativos GTA](docs/NATIVES.md)
- [Guía de Streamer.bot](streamerbot/SETUP_GUIDE.md)
- [Solución de Problemas](docs/TROUBLESHOOTING.md)

## 🔗 Referencias

- [GTA V Native DB](https://gtahash.ru/)
- [SHVDN Wiki](http://www.dev-c.com/gtav/scripthookv/)
- [Streamer.bot Docs](https://docs.streamer.bot/)
- [TikTok Gifts (Venezuela)](https://streamtoearn.io/gifts?region=VE)

## 📝 Notas Técnicas

### Comunicación Asíncrona

El sistema usa archivos JSON como "buzón de correos" para evitar conexiones directas que puedan crashear el juego.

### Nativos Críticos

- `SET_PED_INTO_VEHICLE`: Montado instantáneo en vehículos
- `REQUEST_COLLISION_AT_COORD`: Carga de suelo en teleports
- `SET_WEATHER_TYPE_NOW_PERSIST`: Cambio de clima persistente
- `APPLY_DAMAGE_TO_PED`: Daño directo al jugador

## 🤝 Contribuciones

Este sistema está optimizado para streaming en TikTok. Siéntete libre de adaptarlo para YouTube, Twitch u otras plataformas.

## ⚠️ Disclaimer

Este sistema es para uso educativo y de entretenimiento. Úsalo solo en modo historia o servidores privados. **NO lo uses en GTA Online** para evitar baneos.

---

**Versión**: 7.0 PILLAR  
**Última Actualización**: 2026-02-17  
**Autor**: Sistema de Control Remoto GTA V
