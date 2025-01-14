import pygame as py
import sys, time
from scripts.entities import *
from scripts.tilemap import Tilemap
from scripts.utils import load_image, load_images, Animation
from scripts.clouds import Clouds


class Game:
    def __init__(self):
        #* initialize pygame
        py.init()

        #* create game window
        py.display.set_caption("Just a Hare Higher")
        self.screen = py.display.set_mode((py.display.get_desktop_sizes()[0][0], py.display.get_desktop_sizes()[0][1] - 32))
        self.display = py.Surface((640, 360))

        #* create game clock
        self.clock = py.time.Clock()

        #* assets of the game
        self.assets = {
            'player': load_image('entities/player/player_test.png'),
            'dirt': load_images('tiles/dirt'),
            'empty_dirt': load_images('tiles/empty_dirt'),
            'clouds': load_images('clouds'),
            'background': load_image('Background.png'),
            'collectible/carrot': Animation(load_images('tiles/collectible/carrot')),
            'collectible/radish': Animation(load_images('tiles/collectible/radish')),
            'player/idle': Animation(load_images('entities/player')),
            'tick_enemy/idle': Animation(load_images('entities/tick_enemy')),
            'dung_enemy/idle': Animation(load_images('entities/dung_enemy')),
            'projectile/idle': Animation(load_images('entities/projectiles')),
        }

        #* Assemble the level
        self.tilemap = Tilemap(self)
        self.clouds = Clouds(self.assets['clouds'])
        self.player = Player(self, (100, 200), (16, 16))
        self.load_level()
        self.scroll = [self.player.pos[0] - self.display.get_width()/2, self.player.pos[1] - self.display.get_height()/2]

        #* Player variables
        global jump, jump_time
        jump = False
        jump_time = 0
        self.move_speed = 2

        #* Score variables
        self.score = 0 # for carrots
        self.super_score = 0 # for radishes

    #* game loop
    def run(self) -> None:
        global jump, jump_time

        while True:
            self.display.blit(py.transform.scale(self.assets['background'], self.display.get_size()), (0, 0))

            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() /2 - self.scroll[0]) / 30
            self.scroll[1] += (self.player.rect().centery - self.display.get_height() /2 - self.scroll[1]) / 12
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            self.clouds.update()
            self.clouds.render(self.display, offset=render_scroll)
 
            self.tilemap.render(self.display, offset=render_scroll)

            self.player.update()
            self.player.render(self.display, offset=render_scroll)
            self.player.update()

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

            #* handle events
            self.events()

            if jump == True:
                jump_time = min(10, max(4, jump_time + 1/20))

            #* update the window
            self.screen.blit(py.transform.scale(self.display, self.screen.get_size()), (0, 0))
            py.display.flip()
            self.clock.tick(60) # limit FPS to 60 per second
        
    def events(self) -> None:
        global jump, jump_time

        for event in py.event.get():
            if event.type == py.QUIT:
                self.exit_game()

            if event.type == py.KEYDOWN:
                if event.key == py.K_ESCAPE:
                    self.exit_game()
                if event.key == py.K_LEFT or event.key == py.K_a:
                    # move player left 
                    self.player.velocity[0] -= self.move_speed
                if event.key == py.K_RIGHT or event.key == py.K_d:
                    # move player right
                    self.player.velocity[0] += self.move_speed
                if event.key == py.K_UP or event.key == py.K_w:
                    # start charging the player's jump
                    jump = True

            if event.type == py.KEYUP:
                if event.key == py.K_LEFT or event.key == py.K_a:
                    # stop moving player left
                    self.player.velocity[0] += self.move_speed
                if event.key == py.K_RIGHT or event.key == py.K_d:
                    # stop moving player right
                    self.player.velocity[0] -= self.move_speed
                if event.key == py.K_UP or event.key == py.K_w:
                    # make the player jump
                    if self.player.jumps > 0:
                        self.player.velocity[1] -= (jump_time)
                    jump_time = 0
                    jump = False

    def load_level(self, map_id=0) -> None:
        try:
            self.tilemap.load(f'data/maps/{map_id}.json')
        except FileNotFoundError:
            print("Could not find the Level File(hint: it's a json file)")
            self.exit_game()
        
        #* creates list to hold all projectiles
        self.projectiles = {}
        self.projectiles_id = []

        #* collectibles
        self.collectibles = []
        for collectible in self.tilemap.extract([('collectible', 0), ('collectible', 1)]):
            if collectible['variant'] == 0:
                self.collectibles.append(Collectible(self, collectible['pos'], (16, 16)))
            else: self.collectibles.append(Collectible(self, collectible['pos'], (16, 16), 1))
        
        #* enemies
        self.enemies = []
        self.enemies_id = []
        for spawner in self.tilemap.extract([('spawner', 0), ('spawner', 1), ('spawner', 2)]):
            if spawner['variant'] == 0:
                self.player.pos = spawner['pos']
            elif spawner['variant'] == 1:
                self.enemies.append(TickEnemy(self, spawner['pos'], (16, 16)))
            else: self.enemies.append(DungEnemy(self, spawner['pos'], (16, 16)))
    
    def exit_game(self) -> None:
        print(f"Thanks for playing!\n\nCarrots Collected: {self.score}\nRadishes Collected: {self.super_score}")
        py.quit()
        sys.exit()

game = Game()
game.run()