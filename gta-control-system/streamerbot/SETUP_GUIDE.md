# 🎁 Guía de Integración: Streamer.bot + TikTok + GTA V

Esta guía te enseñará a conectar Streamer.bot con tu sistema de control de GTA V para que los regalos de TikTok ejecuten comandos en el juego.

## 📋 Requisitos Previos

- ✅ Streamer.bot instalado y configurado
- ✅ Cuenta de TikTok conectada a Streamer.bot
- ✅ Dashboard de GTA V corriendo en `http://localhost:3000`
- ✅ GTA V con scripts de Python cargados

## 🔧 Paso 1: Configurar Streamer.bot

### 1.1 Abrir Streamer.bot

1. Abre Streamer.bot
2. Ve a la pestaña **"Actions"**
3. Haz clic en **"Add"** para crear una nueva acción

### 1.2 Crear Acción Base

Crea una acción llamada: `GTA_Ejecutar_Comando`

Esta será la acción base que usaremos para todos los comandos.

## 🎯 Paso 2: Configurar Sub-Actions

### 2.1 Agregar Sub-Action de C# Code

1. Dentro de la acción `GTA_Ejecutar_Comando`, haz clic en **"Add Sub-Action"**
2. Selecciona **"Core" → "C# Code"**
3. Pega el siguiente código:

```csharp
using System;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;

public class CPHInline
{
    public bool Execute()
    {
        // Obtener parámetros
        string accion = CPH.GetArgument<string>("accion");
        int prioridad = CPH.GetArgument<int>("prioridad", 1);
        string usuario = CPH.GetArgument<string>("user", "Sistema");
        string regalo = CPH.GetArgument<string>("regalo", "Comando");
        
        // Validar que tengamos una acción
        if (string.IsNullOrEmpty(accion))
        {
            CPH.LogInfo("Error: No se especificó acción");
            return false;
        }
        
        // Preparar datos JSON
        var jsonData = $@"{{
            ""accion"": ""{accion}"",
            ""prioridad"": {prioridad},
            ""usuario"": ""{usuario}"",
            ""regalo"": ""{regalo}""
        }}";
        
        // Enviar a la API del dashboard
        try
        {
            using (var client = new HttpClient())
            {
                client.Timeout = TimeSpan.FromSeconds(5);
                var content = new StringContent(jsonData, Encoding.UTF8, "application/json");
                var response = client.PostAsync("http://localhost:3000/api/comando", content).Result;
                
                if (response.IsSuccessStatusCode)
                {
                    CPH.LogInfo($"✅ Comando ejecutado: {accion} (Prioridad: {prioridad})");
                    return true;
                }
                else
                {
                    CPH.LogWarn($"⚠️ Error HTTP: {response.StatusCode}");
                    return false;
                }
            }
        }
        catch (Exception ex)
        {
            CPH.LogError($"❌ Error: {ex.Message}");
            return false;
        }
    }
}
```

4. Haz clic en **"Compile"** para verificar que no haya errores
5. Guarda la acción

## 🎁 Paso 3: Mapear Regalos de TikTok

### 3.1 Crear Triggers para Regalos

Ahora crearemos triggers específicos para cada regalo de TikTok.

#### Ejemplo: Regalo "Rosa" (1 moneda)

1. Crea una nueva acción llamada: `TikTok_Rosa`
2. En la pestaña **"Triggers"**, haz clic en **"Add"**
3. Selecciona **"TikTok" → "Gift"**
4. En **"Gift Name"**, escribe: `Rosa` (o el nombre exacto del regalo)
5. En **"Sub-Actions"**, agrega:
   - **Execute Method** → Selecciona la acción `GTA_Ejecutar_Comando`
   - **Set Argument**: 
     - Name: `accion`, Value: `curar`
     - Name: `prioridad`, Value: `1`
     - Name: `regalo`, Value: `Rosa`

#### Ejemplo: Regalo "León" (40,000 monedas)

1. Crea una nueva acción llamada: `TikTok_Leon`
2. Trigger: **TikTok Gift** → `León`
3. Sub-Actions (múltiples comandos):
   - **Execute Method** → `GTA_Ejecutar_Comando`
     - `accion`: `atk_juggernaut`, `prioridad`: `10`
   - **Delay** → 2000ms
   - **Execute Method** → `GTA_Ejecutar_Comando`
     - `accion`: `inv_on`, `prioridad`: `10`
   - **Delay** → 2000ms
   - **Execute Method** → `GTA_Ejecutar_Comando`
     - `accion`: `armas`, `prioridad`: `10`
   - **Delay** → 2000ms
   - **Execute Method** → `GTA_Ejecutar_Comando`
     - `accion`: `veh_khanjali`, `prioridad`: `10`

### 3.2 Tabla de Mapeo Sugerido

| Regalo TikTok | Monedas | Prioridad | Comando(s) | Descripción |
|---------------|---------|-----------|------------|-------------|
| Rosa | 1 | 1 | `curar` | Curación básica |
| Corazón | 10 | 1 | `blindaje` | Armadura completa |
| Helado | 30 | 2 | `cl_rnd` | Clima aleatorio |
| Diamante | 100 | 3 | `veh_t20` | Superdeportivo T20 |
| Castillo | 500 | 4 | `atk_zombies_10` | 10 zombies |
| Cohete | 500 | 4 | `veh_hydra` | Jet militar |
| Yate | 1000 | 5 | `atk_marines` | Marines armados |
| León | 40000 | 10 | Combo épico | Juggernaut + Dios + Armas + Tanque |

## 💬 Paso 4: Comandos de Chat

### 4.1 Crear Comandos de Chat

Permite que los espectadores usen comandos en el chat.

#### Ejemplo: !auto

1. Crea una nueva acción: `Chat_Auto`
2. Trigger: **TikTok Chat Command** → `!auto`
3. Sub-Action:
   - **Execute Method** → `GTA_Ejecutar_Comando`
   - Arguments: `accion`: `rnd_veh`, `prioridad`: `2`

#### Comandos Sugeridos

```
!auto      → rnd_veh (Vehículo aleatorio)
!clima     → cl_rnd (Clima aleatorio)
!curar     → curar (Curación)
!armas     → armas (Todas las armas)
!tp        → tp_mazebank (Teleport Maze Bank)
!caos      → atk_rnd (Ataque aleatorio)
!limpiar   → limpiar_todo (Limpiar mapa)
```

## 🎯 Paso 5: Eventos Automáticos

### 5.1 Nuevo Seguidor

Cuando alguien te sigue, ejecuta un comando especial:

1. Acción: `TikTok_NuevoSeguidor`
2. Trigger: **TikTok Follow**
3. Sub-Action:
   - **Execute Method** → `GTA_Ejecutar_Comando`
   - Arguments: `accion`: `cl_rnd`, `prioridad`: `2`

### 5.2 Nuevo Suscriptor

1. Acción: `TikTok_NuevoSub`
2. Trigger: **TikTok Subscribe**
3. Sub-Action:
   - **Execute Method** → `GTA_Ejecutar_Comando`
   - Arguments: `accion`: `veh_deluxo`, `prioridad`: `5`

## 🔄 Paso 6: Sistema de Cola (Opcional)

Si recibes muchos regalos a la vez, puedes configurar un sistema de cola:

### 6.1 Configurar Queue en Streamer.bot

1. Ve a **Settings** → **General**
2. Activa **"Queue Actions"**
3. Configura:
   - **Queue Delay**: 2000ms (2 segundos entre comandos)
   - **Max Queue Size**: 50

Esto evitará que el juego se sature con demasiados comandos simultáneos.

## 🧪 Paso 7: Probar la Integración

### 7.1 Test Manual

1. En Streamer.bot, haz clic derecho en una acción
2. Selecciona **"Test"**
3. Verifica que el comando se ejecute en GTA V

### 7.2 Test en Vivo

1. Inicia un directo de prueba en TikTok
2. Envía un regalo desde otra cuenta
3. Verifica que el comando se ejecute en el juego

## 🛠️ Solución de Problemas

### Problema: Los comandos no se ejecutan

**Solución:**
1. Verifica que el dashboard esté corriendo: `http://localhost:3000`
2. Revisa los logs de Streamer.bot (pestaña **"Log"**)
3. Verifica que el archivo `comando_gta.json` se esté creando en:
   ```
   H:\Games\Grand Theft Auto V\comando_gta.json
   ```

### Problema: Comandos se ejecutan muy lento

**Solución:**
1. Reduce el **Queue Delay** en Streamer.bot
2. Verifica que el script de Python esté cargado en GTA V
3. Revisa que no haya demasiadas entidades en el mapa (usa `limpiar_todo`)

### Problema: Algunos regalos no funcionan

**Solución:**
1. Verifica el nombre exacto del regalo en TikTok
2. Los nombres pueden variar según el idioma/región
3. Usa el **Event Viewer** de Streamer.bot para ver el nombre real del regalo

## 📊 Monitoreo en Tiempo Real

### Ver Comandos Ejecutados

Puedes ver el estado del sistema en:
```
http://localhost:3000/api/status
```

Esto te mostrará:
- Estado del servidor
- Comandos ejecutados por minuto
- Uptime del sistema

## 🎨 Personalización Avanzada

### Crear Combos Personalizados

Puedes crear secuencias de comandos para regalos especiales:

```csharp
// Combo "Apocalipsis" (para regalo muy caro)
public bool Execute()
{
    // 1. Activar modo dios
    EnviarComando("inv_on", 10);
    System.Threading.Thread.Sleep(1000);
    
    // 2. Dar todas las armas
    EnviarComando("armas", 10);
    System.Threading.Thread.Sleep(1000);
    
    // 3. Spawnear tanque
    EnviarComando("veh_rhino", 10);
    System.Threading.Thread.Sleep(2000);
    
    // 4. 5 estrellas de policía
    EnviarComando("w_5", 10);
    System.Threading.Thread.Sleep(1000);
    
    // 5. Ataque de marines
    EnviarComando("atk_marines", 10);
    
    return true;
}

private void EnviarComando(string accion, int prioridad)
{
    CPH.SetArgument("accion", accion);
    CPH.SetArgument("prioridad", prioridad);
    CPH.RunAction("GTA_Ejecutar_Comando", false);
}
```

## 📝 Notas Finales

- **Seguridad**: Este sistema solo funciona localmente. No expone tu juego a internet.
- **Rendimiento**: El sistema está optimizado para manejar hasta 60 comandos por minuto.
- **Estabilidad**: La limpieza automática cada 60 segundos previene crashes.

## 🔗 Referencias

- [Streamer.bot Documentation](https://docs.streamer.bot/)
- [TikTok Gifts (Venezuela)](https://streamtoearn.io/gifts?region=VE)
- [Dashboard API](http://localhost:3000/api/status)

---

**¿Necesitas ayuda?** Revisa los logs en:
- Streamer.bot: Pestaña "Log"
- Dashboard: Consola de Node.js
- GTA V: ScriptHookVDotNet.log
