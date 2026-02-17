# 🔧 Guía de Solución de Problemas

## 🚨 Problemas Comunes y Soluciones

### 1. Los comandos no se ejecutan en GTA V

#### Síntomas
- Presionas botones en el dashboard pero nada pasa en el juego
- El archivo `comando_gta.json` no se crea

#### Soluciones

**A. Verificar que el dashboard esté corriendo**
```bash
# Abrir navegador en:
http://localhost:3000

# Si no carga, iniciar el dashboard:
cd dashboard
node app.js
```

**B. Verificar ruta del archivo**
```
Ruta esperada: H:\Games\Grand Theft Auto V\comando_gta.json

Si tu GTA está en otra ubicación:
1. Editar dashboard/config.json
2. Cambiar "commandFile" a tu ruta
3. Editar scripts/escucha_dashboard.py
4. Cambiar ARCHIVO_RUTA a tu ruta
5. Reiniciar todo
```

**C. Verificar permisos de escritura**
```bash
# Windows: Ejecutar como administrador
# Verificar que la carpeta no esté protegida
```

**D. Verificar que ScriptHookVDotNet esté instalado**
```
Archivos necesarios en la carpeta de GTA V:
- ScriptHookV.dll
- ScriptHookVDotNet.asi
- ScriptHookVDotNet2.dll
- ScriptHookVDotNet3.dll (si usas v3)
```

---

### 2. El script de Python no se carga en GTA V

#### Síntomas
- GTA V inicia pero los comandos no funcionan
- No aparece mensaje de script cargado

#### Soluciones

**A. Verificar ubicación del script**
```
Copiar escucha_dashboard.py a:
H:\Games\Grand Theft Auto V\scripts\

Si no existe la carpeta "scripts", crearla.
```

**B. Verificar Python para SHVDN**
```
Archivos necesarios:
- Python3.shvdn (en la carpeta de GTA V)
O
- Pytrainer (alternativa)

Descargar de:
https://github.com/crosire/scripthookvdotnet/releases
```

**C. Revisar logs de SHVDN**
```
Abrir: H:\Games\Grand Theft Auto V\ScriptHookVDotNet.log

Buscar errores relacionados con Python o el script
```

**D. Verificar sintaxis del script**
```python
# El script debe tener codificación UTF-8
# Primera línea debe ser:
# -*- coding: utf-8 -*-
```

---

### 3. El juego se crashea al ejecutar comandos

#### Síntomas
- GTA V se cierra inesperadamente
- Pantalla congelada
- Error "ERR_GFX_D3D_INIT"

#### Soluciones

**A. Activar limpieza automática**
```python
# En escucha_dashboard.py, verificar que esté:
INTERVALO_LIMPIEZA = 60  # Segundos

# Ejecutar manualmente:
Comando: limpiar_todo
```

**B. Reducir frecuencia de comandos**
```javascript
// En dashboard/config.json:
"rateLimitMs": 1000,  // Aumentar de 500 a 1000
"maxCommandsPerMinute": 30  // Reducir de 60 a 30
```

**C. Evitar spam de vehículos**
```
No spawnear más de 1 vehículo cada 2 segundos
El script ya tiene protección, pero si usas
Streamer.bot, agregar delays entre comandos
```

**D. Actualizar drivers gráficos**
```
NVIDIA: GeForce Experience
AMD: Adrenalin Software
```

---

### 4. Teleport deja al jugador cayendo al vacío

#### Síntomas
- Al teletransportarse, el jugador cae infinitamente
- Aparece en el cielo sin suelo

#### Soluciones

**A. Verificar función teleport_seguro**
```python
# En escucha_dashboard.py, debe tener:
Function.Call(Hash.REQUEST_COLLISION_AT_COORD, x, y, z)
Script.Wait(1500)  # Espera de 1.5 segundos
```

**B. Aumentar tiempo de espera**
```python
# Si tienes PC lento, aumentar:
Script.Wait(2500)  # 2.5 segundos
```

**C. Verificar coordenadas**
```python
# Las coordenadas en TELEPORTS deben incluir +0.5 en Z
p.Position = Vector3(x, y, z + 0.5)
```

---

### 5. Vehicle Swap deja al jugador sobre el techo

#### Síntomas
- Al cambiar de vehículo, el jugador aparece parado sobre el auto
- No entra automáticamente al vehículo

#### Soluciones

**A. Verificar uso de nativo SET_PED_INTO_VEHICLE**
```python
# En swap_vehiculo(), debe usar:
Function.Call(Hash.SET_PED_INTO_VEHICLE, p.Handle, v.Handle, -1)

# NO usar:
p.SetIntoVehicle(v, VehicleSeat.Driver)  # Esto causa el bug
```

**B. Verificar elevación del Ped**
```python
# Antes de borrar el vehículo anterior:
p.Position = p.Position + Vector3(0, 0, 0.2)
Script.Wait(10)
```

---

### 6. Streamer.bot no envía comandos

#### Síntomas
- Los regalos de TikTok no ejecutan nada
- Logs de Streamer.bot muestran errores

#### Soluciones

**A. Verificar conexión a TikTok**
```
Streamer.bot → Platforms → TikTok
Estado debe ser: "Connected" (verde)
```

**B. Verificar URL de la API**
```csharp
// En el código C# de Streamer.bot:
var response = client.PostAsync("http://localhost:3000/api/comando", content).Result;

// Verificar que el puerto sea 3000
// Verificar que el dashboard esté corriendo
```

**C. Revisar logs de Streamer.bot**
```
Streamer.bot → Log (pestaña inferior)
Buscar errores HTTP o de conexión
```

**D. Probar manualmente**
```bash
# Usar curl o Postman:
curl -X POST http://localhost:3000/api/comando \
  -H "Content-Type: application/json" \
  -d '{"accion":"curar","prioridad":1}'
```

---

### 7. Comandos se ejecutan muy lento

#### Síntomas
- Hay delay de varios segundos entre el regalo y la ejecución
- Los comandos se acumulan

#### Soluciones

**A. Verificar cola de prioridad**
```bash
# Ver estado de la cola:
http://localhost:3000/api/status

# Limpiar cola manualmente:
curl -X POST http://localhost:3000/api/limpiar-cola
```

**B. Reducir Queue Delay en Streamer.bot**
```
Settings → General → Queue Delay: 1000ms
(Reducir de 2000 a 1000)
```

**C. Verificar FPS del juego**
```
Si el juego va a menos de 30 FPS:
- Reducir configuración gráfica
- Ejecutar limpiar_todo
- Cerrar programas en segundo plano
```

---

### 8. Ataques de NPCs no funcionan

#### Síntomas
- Los NPCs aparecen pero no atacan
- Se quedan parados

#### Soluciones

**A. Verificar función spawn_ataque**
```python
# Debe incluir:
npc.Task.FightAgainst(p)
Function.Call(Hash.SET_PED_COMBAT_ABILITY, npc.Handle, 100)
```

**B. Verificar que el modelo se cargue**
```python
m = Model(modelo_ped)
m.Request(1000)
if not m.IsLoaded:
    return  # El modelo no existe o no se cargó
```

**C. Verificar nombres de modelos**
```
Modelos correctos:
- u_m_y_zombie_01 (zombie)
- s_m_y_clown_01 (payaso)
- s_m_y_cop_01 (policía)

Referencia: https://gtahash.ru/
```

---

### 9. Clima no cambia correctamente

#### Síntomas
- El clima se queda en el anterior
- Hay partículas de nieve/lluvia mezcladas

#### Soluciones

**A. Verificar limpieza de clima**
```python
# Antes de cambiar clima, debe ejecutar:
Function.Call(Hash.CLEAR_OVERRIDE_WEATHER)
Function.Call(Hash.CLEAR_WEATHER_TYPE_PERSIST)
```

**B. Usar comando limpiar_clima**
```
Ejecutar: limpiar_clima
Esto fuerza clima soleado y limpia partículas
```

---

### 10. Error "File in use by another process"

#### Síntomas
- Error al escribir comando_gta.json
- El archivo está bloqueado

#### Soluciones

**A. Verificar que no haya múltiples instancias**
```bash
# Cerrar todos los procesos de Node.js
# Cerrar GTA V
# Reiniciar ambos
```

**B. Agregar manejo de errores**
```python
# El script ya tiene try/except
# Verificar que File.Delete esté en el finally
```

**C. Usar archivo temporal**
```javascript
// En app.js, escribir primero a .tmp:
fs.writeFileSync(RUTA_GTA + '.tmp', JSON.stringify(comando));
fs.renameSync(RUTA_GTA + '.tmp', RUTA_GTA);
```

---

## 🔍 Herramientas de Diagnóstico

### Ver estado del sistema
```bash
http://localhost:3000/api/status
```

Respuesta:
```json
{
  "status": "online",
  "version": "7.0.0",
  "uptime": 3600,
  "commandsThisMinute": 15,
  "features": {
    "priorityQueue": true,
    "autoCleanup": true
  }
}
```

### Ver logs en tiempo real

**Dashboard (Node.js)**
```bash
cd dashboard
node app.js
# Los logs aparecerán en la consola
```

**GTA V (SHVDN)**
```
Abrir: H:\Games\Grand Theft Auto V\ScriptHookVDotNet.log
```

**Streamer.bot**
```
Pestaña "Log" en la interfaz
```

---

## 📞 Checklist de Diagnóstico

Antes de reportar un problema, verifica:

- [ ] Dashboard corriendo en puerto 3000
- [ ] GTA V abierto en modo historia
- [ ] ScriptHookV + SHVDN instalados
- [ ] Script de Python en carpeta `scripts/`
- [ ] Archivo `comando_gta.json` se crea al presionar botones
- [ ] Permisos de escritura en carpeta de GTA V
- [ ] No hay antivirus bloqueando archivos
- [ ] Drivers gráficos actualizados
- [ ] Streamer.bot conectado a TikTok (si aplica)

---

## 🆘 Soporte Adicional

### Archivos de log importantes

1. **ScriptHookVDotNet.log**
   ```
   H:\Games\Grand Theft Auto V\ScriptHookVDotNet.log
   ```

2. **Dashboard logs**
   ```
   Consola donde ejecutaste node app.js
   ```

3. **Streamer.bot logs**
   ```
   Streamer.bot → Log tab
   ```

### Información útil para reportar problemas

```
- Versión de GTA V: _____
- Versión de SHVDN: _____
- Versión de Node.js: _____
- Sistema Operativo: _____
- Comando que falla: _____
- Mensaje de error exacto: _____
- Logs relevantes: _____
```

---

## 🔄 Reset Completo del Sistema

Si nada funciona, reset completo:

```bash
# 1. Cerrar todo
- Cerrar GTA V
- Cerrar Dashboard (Ctrl+C)
- Cerrar Streamer.bot

# 2. Limpiar archivos temporales
- Borrar comando_gta.json
- Borrar cola_espera.json

# 3. Reiniciar en orden
1. Iniciar Dashboard: node app.js
2. Iniciar GTA V
3. Iniciar Streamer.bot (si aplica)
4. Probar comando simple: curar
```

---

**Última actualización**: 2026-02-17  
**Versión del sistema**: 7.0 PILLAR
