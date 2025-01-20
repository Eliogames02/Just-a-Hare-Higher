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
        self.screen = py.display.set_mode((1920, 1080))
        self.display = py.Surface((640, 360))
        self.scale = 3

        #* create game clock
        self.clock = py.time.Clock()

        #* Main Menu Setup
        self.assets = {
            'clouds': load_images('clouds'),
            'background': load_image('Background.png'),
        }
        self.clouds = Clouds(self.assets['clouds'])

        self.volume = 100

        py.font.init()
        self.title_text = py.font.SysFont('Times New Roman', 36)
        self.text = py.font.SysFont('Times New Roman', 24)
        self.number_text = py.font.SysFont('Times New Roman', 60)

        self.main_menu = py.Surface((640,360), py.SRCALPHA)

        self.title_screen_loop = True
        self.level_loop = False
        self.settings_loop = False 
        self.win_screen_loop = False


    def run_menu(self):
        """
        This function runs the main menu loop of the game. It handles rendering the
        main menu and the menu events.

        The main menu is rendered by first drawing the background so we don't have an
        abyss. Then it renders the clouds and the menu. The menu is rendered as a
        rectangle with rounded corners. The currently selected button(rectangle) is highlighted differently
        than the other buttons.

        The menu events are handled by the menu_events function.

        The main menu loop limits the frame rate to 60 frames per second and updates
        the window at the end of each frame.
        """
        while self.title_screen_loop:
            
            # draw background so we don't have an abyss
            self.display.blit(py.transform.scale(self.assets['background'], self.display.get_size()), (0, 0))

            self.clouds.update()
            self.clouds.render(self.display)
            
            self.menu_rect = (40, 55, 560, 290)
            self.menu_radius = 50
            self.rects = {0: py.Rect((self.menu_rect[0]+15)*self.scale, (self.menu_rect[1] + self.menu_radius + 15)*self.scale, 94*self.scale, 94*self.scale),
                    1: py.Rect((self.menu_rect[0]+15*2 + 94)*self.scale, (self.menu_rect[1] + self.menu_radius + 15)*self.scale, 94*self.scale, 94*self.scale),
                    2: py.Rect((self.menu_rect[0]+15*3 + 94*2)*self.scale, (self.menu_rect[1] + self.menu_radius + 15)*self.scale, 94*self.scale, 94*self.scale),
                    3: py.Rect((self.menu_rect[0]+15*4 + 94*3)*self.scale, (self.menu_rect[1] + self.menu_radius + 15)*self.scale, 94*self.scale, 94*self.scale),
                    4: py.Rect((self.menu_rect[0]+15*5 + 94*4)*self.scale, (self.menu_rect[1] + self.menu_radius + 15)*self.scale, 94*self.scale, 94*self.scale), 
                    'settings': py.Rect((self.menu_rect[0] + 15)*self.scale, (self.menu_rect[1] + self.menu_radius + 124)*self.scale, 203*self.scale, 94*self.scale),
                    'exit': py.Rect((self.menu_rect[0] + 342)*self.scale, (self.menu_rect[1] + self.menu_radius + 124)*self.scale, 203*self.scale, 94*self.scale),
                    5: py.Rect((self.menu_rect[0] + 15)*self.scale, (self.menu_rect[1] + self.menu_radius + 15)*self.scale, 161*self.scale, 94*self.scale),
                    6: py.Rect((self.menu_rect[0] + 15 + 161 + 15)*self.scale, (self.menu_rect[1] + self.menu_radius + 15)*self.scale, 161*self.scale, 94*self.scale),
                    7: py.Rect((self.menu_rect[0] + 15*2 + 161*2 + 15)*self.scale, (self.menu_rect[1] + self.menu_radius + 15)*self.scale, 161*self.scale, 94*self.scale),
                    }
            
            # draw the background of the menu
            py.draw.rect(self.main_menu, (255, 255, 255, 150), self.menu_rect, 0, self.menu_radius)
            py.draw.rect(self.main_menu, (0, 0, 0, 150), self.menu_rect, 4, self.menu_radius)
            py.draw.line(self.main_menu, (150, 150, 150, 150), (self.menu_rect[0]+4, self.menu_rect[1] + self.menu_radius), (self.menu_rect[0] + self.menu_rect[2]-5, self.menu_rect[1] + self.menu_radius))
                
            # draw the level "buttons" 
            for i in range(5):
                py.draw.rect(self.main_menu, (150, 150, 150, 150), (self.menu_rect[0] + i*94 +15*(i+1), self.menu_rect[1] + self.menu_radius + 15, 94, 94), 0, 25)
                py.draw.rect(self.main_menu, (0, 0, 0, 150), (self.menu_rect[0] + i*94 +15*(i+1), self.menu_rect[1] + self.menu_radius + 15, 94, 94), 2, 25)
        
            # draw the text for the level "buttons"
            for i in range(5):
                self.main_menu.blit(py.font.Font.render(self.number_text, str(i+1), True, (0, 0, 0, 150)), ((self.menu_rect[0] + i*94 +15*(i+1) + 28, self.menu_rect[1] + self.menu_radius + 28)))
            
            # draw the current level "button" differently
            if py.Rect((self.menu_rect[0] + 15)*self.scale, (self.menu_rect[1] + self.menu_radius + 15)*self.scale, 530*self.scale, 94*self.scale).collidepoint(py.mouse.get_pos()):
                # draw the menu "buttons"
                for i in range(5):
                    if self.rects[i].collidepoint(py.mouse.get_pos()):
                        py.draw.rect(self.display, (150, 150, 150, 150), (self.menu_rect[0] + i*94 +15*(i+1), self.menu_rect[1] + self.menu_radius + 15, 94, 94), 0, 25)
                        py.draw.rect(self.display, (0, 0, 0, 150), (self.menu_rect[0] + i*94 +15*(i+1), self.menu_rect[1] + self.menu_radius + 15, 94, 94), 2, 25)
            
                # draw the text for the menu "buttons"
                for i in range(5):
                    if self.rects[i].collidepoint(py.mouse.get_pos()):
                        self.display.blit(py.font.Font.render(self.number_text, str(i+1), True, (0, 0, 0, 150)), ((self.menu_rect[0] + i*94 +15*(i+1) + 28, self.menu_rect[1] + self.menu_radius + 28)))
            
            # draw the settings "button"
            py.draw.rect(self.main_menu, (150, 150, 150, 150), (self.menu_rect[0] + 15, self.menu_rect[1] + self.menu_radius + 124, 203, 94), 0, 25)
            py.draw.rect(self.main_menu, (0, 0, 0, 150), (self.menu_rect[0] + 15, self.menu_rect[1] + self.menu_radius + 124, 203, 94), 2, 25)
            self.main_menu.blit(py.font.Font.render(self.title_text, 'Settings', True, (0, 0, 0, 150)), ((self.menu_rect[0] + 52, self.menu_rect[1] + self.menu_radius + 145)))
            if py.Rect((self.menu_rect[0] + 15)*self.scale, (self.menu_rect[1] + self.menu_radius + 124)*self.scale, 203*self.scale, 94*self.scale).collidepoint(py.mouse.get_pos()):
                py.draw.rect(self.display, (150, 150, 150, 150), (self.menu_rect[0] + 15, self.menu_rect[1] + self.menu_radius + 124, 203, 94), 0, 25)
                py.draw.rect(self.display, (0, 0, 0, 150), (self.menu_rect[0] + 15, self.menu_rect[1] + self.menu_radius + 124, 203, 94), 2, 25)
                self.display.blit(py.font.Font.render(self.title_text, 'Settings', True, (0, 0, 0)), ((self.menu_rect[0] + 52, self.menu_rect[1] + self.menu_radius + 145)))
            
            # draw the exit "button"
            py.draw.rect(self.main_menu, (150, 150, 150, 150), (self.menu_rect[0] + 342, self.menu_rect[1] + self.menu_radius + 124, 203, 94), 0, 25)
            py.draw.rect(self.main_menu, (0, 0, 0, 150), (self.menu_rect[0] + 342, self.menu_rect[1] + self.menu_radius + 124, 203, 94), 2, 25)
            self.main_menu.blit(py.font.Font.render(self.title_text, 'Exit', True, (0, 0, 0, 150)), ((self.menu_rect[0] + 409, self.menu_rect[1] + self.menu_radius + 145)))
            if py.Rect((self.menu_rect[0] + 342)*self.scale, (self.menu_rect[1] + self.menu_radius + 124)*self.scale, 203*self.scale, 94*self.scale).collidepoint(py.mouse.get_pos()):
                py.draw.rect(self.display, (150, 150, 150, 150), (self.menu_rect[0] + 342, self.menu_rect[1] + self.menu_radius + 124, 203, 94), 0, 25)
                py.draw.rect(self.display, (0, 0, 0, 150), (self.menu_rect[0] + 342, self.menu_rect[1] + self.menu_radius + 124, 203, 94), 2, 25)
                self.display.blit(py.font.Font.render(self.title_text, 'Exit', True, (0, 0, 0)), ((self.menu_rect[0] + 409, self.menu_rect[1] + self.menu_radius + 145)))
            
            self.display.blit(self.main_menu, (0,0))
            self.display.blit(py.font.Font.render(self.title_text, "Just A Hare Higher", True, 'black'), (self.menu_rect[0]+142, self.menu_rect[1]+5))

            # draw my logo
            self.logo = py.image.load('data/images/Logo.png').convert_alpha()
            self.display.blit(self.logo, (self.menu_rect[0] + 245, self.menu_rect[1] + self.menu_radius + 140))

            self.menu_events()

            # update the window
            self.screen.blit(py.transform.scale(self.display, self.screen.get_size()), (0, 0)) # scales the diplay to the screen size
            py.display.flip()
            self.clock.tick(60) # limit FPS to 60 per second
        
    def menu_events(self):

        for event in py.event.get():
            if event.type == py.QUIT:
                self.exit_game()

            if event.type == py.KEYDOWN:
                if event.key == py.K_ESCAPE:
                    self.exit_game()

            if event.type == py.MOUSEBUTTONDOWN and (self.settings_loop == False and self.win_screen_loop == False):
                if self.rects[0].collidepoint(py.mouse.get_pos()):
                    self.setup_level(1)
                if self.rects[1].collidepoint(py.mouse.get_pos()):
                    self.setup_level(2)
                if self.rects[2].collidepoint(py.mouse.get_pos()):
                    self.setup_level(3)
                if self.rects[3].collidepoint(py.mouse.get_pos()):
                    self.setup_level(4)
                if self.rects[4].collidepoint(py.mouse.get_pos()):
                    self.setup_level(5)
                if self.rects['settings'].collidepoint(py.mouse.get_pos()):
                    self.settings_menu()
                if self.rects['exit'].collidepoint(py.mouse.get_pos()):
                    self.exit_game()

            if event.type == py.MOUSEBUTTONDOWN and self.settings_loop == True:
                if self.rects[5].collidepoint(py.mouse.get_pos()):
                    self.screen = py.display.set_mode((640, 360)) 
                    self.scale = 1
                if self.rects[6].collidepoint(py.mouse.get_pos()):
                    self.screen = py.display.set_mode((1280, 720)) 
                    self.scale = 2
                if self.rects[7].collidepoint(py.mouse.get_pos()):
                    self.screen = py.display.set_mode((1920, 1080-64)) 
                    self.scale = 3
                if self.rects['settings'].collidepoint(py.mouse.get_pos()):
                    self.volume += 10
                    if self.volume > 100:
                        self.volume = 0
                    py.mixer.music.set_volume(self.volume)
                if self.rects['exit'].collidepoint(py.mouse.get_pos()):
                    self.title_screen_loop = True

            if event.type == py.MOUSEBUTTONDOWN and self.win_screen_loop == True:
                if self.rects['exit'].collidepoint(py.mouse.get_pos()):
                    self.title_screen_loop = True
                    

    def settings_menu(self):
        """
        This function runs the settings menu loop of the game. It handles rendering the
        settings menu and its events.

        The settings menu is rendered by first drawing the background and clouds, then
        drawing the menu with options for screen resolution, volume control, and
        returning to the main menu.

        The settings menu events are handled by the menu_events function, allowing the
        user to interact with the options. The display is updated at the end of each
        frame to show any changes.

        The loop continues until the user decides to return to the main menu, at which
        point it calls run_menu to transition back.
        """
        self.title_screen_loop = False
        self.settings_loop = True
        while self.settings_loop:
            if self.title_screen_loop == True:
                self.settings_loop = False
                self.run_menu()
            self.display.blit(py.transform.scale(self.assets['background'], self.display.get_size()), (0, 0))

            self.clouds.update()
            self.clouds.render(self.display)

            self.rects = {0: py.Rect((self.menu_rect[0]+15)*self.scale, (self.menu_rect[1] + self.menu_radius + 15)*self.scale, 94*self.scale, 94*self.scale),
                    1: py.Rect((self.menu_rect[0]+15*2 + 94)*self.scale, (self.menu_rect[1] + self.menu_radius + 15)*self.scale, 94*self.scale, 94*self.scale),
                    2: py.Rect((self.menu_rect[0]+15*3 + 94*2)*self.scale, (self.menu_rect[1] + self.menu_radius + 15)*self.scale, 94*self.scale, 94*self.scale),
                    3: py.Rect((self.menu_rect[0]+15*4 + 94*3)*self.scale, (self.menu_rect[1] + self.menu_radius + 15)*self.scale, 94*self.scale, 94*self.scale),
                    4: py.Rect((self.menu_rect[0]+15*5 + 94*4)*self.scale, (self.menu_rect[1] + self.menu_radius + 15)*self.scale, 94*self.scale, 94*self.scale), 
                    'settings': py.Rect((self.menu_rect[0] + 15)*self.scale, (self.menu_rect[1] + self.menu_radius + 124)*self.scale, 203*self.scale, 94*self.scale),
                    'exit': py.Rect((self.menu_rect[0] + 342)*self.scale, (self.menu_rect[1] + self.menu_radius + 124)*self.scale, 203*self.scale, 94*self.scale),
                    5: py.Rect((self.menu_rect[0] + 15)*self.scale, (self.menu_rect[1] + self.menu_radius + 15)*self.scale, 161*self.scale, 94*self.scale),
                    6: py.Rect((self.menu_rect[0] + 15 + 161 + 15)*self.scale, (self.menu_rect[1] + self.menu_radius + 15)*self.scale, 161*self.scale, 94*self.scale),
                    7: py.Rect((self.menu_rect[0] + 15*2 + 161*2 + 15)*self.scale, (self.menu_rect[1] + self.menu_radius + 15)*self.scale, 161*self.scale, 94*self.scale),
                    }
            
            # draw the background of the menu
            py.draw.rect(self.main_menu, (255, 255, 255, 150), self.menu_rect, 0, self.menu_radius)
            py.draw.rect(self.main_menu, (0, 0, 0, 150), self.menu_rect, 4, self.menu_radius)
            py.draw.line(self.main_menu, (150, 150, 150, 150), (self.menu_rect[0]+4, self.menu_rect[1] + self.menu_radius), (self.menu_rect[0] + self.menu_rect[2]-5, self.menu_rect[1] + self.menu_radius))
            
            # draw the resolutions
            for i in range(3):
                py.draw.rect(self.main_menu, (150, 150, 150, 150), (self.menu_rect[0] + 15*i + 161*i + 15, self.menu_rect[1] + self.menu_radius + 15, 161, 94), 0, 25)
                py.draw.rect(self.main_menu, (0, 0, 0, 150), (self.menu_rect[0] + 15*i + 161*i + 15, self.menu_rect[1] + self.menu_radius + 15, 161, 94), 2, 25)
                self.main_menu.blit(py.font.Font.render(self.title_text, str(640*(i+1))+'x'+str(360*(i+1)), True, (0, 0, 0, 150)), ((self.menu_rect[0] + 15*i + 150*i + 35, self.menu_rect[1] + self.menu_radius + 35)))
            if py.Rect((self.menu_rect[0] + 15)*self.scale, (self.menu_rect[1] + self.menu_radius + 15)*self.scale, 530*self.scale, 94*self.scale).collidepoint(py.mouse.get_pos()):
                for i in range(3):
                    if self.rects[i+5].collidepoint(py.mouse.get_pos()):
                        py.draw.rect(self.display, (150, 150, 150, 150), (self.menu_rect[0] + 15*i + 161*i + 15, self.menu_rect[1] + self.menu_radius + 15, 161, 94), 0, 25)
                        py.draw.rect(self.display, (0, 0, 0, 150), (self.menu_rect[0] + 15*i + 161*i + 15, self.menu_rect[1] + self.menu_radius + 15, 161, 94), 2, 25)
                        self.display.blit(py.font.Font.render(self.title_text, str(640*(i+1))+'x'+str(360*(i+1)), True, (0, 0, 0, 150)), ((self.menu_rect[0] + 15*i + 150*i + 35, self.menu_rect[1] + self.menu_radius + 35)))

            # draw the volume editor
            py.draw.rect(self.main_menu, (150, 150, 150, 150), (self.menu_rect[0] + 15, self.menu_rect[1] + self.menu_radius + 124, 203, 94), 0, 25)
            py.draw.rect(self.main_menu, (0, 0, 0, 150), (self.menu_rect[0] + 15, self.menu_rect[1] + self.menu_radius + 124, 203, 94), 2, 25)
            self.main_menu.blit(py.font.Font.render(self.title_text, 'Volume: '+str(self.volume), True, (0, 0, 0, 150)), ((self.menu_rect[0] + 25, self.menu_rect[1] + self.menu_radius + 145)))
            if py.Rect((self.menu_rect[0] + 15)*self.scale, (self.menu_rect[1] + self.menu_radius + 124)*self.scale, 203*self.scale, 94*self.scale).collidepoint(py.mouse.get_pos()):
                py.draw.rect(self.display, (150, 150, 150, 150), (self.menu_rect[0] + 15, self.menu_rect[1] + self.menu_radius + 124, 203, 94), 0, 25)
                py.draw.rect(self.display, (0, 0, 0, 150), (self.menu_rect[0] + 15, self.menu_rect[1] + self.menu_radius + 124, 203, 94), 2, 25)

            # draw the return to main menu "button"
            py.draw.rect(self.main_menu, (150, 150, 150, 150), (self.menu_rect[0] + 342, self.menu_rect[1] + self.menu_radius + 124, 203, 94), 0, 25)
            py.draw.rect(self.main_menu, (0, 0, 0, 150), (self.menu_rect[0] + 342, self.menu_rect[1] + self.menu_radius + 124, 203, 94), 2, 25)
            self.main_menu.blit(py.font.Font.render(self.title_text, 'Main Menu', True, (0, 0, 0, 150)), ((self.menu_rect[0] + 365, self.menu_rect[1] + self.menu_radius + 145)))
            if py.Rect((self.menu_rect[0] + 342)*self.scale, (self.menu_rect[1] + self.menu_radius + 124)*self.scale, 203*self.scale, 94*self.scale).collidepoint(py.mouse.get_pos()):
                py.draw.rect(self.display, (150, 150, 150, 150), (self.menu_rect[0] + 342, self.menu_rect[1] + self.menu_radius + 124, 203, 94), 0, 25)
                py.draw.rect(self.display, (0, 0, 0, 150), (self.menu_rect[0] + 342, self.menu_rect[1] + self.menu_radius + 124, 203, 94), 2, 25)
                self.display.blit(py.font.Font.render(self.title_text, 'Main Menu', True, (0, 0, 0)), ((self.menu_rect[0] + 365, self.menu_rect[1] + self.menu_radius + 145)))

            self.display.blit(self.main_menu, (0,0))
            self.display.blit(py.font.Font.render(self.title_text, "Settings", True, 'black'), (self.menu_rect[0]+215, self.menu_rect[1]+5))

            self.display.blit(self.logo, (self.menu_rect[0] + 245, self.menu_rect[1] + self.menu_radius + 140))

            self.menu_events()

            # update the window
            self.screen.blit(py.transform.scale(self.display, self.screen.get_size()), (0, 0)) # scales the diplay to the screen size
            py.display.flip()
            self.clock.tick(60) # limit FPS to 60 per second

    def setup_level(self, level: int) -> None:
        self.title_screen_loop = False
        self.level_loop = True
        
        #* assets of the game
        self.assets = {
            'player': load_image('entities/player/player_test.png'),
            'dirt': load_images('tiles/dirt'),
            'empty_dirt': load_images('tiles/empty_dirt'),
            'clouds': load_images('clouds'),
            'background': load_image('Background.png'),
            'collectible/carrot': Animation(load_images('tiles/collectible/carrot')),
            'collectible/radish': Animation(load_images('tiles/collectible/radish')),
            'collectible/finish': Animation(load_images('tiles/collectible/z_finish')),
            'player/idle': Animation(load_images('entities/player')),
            'tick_enemy/idle': Animation(load_images('entities/tick_enemy')),
            'dung_enemy/idle': Animation(load_images('entities/dung_enemy')),
            'projectile/idle': Animation(load_images('entities/projectiles')),
        }

        #* Assemble the level
        self.tilemap = Tilemap(self)
        self.clouds = Clouds(self.assets['clouds'])
        self.player = Player(self, (100, 200), (16, 16))
        self.load_level(level)
        self.scroll = [self.player.pos[0] - self.display.get_width()/2, self.player.pos[1] - self.display.get_height()/2]

        #* Player variables
        global jump, jump_time
        jump = False
        jump_time = 0
        self.move_speed = 2

        #* Score variables
        self.score = 0 # for carrots
        self.super_score = 0 # for radishes

        self.run_level()

    #* game loop
    def run_level(self) -> None:
        global jump, jump_time

        while self.level_loop:
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

            self.player_input() # handles player inputs

            if jump == True:
                jump_time = min(10, max(4, jump_time + 1/20))

            # updates the window
            self.screen.blit(py.transform.scale(self.display, self.screen.get_size()), (0, 0))
            py.display.flip()
            self.clock.tick(60) # limit FPS to 60 per second
        
    def player_input(self) -> None:
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
                if event.key == py.K_m:
                    self.end_level()

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
        for collectible in self.tilemap.extract([('collectible', 0), ('collectible', 1), ('collectible', 2)]):
            if collectible['variant'] == 0:
                self.collectibles.append(Collectible(self, collectible['pos'], (16, 16)))
            elif collectible['variant'] == 1:
                self.collectibles.append(Collectible(self, collectible['pos'], (16, 16), 1))
            else: self.collectibles.append(Collectible(self, collectible['pos'], (16, 16), 2))
        
        #* enemies
        self.enemies = []
        self.enemies_id = []
        for spawner in self.tilemap.extract([('spawner', 0), ('spawner', 1), ('spawner', 2)]):
            if spawner['variant'] == 0:
                self.player.pos = spawner['pos']
            elif spawner['variant'] == 1:
                self.enemies.append(TickEnemy(self, spawner['pos'], (16, 16)))
            else: self.enemies.append(DungEnemy(self, spawner['pos'], (16, 16)))
    
    def end_level(self) -> None:
        """
        Ends the current level and starts the win screen loop.
        
        This function sets level_loop to False and win_screen_loop to True, 
        then calls the win_menu function to start the win screen loop. 
        It also sets title_screen_loop to True and calls the run_menu function to start the main menu loop.
        
        :return: None
        """
        self.level_loop = False 
        self.win_screen_loop = True
        self.win_menu()
        self.run_menu()
    
    def win_menu(self):
        while self.win_screen_loop:
            
            self.display.blit(py.transform.scale(self.assets['background'], self.display.get_size()), (0, 0))

            self.clouds.update()
            self.clouds.render(self.display)

            self.rects = {0: py.Rect((self.menu_rect[0]+15)*self.scale, (self.menu_rect[1] + self.menu_radius + 15)*self.scale, 94*self.scale, 94*self.scale),
                    1: py.Rect((self.menu_rect[0]+15*2 + 94)*self.scale, (self.menu_rect[1] + self.menu_radius + 15)*self.scale, 94*self.scale, 94*self.scale),
                    2: py.Rect((self.menu_rect[0]+15*3 + 94*2)*self.scale, (self.menu_rect[1] + self.menu_radius + 15)*self.scale, 94*self.scale, 94*self.scale),
                    3: py.Rect((self.menu_rect[0]+15*4 + 94*3)*self.scale, (self.menu_rect[1] + self.menu_radius + 15)*self.scale, 94*self.scale, 94*self.scale),
                    4: py.Rect((self.menu_rect[0]+15*5 + 94*4)*self.scale, (self.menu_rect[1] + self.menu_radius + 15)*self.scale, 94*self.scale, 94*self.scale), 
                    'settings': py.Rect((self.menu_rect[0] + 15)*self.scale, (self.menu_rect[1] + self.menu_radius + 124)*self.scale, 203*self.scale, 94*self.scale),
                    'exit': py.Rect((self.menu_rect[0] + 342)*self.scale, (self.menu_rect[1] + self.menu_radius + 124)*self.scale, 203*self.scale, 94*self.scale),
                    5: py.Rect((self.menu_rect[0] + 15)*self.scale, (self.menu_rect[1] + self.menu_radius + 15)*self.scale, 161*self.scale, 94*self.scale),
                    6: py.Rect((self.menu_rect[0] + 15 + 161 + 15)*self.scale, (self.menu_rect[1] + self.menu_radius + 15)*self.scale, 161*self.scale, 94*self.scale),
                    7: py.Rect((self.menu_rect[0] + 15*2 + 161*2 + 15)*self.scale, (self.menu_rect[1] + self.menu_radius + 15)*self.scale, 161*self.scale, 94*self.scale),
                    }
            
            # draw the background of the menu
            py.draw.rect(self.main_menu, (255, 255, 255, 150), self.menu_rect, 0, self.menu_radius)
            py.draw.rect(self.main_menu, (0, 0, 0, 150), self.menu_rect, 4, self.menu_radius)
            py.draw.line(self.main_menu, (150, 150, 150, 150), (self.menu_rect[0]+4, self.menu_rect[1] + self.menu_radius), (self.menu_rect[0] + self.menu_rect[2]-5, self.menu_rect[1] + self.menu_radius))

            # draw the return to main menu "button"
            py.draw.rect(self.main_menu, (150, 150, 150, 150), (self.menu_rect[0] + 342, self.menu_rect[1] + self.menu_radius + 124, 203, 94), 0, 25)
            py.draw.rect(self.main_menu, (0, 0, 0, 150), (self.menu_rect[0] + 342, self.menu_rect[1] + self.menu_radius + 124, 203, 94), 2, 25)
            self.main_menu.blit(py.font.Font.render(self.title_text, 'Return to', True, (0, 0, 0, 150)), ((self.menu_rect[0] + 365, self.menu_rect[1] + self.menu_radius + 125)))
            self.main_menu.blit(py.font.Font.render(self.title_text, 'Main Menu', True, (0, 0, 0, 150)), ((self.menu_rect[0] + 365, self.menu_rect[1] + self.menu_radius + 165)))
            if py.Rect((self.menu_rect[0] + 342)*self.scale, (self.menu_rect[1] + self.menu_radius + 124)*self.scale, 203*self.scale, 94*self.scale).collidepoint(py.mouse.get_pos()):
                py.draw.rect(self.display, (150, 150, 150, 150), (self.menu_rect[0] + 342, self.menu_rect[1] + self.menu_radius + 124, 203, 94), 0, 25)
                py.draw.rect(self.display, (0, 0, 0, 150), (self.menu_rect[0] + 342, self.menu_rect[1] + self.menu_radius + 124, 203, 94), 2, 25)
                self.display.blit(py.font.Font.render(self.title_text, 'Return to', True, (0, 0, 0, 150)), ((self.menu_rect[0] + 365, self.menu_rect[1] + self.menu_radius + 125)))
                self.display.blit(py.font.Font.render(self.title_text, 'Main Menu', True, (0, 0, 0, 150)), ((self.menu_rect[0] + 365, self.menu_rect[1] + self.menu_radius + 165)))

            self.display.blit(self.main_menu, (0,0))
            self.display.blit(py.font.Font.render(self.title_text, "YOU WIN", True, 'black'), (self.menu_rect[0]+200, self.menu_rect[1]+5))
            
            self.display.blit(py.font.Font.render(self.title_text, f"Carrots: {self.score}", True, 'black'), (self.menu_rect[0]+55, self.menu_rect[1]+self.menu_radius+35))
            self.display.blit(py.font.Font.render(self.title_text, f"Radishes: {self.super_score}", True, 'black'), (self.menu_rect[0]+55, self.menu_rect[1]+self.menu_radius+95))
            self.display.blit(py.font.Font.render(self.title_text, f"Score: {self.score*10 + self.super_score*100}", True, 'black'), (self.menu_rect[0]+55, self.menu_rect[1]+self.menu_radius+155))

            self.menu_events()

            if self.title_screen_loop:
                self.win_screen_loop = False

            # update the window
            self.screen.blit(py.transform.scale(self.display, self.screen.get_size()), (0, 0)) # scales the diplay to the screen size
            py.display.flip()
            self.clock.tick(60) # limit FPS to 60 per second

    def exit_game(self) -> None:
        """
        Exits the game cleanly.

        Prints out the player's score to the console and then closes the pygame window and exits the game.

        :return: None
        """
        try:
            print(f"Thanks for playing!\n\nCarrots Collected: {self.score}\nRadishes Collected: {self.super_score}")
        except AttributeError:
            pass
        py.quit()
        sys.exit()

game = Game()
game.run_menu()