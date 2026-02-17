# 🎮 Dashboard GTA V - Guía de Uso

## ¿Qué es esto?

Este es un **panel de control web** para GTA V que te permite ejecutar más de **200 comandos** en el juego desde tu navegador.

## 🔍 Cómo Funciona

### Los Botones SÍ Funcionan

Los botones que ves en el dashboard **NO son solo imágenes** - son botones interactivos que:

1. **Al hacer clic** → Envían un comando al servidor
2. **El servidor** → Escribe el comando en un archivo JSON
3. **El script de Python** → Lee el archivo y ejecuta el comando en GTA V

### Indicadores Visuales

- **Hover (pasar el mouse)**: El botón brilla en verde
- **Click**: El botón se reduce y cambia de color
- **Ejecutando**: Aparece un mensaje verde en la esquina inferior derecha
- **Estado**: En la parte superior verás "🟢 Conectado" o "🔴 Desconectado"

## 📋 Los 200+ Comandos

Los comandos están organizados en **9 categorías**:

### 1. 🧹 Sistema y Limpieza (4 comandos)
- Limpiar mapa
- Reset jugador
- Reparar vehículo
- Forzar clima soleado

### 2. 💀 Ataques y Oleadas (12 comandos)
- Zombies, payasos, policías
- Pandillas (Ballas, Vagos)
- Marines, aliens, rancheros
- Juggernaut, mimos

### 3. 🛡️ Jugador - Superpoderes (14 comandos)
- Curar, blindaje, invencibilidad
- Invisibilidad, super salto, velocidad
- Todas las armas, super fuerza
- Stamina infinita, oxígeno infinito

### 4. 🌍 Clima y Tiempo (16 comandos)
- Todos los climas: sol, lluvia, nieve, niebla
- Tormentas, ventiscas
- Climas especiales: Navidad, Halloween
- Control de hora del día

### 5. 🏎️ Vehículos Deportivos (12 comandos)
- T20, Zentorno, Adder
- Vagner, Emerus, Krieger
- Y más superdeportivos

### 6. 🚜 Pesados y Especiales (13 comandos)
- Tractores, limusinas, buses
- Tanques (Rhino, Khanjali)
- Batmóvil, DeLorean volador
- Oppressor MK2, moto Tron

### 7. ✈️ Aire y Mar (8 comandos)
- Jets: Hydra, Lazer, Avenger
- Helicópteros: Buzzard, Akula
- Submarino, yate, lancha

### 8. 👮 Nivel de Búsqueda (6 comandos)
- De 0 a 5 estrellas
- Control total de la policía

### 9. 📍 Teleport Seguro (14 comandos)
- Casas de personajes
- Lugares icónicos: Casino, aeropuerto
- Base militar, cárcel
- Monte Chiliad, faro, observatorio

## 🚀 Cómo Iniciar

### Opción 1: Usando el script de inicio (Windows)
```bash
cd gta-control-system/dashboard
start.bat
```

### Opción 2: Manualmente
```bash
cd gta-control-system/dashboard
node app.js
```

### Opción 3: Con npm
```bash
cd gta-control-system/dashboard
npm install
npm start
```

## 🌐 Acceder al Dashboard

Una vez iniciado, abre tu navegador en:
```
http://localhost:3000
```

## ⚙️ Configuración

El archivo [`config.json`](config.json) controla:

- **Puerto**: Por defecto 3000
- **Archivos de comando**: Dónde se guardan los comandos
- **Rate limiting**: Tiempo mínimo entre comandos (500ms)
- **Debug mode**: Activado para ver logs en consola

## 🔧 Solución de Problemas

### "Los botones no hacen nada"

**Causa**: El servidor no está corriendo o hay un error de conexión.

**Solución**:
1. Verifica que el servidor esté corriendo (deberías ver logs en la consola)
2. Revisa que estés en `http://localhost:3000`
3. Abre la consola del navegador (F12) para ver errores

### "Error de conexión"

**Causa**: Los archivos de comando no se pueden crear.

**Solución**:
1. Verifica que tengas permisos de escritura en la carpeta
2. Los archivos ahora se crean en `./comando_gta.json` (misma carpeta)

### "Estado: 🔴 Desconectado"

**Causa**: El servidor no responde.

**Solución**:
1. Reinicia el servidor
2. Verifica que no haya otro proceso usando el puerto 3000

## 📝 Notas Importantes

- **Los botones SÍ son clickeables** - no son solo imágenes decorativas
- Cada botón ejecuta un comando específico cuando haces clic
- El sistema tiene rate limiting para evitar spam (500ms entre comandos)
- Puedes ejecutar hasta 60 comandos por minuto
- El modo debug está activado para que veas los logs

## 🎯 Próximos Pasos

Para que los comandos realmente afecten a GTA V, necesitas:

1. **El script de Python** corriendo (`escucha_dashboard.py`)
2. **GTA V abierto** con el mod menu correspondiente
3. **Los archivos de comando** en la ubicación correcta

Consulta [`QUICK_START.md`](../QUICK_START.md) para la configuración completa.
