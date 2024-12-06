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
            {"type": "bear", "x": 282, "y": 282, "spawn_time": 1},
            {"type": "bird", "x": 200, "y": 250, "spawn_time": 5}
        ]
    }
]

