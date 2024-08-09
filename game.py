import pygame as py
import sys, time
from scripts.entities import *
from scripts.utils import load_image, load_images, Animation
from scripts.clouds import Clouds
from scripts.tilemap import Tilemap

class Game:
    def __init__(self) -> None:
        # pygame setup
        py.init()
        
        # window setup
        py.display.set_caption('Just a Hare Higher')
        self.screen = py.display.set_mode((1280, 960))
        self.display = py.Surface((640, 480))

        # clock/fps setup
        self.clock = py.time.Clock()
        self.delta_time = 0
        self.prev_time = time.time() 

        # font setup
        self.default_font = py.font.SysFont("Time New Roman", 24)

        self.movement = [False, False]
        self.move_speed = 3
        self.stored_movement = [False, False]

        self.assets = {
            'player': load_image('entities/player/player_test.png'),
            'dirt': load_images('tiles/dirt'),
            'spawner': load_images('tiles/spawners'),
            'clouds': load_images('clouds'),
            'background': load_image('Background.png'),
            'collectible/carrot': Animation(load_images('tiles/collectible/carrot')),
            'collectible/radish': Animation(load_images('tiles/collectible/radish')),
            'player/idle': Animation(load_images('entities/player')),
            'tick_enemy/test': Animation(load_images('entities/tick_enemy')),
            'dung_enemy/test': Animation(load_images('entities/dung_enemy')),
            'mole/test': Animation(load_images('entities/mole')),
            'projectile/poop': Animation(load_images('entities/projectiles')),
        }

        #tilemap
        self.tilemap = Tilemap(self, tile_size=16)

        #clouds
        self.clouds = Clouds(self.assets['clouds'])

        # player
        self.player = Player(self, (160, 200), (16, 16))
        
        # loads the level data
        self.load_level()

        # camera positioning
        self.scroll = [self.player.pos[0] - self.display.get_width()/2, self.player.pos[1] - self.display.get_height()/2]

    # Gameloop
    def run(self) -> None:
        while True:
            self.display.blit(py.transform.scale(self.assets['background'], self.display.get_size()), (0,0))

            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() /2 - self.scroll[0]) / 30 * self.delta_time
            self.scroll[1] += (self.player.rect().centery - self.display.get_height() /2 - self.scroll[1]) / 12 * self.delta_time
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            self.clouds.update(self.delta_time)
            self.clouds.render(self.display, offset=render_scroll)
 
            self.tilemap.render(self.display, offset=render_scroll)

            self.player.update(((self.movement[1] - self.movement[0]) * self.move_speed, 0), (0, self.stored_movement[1]))
            self.player.render(self.display, offset=render_scroll)
            self.player.update(((self.movement[1] - self.movement[0]) * self.move_speed, 0), (0, self.stored_movement[1]))

            for collectible in self.collectibles:
                collectible.update()
                collectible.render(self.display, offset=render_scroll)

            for enemy in self.enemies:
                enemy.update()
                enemy.render(self.display, offset=render_scroll)
            
            self.projectiles_to_delete = []
            for projectile in self.projectiles.values():
                projectile.update()
                projectile.render(self.display, offset=render_scroll)

            for projectile in self.projectiles_to_delete:
                self.projectiles_id.remove(projectile)
                del self.projectiles[projectile]
            self.projectiles_to_delete.clear()

            self.event_handler() 
    
            self.screen.blit(py.transform.scale(self.display, self.screen.get_size()), (0, 0))
            self.update_screen()

# Handles all events and inputs
    def event_handler(self) -> None:
        # Checks if any event happens then executes code.
        for event in py.event.get():
            # Exits the program
            if event.type == py.QUIT:
                self.exit_game()

            if event.type == py.KEYDOWN:
                if event.key == py.K_ESCAPE:
                    self.exit_game()
                if event.key == py.K_TAB:
                    pass # pull up the inventory/pause menu - The number of collectibles should be shown here, the main menu should be accessible through a button and the player shouldn't be able to move the character

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
    def update_screen(self) -> None:
        py.display.flip()
        self.clock.tick(60) # limit FPS to 60 per second
        # compute delta time
        now = time.time()
        self.delta_time = (now - self.prev_time) * 60
        self.prev_time = now

    # Exits the game
    def exit_game(self) -> None:
        py.quit()
        sys.exit()

    def load_level(self, map_id=0):
        try:
            self.tilemap.load(f'data/maps/{map_id}.json')
        except FileNotFoundError:
            print("Could not find the Level File(hint: it's a json file)")
            self.exit_game()
        
        # creates list to hold all projectiles
        self.projectiles = {}
        self.projectiles_id = []

        # collectibles
        self.collectibles = []
        for collectible in self.tilemap.extract([('collectible', 0), ('collectible', 1)]):
            if collectible['variant'] == 0:
                self.collectibles.append(Collectible(self, collectible['pos'], (16, 16)))
            else: self.collectibles.append(Collectible(self, collectible['pos'], (16, 16), 1))
        
        self.enemies = []
        self.enemies_id = []
        for spawner in self.tilemap.extract([('spawner', 0), ('spawner', 1), ('spawner', 2)]):
            if spawner['variant'] == 0:
                self.player.pos = spawner['pos']
            elif spawner['variant'] == 1:
                self.enemies.append(TickEnemy(self, spawner['pos'], (16, 16)))
            elif spawner['variant'] == 2: 
                self.enemies.append(DungEnemy(self, spawner['pos'], (16, 16)))
        for spawner in self.tilemap.extract([('spawner', 3)], True):
            self.enemies.append(Mole(self, spawner['pos'], (16, 16)))
    
game = Game()
game.run()