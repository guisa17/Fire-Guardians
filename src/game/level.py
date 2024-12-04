from src.game.fire import Fire
from src.game.animals import Bear, Monkey, Bird
from src.game.water_station import WaterStation
from src.game.powerup import WaterRefillPowerUp, ExtraLifePowerUp, SpeedBoostPowerUp, ShieldPowerUp
from src.core.settings import SPRITE_SCALE,SCREEN_WIDTH,SCREEN_HEIGHT
from src.core.utils import generate_random_fire

def create_level_1():
    fires = generate_random_fire(5, 16 * SPRITE_SCALE, 16 * SPRITE_SCALE, player_position=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), min_distance=100, min_fire_distance=50)
    animals = []
    powerups = [
        WaterRefillPowerUp(200, 200),
        ExtraLifePowerUp(300, 300)
    ]
    water_station = WaterStation(100, 100)
    return fires, animals, powerups, water_station

def create_level_2():
    fires = generate_random_fire(7, 16 * SPRITE_SCALE, 16 * SPRITE_SCALE, player_position=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), min_distance=100, min_fire_distance=50)
    animals = [Bear(300, 300), Monkey(500, 500)]
    powerups = [
        WaterRefillPowerUp(200, 200),
        ShieldPowerUp(400, 400)
    ]
    water_station = WaterStation(500, 200)
    return fires, animals, powerups, water_station

def create_level_3():
    fires = generate_random_fire(10, 16 * SPRITE_SCALE, 16 * SPRITE_SCALE, player_position=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), min_distance=100, min_fire_distance=50)
    animals = [Bear(200, 200), Monkey(300, 300), Bird(400, 100)]
    powerups = [
        ExtraLifePowerUp(400, 400),
        SpeedBoostPowerUp(600, 300)
    ]
    water_station = WaterStation(700, 600)
    return fires, animals, powerups, water_station

def create_level_4():
    fires = generate_random_fire(12, 16 * SPRITE_SCALE, 16 * SPRITE_SCALE, player_position=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), min_distance=100, min_fire_distance=50)
    animals = [Bear(200, 200), Monkey(500, 500), Bird(100, 100), Bear(600, 300)]
    powerups = [
        ShieldPowerUp(600, 100),
        WaterRefillPowerUp(700, 200)
    ]
    water_station = WaterStation(300, 300)
    return fires, animals, powerups, water_station

def create_level_5():
    fires = generate_random_fire(15, 16 * SPRITE_SCALE, 16 * SPRITE_SCALE, player_position=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), min_distance=100, min_fire_distance=50)
    animals = [Bear(400, 400), Monkey(200, 200), Bird(100, 100), Bear(600, 600)]
    powerups = [
        SpeedBoostPowerUp(400, 400)
    ]
    water_station = WaterStation(500, 500)
    return fires, animals, powerups, water_station
