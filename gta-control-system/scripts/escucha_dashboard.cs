/*
 * GTA V Remote Control Listener - C# Version
 * Script for ScriptHookVDotNet that reads commands from JSON file
 * 
 * Compile with: csc /target:library /out:escucha_dashboard.dll /reference:"GTAVScriptHookVDotNet.dll" escucha_dashboard.cs
 * Or use any C# IDE with ScriptHookVDotNet references
 */

using System;
using System.IO;
using System.Threading;
using GTA;
using GTA.Native;
using GTA.Math;

public class EscuchaDashboard : Script
{
    private static string CommandFilePath = "H:\\Games\\Grand Theft Auto V\\comando_gta.json";
    private static string LastCommand = "";
    private static DateTime LastExecuteTime = DateTime.Now;
    private static int CooldownMs = 500;
    
    public EscuchaDashboard()
    {
        Tick += OnTick;
    }
    
    private void OnTick(object sender, EventArgs e)
    {
        try
        {
            // Polling automático cada tick (~100ms)
            if (File.Exists(CommandFilePath))
            {
                string jsonContent = File.ReadAllText(CommandFilePath);
                
                if (!string.IsNullOrEmpty(jsonContent) && jsonContent.Length > 5)
                {
                    string accion = ExtractAction(jsonContent);
                    
                    // Evitar duplicados con cooldown
                    if (!string.IsNullOrEmpty(accion) && 
                        (accion != LastCommand || (DateTime.Now - LastExecuteTime).TotalMilliseconds > CooldownMs))
                    {
                        ExecuteCommand(accion);
                        LastCommand = accion;
                        LastExecuteTime = DateTime.Now;
                        
                        // Limpiar archivo después de ejecutar
                        try { File.Delete(CommandFilePath); } catch { }
                    }
                }
            }
        }
        catch (Exception ex)
        {
            // Silencioso para evitar spam en consola
        }
    }
    
    private string ExtractAction(string json)
    {
        try
        {
            // Buscar "accion":"valor"
            int start = json.IndexOf("\"accion\":\"");
            if (start == -1) return null;
            
            start += 10; // Longitud de "accion":"
            int end = json.IndexOf("\"", start);
            if (end == -1) return null;
            
            return json.Substring(start, end - start);
        }
        catch
        {
            return null;
        }
    }
    
    private void ExecuteCommand(string accion)
    {
        Player p = Game.Player;
        Ped playerPed = p.Character;
        
        switch (accion.ToLower())
        {
            // ========== SISTEMA Y LIMPIEZA ==========
            case "limpiar_todo":
                World.Cleanup();
                Game.DisplaySubtitle("~g~🧹 Mapa limpiado!", 3000);
                break;
                
            case "suicidio":
                playerPed.Kill();
                Game.DisplaySubtitle("~r~💀 Reiniciando...", 2000);
                break;
                
            case "fix_veh":
                if (playerPed.CurrentVehicle != null)
                {
                    playerPed.CurrentVehicle.Repair();
                    Game.DisplaySubtitle("~g~🔧 Vehículo reparado!", 3000);
                }
                break;
                
            case "limpiar_clima":
                Function.Call(Hash.SET_WEATHER_TYPE_NOW, "EXTRASUNNY");
                Game.DisplaySubtitle("~g~☀️ Clima soleado!", 3000);
                break;
                
            // ========== ATAQUES ==========
            case "atk_zombies_10":
                SpawnAttack("zombie", 10);
                Game.DisplaySubtitle("~r~🧟 10 Zombies!", 3000);
                break;
                
            case "atk_clowns_5":
                SpawnAttack("clown", 5);
                Game.DisplaySubtitle("~r~🤡 5 Payasos!", 3000);
                break;
                
            case "atk_police_15":
                SpawnAttack("police", 15);
                Game.DisplaySubtitle("~r~🚓 15 Policías!", 3000);
                break;
                
            case "atk_bomberos":
                SpawnAttack("fireman", 5);
                Game.DisplaySubtitle("~r~🚒 Bombberos!", 3000);
                break;
                
            case "atk_ballas":
                SpawnAttack("ballas", 8);
                Game.DisplaySubtitle("~r~💜 Ballas!", 3000);
                break;
                
            case "atk_vagos":
                SpawnAttack("vagos", 8);
                Game.DisplaySubtitle("~r~💛 Vagos!", 3000);
                break;
                
            case "atk_marines":
                SpawnAttack("marine", 6);
                Game.DisplaySubtitle("~r~🎖️ Marines!", 3000);
                break;
                
            case "atk_aliens":
                SpawnAttack("alien", 5);
                Game.DisplaySubtitle("~r~👽 Alienígenas!", 3000);
                break;
                
            case "atk_rancheros":
                SpawnAttack("ranchcop", 6);
                Game.DisplaySubtitle("~r~🤠 Rancheros!", 3000);
                break;
                
            case "atk_juggernaut":
                SpawnAttack("juggernaut", 1);
                Game.DisplaySubtitle("~r~🛡️ JUGGERNAUT!", 3000);
                break;
                
            case "atk_mime":
                SpawnAttack("mime", 5);
                Game.DisplaySubtitle("~r~🎭 Mimos!", 3000);
                break;
                
            // ========== JUGADOR - SUPER PODERES ==========
            case "curar":
                playerPed.Health = playerPed.MaxHealth;
                Game.DisplaySubtitle("~g~❤️ Salud restaurada!", 3000);
                break;
                
            case "blindaje":
                p.Armor = 100;
                Game.DisplaySubtitle("~g~🛡️ blindaje completo!", 3000);
                break;
                
            case "inv_on":
                // Método dual para máxima compatibilidad
                Function.Call(Hash.SET_PLAYER_INVINCIBLE, p.Handle, true);
                playerPed.IsInvincible = true;
                Game.DisplaySubtitle("~g~😇 MODO DIOS: ON", 3000);
                break;
                
            case "inv_off":
                Function.Call(Hash.SET_PLAYER_INVINCIBLE, p.Handle, false);
                playerPed.IsInvincible = false;
                Game.DisplaySubtitle("~r~😈 MODO DIOS: OFF", 3000);
                break;
                
            case "invisible":
                playerPed.IsVisible = !playerPed.IsVisible;
                Game.DisplaySubtitle(playerPed.IsVisible ? "~g~👤 Visible" : "~g~👻 Invisible", 3000);
                break;
                
            case "fuego":
                Function.Call(Hash.SET_ENTITY_PROOFS, playerPed.Handle, false, false, false, false, false, false, true, false, false, false, false);
                Game.DisplaySubtitle("~g~🔥 Inmune al fuego!", 3000);
                break;
                
            case "salto":
                Function.Call(Hash.SET_SUPER_JUMP_THIS_FRAME, Game.Player.Handle);
                Game.DisplaySubtitle("~g~🦘 SUPER SALTO!", 3000);
                break;
                
            case "correr":
                Function.Call(Hash.SET_RUN_SPRINT_THIS_FRAME, Game.Player.Handle);
                Game.DisplaySubtitle("~g~⚡ VELOCIDAD EXTREMA!", 3000);
                break;
                
            case "armas":
                GiveAllWeapons(playerPed);
                Game.DisplaySubtitle("~g~🔫 100+ armas equipadas!", 3000);
                break;
                
            case "quitar_armas":
                playerPed.Weapons.RemoveAll();
                Game.DisplaySubtitle("~r~🚫 Armas retiradas!", 3000);
                break;
                
            case "borracho":
                Function.Call(Hash.SET_PED_IS_DRUNK, playerPed.Handle, true);
                Game.DisplaySubtitle("~g~🥴 Efecto borracho!", 3000);
                break;
                
            case "super_fuerza":
                Function.Call(Hash.SET_PED_MELEE_WEAPON_DAMAGE_MODIFIER, playerPed.Handle, 10.0f);
                Game.DisplaySubtitle("~g~💪 SUPER FUERZA!", 3000);
                break;
                
            case "stamina":
                Function.Call(Hash.SET_PED_STAMINA, playerPed.Handle, 100.0f);
                Game.DisplaySubtitle("~g~🏃 Stamina infinita!", 3000);
                break;
                
            // ========== CLIMA ==========
            case "cl_extrasunny":
                Function.Call(Hash.SET_WEATHER_TYPE_NOW, "EXTRASUNNY");
                Game.DisplaySubtitle("~b~☀️ Soleado!", 3000);
                break;
                
            case "cl_clear":
                Function.Call(Hash.SET_WEATHER_TYPE_NOW, "CLEAR");
                Game.DisplaySubtitle("~b~🌈 Despejado!", 3000);
                break;
                
            case "cl_clouds":
                Function.Call(Hash.SET_WEATHER_TYPE_NOW, "CLOUDS");
                Game.DisplaySubtitle("~b~☁️ Nublado!", 3000);
                break;
                
            case "cl_smog":
                Function.Call(Hash.SET_WEATHER_TYPE_NOW, "SMOG");
                Game.DisplaySubtitle("~b~🌫️ Smog!", 3000);
                break;
                
            case "cl_foggy":
                Function.Call(Hash.SET_WEATHER_TYPE_NOW, "FOGGY");
                Game.DisplaySubtitle("~b~🌫️ Niebla!", 3000);
                break;
                
            case "cl_rain":
                Function.Call(Hash.SET_WEATHER_TYPE_NOW, "RAIN");
                Game.DisplaySubtitle("~b~🌧️ Lluvia!", 3000);
                break;
                
            case "cl_thunder":
                Function.Call(Hash.SET_WEATHER_TYPE_NOW, "THUNDER");
                Game.DisplaySubtitle("~b~⚡ Tormenta!", 3000);
                break;
                
            case "cl_snow":
                Function.Call(Hash.SET_WEATHER_TYPE_NOW, "SNOW");
                Game.DisplaySubtitle("~b~❄️ Nieve!", 3000);
                break;
                
            case "cl_blizzard":
                Function.Call(Hash.SET_WEATHER_TYPE_NOW, "BLIZZARD");
                Game.DisplaySubtitle("~b~🌨️ Ventisca!", 3000);
                break;
                
            case "cl_xmas":
                Function.Call(Hash.SET_WEATHER_TYPE_NOW, "XMAS");
                Game.DisplaySubtitle("~b~🎄 Navidad!", 3000);
                break;
                
            case "cl_halloween":
                Function.Call(Hash.SET_WEATHER_TYPE_NOW, "HALLOWEEN");
                Game.DisplaySubtitle("~b~🎃 Halloween!", 3000);
                break;
                
            case "t_amanecer":
                World.CurrentTimeOfDay = new TimeSpan(6, 0, 0);
                Game.DisplaySubtitle("~b~🌅 Amanecer (06:00)", 3000);
                break;
                
            case "t_dia":
                World.CurrentTimeOfDay = new TimeSpan(12, 0, 0);
                Game.DisplaySubtitle("~b~☀️ Mediodía (12:00)", 3000);
                break;
                
            case "t_noche":
                World.CurrentTimeOfDay = new TimeSpan(0, 0, 0);
                Game.DisplaySubtitle("~b~🌙 Noche (00:00)", 3000);
                break;
                
            // ========== VEHÍCULOS ==========
            case "veh_t20":
                SpawnVehicle("t20", playerPed.Position.Around(10f));
                break;
                
            case "veh_zentorno":
                SpawnVehicle("zentorno", playerPed.Position.Around(10f));
                break;
                
            case "veh_adder":
                SpawnVehicle("adder", playerPed.Position.Around(10f));
                break;
                
            case "veh_vagner":
                SpawnVehicle("vagner", playerPed.Position.Around(10f));
                break;
                
            case "veh_emerus":
                SpawnVehicle("emerus", playerPed.Position.Around(10f));
                break;
                
            case "veh_krieger":
                SpawnVehicle("krieger", playerPed.Position.Around(10f));
                break;
                
            case "veh_tyrant":
                SpawnVehicle("tyrant", playerPed.Position.Around(10f));
                break;
                
            case "veh_tezeract":
                SpawnVehicle("tezeract", playerPed.Position.Around(10f));
                break;
                
            case "veh_tempesta":
                SpawnVehicle("tempesta", playerPed.Position.Around(10f));
                break;
                
            case "veh_entity2":
                SpawnVehicle("entity2", playerPed.Position.Around(10f));
                break;
                
            case "veh_osiris":
                SpawnVehicle("osiris", playerPed.Position.Around(10f));
                break;
                
            case "veh_prototipo":
                SpawnVehicle("prototipo", playerPed.Position.Around(10f));
                break;
                
            case "veh_tractor":
                SpawnVehicle("tractor", playerPed.Position.Around(10f));
                break;
                
            case "veh_tractor2":
                SpawnVehicle("tractor2", playerPed.Position.Around(10f));
                break;
                
            case "veh_stretch":
                SpawnVehicle("stretch", playerPed.Position.Around(10f));
                break;
                
            case "veh_patriot2":
                SpawnVehicle("patriot2", playerPed.Position.Around(10f));
                break;
                
            case "veh_bus":
                SpawnVehicle("bus", playerPed.Position.Around(10f));
                break;
                
            case "veh_dump":
                SpawnVehicle("dump", playerPed.Position.Around(10f));
                break;
                
            case "veh_rhino":
                SpawnVehicle("rhino", playerPed.Position.Around(10f));
                break;
                
            case "veh_khanjali":
                SpawnVehicle("khanjali", playerPed.Position.Around(10f));
                break;
                
            case "veh_vigilante":
                SpawnVehicle("vigilante", playerPed.Position.Around(10f));
                break;
                
            case "veh_deluxo":
                SpawnVehicle("deluxo", playerPed.Position.Around(10f));
                break;
                
            case "veh_oppressor2":
                SpawnVehicle("oppressor2", playerPed.Position.Around(10f));
                break;
                
            case "veh_shotaro":
                SpawnVehicle("shotaro", playerPed.Position.Around(10f));
                break;
                
            case "veh_hydra":
                SpawnVehicle("hydra", playerPed.Position.Around(10f));
                break;
                
            case "veh_lazer":
                SpawnVehicle("lazer", playerPed.Position.Around(10f));
                break;
                
            case "veh_avenger":
                SpawnVehicle("avenger", playerPed.Position.Around(10f));
                break;
                
            case "veh_buzzard":
                SpawnVehicle("buzzard", playerPed.Position.Around(10f));
                break;
                
            case "veh_akula":
                SpawnVehicle("akula", playerPed.Position.Around(10f));
                break;
                
            case "veh_submersible":
                SpawnVehicle("submersible", playerPed.Position.Around(10f));
                break;
                
            case "veh_tropic":
                SpawnVehicle("tropic", playerPed.Position.Around(10f));
                break;
                
            case "veh_jetmax":
                SpawnVehicle("jetmax", playerPed.Position.Around(10f));
                break;
                
            // ========== NIVEL DE BÚSQUEDA ==========
            case "w_0":
                p.WantedLevel = 0;
                Game.DisplaySubtitle("~g~🕊️ 0 Estrellas", 3000);
                break;
                
            case "w_1":
                p.WantedLevel = 1;
                Game.DisplaySubtitle("~r~⭐ 1 Estrella", 3000);
                break;
                
            case "w_2":
                p.WantedLevel = 2;
                Game.DisplaySubtitle("~r~⭐⭐ 2 Estrellas", 3000);
                break;
                
            case "w_3":
                p.WantedLevel = 3;
                Game.DisplaySubtitle("~r~⭐⭐⭐ 3 Estrellas", 3000);
                break;
                
            case "w_4":
                p.WantedLevel = 4;
                Game.DisplaySubtitle("~r~⭐⭐⭐⭐ 4 Estrellas", 3000);
                break;
                
            case "w_5":
                p.WantedLevel = 5;
                Game.DisplaySubtitle("~r~⭐⭐⭐⭐⭐ 5 Estrellas", 3000);
                break;
                
            // ========== TELEPORTS ==========
            case "tp_michael":
                playerPed.Position = new Vector3(-852.4f, 160.5f, 65.6f);
                Game.DisplaySubtitle("~b~🏠 Casa Michael", 3000);
                break;
                
            case "tp_franklin":
                playerPed.Position = new Vector3(7.9f, 545.5f, 175.5f);
                Game.DisplaySubtitle("~b~🏠 Casa Franklin", 3000);
                break;
                
            case "tp_mazebank":
                playerPed.Position = new Vector3(-75.0f, -818.0f, 300.0f);
                Game.DisplaySubtitle("~b~🏢 Maze Bank Tower", 3000);
                break;
                
            case "tp_airport":
                playerPed.Position = new Vector3(-1034.0f, -2733.0f, 13.8f);
                Game.DisplaySubtitle("~b~✈️ Aeropuerto LSIA", 3000);
                break;
                
            case "tp_militar":
                playerPed.Position = new Vector3(-2040.0f, 3130.0f, 32.8f);
                Game.DisplaySubtitle("~b~🎖️ Base Militar", 3000);
                break;
                
            case "tp_carcel":
                playerPed.Position = new Vector3(1848.0f, 2605.0f, 45.5f);
                Game.DisplaySubtitle("~b~🔒 Cárcel", 3000);
                break;
                
            case "tp_casino":
                playerPed.Position = new Vector3(935.0f, 46.0f, 81.0f);
                Game.DisplaySubtitle("~b~🎰 Casino", 3000);
                break;
                
            case "tp_yatch":
                playerPed.Position = new Vector3(-2023.0f, -1050.0f, 6.0f);
                Game.DisplaySubtitle("~b~🛥️ Yate", 3000);
                break;
                
            case "tp_chiliad":
                playerPed.Position = new Vector3(493.0f, 556.0f, 760.0f);
                Game.DisplaySubtitle("~b~🏔️ Mt. Chiliad", 3000);
                break;
                
            case "tp_humanelabs":
                playerPed.Position = new Vector3(3525.0f, 3705.0f, 20.0f);
                Game.DisplaySubtitle("~b~🧪 Humane Labs", 3000);
                break;
                
            case "tp_paleto":
                playerPed.Position = new Vector3(-308.0f, 6095.0f, 31.0f);
                Game.DisplaySubtitle("~b~🌲 Paleto Bay", 3000);
                break;
                
            case "tp_observatory":
                playerPed.Position = new Vector3(-438.5f, 1076.0f, 352.0f);
                Game.DisplaySubtitle("~b~🔭 Observatorio", 3000);
                break;
                
            case "tp_korthacenter":
                playerPed.Position = new Vector3(-256.0f, -406.0f, 40.0f);
                Game.DisplaySubtitle("~b~🏛️ Kortz Center", 3000);
                break;
                
            case "tp_lighthouse":
                playerPed.Position = new Vector3(3265.0f, -4715.0f, 17.0f);
                Game.DisplaySubtitle("~b~🚨 Faro", 3000);
                break;
                
            default:
                Game.DisplaySubtitle("~r~❓ Comando desconocido: " + accion, 3000);
                break;
        }
    }
    
    private void SpawnVehicle(string modelName, Vector3 position)
    {
        try
        {
            Model model = new Model(modelName);
            model.Request(250);
            
            Vehicle vehicle = World.CreateVehicle(model, position);
            vehicle.IsEngineRunning = true;
            
            Game.Player.Character.Task.WarpIntoVehicle(vehicle, VehicleSeat.Driver);
            
            Game.DisplaySubtitle("~b~🚗 " + modelName.ToUpper() + " spawneado!", 3000);
        }
        catch (Exception ex)
        {
            Game.DisplaySubtitle("~r~❌ Error spawneando: " + modelName, 3000);
        }
    }
    
    private void SpawnAttack(string pedType, int count)
    {
        try
        {
            Vector3 playerPos = Game.Player.Character.Position;
            
            for (int i = 0; i < count; i++)
            {
                Vector3 spawnPos = playerPos.Around(30f);
                spawnPos.Z = playerPos.Z;
                
                Model model = GetPedModel(pedType);
                model.Request(1000);
                
                Ped ped = World.CreatePed(model, spawnPos);
                
                if (ped != null && ped.Exists())
                {
                    ped.Task.FightAgainst(Game.Player.Character);
                    ped.IsEnemy = true;
                }
            }
        }
        catch { }
    }
    
    private Model GetPedModel(string pedType)
    {
        switch (pedType.ToLower())
        {
            case "zombie": return new Model(PedHash.Zombie01);
            case "clown": return new Model(PedHash.Clown01);
            case "police": return new Model(PedHash.Cop01);
            case "fireman": return new Model(PedHash.Fireman01);
            case "ballas": return new Model(PedHash.BallaOrig01);
            case "vagos": return new Model(PedHash.VagosPrime01);
            case "marine": return new Model(PedHash.Marine01);
            case "alien": return new Model(PedHash.Alien01);
            case "ranchcop": return new Model(PedHash.RanchCop01);
            case "juggernaut": return new Model(PedHash.Juggernaut01);
            case "mime": return new Model(PedHash.Mime01);
            default: return new Model(PedHash.Male01);
        }
    }
    
    private void GiveAllWeapons(Ped ped)
    {
        WeaponHash[] armas = {
            WeaponHash.Knife, WeaponHash.Dagger, WeaponHash.Hammer, WeaponHash.Bat, WeaponHash.Crowbar,
            WeaponHash.GolfClub, WeaponHash.Bottle, WeaponHash.Hatchet, WeaponHash.Unarmed,
            WeaponHash.Pistol, WeaponHash.CombatPistol, WeaponHash.Pistol50, WeaponHash.SNSPistol,
            WeaponHash.HeavyPistol, WeaponHash.MachinePistol, WeaponHash.Revolver,
            WeaponHash.MicroSMG, WeaponHash.SMG, WeaponHash.AssaultSMG, WeaponHash.MiniSMG,
            WeaponHash.MG, WeaponHash.CombatMG, WeaponHash.Gusenberg,
            WeaponHash.AssaultRifle, WeaponHash.CarbineRifle, WeaponHash.AdvancedRifle,
            WeaponHash.SpecialCarbine, WeaponHash.BullpupRifle, WeaponHash.CompactRifle,
            WeaponHash.SniperRifle, WeaponHash.HeavySniper, WeaponHash.MarksmanRifle,
            WeaponHash.RPG, WeaponHash.GrenadeLauncher, WeaponHash.Minigun, WeaponHash.Firework,
            WeaponHash.Grenade, WeaponHash.StickyBomb, WeaponHash.Molotov, WeaponHash.ProximityMine,
            WeaponHash.PumpShotgun, WeaponHash.Sawnoff, WeaponHash.BullpupShotgun, WeaponHash.AssaultShotgun,
            WeaponHash.Musket, WeaponHash.HeavyShotgun, WeaponHash.DoubleBarrel,
            WeaponHash.SMG_MK2, WeaponHash.AssaultRifle_MK2, WeaponHash.CarbineRifle_MK2,
            WeaponHash.Pistol_MK2, WeaponHash.Sniper_MK2, WeaponHash.PrecisionRifle,
            WeaponHash.Revolver_MK2, WeaponHash.DoubleAction, WeaponHash.RayPistol,
            WeaponHash.RayCarbine, WeaponHash.RayMinigun, WeaponHash.CeramicPistol,
            WeaponHash.NavyRevolver, WeaponHash.GadgetPistol, WeaponHash.PericoPistol,
            WeaponHash.CandyCane, WeaponHash.Machete, WeaponHash.RubyPhone,
            WeaponHash.Knuckle, WeaponHash.Wrench, WeaponHash.BattleAxe
        };
        
        int count = 0;
        foreach (WeaponHash weapon in armas)
        {
            try
            {
                ped.Weapons.Give(weapon, 9999, true, true);
                count++;
            }
            catch { }
        }
    }
}
