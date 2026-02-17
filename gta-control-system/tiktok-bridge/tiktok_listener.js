/**
 * TikTok Live → GTA V Bridge
 * Escucha eventos de TikTok Live y los envía al dashboard de GTA V
 * 
 * Instalación:
 * npm install tiktok-live-connector axios
 * 
 * Uso:
 * node tiktok_listener.js TU_USUARIO_TIKTOK
 */

const { WebcastPushConnection } = require('tiktok-live-connector');
const axios = require('axios');

// Configuración
const DASHBOARD_URL = 'http://localhost:3000';
const TIKTOK_USERNAME = process.argv[2] || 'tu_usuario_tiktok';

// Validar que se proporcionó un usuario
if (TIKTOK_USERNAME === 'tu_usuario_tiktok') {
    console.error('❌ Error: Debes proporcionar tu nombre de usuario de TikTok');
    console.log('Uso: node tiktok_listener.js TU_USUARIO_TIKTOK');
    process.exit(1);
}

// Mapeo de regalos a comandos (basado en nombres en inglés)
const GIFT_COMMANDS = {
    // Regalos básicos (1-50 monedas)
    'Rose': { cmd: 'curar', priority: 1, desc: 'Curación' },
    'TikTok': { cmd: 'curar', priority: 1, desc: 'Curación' },
    'Heart': { cmd: 'blindaje', priority: 1, desc: 'Armadura' },
    'Thumbs Up': { cmd: 'fix_veh', priority: 1, desc: 'Reparar vehículo' },
    'Ice Cream': { cmd: 'cl_rnd', priority: 2, desc: 'Clima aleatorio' },
    'Donut': { cmd: 't_dia', priority: 2, desc: 'Mediodía' },
    'Rainbow': { cmd: 'cl_clear', priority: 2, desc: 'Clima despejado' },
    
    // Regalos medios (100-500 monedas)
    'Diamond': { cmd: 'veh_t20', priority: 3, desc: 'T20' },
    'Crown': { cmd: 'veh_zentorno', priority: 3, desc: 'Zentorno' },
    'Trophy': { cmd: 'veh_adder', priority: 3, desc: 'Adder' },
    'Castle': { cmd: 'atk_zombies_10', priority: 4, desc: '10 Zombies' },
    'Rocket': { cmd: 'atk_police_15', priority: 4, desc: 'Policías' },
    'Ferrari': { cmd: 'veh_rhino', priority: 4, desc: 'Tanque' },
    
    // Regalos caros (1000-5000 monedas)
    'Yacht': { cmd: 'atk_marines', priority: 5, desc: 'Marines' },
    'Plane': { cmd: 'veh_hydra', priority: 5, desc: 'Jet Hydra' },
    'Mansion': { cmd: 'atk_aliens', priority: 5, desc: 'Aliens' },
    'Planet': { cmd: 'atk_juggernaut', priority: 6, desc: 'Juggernaut' },
    'Galaxy': { cmd: 'w_5', priority: 6, desc: '5 Estrellas' },
    'Universe': { cmd: 'limpiar_todo', priority: 6, desc: 'Limpiar todo' },
    
    // Regalos legendarios (40000+ monedas) - Combos
    'Lion': { 
        combo: ['atk_juggernaut', 'inv_on', 'armas', 'veh_khanjali'], 
        priority: 10, 
        desc: 'Combo Legendario' 
    },
    'Dragon': { 
        combo: ['w_5', 'atk_marines', 'atk_police_15'], 
        priority: 10, 
        desc: 'Caos Total' 
    },
    'Phoenix': { 
        combo: ['limpiar_todo', 'curar', 'inv_on', 'veh_hydra'], 
        priority: 10, 
        desc: 'Renacimiento' 
    }
};

// Mapeo de comandos de chat
const CHAT_COMMANDS = {
    '!auto': 'rnd_veh',
    '!clima': 'cl_rnd',
    '!curar': 'curar',
    '!armas': 'armas',
    '!tp': 'tp_mazebank',
    '!caos': 'atk_rnd',
    '!limpiar': 'limpiar_todo',
    '!tanque': 'veh_rhino',
    '!jet': 'veh_hydra',
    '!zombies': 'atk_zombies_10',
    '!dios': 'inv_on',
    '!mortal': 'inv_off'
};

// Estadísticas
let stats = {
    giftsReceived: 0,
    commandsExecuted: 0,
    chatCommands: 0,
    errors: 0,
    startTime: Date.now()
};

/**
 * Enviar comando al dashboard
 */
async function sendCommand(command, priority = 1, username = 'Sistema', gift = 'Comando') {
    try {
        const response = await axios.post(`${DASHBOARD_URL}/api/comando`, {
            accion: command,
            prioridad: priority,
            usuario: username,
            regalo: gift
        }, {
            timeout: 5000
        });
        
        if (response.data.success) {
            stats.commandsExecuted++;
            console.log(`✅ [${new Date().toLocaleTimeString()}] ${username} → ${gift} → ${command}`);
            return true;
        }
        return false;
    } catch (error) {
        stats.errors++;
        console.error(`❌ Error enviando comando: ${error.message}`);
        return false;
    }
}

/**
 * Ejecutar combo de comandos con delays
 */
async function executeCombo(commands, priority, username, gift) {
    console.log(`🎁 [COMBO] ${username} envió ${gift} → ${commands.length} comandos`);
    
    for (let i = 0; i < commands.length; i++) {
        await sendCommand(commands[i], priority, username, `${gift} (${i+1}/${commands.length})`);
        
        // Delay entre comandos del combo
        if (i < commands.length - 1) {
            await new Promise(resolve => setTimeout(resolve, 2000));
        }
    }
}

/**
 * Verificar que el dashboard esté disponible
 */
async function checkDashboard() {
    try {
        const response = await axios.get(`${DASHBOARD_URL}/api/status`, { timeout: 3000 });
        if (response.data.status === 'online') {
            console.log('✅ Dashboard conectado');
            console.log(`   Versión: ${response.data.version}`);
            console.log(`   Comandos disponibles: ${response.data.totalCommands}`);
            return true;
        }
    } catch (error) {
        console.error('❌ No se puede conectar al dashboard');
        console.error(`   Asegúrate de que esté corriendo en ${DASHBOARD_URL}`);
        return false;
    }
}

/**
 * Mostrar estadísticas
 */
function showStats() {
    const uptime = Math.floor((Date.now() - stats.startTime) / 1000);
    const minutes = Math.floor(uptime / 60);
    const seconds = uptime % 60;
    
    console.log('\n╔════════════════════════════════════════╗');
    console.log('║         ESTADÍSTICAS                   ║');
    console.log('╠════════════════════════════════════════╣');
    console.log(`║ 🎁 Regalos recibidos: ${stats.giftsReceived.toString().padEnd(16)}║`);
    console.log(`║ ⚡ Comandos ejecutados: ${stats.commandsExecuted.toString().padEnd(14)}║`);
    console.log(`║ 💬 Comandos de chat: ${stats.chatCommands.toString().padEnd(16)}║`);
    console.log(`║ ❌ Errores: ${stats.errors.toString().padEnd(26)}║`);
    console.log(`║ ⏱️  Tiempo activo: ${minutes}m ${seconds}s${' '.repeat(14 - minutes.toString().length - seconds.toString().length)}║`);
    console.log('╚════════════════════════════════════════╝\n');
}

// Mostrar estadísticas cada 5 minutos
setInterval(showStats, 5 * 60 * 1000);

/**
 * Inicializar conexión a TikTok Live
 */
async function main() {
    console.log('╔════════════════════════════════════════════════════════╗');
    console.log('║   🎮 TikTok Live → GTA V Bridge                       ║');
    console.log('╠════════════════════════════════════════════════════════╣');
    console.log(`║   📺 Usuario TikTok: ${TIKTOK_USERNAME.padEnd(32)}║`);
    console.log(`║   🌐 Dashboard: ${DASHBOARD_URL.padEnd(36)}║`);
    console.log('╚════════════════════════════════════════════════════════╝\n');
    
    // Verificar dashboard
    console.log('🔍 Verificando conexión al dashboard...');
    const dashboardOk = await checkDashboard();
    
    if (!dashboardOk) {
        console.log('\n⚠️  El dashboard no está disponible, pero continuaré intentando...\n');
    }
    
    // Crear conexión a TikTok
    const tiktokLiveConnection = new WebcastPushConnection(TIKTOK_USERNAME, {
        processInitialData: true,
        enableExtendedGiftInfo: true,
        enableWebsocketUpgrade: true,
        requestPollingIntervalMs: 1000
    });
    
    // Evento: Conectado
    tiktokLiveConnection.on('connected', state => {
        console.log('🔴 ¡Conectado a TikTok Live!');
        console.log(`   Room ID: ${state.roomId}`);
        console.log(`   Espectadores: ${state.viewerCount || 0}`);
        console.log('\n📡 Escuchando eventos...\n');
    });
    
    // Evento: Regalo recibido
    tiktokLiveConnection.on('gift', data => {
        stats.giftsReceived++;
        
        const giftName = data.giftName;
        const username = data.uniqueId || data.nickname || 'Anónimo';
        const repeatCount = data.repeatCount || 1;
        const giftConfig = GIFT_COMMANDS[giftName];
        
        if (giftConfig) {
            console.log(`🎁 ${username} envió ${repeatCount}x ${giftName}`);
            
            // Si es un combo
            if (giftConfig.combo) {
                executeCombo(giftConfig.combo, giftConfig.priority, username, giftName);
            } else {
                // Comando simple
                sendCommand(giftConfig.cmd, giftConfig.priority, username, giftName);
            }
        } else {
            console.log(`⚪ ${username} envió ${giftName} (no mapeado)`);
        }
    });
    
    // Evento: Mensaje de chat
    tiktokLiveConnection.on('chat', data => {
        const message = data.comment.toLowerCase().trim();
        const username = data.uniqueId || data.nickname || 'Anónimo';
        
        // Verificar si es un comando
        if (message.startsWith('!')) {
            const command = CHAT_COMMANDS[message];
            
            if (command) {
                stats.chatCommands++;
                console.log(`💬 ${username}: ${message} → ${command}`);
                sendCommand(command, 2, username, message);
            }
        }
    });
    
    // Evento: Nuevo seguidor
    tiktokLiveConnection.on('follow', data => {
        const username = data.uniqueId || data.nickname || 'Anónimo';
        console.log(`👤 ¡${username} te siguió! → Clima aleatorio`);
        sendCommand('cl_rnd', 2, username, 'Nuevo Seguidor');
    });
    
    // Evento: Compartir stream
    tiktokLiveConnection.on('share', data => {
        const username = data.uniqueId || data.nickname || 'Anónimo';
        console.log(`📤 ${username} compartió el stream → Vehículo aleatorio`);
        sendCommand('rnd_veh', 2, username, 'Compartir');
    });
    
    // Evento: Like
    tiktokLiveConnection.on('like', data => {
        const username = data.uniqueId || data.nickname || 'Anónimo';
        const likeCount = data.likeCount || 1;
        
        // Solo ejecutar comando cada 100 likes
        if (likeCount >= 100 && likeCount % 100 === 0) {
            console.log(`❤️ ${username} dio ${likeCount} likes → Curación`);
            sendCommand('curar', 1, username, `${likeCount} Likes`);
        }
    });
    
    // Evento: Desconectado
    tiktokLiveConnection.on('disconnected', () => {
        console.log('⚠️  Desconectado de TikTok Live');
        console.log('   Intentando reconectar en 10 segundos...');
        setTimeout(() => {
            console.log('🔄 Reconectando...');
            tiktokLiveConnection.connect().catch(err => {
                console.error('❌ Error al reconectar:', err.message);
            });
        }, 10000);
    });
    
    // Evento: Error
    tiktokLiveConnection.on('error', err => {
        stats.errors++;
        console.error('❌ Error:', err.message);
    });
    
    // Conectar
    try {
        await tiktokLiveConnection.connect();
    } catch (err) {
        console.error('❌ Error al conectar a TikTok Live:');
        console.error(`   ${err.message}`);
        console.error('\n💡 Posibles soluciones:');
        console.error('   1. Verifica que el usuario de TikTok sea correcto');
        console.error('   2. Asegúrate de estar en vivo en TikTok');
        console.error('   3. Verifica tu conexión a internet');
        process.exit(1);
    }
}

// Manejo de cierre graceful
process.on('SIGINT', () => {
    console.log('\n\n🛑 Cerrando...');
    showStats();
    process.exit(0);
});

// Iniciar
main().catch(err => {
    console.error('❌ Error fatal:', err);
    process.exit(1);
});
