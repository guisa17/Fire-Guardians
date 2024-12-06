"""
Configuraciones de los niveles
"""

LEVELS = [
    {
        "level_file": "assets/levels/1.json",
        "fire_spawn_interval": 10,          # intervalo de aparición
        "min_active_fires": 2,              # min fuegos activos
        "max_active_fires": 7,              # max fuegos activos
        "max_spread_fire": 3,               # max fuegos por spread
        "fire_intensity": 100,
        "time_limit": 60,
        "animals": [
            {"type": "bear", "x": 282, "y": 282, "spawn_time": 10},
            {"type": "monkey", "x": 636, "y": 512, "spawn_time": 20}
        ],
        "timed_powerups": [
            {"type": "ExtraLifePowerUp", "time": 30}
        ]
    },
    {
        "level_file": "assets/levels/2.json",
        "fire_spawn_interval": 7,          # intervalo de aparición
        "min_active_fires": 4,              # min fuegos activos
        "max_active_fires": 10,              # max fuegos activos
        "max_spread_fire": 5,               # max fuegos por spread
        "fire_intensity": 110,
        "time_limit": 75,
        "animals": [
            {"type": "bear", "x": 186, "y": 282, "spawn_time": 15},
            {"type": "monkey", "x": 636, "y": 90, "spawn_time": 40},
            {"type": "bird", "x": 138, "y": 560, "spawn_time": 25},
        ],
        "timed_powerups": [
            {"type": "ExtraLifePowerUp", "time": 30}
        ]
    },
    {
        "level_file": "assets/levels/3.json",
        "fire_spawn_interval": 5,           # intervalo de aparición
        "min_active_fires": 5,              # min fuegos activos
        "max_active_fires": 15,             # max fuegos activos
        "max_spread_fire": 7,               # max fuegos por spread
        "fire_intensity": 120,
        "time_limit": 90,
        "animals": [
            {"type": "bear", "x": 684, "y": 90, "spawn_time": 10},
            {"type": "bird", "x": 240, "y": 512, "spawn_time": 20},
            {"type": "monkey", "x": 288, "y": 368, "spawn_time": 35}
        ],
        "timed_powerups": [
            {"type": "WaterRefillPowerUp", "time": 30},
            {"type": "ExtraLifePowerUp", "time": 40},
            {"type": "WaterRefillPowerUp", "time": 50}
        ]
    },
    {
        "level_file": "assets/levels/4.json",
        "fire_spawn_interval": 3,           # intervalo de aparición
        "min_active_fires": 7,              # min fuegos activos
        "max_active_fires": 20,             # max fuegos activos
        "max_spread_fire": 10,              # max fuegos por spread
        "fire_intensity": 130,
        "time_limit": 100,
        "animals": [
            {"type": "bear", "x": 192, "y": 512, "spawn_time": 15},
            {"type": "monkey", "x": 780, "y": 512, "spawn_time": 35},
            {"type": "bird", "x": 192, "y": 224, "spawn_time": 50},
            {"type": "bear", "x": 828, "y": 320, "spawn_time": 65},
            {"type": "monkey", "x": 576, "y": 48, "spawn_time": 75},
        ],
        "timed_powerups": [
            {"type": "WaterRefillPowerUp", "time": 20},
            {"type": "ExtraLifePowerUp", "time": 30},
            {"type": "WaterRefillPowerUp", "time": 40},
            {"type": "SpeedBoostPowerUp", "time": 55},
            {"type": "WaterRefillPowerUp", "time": 60}
        ]
    },
    {
        "level_file": "assets/levels/5.json",
        "fire_spawn_interval": 3,           # intervalo de aparición
        "min_active_fires": 5,              # min fuegos activos
        "max_active_fires": 20,             # max fuegos activos
        "max_spread_fire": 10,              # max fuegos por spread
        "fire_intensity": 140,
        "time_limit": 120,
        "animals": [
            {"type": "bird", "x": 636, "y": 240, "spawn_time": 10},
            {"type": "bear", "x": 282, "y": 282, "spawn_time": 20},
            {"type": "bird", "x": 240, "y": 480, "spawn_time": 25},
            {"type": "monkey", "x": 540, "y": 512, "spawn_time": 30},
            {"type": "bird", "x": 432, "y": 144, "spawn_time": 35},
            {"type": "bear", "x": 672, "y": 384, "spawn_time": 40},
            {"type": "monkey", "x": 432, "y": 432, "spawn_time": 45},
        ],
        "timed_powerups": [
            {"type": "ExtraLifePowerUp", "time": 25},
            {"type": "ExtraLifePowerUp", "time": 35},
            {"type": "WaterRefillPowerUp", "time": 45},
            {"type": "ExtraLifePowerUp", "time": 55},
            {"type": "WaterRefillPowerUp", "time": 65},
            {"type": "WaterRefillPowerUp", "time": 80},
        ]
    },
]
