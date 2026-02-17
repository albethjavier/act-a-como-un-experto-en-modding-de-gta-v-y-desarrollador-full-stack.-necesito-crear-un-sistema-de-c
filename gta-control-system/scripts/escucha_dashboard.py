# -*- coding: utf-8 -*-
"""
GTA V Remote Control Listener - PILLAR V7
Script principal de escucha para ScriptHookVDotNet

Mejoras V7:
- Vehicle Swap perfecto con SET_PED_INTO_VEHICLE
- Teleport seguro con REQUEST_COLLISION_AT_COORD
- Limpieza automática de entidades
- Fade effects cinematográficos
- Manejo robusto de errores
"""

from System.IO import File
from System import DateTime
from GTA import Game, World, Model, VehicleHash, WeaponHash, Script, VehicleSeat, Weather
from GTA.Native import Function, Hash
from GTA.Math import Vector3

# ============================================================================
# CONFIGURACIÓN
# ============================================================================

ARCHIVO_RUTA = "H:\\Games\\Grand Theft Auto V\\comando_gta.json"
ULTIMA_LIMPIEZA = DateTime.Now
INTERVALO_LIMPIEZA = 60  # Segundos entre limpiezas automáticas

# ============================================================================
# FUNCIONES AUXILIARES
# ============================================================================

def extraer_accion(raw_text):
    """
    Extrae la acción del JSON sin usar librerías JSON
    Método robusto que evita errores de codificación
    """
    try:
        if '"accion":"' in raw_text:
            return raw_text.split('"accion":"')[1].split('"')[0]
        return None
    except:
        return None

def fade_out(duracion_ms=100):
    """Efecto de fundido a negro"""
    Function.Call(Hash.DO_SCREEN_FADE_OUT, duracion_ms)
    Script.Wait(duracion_ms + 50)

def fade_in(duracion_ms=100):
    """Efecto de fundido desde negro"""
    Function.Call(Hash.DO_SCREEN_FADE_IN, duracion_ms)

def limpiar_entidades_viejas():
    """
    Limpia vehículos abandonados y NPCs muertos
    Previene crashes por acumulación de entidades
    """
    p = Game.Player.Character
    vehiculo_actual = p.CurrentVehicle if p.IsInVehicle() else None
    
    # Limpiar vehículos
    for v in World.GetAllVehicles():
        try:
            if v != vehiculo_actual and v.IsDead:
                v.Delete()
        except:
            pass
    
    # Limpiar NPCs muertos
    for npc in World.GetAllPeds():
        try:
            if npc != p and npc.IsDead:
                npc.Delete()
        except:
            pass

def teleport_seguro(x, y, z):
    """
    Teletransporte con carga de colisiones
    Previene caídas al vacío
    """
    p = Game.Player.Character
    
    # Congelar jugador
    p.IsPositionFrozen = True
    
    # Solicitar carga de colisiones en destino
    Function.Call(Hash.REQUEST_COLLISION_AT_COORD, x, y, z)
    
    # Establecer foco en la nueva ubicación
    Function.Call(Hash.SET_FOCUS_ENTITY, p.Handle)
    
    # Mover a posición elevada (+0.5 en Z para seguridad)
    p.Position = Vector3(x, y, z + 0.5)
    
    # Esperar carga de colisiones
    Script.Wait(1500)
    
    # Descongelar
    p.IsPositionFrozen = False

def swap_vehiculo(modelo_nombre):
    """
    Intercambio de vehículo optimizado
    Usa nativos directos para evitar bugs de posición
    """
    p = Game.Player.Character
    
    # Cargar modelo
    m = Model(modelo_nombre)
    m.Request(1000)
    
    if not m.IsLoaded:
        return False
    
    # Fade out para transición suave
    fade_out(100)
    
    # Guardar velocidad si está en vehículo
    velocidad_anterior = Vector3(0, 0, 0)
    if p.IsInVehicle():
        try:
            velocidad_anterior = p.CurrentVehicle.Velocity
            # Elevar jugador ligeramente antes de borrar vehículo
            p.Position = p.Position + Vector3(0, 0, 0.2)
            Script.Wait(10)
            p.CurrentVehicle.Delete()
        except:
            pass
    
    # Crear nuevo vehículo
    posicion_spawn = p.Position + p.ForwardVector * 2
    v = World.CreateVehicle(m, posicion_spawn)
    
    if v:
        # Restaurar velocidad
        v.Velocity = velocidad_anterior
        
        # CRÍTICO: Usar nativo directo para montar instantáneamente
        Function.Call(Hash.SET_PED_INTO_VEHICLE, p.Handle, v.Handle, -1)
        
        # Pequeña espera para sincronización
        Script.Wait(50)
    
    # Fade in
    fade_in(100)
    
    return True

def spawn_ataque(modelo_ped, cantidad, arma):
    """
    Spawnea NPCs agresivos con armas
    """
    p = Game.Player.Character
    m = Model(modelo_ped)
    m.Request(1000)
    
    if not m.IsLoaded:
        return
    
    for i in range(cantidad):
        # Posición alrededor del jugador
        offset = p.ForwardVector * (4 + i * 2)
        npc = World.CreatePed(m, p.Position + offset)
        
        if npc:
            # Dar arma y munición
            npc.Weapons.Give(arma, 999, True, True)
            
            # Asignar tarea de combate inmediata
            npc.Task.FightAgainst(p)
            
            # Hacer agresivo
            Function.Call(Hash.SET_PED_COMBAT_ABILITY, npc.Handle, 100)
            Function.Call(Hash.SET_PED_COMBAT_MOVEMENT, npc.Handle, 2)

# ============================================================================
# DICCIONARIOS DE COMANDOS
# ============================================================================

# Climas
CLIMAS = {
    "cl_extrasunny": "EXTRASUNNY",
    "cl_clear": "CLEAR",
    "cl_clouds": "CLOUDS",
    "cl_smog": "SMOG",
    "cl_foggy": "FOGGY",
    "cl_rain": "RAIN",
    "cl_thunder": "THUNDER",
    "cl_snow": "SNOW",
    "cl_blizzard": "BLIZZARD",
    "cl_xmas": "XMAS",
    "cl_halloween": "HALLOWEEN",
    "cl_neutral": "NEUTRAL"
}

# Teleports (coordenadas corregidas V7)
TELEPORTS = {
    "tp_michael": (-806.3, 171.2, 72.0),      # Entrada jardín frontal
    "tp_franklin": (7.9, 548.1, 175.5),
    "tp_mazebank": (-75.0, -818.0, 326.0),
    "tp_airport": (-1034.0, -2730.0, 13.0),
    "tp_militar": (-2047.0, 3132.0, 32.0),
    "tp_carcel": (1690.0, 2605.0, 45.0),
    "tp_casino": (924.0, 47.0, 81.0),
    "tp_yatch": (-2023.0, -1038.0, 5.0),
    "tp_chiliad": (501.9, 5593.1, 796.2),
    "tp_humanelabs": (3611.0, 3712.0, 28.0),
    "tp_paleto": (-415.0, 6050.0, 31.0),
    "tp_observatory": (-440.0, 1146.0, 192.0),
    "tp_korthacenter": (-2274.0, 239.0, 174.0),
    "tp_lighthouse": (3328.0, 5174.0, 18.0)   # Entrada del sendero
}

# Ataques (modelo, cantidad, arma)
ATAQUES = {
    "atk_zombies_10": ("u_m_y_zombie_01", 10, WeaponHash.Unarmed),
    "atk_clowns_5": ("s_m_y_clown_01", 5, WeaponHash.Dagger),
    "atk_police_15": ("s_m_y_cop_01", 15, WeaponHash.CombatPistol),
    "atk_bomberos": ("s_m_y_fireman_01", 6, WeaponHash.Hatchet),
    "atk_ballas": ("g_m_y_ballasout_01", 6, WeaponHash.Pistol),
    "atk_vagos": ("g_m_y_vagos_01", 6, WeaponHash.MicroSMG),
    "atk_marines": ("s_m_y_marine_01", 4, WeaponHash.CarbineRifle),
    "atk_aliens": ("s_m_m_movalien_01", 8, WeaponHash.Pistol),
    "atk_rancheros": ("a_m_m_hillbilly_01", 6, WeaponHash.DoubleActionRevolver),
    "atk_juggernaut": ("u_m_m_juggernaut_01", 1, WeaponHash.Minigun),
    "atk_mime": ("s_m_y_mime", 5, WeaponHash.Knife)
}

# ============================================================================
# FUNCIÓN PRINCIPAL - ON_TICK
# ============================================================================

def on_tick():
    """
    Función principal ejecutada cada frame
    """
    global ULTIMA_LIMPIEZA
    
    # Limpieza automática cada 60 segundos
    if (DateTime.Now - ULTIMA_LIMPIEZA).TotalSeconds > INTERVALO_LIMPIEZA:
        limpiar_entidades_viejas()
        ULTIMA_LIMPIEZA = DateTime.Now
    
    # Verificar si existe archivo de comando
    if not File.Exists(ARCHIVO_RUTA):
        return
    
    try:
        # Leer archivo
        raw_text = File.ReadAllText(ARCHIVO_RUTA)
        accion = extraer_accion(raw_text)
        
        if not accion:
            File.Delete(ARCHIVO_RUTA)
            return
        
        p = Game.Player.Character
        
        # ====================================================================
        # PROCESAMIENTO DE COMANDOS
        # ====================================================================
        
        # --- CLIMA ---
        if accion in CLIMAS:
            Function.Call(Hash.CLEAR_OVERRIDE_WEATHER)
            Function.Call(Hash.CLEAR_WEATHER_TYPE_PERSIST)
            Function.Call(Hash.SET_WEATHER_TYPE_NOW_PERSIST, CLIMAS[accion])
            # Activar huellas en nieve
            if accion in ["cl_snow", "cl_blizzard", "cl_xmas"]:
                Function.Call(Hash.SET_FORCE_PED_FOOTSTEPS_TRACKS, True)
        
        # --- TIEMPO DEL DÍA ---
        elif accion == "t_amanecer":
            Function.Call(Hash.SET_CLOCK_TIME, 6, 0, 0)
        elif accion == "t_dia":
            Function.Call(Hash.SET_CLOCK_TIME, 12, 0, 0)
        elif accion == "t_noche":
            Function.Call(Hash.SET_CLOCK_TIME, 0, 0, 0)
        
        # --- TELEPORT ---
        elif accion in TELEPORTS:
            coords = TELEPORTS[accion]
            teleport_seguro(coords[0], coords[1], coords[2])
        
        # --- ATAQUES ---
        elif accion in ATAQUES:
            config = ATAQUES[accion]
            spawn_ataque(config[0], config[1], config[2])
        
        # --- VEHÍCULOS ---
        elif accion.startswith("veh_"):
            modelo = accion.replace("veh_", "")
            swap_vehiculo(modelo)
        
        # --- JUGADOR ---
        elif accion == "curar":
            p.Health = p.MaxHealth
        
        elif accion == "blindaje":
            p.Armor = 100
        
        elif accion == "inv_on":
            p.IsInvincible = True
        
        elif accion == "inv_off":
            p.IsInvincible = False
        
        elif accion == "invisible":
            p.IsVisible = not p.IsVisible
        
        elif accion == "fuego":
            p.IsFireProof = True
        
        elif accion == "salto":
            Function.Call(Hash.SET_SUPER_JUMP_THIS_FRAME, Game.Player.Handle)
        
        elif accion == "correr":
            Function.Call(Hash.SET_RUN_SPRINT_MULTIPLIER_FOR_PLAYER, Game.Player.Handle, 1.49)
        
        elif accion == "armas":
            for w in WeaponHash.GetValues(WeaponHash):
                try:
                    p.Weapons.Give(w, 999, False, True)
                except:
                    pass
        
        elif accion == "quitar_armas":
            Function.Call(Hash.REMOVE_ALL_PED_WEAPONS, p.Handle, True)
        
        elif accion == "borracho":
            Function.Call(Hash.SET_PED_IS_DRUNK, p.Handle, True)
        
        elif accion == "super_fuerza":
            Function.Call(Hash.SET_PED_MELEE_WEAPON_DAMAGE_MODIFIER, p.Handle, 10.0)
        
        elif accion == "stamina":
            Function.Call(Hash.SET_PLAYER_STAMINA, Game.Player.Handle, 100.0)
        
        elif accion == "oxigeno":
            Function.Call(Hash.SET_PED_MAX_TIME_UNDERWATER, p.Handle, 999999.0)
        
        # --- VEHÍCULO ACTUAL ---
        elif accion == "fix_veh":
            if p.IsInVehicle():
                p.CurrentVehicle.Repair()
        
        # --- POLICÍA ---
        elif accion.startswith("w_"):
            nivel = int(accion.replace("w_", ""))
            Game.Player.WantedLevel = nivel
        
        # --- SISTEMA ---
        elif accion == "suicidio":
            Function.Call(Hash.APPLY_DAMAGE_TO_PED, p.Handle, 5000, True)
        
        elif accion == "limpiar_todo":
            vehiculo_actual = p.CurrentVehicle if p.IsInVehicle() else None
            
            # Eliminar todos los vehículos excepto el actual
            for v in World.GetAllVehicles():
                try:
                    if v != vehiculo_actual:
                        v.Delete()
                except:
                    pass
            
            # Eliminar todos los NPCs excepto el jugador
            for npc in World.GetAllPeds():
                try:
                    if npc != p:
                        npc.Delete()
                except:
                    pass
        
        elif accion == "limpiar_clima":
            Function.Call(Hash.CLEAR_OVERRIDE_WEATHER)
            Function.Call(Hash.SET_WEATHER_TYPE_NOW_PERSIST, "EXTRASUNNY")
        
        # Borrar archivo de comando
        File.Delete(ARCHIVO_RUTA)
        
    except Exception as e:
        # En caso de error, intentar borrar el archivo para evitar bucles
        try:
            if File.Exists(ARCHIVO_RUTA):
                File.Delete(ARCHIVO_RUTA)
        except:
            pass

# ============================================================================
# NOTAS TÉCNICAS
# ============================================================================
"""
NATIVOS CRÍTICOS UTILIZADOS:

1. SET_PED_INTO_VEHICLE (Hash)
   - Monta al jugador instantáneamente en el vehículo
   - Evita bugs de posición donde el jugador queda sobre el techo

2. REQUEST_COLLISION_AT_COORD
   - Fuerza la carga de colisiones en coordenadas específicas
   - Previene caídas al vacío en teleports

3. SET_FOCUS_ENTITY
   - Prioriza la carga de recursos alrededor de una entidad
   - Mejora la estabilidad en teleports largos

4. DO_SCREEN_FADE_OUT/IN
   - Efectos cinematográficos de transición
   - Oculta micro-errores de animación

5. SET_WEATHER_TYPE_NOW_PERSIST
   - Cambia el clima inmediatamente y lo mantiene
   - Debe usarse después de CLEAR_OVERRIDE_WEATHER

OPTIMIZACIONES V7:

- Limpieza automática cada 60s para prevenir crashes
- Extracción de JSON sin librerías para evitar errores de encoding
- Elevación del Ped antes de borrar vehículo (+0.2 en Z)
- Micro-delays (Script.Wait) para sincronización con RAGE Engine
- Fade effects para transiciones suaves
- Manejo robusto de excepciones en todas las operaciones críticas

REFERENCIAS:
- GTA V Native DB: https://gtahash.ru/
- SHVDN Wiki: http://www.dev-c.com/gtav/scripthookv/
"""
