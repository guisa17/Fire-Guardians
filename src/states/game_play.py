import pygame
import random
from src.game.player import Player
from src.game.fire import Fire
from src.game.water_station import WaterStation
from src.game.level_loader import load_level, draw_tiles, draw_elements, is_tile_walkable
from src.game.levels import LEVELS
from src.core.settings import SPRITE_SCALE, SCREEN_WIDTH, SCREEN_HEIGHT


def create_random_fire(level_data, tile_size, water_stations, fires):
    """
    Crea un fuego en una posición aleatoria válida.
    """
    hydrant_positions = {(ws.x // tile_size, ws.y // tile_size) for ws in water_stations}

    for _ in range(10):  # Intentar encontrar una posición válida hasta 10 veces
        col = random.randint(0, len(level_data["level"][0]) - 1)
        row = random.randint(0, len(level_data["level"]) - 1)

        if (col, row) in hydrant_positions:
            continue

        x = col * tile_size
        y = row * tile_size
        fire_rect = pygame.Rect(x, y, tile_size, tile_size)

        # Solo colocar fuego en tiles "walkable" y lejos de otros fuegos
        if is_tile_walkable(level_data, fire_rect, tile_size):
            for fire in fires:
                if fire.get_rect().colliderect(fire_rect):
                    break
            else:
                return Fire(x, y)

    return None  # No encontró posición válida


def initialize_water_stations(level_data):
    """
    Crea los hidrantes basados en los elementos del nivel.
    """
    water_stations = []
    for element in level_data["elements"]:
        if element["type"] == "hydrant":
            water_stations.append(WaterStation(element["x"], element["y"]))
    return water_stations


class GamePlay:
    def __init__(self, level_number):
        """
        Inicializa el juego para el nivel seleccionado.
        """
        self.level_config = LEVELS[level_number - 1]
        self.player = None
        self.fires = []
        self.water_stations = []
        self.fire_spawn_timer = 0
        self.running = True
        self.level_data = None
        self.tiles_spritesheet = None
        self.element_sprites = None


    def setup_level(self):
        """
        Configura el nivel, inicializando jugador, fuegos e hidrantes.
        """
        # Cargar nivel y configuraciones
        self.level_data = load_level("level.json")
        self.player = Player(0, 0)
        start_position = self.level_data["player_start"]
        self.player.x = start_position["x"]
        self.player.y = start_position["y"]

        # Inicializar elementos del nivel
        self.water_stations = initialize_water_stations(self.level_data)
        self.tiles_spritesheet = pygame.image.load("assets/images/tiles/tiles.png").convert_alpha()
        self.element_sprites = self.load_element_sprites()

        # Generar los fuegos iniciales
        for _ in range(self.level_config["max_active_fires"]):
            new_fire = create_random_fire(self.level_data, 16 * SPRITE_SCALE, self.water_stations, self.fires)
            if new_fire:
                self.fires.append(new_fire)


    def load_element_sprites(self):
        """
        Carga los sprites para elementos adicionales como los hidrantes.
        """
        hydrant_sprite = pygame.image.load("assets/images/hydrant/hydrant.png").convert_alpha()
        hydrant_sprite = pygame.transform.scale(hydrant_sprite, (16 * SPRITE_SCALE, 16 * SPRITE_SCALE))
        return {"hydrant": hydrant_sprite}


    def update(self, dt):
        """
        Actualiza la lógica del nivel, incluyendo fuegos, jugador y temporizador.
        """
        self.fire_spawn_timer += dt
        if self.fire_spawn_timer >= self.level_config["fire_spawn_interval"]:
            self.fire_spawn_timer = 0

            # Generar nuevos fuegos si no se ha alcanzado el límite
            fires_to_spawn = self.level_config["max_active_fires"] - len(self.fires)
            for _ in range(fires_to_spawn):
                new_fire = create_random_fire(self.level_data, 16 * SPRITE_SCALE, self.water_stations, self.fires)
                if new_fire:
                    self.fires.append(new_fire)

        # Actualizar el temporizador del jugador
        self.player.time_left -= dt
        if self.player.time_left <= 0:
            self.running = False

        # Obtener teclas presionadas
        keys = pygame.key.get_pressed()

        # Actualizar lógica del jugador
        self.player.update(dt, keys, self.level_data, 16 * SPRITE_SCALE, self.water_stations)
        self.player.interact_with_fire(self.fires, keys)
        self.player.handle_collision(self.fires, dt, self.level_data, 16 * SPRITE_SCALE)
        self.player.recharge_water(self.water_stations, keys, dt=dt)

        # Actualizar lógica de los fuegos
        for fire in self.fires:
            fire.update(dt)
            fire.update_spread(dt, self.fires, self.level_config["max_spread_fire"], self.player, self.water_stations, self.level_data, 16 * SPRITE_SCALE)


    def draw(self, screen):
        """
        Dibuja todos los elementos del nivel en la pantalla.
        """
        # Dibujar nivel y elementos
        screen.fill((0, 0, 0))  # Fondo negro
        draw_tiles(screen, self.level_data["level"], self.tiles_spritesheet, 16, SPRITE_SCALE)
        draw_elements(screen, self.level_data["elements"], self.element_sprites)

        # Dibujar hidrantes
        for water_station in self.water_stations:
            water_station.draw(screen)

        # Dibujar jugador
        self.player.draw(screen)

        # Dibujar fuegos
        for fire in self.fires:
            fire.draw(screen)

        # Dibujar HUD del jugador
        self.player.draw_hud(screen)
