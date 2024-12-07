import pygame
import random
from src.game.player import Player
from src.game.fire import Fire
from src.game.water_station import WaterStation
from src.game.level_loader import load_level, draw_tiles, draw_elements, is_tile_walkable
from src.core.settings import SPRITE_SCALE
from src.game.animals import Bear, Monkey, Bird
from src.game.powerup import ShieldPowerUp, WaterRefillPowerUp, SpeedBoostPowerUp, ExtraLifePowerUp
from src.core.utils import load_image
from src.game.levels import LEVELS


class GamePlay:
    """
    Inicialización de la configuración del gameplay
    """
    def __init__(self, screen, level_config, on_game_over, on_level_complete, level_index=0, sounds=None):
        self.screen = screen
        self.level_file = level_config["level_file"]
        self.fire_spawn_interval = level_config["fire_spawn_interval"]
        self.min_active_fires = level_config["min_active_fires"]
        self.max_active_fires = level_config["max_active_fires"]
        self.max_spread_fire = level_config["max_spread_fire"]
        self.fire_intensity = level_config["fire_intensity"]
        self.time_limit = level_config["time_limit"]
        self.on_game_over = on_game_over
        self.on_level_complete = on_level_complete
        self.level_index = level_index
        self.sounds = sounds if sounds else {}
        
        self.special_mode_triggered = False
        self.special_extinguish_mode = False
        self.special_presses = 0
        self.is_last_level = (self.level_index == 4)

        # Inicializar datos del nivel
        self.level_data = load_level(self.level_file)

        # Cargar spritesheet de tiles
        self.tiles_spritesheet = pygame.image.load("assets/images/tiles/tiles.png").convert_alpha()
        self.element_sprites = self.load_element_sprites()

        # Carga de la imagen de FJ_keys
        self.fj_keys_image = load_image("keys/FJ_keys.png")

        # Extraer los frames
        fj_frame_width = 16
        fj_frame_height = 16
        self.fj_keys_frames = []

        for i in range(2):
            frame = self.fj_keys_image.subsurface(pygame.Rect(i * fj_frame_width, 0, fj_frame_width, fj_frame_height))
            frame = pygame.transform.scale(frame, (fj_frame_width * SPRITE_SCALE, fj_frame_height * SPRITE_SCALE))
            self.fj_keys_frames.append(frame)

        self.fj_keys_index = 0
        self.fj_keys_timer = 0
        self.fj_keys_frame_duration = 0.5
        self.fj_show_keys = True

        # Inicializar entidades del nivel
        self.fires = []
        self.fire_spawn_timer = 0
        self.water_stations = self.initialize_water_stations()
        self.player = self.initialize_player()
        self.total_time = self.time_limit
        self.remaining_time = self.total_time
        self.animation_timer = 0

        # Inicializar animales
        self.animals = self.initialize_animals(level_config.get("animals", []))

        # Inicializar powerups
        self.powerups = []

        # Cargar configuración de powerups predeterminados
        timed_powerups_data = level_config.get("timed_powerups", [])
        self.timed_powerups = []
        for tp_data in timed_powerups_data:
            powerup_class = self.get_powerup_class(tp_data["type"])
            
            if powerup_class is not None:
                self.timed_powerups.append({
                    "powerup_class": powerup_class,
                    "time": tp_data["time"],
                    "spawned": False
                })

        # Generar fuegos iniciales
        for _ in range(self.min_active_fires):
            new_fire = self.create_random_fire()
            if new_fire:
                self.fires.append(new_fire)
        
        self.fire_sound_playing = False
        self.recharge_sound_playing = False
        self.steps_sound_playing = False
        

    def load_element_sprites(self):
        """
        Carga los sprites para los elementos adicionales (hidrantes, etc.).
        """
        hydrant_sprite = pygame.image.load("assets/images/hydrant/hydrant.png").convert_alpha()
        hydrant_sprite = pygame.transform.scale(hydrant_sprite, (16 * SPRITE_SCALE, 16 * SPRITE_SCALE))
        return {"hydrant": hydrant_sprite}


    def initialize_player(self):
        """
        Inicializa al jugador en la posición inicial definida en el nivel.
        """
        start_position = self.level_data["player_start"]
        return Player(start_position["x"], start_position["y"], sounds=self.sounds)


    def initialize_water_stations(self):
        """
        Inicializa las estaciones de agua (hidrantes) del nivel.
        """
        water_stations = []
        for element in self.level_data["elements"]:
            if element["type"] == "hydrant":
                water_stations.append(WaterStation(element["x"], element["y"]))
        return water_stations


    def initialize_animals(self, animal_data):
        """
        Crea instancias de animales basados en los datos del nivel
        """
        animals = []
        for animal_info in animal_data:
            x, y = animal_info["x"], animal_info["y"]
            spawn_time = animal_info.get("spawn_time", 0)
            
            if animal_info["type"] == "bear":
                animal = Bear(x, y, spawn_time)
            elif animal_info["type"] == "monkey":
                animal = Monkey(x, y, spawn_time)
            elif animal_info["type"] == "bird":
                animal = Bird(x, y, spawn_time)
            else:
                continue

            animal.is_active = False

            # Incremento de vida
            extra_life = 50 * self.level_index
            animal.life += extra_life
            animal.max_life += extra_life

            animals.append(animal)
        
        self.total_animals = len(animals)
        self.rescued_animals_count = 0
        return animals


    def get_powerup_class(self, powerup_type):
        """
        Devolver clase correspondiente de powerup
        """
        mapping = {
            "ExtraLifePowerUp": ExtraLifePowerUp,
            "WaterRefillPowerUp": WaterRefillPowerUp,
            "SpeedBoostPowerUp": SpeedBoostPowerUp,
            "ShieldPowerUp": ShieldPowerUp
        }
        return mapping.get(powerup_type, None)
        

    def create_random_fire(self):
        """
        Crea un fuego en una posición aleatoria válida.
        """
        tile_size = 16 * SPRITE_SCALE
        hydrant_positions = {(ws.x // tile_size, ws.y // tile_size) for ws in self.water_stations}

        for _ in range(10):  # Intentar encontrar una posición válida hasta 10 veces
            col = random.randint(0, len(self.level_data["level"][0]) - 1)
            row = random.randint(0, len(self.level_data["level"]) - 1)

            if (col, row) in hydrant_positions:
                continue

            x = col * tile_size
            y = row * tile_size
            fire_rect = pygame.Rect(x, y, tile_size, tile_size)

            if is_tile_walkable(self.level_data, fire_rect, tile_size):
                if any(fire.get_rect().colliderect(fire_rect) for fire in self.fires):
                    continue
                
                fire = Fire(x, y)
                fire.intensity = self.fire_intensity
                return Fire(x, y)

        return None


    def create_random_powerup(self, powerup_class):
        """
        Crea un powerup de una cierta clase en un posición aleatoria
        """
        tile_size = 16 * SPRITE_SCALE
        hydrant_positions = {(ws.x // tile_size, ws.y // tile_size) for ws in self.water_stations}

        for _ in range(50):
            col = random.randint(0, len(self.level_data["level"][0]) - 1)
            row = random.randint(0, len(self.level_data["level"]) - 1)

            if (col, row) in hydrant_positions:
                continue

            x = col * tile_size
            y = row * tile_size
            rect = pygame.Rect(x, y, tile_size, tile_size)

            if is_tile_walkable(self.level_data, rect, tile_size):
                return powerup_class(x, y)
        
        return None


    def special_fire_extinguish(self, keys):
        if self.fj_show_keys:
            if keys[pygame.K_f] and keys[pygame.K_j]:
                self.fj_show_keys = False

        if keys[pygame.K_f] and keys[pygame.K_j]:
                self.special_presses += 1
                # Cada 10 presiones reducimos intensidad de todos los fuegos en 5
                if self.special_presses % 10 == 0:
                    for fire in self.fires:
                        if fire.is_active:
                            fire.extinguish(5)
                    self.sounds["extinguish"].play()


    def update(self, dt, keys):
        """
        Actualiza la lógica del juego.
        """
        # Reducir el tiempo restante
        self.remaining_time -= dt
        if self.remaining_time <= 0:
            self.on_game_over()
        
        self.animation_timer += dt

        # Manejo del temporizador para aparición de fuegos
        self.fire_spawn_timer += dt
        if self.fire_spawn_timer >= self.fire_spawn_interval:
            self.fire_spawn_timer = 0

            # Generar nuevos fuegos si no se ha alcanzado el límite
            if len(self.fires) < self.max_active_fires:
                new_fire = self.create_random_fire()
                if new_fire:
                    self.fires.append(new_fire)
        
        # Actualizar la lógica del jugador
        self.player.update(dt, keys, self.level_data, 16 * SPRITE_SCALE, self.water_stations, self.animals)

        # Sonido de pasos
        if self.player.is_running:
            if not self.steps_sound_playing:
                self.sounds["steps"].play(-1)
                self.sounds["steps"].set_volume(0.2)
                self.steps_sound_playing = True
        else:
            if self.steps_sound_playing:
                self.sounds["steps"].stop()
                self.sounds["steps"].set_volume(0.2)
                self.steps_sound_playing = False
        
        # Sonido de recarga
        if keys[pygame.K_r]:
            # Reproduces recarga si no suena ya
            if not self.recharge_sound_playing:
                self.sounds["recharge"].play(-1)
                self.recharge_sound_playing = True
        else:
            if self.recharge_sound_playing:
                self.sounds["recharge"].stop()
                self.recharge_sound_playing = False

        # Si estamos modo especial
        if self.special_extinguish_mode:
            self.special_fire_extinguish(keys)
        else:
            self.player.interact_with_fire(self.fires, keys)

        # self.player.interact_with_fire(self.fires, keys)
        self.player.interact_with_animals(self.animals, keys)
        self.player.handle_collision(self.fires, dt, self.level_data, 16 * SPRITE_SCALE)
        self.player.recharge_water(self.water_stations, keys, dt=dt)
        
        # Interactuar con powerups
        self.player.interact_with_powerups(self.powerups)

        # Actualizar la lógica de los fuegos
        for fire in self.fires:
            fire.update(dt)
            fire.update_spread(dt, self.fires, self.max_spread_fire, self.player, self.water_stations, self.level_data, 16 * SPRITE_SCALE)
        
        # Tiempo transcurrido
        elapsed_time = self.total_time - self.remaining_time

        # Control del sonido de fuego
        active_fires_count = sum(f.is_active for f in self.fires)
        if active_fires_count > 0 and not self.fire_sound_playing:
            self.sounds["fire"].play(-1)
            self.fire_sound_playing = True
        elif active_fires_count == 0 and self.fire_sound_playing:
            self.sounds["fire"].stop()
            self.fire_sound_playing = False

        # Último nivel
        if self.is_last_level and not self.special_mode_triggered:
            no_animals_left = (len(self.animals) == 0)
            no_water_powerups = True

            for p in self.powerups:
                if isinstance(p, WaterRefillPowerUp) and p.is_active:
                    no_water_powerups = False
                    break
            
            if elapsed_time >= 90 and no_animals_left and no_water_powerups:
                self.special_mode_triggered = True
                self.special_extinguish_mode = True
                self.player.water = 0

                # Generar más fuego
                for _ in range(25):
                    new_fire = self.create_random_fire()
                    if new_fire:
                        self.fires.append(new_fire)

        # Aparición de animales según spawn_time
        for animal in self.animals:
            if (not animal.is_active
                and not animal.is_rescued
                and not animal.has_been_rescued
                and elapsed_time >= animal.spawn_time):
                animal.is_active = True
                # Reproducir sonido de animal
                if isinstance(animal, Bird):
                    self.sounds["bird"].play()
                elif isinstance(animal, Bear):
                    self.sounds["bear"].play()
                elif isinstance(animal, Monkey):
                    self.sounds["monkey"].play()
        
        # Actualizamos los animales
        for animal in self.animals:
            animal.update(dt)
        
        # Generar powerup si animal fue rescatado
        for animal in self.animals:
            if animal.has_been_rescued and animal.powerup_class and not animal.notify_powerup:
                new_powerup = animal.powerup_class(animal.x, animal.y)
                self.powerups.append(new_powerup)
                animal.notify_powerup = True
                self.sounds["powerup"].play()
        
        # Contar animales rescatados
        for animal in self.animals:
            if animal.has_been_rescued and animal.counted_as_rescued == False:
                animal.counted_as_rescued = True
                self.rescued_animals_count += 1

        # Verificar power-ups temporizados
        for tp in self.timed_powerups:
            if not tp["spawned"] and elapsed_time >= tp["time"]:
                # Crear power-up en una posición aleatoria válida
                p_instance = self.create_random_powerup(tp["powerup_class"])
                if p_instance:
                    self.powerups.append(p_instance)
                    tp["spawned"] = True
                    self.sounds["powerup"].play()

        # Filtrar animales rescatados
        self.animals = [animal for animal in self.animals
                        if not (not animal.is_active and not animal.is_rescued and animal.has_been_rescued)]
        
        # Filtrar power-ups recolectados
        self.powerups = [powerup for powerup in self.powerups if powerup.is_active]

        # Verificar todos los fuegos apagados
        all_fires_out = all(not fire.is_active for fire in self.fires)
        all_animals_rescued = (self.rescued_animals_count == self.total_animals)

        # Verificar si el nivel ha sido completado
        if all_fires_out and all_animals_rescued and self.remaining_time > 0:
            self.on_level_complete()

        # Animar teclas FJ si se muestran
        if self.special_extinguish_mode and self.fj_show_keys:
            self.fj_keys_timer += dt
            if self.fj_keys_timer >= self.fj_keys_frame_duration:
                self.fj_keys_timer = 0
                self.fj_keys_index = (self.fj_keys_index + 1) % len(self.fj_keys_frames)


    def draw(self):
        """
        Renderiza todos los elementos del juego en pantalla.
        """
        # Dibujar el nivel
        self.screen.fill((0, 0, 0))
        draw_tiles(self.screen, self.level_data["level"], self.tiles_spritesheet, 16, SPRITE_SCALE, self.animation_timer)
        draw_elements(self.screen, self.level_data["elements"], self.element_sprites)

        # Dibujar estaciones de agua
        for water_station in self.water_stations:
            water_station.draw(self.screen)

        # Dibujar fuegos
        for fire in self.fires:
            fire.draw(self.screen)

        # Dibujar animales
        for animal in self.animals:
            animal.draw(self.screen)

        # Dibuja los powerups
        for powerup in self.powerups:
            powerup.draw(self.screen)

        # Dibujar jugador
        self.player.draw(self.screen)

        # Dibujar el HUD
        self.player.draw_hud(self.screen, self.total_time, self.remaining_time)

        # Dibujar las teclas FJ sobre el jugador si está en modo especial y si se muestran
        if self.special_extinguish_mode and self.fj_show_keys:
            key_sprite = self.fj_keys_frames[self.fj_keys_index]
            key_width, key_height = key_sprite.get_size()
            x_pos = self.player.x
            y_pos = self.player.y - key_height - 10
            self.screen.blit(key_sprite, (x_pos, y_pos))
            