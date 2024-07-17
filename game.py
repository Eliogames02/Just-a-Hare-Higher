import pygame as py
import sys
from scripts.entities import PhysicsEntity, Player, Collectible 
from scripts.utils import load_image, load_images, Animation
from scripts.tilemap import Tilemap

BG_COLOR = (152, 245, 255)

class Game:
    def __init__(self) -> None:
        # pygame setup
        py.init()
        
        # window setup
        py.display.set_caption('Just a Hare Higher')
        self.screen = py.display.set_mode((640, 480))
        self.display = py.Surface((320, 240))

        # clock/fps setup
        self.clock = py.time.Clock()

        # font setup
        self.default_font = py.font.SysFont("Time New Roman", 24)

        self.movement = [False, False]
        self.move_speed = 3
        self.stored_movement = [False, False]

        self.assets = {
            'player': load_image('entities/player/player_test.png'),
            'dirt': load_images('tiles/dirt'),
            'collectible/carrot': Animation(load_images('tiles/collectible/carrot')),
            'player/idle': Animation(load_images('entities/player')),
        }

        #tilemap
        self.tilemap = Tilemap(self, tile_size=16)
        try:
            self.tilemap.load('data/maps/map.json')
        except FileNotFoundError:
            pass

        # player
        self.player = Player(self, (160, 200), (16, 16))

        #camera setup
        self.scroll = [0, 0]

        # collectibles
        self.collectibles = []
        for carrot in self.tilemap.extract([('collectible', 0)]):
            self.collectibles.append(Collectible(self, carrot['pos'], (16, 16)))
        
        self.collected_collectibles = []

    # Gameloop
    def run(self) -> None:
        while True:
            self.display.fill(BG_COLOR)

            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() /2 - self.scroll[0]) / 30
            self.scroll[1] += (self.player.rect().centery - self.display.get_height() /2 - self.scroll[1]) / 12
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))
 
            self.tilemap.render(self.display, offset=render_scroll)

            self.player.update(self.tilemap, ((self.movement[1] - self.movement[0]) * self.move_speed, 0), (0, self.stored_movement[1]))
            self.player.render(self.display, offset=render_scroll)

            for collectible in self.collectibles:
                if collectible.collected():
                    self.collected_collectibles.append(collectible)
                else: 
                    collectible.update()
                    collectible.render(self.display, offset=render_scroll)

            event_handler(self) 
    
            self.screen.blit(py.transform.scale(self.display, self.screen.get_size()), (0, 0))
            update_screen(self.clock)

# Handles all events and inputs
def event_handler(self) -> None:
    # Checks if any event happens then executes code.
    for event in py.event.get():
        # Exits the program
        if event.type == py.QUIT:
            exit_game()

        if event.type == py.KEYDOWN:
            if event.key == py.K_ESCAPE:
                exit_game()

            if event.key == py.K_LEFT or event.key == py.K_a:
                self.movement[0] = True
            if event.key == py.K_RIGHT or event.key == py.K_d:
                self.movement[1] = True

            if event.key == py.K_w or event.key == py.K_UP:
                self.stored_movement[1] = True

        if event.type == py.KEYUP:
            if event.key == py.K_LEFT or event.key == py.K_a:
                self.movement[0] = False
            if event.key == py.K_RIGHT or event.key == py.K_d:
                self.movement[1] = False
            if event.key == py.K_UP or event.key == py.K_w:
                self.stored_movement[1] = False

# Handles updating the screen and fps
def update_screen(clock) -> None:
    py.display.flip()
    clock.tick(60)
# Exits the game
def exit_game() -> None:
    py.quit()
    sys.exit()
    
game = Game()
game.run()