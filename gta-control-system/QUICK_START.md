# ⚡ Guía de Inicio Rápido - 5 Minutos

## 🎯 Para Usuarios que Ya Tienen Todo Instalado

Si ya tienes GTA V, ScriptHookV, SHVDN y Node.js instalados, sigue estos pasos:

### 1️⃣ Configurar Rutas (30 segundos)

Editar [`dashboard/config.json`](dashboard/config.json):

```json
{
  "paths": {
    "commandFile": "TU_RUTA\\Grand Theft Auto V\\comando_gta.json",
    "queueFile": "TU_RUTA\\Grand Theft Auto V\\cola_espera.json"
  }
}
```

Editar [`scripts/escucha_dashboard.py`](scripts/escucha_dashboard.py):

```python
ARCHIVO_RUTA = "TU_RUTA\\Grand Theft Auto V\\comando_gta.json"
```

### 2️⃣ Instalar Dashboard (1 minuto)

```bash
cd dashboard
npm install
```

### 3️⃣ Copiar Scripts (30 segundos)

Copiar todos los archivos `.py` de `scripts/` a:
```
TU_RUTA\Grand Theft Auto V\scripts\
```

### 4️⃣ Iniciar Todo (1 minuto)

**Terminal 1 - Dashboard:**
```bash
cd dashboard
node app.js
# O doble clic en start.bat
```

**Abrir navegador:**
```
http://localhost:3000
```

**Iniciar GTA V:**
- Modo historia (NO Online)
- Esperar carga completa

### 5️⃣ Probar (30 segundos)

En el navegador, presionar: **"❤️ CURAR"**

En GTA V: Tu personaje se cura → ✅ **¡Funciona!**

---

## 🆕 Para Usuarios Nuevos

Si es tu primera vez, sigue la [Guía de Instalación Completa](INSTALL.md) (30-45 minutos).

---

## 🎁 Integración TikTok (Opcional)

1. Instalar [Streamer.bot](https://streamer.bot)
2. Seguir [Guía de Streamer.bot](streamerbot/SETUP_GUIDE.md)
3. Mapear regalos usando [tiktok_gifts.json](streamerbot/tiktok_gifts.json)

---

## 📚 Documentación

| Documento | Descripción |
|-----------|-------------|
| [README.md](README.md) | Visión general del sistema |
| [INSTALL.md](INSTALL.md) | Instalación completa paso a paso |
| [COMMANDS.md](docs/COMMANDS.md) | Lista de 200+ comandos |
| [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) | Solución de problemas |
| [SETUP_GUIDE.md](streamerbot/SETUP_GUIDE.md) | Integración Streamer.bot |

---

## 🔥 Comandos Más Populares

| Botón | Comando | Efecto |
|-------|---------|--------|
| ❤️ CURAR | `curar` | Salud al 100% |
| T20 | `veh_t20` | Superdeportivo |
| 🧟 10 ZOMBIES | `atk_zombies_10` | Horda de zombies |
| 🏢 MAZE BANK | `tp_mazebank` | Teleport a torre |
| 😇 DIOS ON | `inv_on` | Invencibilidad |
| 🔫 ARMAS | `armas` | Arsenal completo |
| ♻️ LIMPIAR | `limpiar_todo` | Reset del mapa |

---

## ⚠️ Recordatorios Importantes

- ✅ Usar solo en **modo historia**
- ✅ Dashboard debe estar corriendo en puerto **3000**
- ✅ Scripts deben estar en carpeta **scripts/** de GTA V
- ❌ **NO usar en GTA Online** (riesgo de baneo)

---

## 🆘 Ayuda Rápida

**Problema**: Los comandos no funcionan  
**Solución**: Ver [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) → Sección 1

**Problema**: El juego crashea  
**Solución**: Ejecutar comando `limpiar_todo` cada 5 minutos

**Problema**: Streamer.bot no conecta  
**Solución**: Verificar que dashboard esté en `http://localhost:3000`

---

## 🎮 ¡A Jugar!

Una vez todo configurado:

1. Abre el dashboard en tu navegador
2. Inicia GTA V (modo historia)
3. Presiona botones y disfruta
4. Si haces streaming, conecta Streamer.bot

**¡Diviértete y haz streams épicos!** 🚀

---

**Versión**: 7.0 PILLAR  
**Tiempo de setup**: 5 minutos (usuarios experimentados) | 45 minutos (nuevos usuarios)
