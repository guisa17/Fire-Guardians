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
        "fire_spawn_interval": 6,          # intervalo de aparición
        "min_active_fires": 4,              # min fuegos activos
        "max_active_fires": 10,              # max fuegos activos
        "max_spread_fire": 5,               # max fuegos por spread
        "fire_intensity": 120,
        "time_limit": 70,
        "animals": [
            {"type": "bear", "x": 282, "y": 282, "spawn_time": 10},
            {"type": "monkey", "x": 636, "y": 512, "spawn_time": 20}
        ],
        "timed_powerups": [
            {"type": "WaterRefillPowerUp", "time": 40}
        ]
    },
    {
        "level_file": "assets/levels/3.json",
        "fire_spawn_interval": 4,          # intervalo de aparición
        "min_active_fires": 5,              # min fuegos activos
        "max_active_fires": 15,              # max fuegos activos
        "max_spread_fire": 7,               # max fuegos por spread
        "fire_intensity": 140,
        "time_limit": 80,
        "animals": [
            {"type": "bear", "x": 282, "y": 282, "spawn_time": 10},
            {"type": "monkey", "x": 636, "y": 512, "spawn_time": 20}
        ],
        "timed_powerups": [
            {"type": "WaterRefillPowerUp", "time": 40}
        ]
    }
]
