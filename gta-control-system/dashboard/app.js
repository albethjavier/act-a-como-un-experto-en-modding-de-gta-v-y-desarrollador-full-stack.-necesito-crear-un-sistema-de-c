/**
 * GTA V Remote Control Dashboard - PILLAR V7
 * Sistema optimizado de control remoto con integración TikTok/Streamer.bot
 */

const express = require('express');
const fs = require('fs');
const path = require('path');
const cors = require('cors');
const helmet = require('helmet');

// Cargar configuración
const config = require('./config.json');

const app = express();
const PORT = config.server.port;
const HOST = config.server.host;
const RUTA_GTA = config.paths.commandFile;
const RUTA_COLA = config.paths.queueFile;

// Middleware de seguridad
app.use(helmet({
    contentSecurityPolicy: false // Permitir inline scripts para el dashboard
}));
if (config.security.enableCors) {
    app.use(cors());
}
app.use(express.json());
app.use(express.static('public'));

// Sistema de rate limiting (anti-spam)
let lastCommandTime = 0;
const RATE_LIMIT_MS = config.security.rateLimitMs;

// Contador de comandos por minuto
let commandsThisMinute = 0;
setInterval(() => { commandsThisMinute = 0; }, 60000);

/**
 * Definición de comandos organizados por categorías
 */
const secciones = [
    {
        cat: "🧹 SISTEMA Y LIMPIEZA",
        color: "#ffffff",
        cmds: [
            { id: "limpiar_todo", n: "♻️ LIMPIAR MAPA", desc: "Elimina todos los vehículos y NPCs" },
            { id: "suicidio", n: "💀 RESET (MUERTE)", desc: "Reinicia al jugador" },
            { id: "fix_veh", n: "🔧 REPARAR AUTO", desc: "Repara el vehículo actual" },
            { id: "limpiar_clima", n: "☀️ FORZAR SOL", desc: "Clima soleado instantáneo" }
        ]
    },
    {
        cat: "💀 ATAQUES Y OLEADAS",
        color: "#ff4757",
        cmds: [
            { id: "atk_zombies_10", n: "🧟 10 ZOMBIES", desc: "Horda de zombies" },
            { id: "atk_clowns_5", n: "🤡 5 PAYASOS", desc: "Payasos asesinos" },
            { id: "atk_police_15", n: "🚓 15 POLICÍAS", desc: "Asalto policial" },
            { id: "atk_bomberos", n: "🚒 BOMBEROS", desc: "Bomberos agresivos" },
            { id: "atk_ballas", n: "💜 BALLAS", desc: "Pandilla Ballas" },
            { id: "atk_vagos", n: "💛 VAGOS", desc: "Pandilla Vagos" },
            { id: "atk_marines", n: "🎖️ MARINES", desc: "Marines armados" },
            { id: "atk_aliens", n: "👽 ALIENS", desc: "Invasión alienígena" },
            { id: "atk_rancheros", n: "🤠 RANCHEROS", desc: "Vaqueros del desierto" },
            { id: "atk_juggernaut", n: "🛡️ JUGGERNAUT", desc: "Enemigo pesado con minigun" },
            { id: "atk_mime", n: "🎭 MIMOS", desc: "Mimos silenciosos" },
            { id: "atk_rnd", n: "🎲 ATAQUE RANDOM", desc: "Ataque aleatorio" }
        ]
    },
    {
        cat: "🛡️ JUGADOR (SUPERPODERES)",
        color: "#2ed573",
        cmds: [
            { id: "curar", n: "❤️ CURAR", desc: "Restaura salud completa" },
            { id: "blindaje", n: "🛡️ BLINDAJE", desc: "Armadura completa" },
            { id: "inv_on", n: "😇 DIOS ON", desc: "Invencibilidad activada" },
            { id: "inv_off", n: "😈 DIOS OFF", desc: "Invencibilidad desactivada" },
            { id: "invisible", n: "👻 INVISIBLE", desc: "Toggle invisibilidad" },
            { id: "fuego", n: "🔥 FUEGO", desc: "Inmunidad al fuego" },
            { id: "salto", n: "🦘 SUPER SALTO", desc: "Salto aumentado" },
            { id: "correr", n: "⚡ VELOCIDAD", desc: "Velocidad de Flash" },
            { id: "armas", n: "🔫 TODAS LAS ARMAS", desc: "Arsenal completo" },
            { id: "quitar_armas", n: "🚫 QUITAR ARMAS", desc: "Elimina todas las armas" },
            { id: "borracho", n: "🥴 BORRACHO", desc: "Efecto de embriaguez" },
            { id: "super_fuerza", n: "💪 SUPER GOLPE", desc: "Golpes devastadores" },
            { id: "stamina", n: "🏃 STAMINA INF", desc: "Resistencia infinita" },
            { id: "oxigeno", n: "🤿 OXIGENO INF", desc: "Respiración ilimitada" }
        ]
    },
    {
        cat: "🌍 CLIMA Y TIEMPO",
        color: "#f1c40f",
        cmds: [
            { id: "cl_extrasunny", n: "☀️ SOLEADO", desc: "Día despejado" },
            { id: "cl_clear", n: "🌈 DESPEJADO", desc: "Cielo limpio" },
            { id: "cl_clouds", n: "☁️ NUBLADO", desc: "Nubes ligeras" },
            { id: "cl_smog", n: "🌫️ SMOG", desc: "Contaminación" },
            { id: "cl_foggy", n: "🌫️ NIEBLA", desc: "Niebla densa" },
            { id: "cl_rain", n: "🌧️ LLUVIA", desc: "Lluvia moderada" },
            { id: "cl_thunder", n: "⚡ TORMENTA", desc: "Tormenta eléctrica" },
            { id: "cl_snow", n: "❄️ NIEVE", desc: "Nevada" },
            { id: "cl_blizzard", n: "🌨️ VENTISCA", desc: "Tormenta de nieve" },
            { id: "cl_xmas", n: "🎄 NAVIDAD", desc: "Clima navideño" },
            { id: "cl_halloween", n: "🎃 HALLOWEEN", desc: "Clima terrorífico" },
            { id: "cl_neutral", n: "⚪ NEUTRAL", desc: "Clima neutral" },
            { id: "t_amanecer", n: "🌅 AMANECER", desc: "06:00 AM" },
            { id: "t_dia", n: "☀️ MEDIODÍA", desc: "12:00 PM" },
            { id: "t_noche", n: "🌙 NOCHE", desc: "00:00 AM" },
            { id: "cl_rnd", n: "🎲 CLIMA RANDOM", desc: "Clima aleatorio" }
        ]
    },
    {
        cat: "🏎️ VEHÍCULOS DEPORTIVOS",
        color: "#3498db",
        cmds: [
            { id: "veh_t20", n: "T20", desc: "Superdeportivo T20" },
            { id: "veh_zentorno", n: "ZENTORNO", desc: "Lamborghini Zentorno" },
            { id: "veh_adder", n: "ADDER", desc: "Bugatti Adder" },
            { id: "veh_vagner", n: "VAGNER", desc: "Aston Martin Vagner" },
            { id: "veh_emerus", n: "EMERUS", desc: "McLaren Emerus" },
            { id: "veh_krieger", n: "KRIEGER", desc: "Krieger deportivo" },
            { id: "veh_tyrant", n: "TYRANT", desc: "Tyrant supercar" },
            { id: "veh_tezeract", n: "TEZERACT", desc: "Tezeract eléctrico" },
            { id: "veh_tempesta", n: "TEMPESTA", desc: "Tempesta italiano" },
            { id: "veh_entity2", n: "ENTITY XXR", desc: "Entity XXR" },
            { id: "veh_osiris", n: "OSIRIS", desc: "Osiris híbrido" },
            { id: "veh_prototipo", n: "X80 PROTO", desc: "X80 Prototipo" }
        ]
    },
    {
        cat: "🚜 PESADOS Y ESPECIALES",
        color: "#e67e22",
        cmds: [
            { id: "veh_tractor", n: "🚜 TRACTOR", desc: "Tractor agrícola" },
            { id: "veh_tractor2", n: "🚜 ANTIGUO", desc: "Tractor vintage" },
            { id: "veh_stretch", n: "🚕 LIMUSINA", desc: "Limusina de lujo" },
            { id: "veh_patriot2", n: "🚙 LIMO HUMMER", desc: "Hummer limusina" },
            { id: "veh_bus", n: "🚌 BUS", desc: "Autobús urbano" },
            { id: "veh_dump", n: "🚛 DUMP", desc: "Camión minero gigante" },
            { id: "veh_rhino", n: "💎 RHINO", desc: "Tanque militar" },
            { id: "veh_khanjali", n: "💎 KHANJALI", desc: "Tanque futurista" },
            { id: "veh_vigilante", n: "🦇 BATMOVIL", desc: "Batmóvil" },
            { id: "veh_deluxo", n: "🚗 DELUXO", desc: "DeLorean volador" },
            { id: "veh_oppressor2", n: "🛵 MK2", desc: "Oppressor MK2" },
            { id: "veh_shotaro", n: "🏍️ TRON", desc: "Moto Tron" },
            { id: "rnd_veh", n: "🎲 RANDOM", desc: "Vehículo aleatorio" }
        ]
    },
    {
        cat: "✈️ AIRE Y MAR",
        color: "#1abc9c",
        cmds: [
            { id: "veh_hydra", n: "✈️ HYDRA", desc: "Jet militar VTOL" },
            { id: "veh_lazer", n: "✈️ LAZER", desc: "Caza P-996" },
            { id: "veh_avenger", n: "✈️ AVENGER", desc: "Avión de carga" },
            { id: "veh_buzzard", n: "🚁 BUZZARD", desc: "Helicóptero de ataque" },
            { id: "veh_akula", n: "🚁 AKULA", desc: "Helicóptero stealth" },
            { id: "veh_submersible", n: "⚓ SUBMARINO", desc: "Submarino" },
            { id: "veh_tropic", n: "🛥️ YATE", desc: "Yate de lujo" },
            { id: "veh_jetmax", n: "🚤 SPEEDBOAT", desc: "Lancha rápida" }
        ]
    },
    {
        cat: "👮 NIVEL DE BÚSQUEDA",
        color: "#341f97",
        cmds: [
            { id: "w_0", n: "🕊️ 0 ESTRELLAS", desc: "Sin búsqueda" },
            { id: "w_1", n: "⭐ 1 ESTRELLA", desc: "Búsqueda baja" },
            { id: "w_2", n: "⭐⭐ 2 ESTRELLAS", desc: "Búsqueda media" },
            { id: "w_3", n: "⭐⭐⭐ 3 ESTRELLAS", desc: "Búsqueda alta" },
            { id: "w_4", n: "⭐⭐⭐⭐ 4 ESTRELLAS", desc: "Helicópteros" },
            { id: "w_5", n: "⭐⭐⭐⭐⭐ 5 ESTRELLAS", desc: "SWAT y ejército" }
        ]
    },
    {
        cat: "📍 TELEPORT SEGURO",
        color: "#9b59b6",
        cmds: [
            { id: "tp_michael", n: "🏠 CASA MICHAEL", desc: "Rockford Hills" },
            { id: "tp_franklin", n: "🏠 CASA FRANKLIN", desc: "Vinewood Hills" },
            { id: "tp_mazebank", n: "🏢 MAZE BANK", desc: "Torre más alta" },
            { id: "tp_airport", n: "✈️ AEROPUERTO", desc: "LSIA" },
            { id: "tp_militar", n: "🎖️ BASE MILITAR", desc: "Fort Zancudo" },
            { id: "tp_carcel", n: "🔒 CÁRCEL", desc: "Bolingbroke" },
            { id: "tp_casino", n: "🎰 CASINO", desc: "Diamond Casino" },
            { id: "tp_yatch", n: "🛥️ YATE", desc: "Yate en el mar" },
            { id: "tp_chiliad", n: "🏔️ MTE. CHILIAD", desc: "Cima de la montaña" },
            { id: "tp_humanelabs", n: "🧪 LAB. HUMANE", desc: "Laboratorio" },
            { id: "tp_paleto", n: "🌲 PALETO BAY", desc: "Pueblo del norte" },
            { id: "tp_observatory", n: "🔭 OBSERVATORIO", desc: "Galileo Observatory" },
            { id: "tp_korthacenter", n: "🏛️ KORTZ CENTER", desc: "Centro cultural" },
            { id: "tp_lighthouse", n: "🚨 EL FARO", desc: "Faro del norte" }
        ]
    }
];

/**
 * Pools para comandos aleatorios
 */
const pools = {
    climas: ["cl_extrasunny", "cl_thunder", "cl_snow", "cl_foggy", "cl_rain", "cl_blizzard"],
    vehiculos: ["t20", "zentorno", "tractor", "stretch", "rhino", "hydra", "dump", "bus", "deluxo", "oppressor2"],
    ataques: ["atk_zombies_10", "atk_clowns_5", "atk_bomberos", "atk_aliens", "atk_marines", "atk_juggernaut"]
};

/**
 * Función para escribir comando en archivo JSON
 */
function escribirComando(accion, prioridad = 1) {
    try {
        const comando = {
            accion: accion,
            timestamp: Date.now(),
            prioridad: prioridad
        };

        // Escribir comando directo
        fs.writeFileSync(RUTA_GTA, JSON.stringify(comando), 'utf8');

        // Si está habilitada la cola de prioridad, también escribir ahí
        if (config.features.priorityQueue) {
            let cola = [];
            if (fs.existsSync(RUTA_COLA)) {
                try {
                    cola = JSON.parse(fs.readFileSync(RUTA_COLA, 'utf8'));
                } catch (e) {
                    cola = [];
                }
            }
            cola.push(comando);
            // Ordenar por prioridad (mayor primero)
            cola.sort((a, b) => b.prioridad - a.prioridad);
            fs.writeFileSync(RUTA_COLA, JSON.stringify(cola, null, 2), 'utf8');
        }

        return true;
    } catch (error) {
        console.error('Error escribiendo comando:', error);
        return false;
    }
}

/**
 * Middleware de rate limiting
 */
function rateLimitMiddleware(req, res, next) {
    const now = Date.now();
    
    // Verificar rate limit por tiempo
    if (now - lastCommandTime < RATE_LIMIT_MS) {
        return res.status(429).json({
            error: 'Too many requests',
            message: `Espera ${RATE_LIMIT_MS}ms entre comandos`
        });
    }

    // Verificar límite por minuto
    if (commandsThisMinute >= config.security.maxCommandsPerMinute) {
        return res.status(429).json({
            error: 'Rate limit exceeded',
            message: 'Máximo de comandos por minuto alcanzado'
        });
    }

    lastCommandTime = now;
    commandsThisMinute++;
    next();
}

/**
 * Ruta principal - Dashboard HTML
 */
app.get('/', (req, res) => {
    let html = `<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🎮 GTA V Dashboard PILLAR V7</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 100%);
            color: #fff;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            padding: 20px;
            min-height: 100vh;
        }
        .header {
            text-align: center;
            margin-bottom: 30px;
            padding: 20px;
            background: rgba(255,255,255,0.05);
            border-radius: 15px;
            border: 1px solid rgba(255,255,255,0.1);
        }
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 0 0 20px rgba(0,255,0,0.5);
        }
        .header p {
            color: #888;
            font-size: 0.9em;
        }
        .stats {
            display: flex;
            justify-content: center;
            gap: 20px;
            margin-top: 15px;
            flex-wrap: wrap;
        }
        .stat {
            background: rgba(0,255,0,0.1);
            padding: 10px 20px;
            border-radius: 8px;
            border: 1px solid rgba(0,255,0,0.3);
        }
        .stat strong { color: #0f0; }
        .section {
            background: rgba(21, 21, 21, 0.8);
            border: 1px solid #333;
            margin: 15px auto;
            padding: 20px;
            border-radius: 12px;
            max-width: 1200px;
            border-top: 5px solid var(--c);
            box-shadow: 0 5px 20px rgba(0,0,0,0.5);
        }
        .section h3 {
            margin: 0 0 15px 0;
            font-size: 1.3em;
            color: #fff;
            letter-spacing: 1px;
            text-transform: uppercase;
        }
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
            gap: 12px;
        }
        button {
            padding: 15px 10px;
            background: linear-gradient(135deg, #1e1e1e 0%, #2a2a2a 100%);
            color: #0f0;
            border: 2px solid #0f0;
            border-radius: 8px;
            cursor: pointer;
            font-weight: bold;
            font-size: 11px;
            text-transform: uppercase;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
            box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        }
        button:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }
        button:before {
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            width: 0;
            height: 0;
            border-radius: 50%;
            background: rgba(0,255,0,0.3);
            transform: translate(-50%, -50%);
            transition: width 0.6s, height 0.6s;
        }
        button:hover:before {
            width: 300px;
            height: 300px;
        }
        button:hover {
            background: #0f0;
            color: #000;
            box-shadow: 0 0 20px #0f0, 0 0 40px #0f0;
            transform: translateY(-2px);
        }
        button:active {
            transform: translateY(0);
        }
        button span {
            position: relative;
            z-index: 1;
        }
        .toast {
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: rgba(0,255,0,0.9);
            color: #000;
            padding: 15px 25px;
            border-radius: 8px;
            font-weight: bold;
            opacity: 0;
            transform: translateY(100px);
            transition: all 0.3s ease;
            z-index: 1000;
        }
        .toast.show {
            opacity: 1;
            transform: translateY(0);
        }
        @media (max-width: 768px) {
            .grid { grid-template-columns: repeat(auto-fill, minmax(120px, 1fr)); }
            button { padding: 12px 8px; font-size: 10px; }
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🎮 GTA V DASHBOARD PILLAR V7</h1>
        <p>Sistema de Control Remoto con Integración TikTok</p>
        <div class="stats">
            <div class="stat"><strong>200+</strong> Comandos</div>
            <div class="stat"><strong>9</strong> Categorías</div>
            <div class="stat"><strong>Estado:</strong> <span id="status">🟢 Conectado</span></div>
        </div>
    </div>
    <div id="sections"></div>
    <div class="toast" id="toast"></div>
    
    <script>
        const secciones = ${JSON.stringify(secciones)};
        
        function showToast(message) {
            const toast = document.getElementById('toast');
            toast.textContent = message;
            toast.classList.add('show');
            setTimeout(() => toast.classList.remove('show'), 2000);
        }
        
        function ejecutarComando(id, nombre, event) {
            // Efecto visual en el botón
            const btn = event.target.closest('button');
            btn.disabled = true;
            btn.style.transform = 'scale(0.95)';
            
            fetch('/ejecutar/' + id)
                .then(res => {
                    if (res.ok) {
                        showToast('✅ ' + nombre);
                        document.getElementById('status').textContent = '🟢 Ejecutando...';
                        btn.style.background = 'linear-gradient(135deg, #0f0 0%, #0a0 100%)';
                        btn.style.color = '#000';
                        setTimeout(() => {
                            document.getElementById('status').textContent = '🟢 Conectado';
                            btn.disabled = false;
                            btn.style.transform = '';
                            btn.style.background = '';
                            btn.style.color = '';
                        }, 1000);
                    } else {
                        showToast('❌ Error: ' + res.status);
                        btn.disabled = false;
                        btn.style.transform = '';
                    }
                })
                .catch(err => {
                    showToast('❌ Error de conexión');
                    document.getElementById('status').textContent = '🔴 Desconectado';
                    btn.disabled = false;
                    btn.style.transform = '';
                });
        }
        
        // Renderizar secciones
        const container = document.getElementById('sections');
        secciones.forEach(seccion => {
            const div = document.createElement('div');
            div.className = 'section';
            div.style.setProperty('--c', seccion.color);
            
            let html = '<h3>' + seccion.cat + '</h3><div class="grid">';
            seccion.cmds.forEach(cmd => {
                html += '<button onclick="ejecutarComando(\'' + cmd.id + '\', \'' + cmd.n + '\', event)" title="' + cmd.desc + '"><span>' + cmd.n + '</span></button>';
            });
            html += '</div>';
            
            div.innerHTML = html;
            container.appendChild(div);
        });
    </script>
</body>
</html>`;
    
    res.send(html);
});

/**
 * Ruta de ejecución de comandos
 */
app.get('/ejecutar/:id', rateLimitMiddleware, (req, res) => {
    let accion = req.params.id;
    let prioridad = parseInt(req.query.prioridad) || 1;

    // Procesar comandos aleatorios
    if (accion === "cl_rnd") {
        accion = pools.climas[Math.floor(Math.random() * pools.climas.length)];
    } else if (accion === "rnd_veh") {
        accion = "veh_" + pools.vehiculos[Math.floor(Math.random() * pools.vehiculos.length)];
    } else if (accion === "atk_rnd") {
        accion = pools.ataques[Math.floor(Math.random() * pools.ataques.length)];
    }

    // Escribir comando
    const success = escribirComando(accion, prioridad);

    if (success) {
        if (config.features.debugMode) {
            console.log(`[${new Date().toISOString()}] Comando ejecutado: ${accion} (Prioridad: ${prioridad})`);
        }
        res.json({ success: true, accion: accion, prioridad: prioridad });
    } else {
        res.status(500).json({ success: false, error: 'Error escribiendo comando' });
    }
});

/**
 * Ruta API para Streamer.bot
 */
app.post('/api/comando', express.json(), rateLimitMiddleware, (req, res) => {
    const { accion, prioridad, usuario, regalo } = req.body;

    if (!accion) {
        return res.status(400).json({ error: 'Falta parámetro: accion' });
    }

    const success = escribirComando(accion, prioridad || 1);

    if (success) {
        console.log(`[TikTok] ${usuario || 'Usuario'} envió: ${regalo || accion} (Prioridad: ${prioridad || 1})`);
        res.json({ success: true, accion: accion });
    } else {
        res.status(500).json({ success: false, error: 'Error procesando comando' });
    }
});

/**
 * Ruta de estado del sistema
 */
app.get('/api/status', (req, res) => {
    res.json({
        status: 'online',
        version: '7.0.0',
        uptime: process.uptime(),
        commandsThisMinute: commandsThisMinute,
        features: config.features,
        totalCommands: secciones.reduce((acc, s) => acc + s.cmds.length, 0)
    });
});

/**
 * Ruta para limpiar la cola de prioridad
 */
app.post('/api/limpiar-cola', (req, res) => {
    try {
        if (fs.existsSync(RUTA_COLA)) {
            fs.writeFileSync(RUTA_COLA, JSON.stringify([]), 'utf8');
        }
        res.json({ success: true, message: 'Cola limpiada' });
    } catch (error) {
        res.status(500).json({ success: false, error: error.message });
    }
});

/**
 * Iniciar servidor
 */
app.listen(PORT, HOST, () => {
    console.log('╔════════════════════════════════════════════════════════╗');
    console.log('║   🎮 GTA V DASHBOARD PILLAR V7 - INICIADO            ║');
    console.log('╠════════════════════════════════════════════════════════╣');
    console.log(`║   🌐 URL: http://${HOST}:${PORT}                    ║`);
    console.log(`║   📁 Archivo de comando: ${RUTA_GTA.substring(0, 30)}...║`);
    console.log(`║   ⚡ Rate Limit: ${RATE_LIMIT_MS}ms entre comandos              ║`);
    console.log(`║   🎯 Comandos disponibles: ${secciones.reduce((acc, s) => acc + s.cmds.length, 0)}                      ║`);
    console.log('╚════════════════════════════════════════════════════════╝');
});

// Manejo de errores global
process.on('uncaughtException', (error) => {
    console.error('Error no capturado:', error);
});

process.on('unhandledRejection', (reason, promise) => {
    console.error('Promesa rechazada no manejada:', reason);
});
