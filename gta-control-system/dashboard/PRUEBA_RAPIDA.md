# 🧪 Prueba Rápida del Dashboard

## Objetivo
Verificar que los botones del dashboard funcionan correctamente (son clickeables y ejecutan comandos).

## Pasos para Probar

### 1. Instalar Dependencias
```bash
cd gta-control-system/dashboard
npm install
```

### 2. Iniciar el Servidor
```bash
npm start
```

Deberías ver algo como:
```
╔════════════════════════════════════════════════════════╗
║   🎮 GTA V DASHBOARD PILLAR V7 - INICIADO            ║
╠════════════════════════════════════════════════════════╣
║   🌐 URL: http://0.0.0.0:3000                         ║
║   📁 Archivo de comando: ./comando_gta.json...        ║
║   ⚡ Rate Limit: 500ms entre comandos                 ║
║   🎯 Comandos disponibles: 99                         ║
╚════════════════════════════════════════════════════════╝
```

### 3. Abrir el Dashboard
Abre tu navegador en: **http://localhost:3000**

### 4. Probar los Botones

#### ✅ Qué Deberías Ver:
- **9 secciones** con diferentes colores
- **Botones con emojis** y nombres descriptivos
- **Estadísticas** en la parte superior: "200+ Comandos", "9 Categorías"

#### ✅ Qué Deberías Poder Hacer:

1. **Pasar el mouse sobre un botón**:
   - El botón brilla en verde
   - Aparece un efecto de onda
   - El cursor cambia a "pointer" (manita)

2. **Hacer clic en un botón**:
   - El botón se reduce ligeramente
   - Cambia de color a verde brillante
   - Aparece un mensaje en la esquina inferior derecha: "✅ [NOMBRE DEL COMANDO]"
   - El estado cambia a "🟢 Ejecutando..."
   - Después de 1 segundo vuelve a "🟢 Conectado"

3. **Ver el archivo de comando**:
   - Se crea un archivo `comando_gta.json` en la carpeta del dashboard
   - Contiene el último comando ejecutado

### 5. Verificar que Funciona

#### Opción A: Ver el archivo de comando
```bash
# En otra terminal (mientras el servidor corre)
cat gta-control-system/dashboard/comando_gta.json
```

Deberías ver algo como:
```json
{
  "accion": "curar",
  "timestamp": 1708176497085,
  "prioridad": 1
}
```

#### Opción B: Ver los logs del servidor
En la terminal donde corre el servidor, deberías ver:
```
[2026-02-17T12:48:17.085Z] Comando ejecutado: curar (Prioridad: 1)
```

### 6. Probar Diferentes Comandos

Prueba hacer clic en varios botones de diferentes categorías:

- ❤️ CURAR (Sistema)
- 🧟 10 ZOMBIES (Ataques)
- ☀️ SOLEADO (Clima)
- 🏎️ T20 (Vehículos)
- ⭐ 1 ESTRELLA (Búsqueda)
- 🏠 CASA MICHAEL (Teleport)

Cada clic debería:
1. Mostrar el mensaje de confirmación
2. Actualizar el archivo `comando_gta.json`
3. Aparecer en los logs del servidor

## 🎯 Resultado Esperado

Si todo funciona correctamente:

✅ Los botones **SÍ son clickeables** (no son solo imágenes)  
✅ Cada clic ejecuta un comando  
✅ Aparecen mensajes de confirmación  
✅ Se crea/actualiza el archivo JSON  
✅ Los logs muestran la actividad  

## ❌ Problemas Comunes

### "Cannot find module 'express'"
**Solución**: Ejecuta `npm install` en la carpeta dashboard

### "EADDRINUSE: address already in use"
**Solución**: Ya hay algo corriendo en el puerto 3000. Ciérralo o cambia el puerto en `config.json`

### "Los botones no responden"
**Solución**: 
1. Abre la consola del navegador (F12)
2. Ve a la pestaña "Console"
3. Busca errores en rojo
4. Comparte el error para ayudarte

### "Error escribiendo comando"
**Solución**: Verifica que tengas permisos de escritura en la carpeta

## 📊 Estadísticas del Sistema

El dashboard incluye:
- **99 comandos únicos** organizados en 9 categorías
- **Rate limiting**: 500ms entre comandos
- **Máximo**: 60 comandos por minuto
- **Feedback visual** en cada acción

## 🔍 Inspeccionar el Código

Si quieres ver cómo funciona internamente:

1. **Abre el navegador en** http://localhost:3000
2. **Presiona F12** para abrir DevTools
3. **Ve a la pestaña "Elements"**
4. **Inspecciona un botón** - verás que tiene:
   - `onclick="ejecutarComando('id', 'nombre', event)"`
   - `title="descripción del comando"`
   - Estilos CSS para los efectos visuales

## ✅ Confirmación Final

Si puedes:
- ✅ Ver el dashboard con todos los botones
- ✅ Hacer clic en los botones y ver el efecto visual
- ✅ Ver los mensajes de confirmación
- ✅ Ver el archivo `comando_gta.json` actualizándose

**¡Entonces el dashboard está funcionando perfectamente!** 🎉

Los botones **NO son solo imágenes** - son botones interactivos completamente funcionales.

## 🚀 Siguiente Paso

Para que los comandos realmente afecten a GTA V, necesitas:
1. Configurar el script de Python (`escucha_dashboard.py`)
2. Tener GTA V corriendo con el mod menu
3. Conectar todo el sistema

Consulta [`QUICK_START.md`](../QUICK_START.md) para la configuración completa.
