# -*- coding: utf-8 -*-
"""
GTA V Remote Control Listener - PILLAR V8
Script principal de escucha para ScriptHookVDotNet

Mejoras V8:
- Polling automático cada 100ms (sin necesidad de F9)
- Comandos de modo dios y armas corregidos
- Mejor manejo de estados persistentes
- Sistema de cooldown para evitar spam
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
ULTIMO_COMANDO = ""
ULTIMO_TIEMPO = DateTime.Now

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

def dar_todas_armas():
    """
    Da todas las armas disponibles con munición infinita
    Método mejorado con manejo de errores
    """
    p = Game.Player.Character
    
    # Lista completa de armas
    armas = [
        # Cuerpo a cuerpo
        WeaponHash.Knife, WeaponHash.Nightstick, WeaponHash.Hammer, WeaponHash.Bat,
        WeaponHash.Crowbar, WeaponHash.GolfClub, WeaponHash.Bottle, WeaponHash.Dagger,
        WeaponHash.Hatchet, WeaponHash.KnuckleDuster, WeaponHash.Machete, WeaponHash.Flashlight,
        WeaponHash.SwitchBlade, WeaponHash.PoolCue, WeaponHash.Wrench, WeaponHash.BattleAxe,
        
        # Pistolas
        WeaponHash.Pistol, WeaponHash.CombatPistol, WeaponHash.APPistol, WeaponHash.Pistol50,
        WeaponHash.SNSPistol, WeaponHash.HeavyPistol, WeaponHash.VintagePistol, WeaponHash.MarksmanPistol,
        WeaponHash.Revolver, WeaponHash.DoubleActionRevolver, WeaponHash.CeramicPistol, WeaponHash.NavyRevolver,
        
        # SMGs
        WeaponHash.MicroSMG, WeaponHash.SMG, WeaponHash.AssaultSMG, WeaponHash.CombatPDW,
        WeaponHash.MachinePistol, WeaponHash.MiniSMG, WeaponHash.UnholyHellbringer,
        
        # Escopetas
        WeaponHash.PumpShotgun, WeaponHash.SawnOffShotgun, WeaponHash.AssaultShotgun,
        WeaponHash.BullpupShotgun, WeaponHash.Musket, WeaponHash.HeavyShotgun,
        WeaponHash.DoubleBarrelShotgun, WeaponHash.SweeperShotgun, WeaponHash.CombatShotgun,
        
        # Rifles de asalto
        WeaponHash.AssaultRifle, WeaponHash.CarbineRifle, WeaponHash.AdvancedRifle,
        WeaponHash.SpecialCarbine, WeaponHash.BullpupRifle, WeaponHash.CompactRifle,
        WeaponHash.MilitaryRifle, WeaponHash.HeavyRifle, WeaponHash.TacticalRifle,
        
        # LMGs
        WeaponHash.MG, WeaponHash.CombatMG, WeaponHash.Gusenberg,
        
        # Francotiradores
        WeaponHash.SniperRifle, WeaponHash.HeavySniper, WeaponHash.MarksmanRifle,
        
        # Pesadas
        WeaponHash.RPG, WeaponHash.GrenadeLauncher, WeaponHash.Minigun, WeaponHash.Firework,
        WeaponHash.Railgun, WeaponHash.HomingLauncher, WeaponHash.CompactGrenadeLauncher,
        WeaponHash.Widowmaker, WeaponHash.RayMinigun,
        
        # Lanzables
        WeaponHash.Grenade, WeaponHash.StickyBomb, WeaponHash.ProximityMine,
        WeaponHash.BZGas, WeaponHash.Molotov, WeaponHash.FireExtinguisher,
        WeaponHash.PetrolCan, WeaponHash.Flare, WeaponHash.Ball, WeaponHash.Snowball,
        WeaponHash.SmokeGrenade, WeaponHash.PipeBomb,
        
        # Especiales
        WeaponHash.StunGun, WeaponHash.FlareGun, WeaponHash.UpNAtomizer,
        WeaponHash.EMPLauncher, WeaponHash.HazardCan
    ]
    
    contador = 0
    for arma in armas:
        try:
            p.Weapons.Give(arma, 9999, False, True)
            contador += 1
        except:
            pass
    
    # Notificación visual
    Game.DisplaySubtitle("~g~" + str(contador) + " armas equipadas!", 3000)

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
    "tp_michael": (-806.3, 171.2, 72.0),
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
    "tp_lighthouse": (3328.0, 5174.0, 18.0)
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
    POLLING AUTOMÁTICO - No requiere presionar F9
    """
    global ULTIMA_LIMPIEZA, ULTIMO_COMANDO, ULTIMO_TIEMPO
    
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
        
        # Prevenir ejecución duplicada del mismo comando
        if accion == ULTIMO_COMANDO and (DateTime.Now - ULTIMO_TIEMPO).TotalMilliseconds < 500:
            return
        
        ULTIMO_COMANDO = accion
        ULTIMO_TIEMPO = DateTime.Now
        
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
            Game.DisplaySubtitle("~b~Clima cambiado", 2000)
        
        # --- TIEMPO DEL DÍA ---
        elif accion == "t_amanecer":
            Function.Call(Hash.SET_CLOCK_TIME, 6, 0, 0)
            Game.DisplaySubtitle("~y~Amanecer", 2000)
        elif accion == "t_dia":
            Function.Call(Hash.SET_CLOCK_TIME, 12, 0, 0)
            Game.DisplaySubtitle("~y~Mediodía", 2000)
        elif accion == "t_noche":
            Function.Call(Hash.SET_CLOCK_TIME, 0, 0, 0)
            Game.DisplaySubtitle("~y~Medianoche", 2000)
        
        # --- TELEPORT ---
        elif accion in TELEPORTS:
            coords = TELEPORTS[accion]
            teleport_seguro(coords[0], coords[1], coords[2])
            Game.DisplaySubtitle("~p~Teletransportado", 2000)
        
        # --- ATAQUES ---
        elif accion in ATAQUES:
            config = ATAQUES[accion]
            spawn_ataque(config[0], config[1], config[2])
            Game.DisplaySubtitle("~r~Enemigos spawneados!", 3000)
        
        # --- VEHÍCULOS ---
        elif accion.startswith("veh_"):
            modelo = accion.replace("veh_", "")
            if swap_vehiculo(modelo):
                Game.DisplaySubtitle("~b~Vehículo spawneado", 2000)
        
        # --- JUGADOR ---
        elif accion == "curar":
            p.Health = p.MaxHealth
            Game.DisplaySubtitle("~g~Curado", 2000)
        
        elif accion == "blindaje":
            p.Armor = 100
            Game.DisplaySubtitle("~b~Blindaje completo", 2000)
        
        elif accion == "inv_on":
            # Método mejorado para invencibilidad
            Function.Call(Hash.SET_PLAYER_INVINCIBLE, Game.Player.Handle, True)
            p.IsInvincible = True
            Game.DisplaySubtitle("~g~MODO DIOS: ON", 3000)
        
        elif accion == "inv_off":
            Function.Call(Hash.SET_PLAYER_INVINCIBLE, Game.Player.Handle, False)
            p.IsInvincible = False
            Game.DisplaySubtitle("~r~MODO DIOS: OFF", 3000)
        
        elif accion == "invisible":
            p.IsVisible = not p.IsVisible
            estado = "ON" if not p.IsVisible else "OFF"
            Game.DisplaySubtitle("~p~Invisibilidad: " + estado, 2000)
        
        elif accion == "fuego":
            p.IsFireProof = True
            Game.DisplaySubtitle("~o~Inmune al fuego", 2000)
        
        elif accion == "salto":
            Function.Call(Hash.SET_SUPER_JUMP_THIS_FRAME, Game.Player.Handle)
            Game.DisplaySubtitle("~y~Super salto activado", 2000)
        
        elif accion == "correr":
            Function.Call(Hash.SET_RUN_SPRINT_MULTIPLIER_FOR_PLAYER, Game.Player.Handle, 1.49)
            Game.DisplaySubtitle("~y~Velocidad aumentada", 2000)
        
        elif accion == "armas":
            dar_todas_armas()
        
        elif accion == "quitar_armas":
            Function.Call(Hash.REMOVE_ALL_PED_WEAPONS, p.Handle, True)
            Game.DisplaySubtitle("~r~Armas removidas", 2000)
        
        elif accion == "borracho":
            Function.Call(Hash.SET_PED_IS_DRUNK, p.Handle, True)
            Game.DisplaySubtitle("~p~Modo borracho", 2000)
        
        elif accion == "super_fuerza":
            Function.Call(Hash.SET_PED_MELEE_WEAPON_DAMAGE_MODIFIER, p.Handle, 10.0)
            Game.DisplaySubtitle("~r~Super fuerza activada", 2000)
        
        elif accion == "stamina":
            Function.Call(Hash.SET_PLAYER_STAMINA, Game.Player.Handle, 100.0)
            Game.DisplaySubtitle("~g~Stamina restaurada", 2000)
        
        elif accion == "oxigeno":
            Function.Call(Hash.SET_PED_MAX_TIME_UNDERWATER, p.Handle, 999999.0)
            Game.DisplaySubtitle("~b~Oxígeno infinito", 2000)
        
        # --- VEHÍCULO ACTUAL ---
        elif accion == "fix_veh":
            if p.IsInVehicle():
                p.CurrentVehicle.Repair()
                Game.DisplaySubtitle("~g~Vehículo reparado", 2000)
        
        # --- POLICÍA ---
        elif accion.startswith("w_"):
            nivel = int(accion.replace("w_", ""))
            Game.Player.WantedLevel = nivel
            Game.DisplaySubtitle("~r~Nivel de búsqueda: " + str(nivel), 2000)
        
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
            
            Game.DisplaySubtitle("~g~Mundo limpiado", 2000)
        
        elif accion == "limpiar_clima":
            Function.Call(Hash.CLEAR_OVERRIDE_WEATHER)
            Function.Call(Hash.SET_WEATHER_TYPE_NOW_PERSIST, "EXTRASUNNY")
            Game.DisplaySubtitle("~b~Clima reseteado", 2000)
        
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
# NOTAS TÉCNICAS V8
# ============================================================================
"""
CAMBIOS PRINCIPALES V8:

1. POLLING AUTOMÁTICO:
   - El script verifica el archivo cada frame (~100ms)
   - NO requiere presionar F9 manualmente
   - Sistema de cooldown para evitar ejecuciones duplicadas

2. MODO DIOS MEJORADO:
   - Usa SET_PLAYER_INVINCIBLE nativo además de IsInvincible
   - Más robusto y persistente

3. ARMAS MEJORADAS:
   - Función dar_todas_armas() con lista completa
   - Manejo de errores por arma
   - Contador de armas equipadas

4. NOTIFICACIONES VISUALES:
   - Cada comando muestra un mensaje en pantalla
   - Colores según tipo de acción
   - Duración apropiada (2-3 segundos)

5. PREVENCIÓN DE DUPLICADOS:
   - Sistema de tracking del último comando
   - Cooldown de 500ms entre comandos idénticos

NATIVOS CRÍTICOS UTILIZADOS:

- SET_PLAYER_INVINCIBLE: Invencibilidad a nivel de jugador
- SET_PED_INTO_VEHICLE: Montaje instantáneo en vehículo
- REQUEST_COLLISION_AT_COORD: Carga de colisiones para teleport
- DO_SCREEN_FADE_OUT/IN: Transiciones cinematográficas
- Game.DisplaySubtitle: Notificaciones en pantalla

REFERENCIAS:
- GTA V Native DB: https://gtahash.ru/
- SHVDN Wiki: http://www.dev-c.com/gtav/scripthookv/
"""
