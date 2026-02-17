# -*- coding: utf-8 -*-
"""
Gestor de Cola de Prioridad - PILLAR V7
Árbitro que gestiona comandos según valor de regalos TikTok

Este script lee comandos entrantes, les asigna prioridad según
el valor del regalo de TikTok y los organiza en una cola.
"""

from System.IO import File
from System import DateTime
import json

# ============================================================================
# CONFIGURACIÓN
# ============================================================================

ARCHIVO_COMANDO = "H:\\Games\\Grand Theft Auto V\\comando_gta.json"
ARCHIVO_COLA = "H:\\Games\\Grand Theft Auto V\\cola_espera.json"
INTERVALO_PROCESAMIENTO = 2000  # ms entre comandos

# ============================================================================
# TABLA DE PRIORIDADES (Basada en streamtoearn.io - Venezuela)
# ============================================================================

PRIORIDADES_REGALOS = {
    # Regalos Básicos (1-10 monedas)
    "rosa": 1,
    "corazon": 1,
    "dedo_arriba": 1,
    "aplausos": 1,
    
    # Regalos Bajos (11-50 monedas)
    "helado": 2,
    "donut": 2,
    "arcoiris": 2,
    "sol": 2,
    
    # Regalos Medios (51-100 monedas)
    "diamante": 3,
    "corona": 3,
    "trofeo": 3,
    
    # Regalos Altos (101-500 monedas)
    "castillo": 4,
    "cohete": 4,
    "ferrari": 4,
    
    # Regalos Premium (501-1000 monedas)
    "yate": 5,
    "avion": 5,
    "mansion": 5,
    
    # Regalos Épicos (1001-10000 monedas)
    "planeta": 6,
    "galaxia": 6,
    "universo": 6,
    
    # Regalos Legendarios (10000+ monedas)
    "leon": 10,
    "dragon": 10,
    "fenix": 10
}

# ============================================================================
# MAPEO DE REGALOS A COMANDOS
# ============================================================================

REGALO_A_COMANDO = {
    # Básicos - Curaciones y reparaciones
    "rosa": "curar",
    "corazon": "blindaje",
    "dedo_arriba": "fix_veh",
    
    # Bajos - Climas y efectos
    "helado": "cl_rnd",
    "donut": "t_dia",
    "arcoiris": "cl_clear",
    
    # Medios - Vehículos deportivos
    "diamante": "veh_t20",
    "corona": "veh_zentorno",
    "trofeo": "veh_adder",
    
    # Altos - Ataques
    "castillo": "atk_zombies_10",
    "cohete": "atk_police_15",
    "ferrari": "veh_rhino",
    
    # Premium - Ataques masivos
    "yate": "atk_marines",
    "avion": "veh_hydra",
    "mansion": "atk_aliens",
    
    # Épicos - Caos total
    "planeta": "atk_juggernaut",
    "galaxia": "w_5",
    "universo": "limpiar_todo",
    
    # Legendarios - Poder absoluto
    "leon": ["atk_juggernaut", "inv_on", "armas", "veh_khanjali"],
    "dragon": ["w_5", "atk_marines", "atk_police_15"],
    "fenix": ["limpiar_todo", "curar", "inv_on", "veh_hydra"]
}

# ============================================================================
# FUNCIONES
# ============================================================================

def obtener_prioridad(regalo_nombre):
    """Obtiene la prioridad de un regalo"""
    return PRIORIDADES_REGALOS.get(regalo_nombre.lower(), 1)

def obtener_comando(regalo_nombre):
    """Obtiene el comando asociado a un regalo"""
    return REGALO_A_COMANDO.get(regalo_nombre.lower(), None)

def leer_cola():
    """Lee la cola de espera"""
    if not File.Exists(ARCHIVO_COLA):
        return []
    try:
        contenido = File.ReadAllText(ARCHIVO_COLA)
        return json.loads(contenido)
    except:
        return []

def escribir_cola(cola):
    """Escribe la cola de espera"""
    try:
        contenido = json.dumps(cola, indent=2)
        File.WriteAllText(ARCHIVO_COLA, contenido)
        return True
    except:
        return False

def agregar_a_cola(comando, prioridad, usuario="Sistema", regalo="Comando"):
    """Agrega un comando a la cola con prioridad"""
    cola = leer_cola()
    
    nuevo_item = {
        "accion": comando,
        "prioridad": prioridad,
        "usuario": usuario,
        "regalo": regalo,
        "timestamp": DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss")
    }
    
    cola.append(nuevo_item)
    
    # Ordenar por prioridad (mayor primero)
    cola.sort(key=lambda x: x.get("prioridad", 1), reverse=True)
    
    return escribir_cola(cola)

def procesar_siguiente_comando():
    """
    Procesa el siguiente comando de la cola
    Retorna True si procesó algo, False si la cola está vacía
    """
    cola = leer_cola()
    
    if not cola:
        return False
    
    # Tomar el primer comando (mayor prioridad)
    comando = cola.pop(0)
    
    # Escribir comando para ejecución
    try:
        comando_json = json.dumps({"accion": comando["accion"]})
        File.WriteAllText(ARCHIVO_COMANDO, comando_json)
    except:
        pass
    
    # Actualizar cola
    escribir_cola(cola)
    
    return True

def on_tick():
    """
    Función principal - procesa comandos de la cola
    """
    # Verificar si hay un comando en ejecución
    if File.Exists(ARCHIVO_COMANDO):
        return  # Esperar a que se procese
    
    # Procesar siguiente comando de la cola
    procesar_siguiente_comando()

# ============================================================================
# FUNCIONES PARA STREAMER.BOT
# ============================================================================

def procesar_regalo_tiktok(regalo_nombre, usuario="Viewer"):
    """
    Función llamada por Streamer.bot cuando se recibe un regalo
    
    Parámetros:
    - regalo_nombre: Nombre del regalo (ej: "leon", "rosa")
    - usuario: Nombre del usuario que envió el regalo
    """
    # Obtener prioridad
    prioridad = obtener_prioridad(regalo_nombre)
    
    # Obtener comando(s)
    comandos = obtener_comando(regalo_nombre)
    
    if not comandos:
        # Si no hay mapeo, usar comando genérico
        comandos = "curar"
    
    # Si es una lista de comandos (regalos legendarios)
    if isinstance(comandos, list):
        for cmd in comandos:
            agregar_a_cola(cmd, prioridad, usuario, regalo_nombre)
    else:
        agregar_a_cola(comandos, prioridad, usuario, regalo_nombre)

# ============================================================================
# EJEMPLO DE USO
# ============================================================================

"""
# Desde Streamer.bot (C# Code):

using System.Net.Http;
using System.Text;

public bool CPHInline()
{
    var regalo = args["giftName"].ToString();
    var usuario = args["userName"].ToString();
    
    // Llamar a la API del dashboard
    var client = new HttpClient();
    var content = new StringContent(
        $"{{\"accion\":\"{regalo}\",\"usuario\":\"{usuario}\",\"prioridad\":5}}",
        Encoding.UTF8,
        "application/json"
    );
    
    var response = client.PostAsync("http://localhost:3000/api/comando", content).Result;
    
    return true;
}
"""
