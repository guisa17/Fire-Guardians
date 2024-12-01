import pygame
from src.core.settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from src.game.fire import Fire
from src.game.player import Player
from src.core.utils import draw_status

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Fire Guardians")
    clock = pygame.time.Clock()

    GREEN = (34, 139, 34)
    player = Player(x=100, y=100)
    fires = Fire.spawn_random_fires(amount=5)

    running = True
    while running:
        dt = clock.tick(FPS) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        player.update(dt, keys)

        if keys[pygame.K_SPACE]:
            player.extinguish_fire(fires)

        screen.fill(GREEN)
        for fire in fires:
            fire.draw(screen)
        player.draw(screen)
        draw_status(screen, player)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
