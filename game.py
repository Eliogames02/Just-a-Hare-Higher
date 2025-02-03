import pygame as py
import sys, time, json
from scripts.entities import *
from scripts.tilemap import Tilemap
from scripts.utils import load_image, load_images, Animation
from scripts.clouds import Clouds


class Game:
    def __init__(self):
        """
        Initializes the Game class, setting up the pygame environment and creating a game window, clock, and assets.

        This constructor initializes the pygame library, sets up the display window and title, prepares the clock for frame rate control,
        and initializes game assets such as images for clouds and the background. It also sets up the game volume, font for rendering text,
        and main menu surface. Additionally, it initializes the game's loop states and sets up the levels dictionary.

        Attributes:
            screen (pygame.Surface): The main display surface for the game.
            display (pygame.Surface): A secondary surface for rendering the game's content.
            scale (int): The scale factor for the game window.
            clock (pygame.time.Clock): Used to control the frame rate of the game.
            assets (dict): A dictionary containing loaded images for clouds and the background.
            clouds (Clouds): The clouds instance used in the game.
            volume (int): The game's current volume.
            title_text (pygame.font.Font): The font used for rendering title text.
            text (pygame.font.Font): The font used for rendering normal text.
            number_text (pygame.font.Font): The font used for rendering large numbers.
            main_menu (pygame.Surface): The main menu surface.
            title_screen_loop (bool): A flag indicating if the title screen is to be displayed.
            level_loop (bool): A flag indicating if the level is to be displayed.
            settings_loop (bool): A flag indicating if the settings menu is to be displayed.
            win_screen_loop (bool): A flag indicating if the win screen is to be displayed.
            current_level (int): The current level being played.
            levels (dict): A dictionary containing the levels and their completion status.
        """
        py.init()

        # create game window
        py.display.set_caption("Just a Hare Higher")
        self.screen = py.display.set_mode((1920, 1080))
        self.display = py.Surface((640, 360))
        self.scale = 3

        self.clock = py.time.Clock()

        # Main Menu Setup
        self.assets = {
            'clouds': load_images('clouds'),
            'background': load_image('Background.png'),
        }
        self.clouds = Clouds(self.assets['clouds'])

        self.volume = 100

        py.font.init()
        self.title_text = py.font.SysFont('Times New Roman', 36)
        self.normal_text = py.font.SysFont('Times New Roman', 24)
        self.menu_text = py.font.SysFont('Times New Roman', 18)
        self.smol_text = py.font.SysFont('Times New Roman', 14)
        self.number_text = py.font.SysFont('Times New Roman', 60)

        self.main_menu = py.Surface((640,360), py.SRCALPHA)

        self.title_screen_loop = True
        self.level_loop = False
        self.settings_loop = False 
        self.win_screen_loop = False

        self.current_level = 1
        self.levels = {0: {'Completed': True}}

    def run_menu(self):
        """
        The main menu loop for the game. This function is responsible for drawing the title screen, checking for events,
        and updating the game window. It also loads the levels and their completion status, and sets up the main menu surface.
        
        Attributes:
            main_menu (pygame.Surface): The main menu surface.
            menu_rect (tuple): The rectangle coordinates for the main menu.
            menu_radius (int): The radius of the main menu.
            rects (dict): A dictionary containing the rectangles for the level "buttons" and the settings and exit "buttons".
        """
        for i in range(1, 6):
            self.load(i)
        self.high_scores = {1: [self.levels[1]['Carrots'], self.levels[1]['Radishes'], self.levels[1]['Score']], 
                            2: [self.levels[2]['Carrots'], self.levels[2]['Radishes'], self.levels[2]['Score']], 
                            3: [self.levels[3]['Carrots'], self.levels[3]['Radishes'], self.levels[3]['Score']], 
                            4: [self.levels[4]['Carrots'], self.levels[4]['Radishes'], self.levels[4]['Score']], 
                            5: [self.levels[5]['Carrots'], self.levels[5]['Radishes'], self.levels[5]['Score']]}
        
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
                    'wipe': py.Rect((self.menu_rect[0] + 342)*self.scale, (self.menu_rect[1] + 3)*self.scale, 150*self.scale, 47*self.scale)
                    }
            
            # draw the background of the menu
            py.draw.rect(self.main_menu, (255, 255, 255, 150), self.menu_rect, 0, self.menu_radius)
            py.draw.rect(self.main_menu, (0, 0, 0, 150), self.menu_rect, 4, self.menu_radius)
            py.draw.line(self.main_menu, (150, 150, 150, 150), (self.menu_rect[0]+4, self.menu_rect[1] + self.menu_radius), (self.menu_rect[0] + self.menu_rect[2]-5, self.menu_rect[1] + self.menu_radius))
                
            # draw the level "buttons" 
            for i in range(5):
                py.draw.rect(self.main_menu, (150, 150, 150, 150), (self.menu_rect[0] + i*94 +15*(i+1), self.menu_rect[1] + self.menu_radius + 5, 94, 63), 0, 25)
                py.draw.rect(self.main_menu, (0, 0, 0, 150), (self.menu_rect[0] + i*94 +15*(i+1), self.menu_rect[1] + self.menu_radius + 5, 94, 63), 2, 25)
                
            # draw the text for the level "buttons"
            for i in range(5):
                self.main_menu.blit(py.font.Font.render(self.number_text, str(i+1), True, (0, 0, 0, 150)), ((self.menu_rect[0] + i*94 +15*(i+1) + 28, self.menu_rect[1] + self.menu_radius + 4)))
                if self.levels[i]['Completed'] == False:
                    py.draw.line(self.main_menu, (150, 0, 0), (self.menu_rect[0] + i*94 +15*(i+1), self.menu_rect[1] + self.menu_radius + 5), (self.menu_rect[0] + i*94 +15*(i+1) + 94, self.menu_rect[1] + self.menu_radius + 5 + 63), 2)
                    py.draw.line(self.main_menu, (150, 0, 0), (self.menu_rect[0] + i*94 +15*(i+1) + 94, self.menu_rect[1] + self.menu_radius + 5), (self.menu_rect[0] + i*94 +15*(i+1), self.menu_rect[1] + self.menu_radius + 5 + 63), 2)

            self.main_menu.blit(py.font.Font.render(self.smol_text, 'High Scores', True, (0, 0, 0, 150)), ((self.menu_rect[0] + 5, self.menu_rect[1] + self.menu_radius + 70)))
            self.main_menu.blit(py.font.Font.render(self.smol_text, 'Fastest Times', True, (0, 0, 0, 150)), ((self.menu_rect[0] + 5, self.menu_rect[1] + self.menu_radius + 90)))

            for i in range(5):
                self.main_menu.blit(py.font.Font.render(self.menu_text, str(self.high_scores[i+1][2]), True, (0, 0, 0, 150)), ((self.menu_rect[0] + i*94 +15*(i+1) + 60, self.menu_rect[1] + self.menu_radius + 70)))
            
            for i in range(5):
                if self.levels[i+1]['Time'] == '99:59:59':
                    self.main_menu.blit(py.font.Font.render(self.menu_text, 'N/A', True, (0, 0, 0, 150)), ((self.menu_rect[0] + i*94 +15*(i+1) + 32, self.menu_rect[1] + self.menu_radius + 100)))
                else:
                    self.main_menu.blit(py.font.Font.render(self.menu_text, str(self.levels[i+1]['Time']), True, (0, 0, 0, 150)), ((self.menu_rect[0] + i*94 +15*(i+1) + 32, self.menu_rect[1] + self.menu_radius + 100)))

            # draw the current level "button" differently
            if py.Rect((self.menu_rect[0] + 15)*self.scale, (self.menu_rect[1] + self.menu_radius + 15)*self.scale, 530*self.scale, 94*self.scale).collidepoint(py.mouse.get_pos()):
                # draw the menu "buttons"
                for i in range(5):
                    if self.rects[i].collidepoint(py.mouse.get_pos()) and self.levels[i]['Completed'] == True:
                        py.draw.rect(self.display, (150, 150, 150, 150), (self.menu_rect[0] + i*94 +15*(i+1), self.menu_rect[1] + self.menu_radius + 5, 94, 63), 0, 25)
                        py.draw.rect(self.display, (0, 0, 0, 150), (self.menu_rect[0] + i*94 +15*(i+1), self.menu_rect[1] + self.menu_radius + 5, 94, 63), 2, 25)
            
                # draw the text for the menu "buttons"
                for i in range(5):
                    if self.rects[i].collidepoint(py.mouse.get_pos()):
                        self.display.blit(py.font.Font.render(self.number_text, str(i+1), True, (0, 0, 0, 150)), ((self.menu_rect[0] + i*94 +15*(i+1) + 28, self.menu_rect[1] + self.menu_radius + 4)))
            
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
        """
        Handles all events while in the main menu or settings menu.

        Events that are handled include the player clicking on the different
        options in the main menu, the player adjusting the volume in the settings
        menu, the player adjusting the screen resolution in the settings menu, and
        the player exiting to the main menu from the settings menu or the win
        screen.

        """
        for event in py.event.get():
            if event.type == py.QUIT:
                self.exit_game()

            if event.type == py.KEYDOWN:
                if event.key == py.K_ESCAPE:
                    self.exit_game()

            if event.type == py.MOUSEBUTTONDOWN and (self.settings_loop == False and self.win_screen_loop == False):
                if self.rects[0].collidepoint(py.mouse.get_pos()):
                    self.setup_level(1)
                if self.rects[1].collidepoint(py.mouse.get_pos()) and self.levels[1]['Completed'] == True:
                    self.setup_level(2)
                if self.rects[2].collidepoint(py.mouse.get_pos()) and self.levels[2]['Completed'] == True:
                    self.setup_level(3)
                if self.rects[3].collidepoint(py.mouse.get_pos()) and self.levels[3]['Completed'] == True:
                    self.setup_level(4)
                if self.rects[4].collidepoint(py.mouse.get_pos()) and self.levels[4]['Completed'] == True:
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
                if self.rects['wipe'].collidepoint(py.mouse.get_pos()):
                    self.wipe_data()

            if event.type == py.MOUSEBUTTONDOWN and self.win_screen_loop == True:
                if self.rects['exit'].collidepoint(py.mouse.get_pos()):
                    self.title_screen_loop = True
                    
    def settings_menu(self):
        """
        Handles all events while in the settings menu.

        Events that are handled include the player changing the screen
        resolution, the player adjusting the volume, the player exiting to the
        main menu, and the player wiping all save data.
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
                    'wipe': py.Rect((self.menu_rect[0] + 342)*self.scale, (self.menu_rect[1] + 3)*self.scale, 150*self.scale, 47*self.scale)
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

            # draw the wipe data button
            py.draw.rect(self.main_menu, (150, 150, 150, 150), (self.menu_rect[0] + 342, self.menu_rect[1]+3, 150, 47), 0, 25)
            py.draw.rect(self.main_menu, (0, 0, 0, 150), (self.menu_rect[0] + 342, self.menu_rect[1]+3, 150, 47), 2, 25)
            self.main_menu.blit(py.font.Font.render(self.normal_text, 'Wipe Data', True, (0, 0, 0, 150)), ((self.menu_rect[0] + 365, self.menu_rect[1] +10)))
            if py.Rect((self.menu_rect[0] + 342)*self.scale, (self.menu_rect[1] + 3)*self.scale, 150*self.scale, 47*self.scale).collidepoint(py.mouse.get_pos()):
                py.draw.rect(self.display, (150, 150, 150, 150), (self.menu_rect[0] + 342, self.menu_rect[1]+3, 150, 47), 0, 25)
                py.draw.rect(self.display, (0, 0, 0, 150), (self.menu_rect[0] + 342, self.menu_rect[1]+3, 150, 47), 2, 25)
            
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
        """
        Sets up the game for a level.

        This function sets up the game state to begin a new level. This includes loading
        the assets, assembling the level, setting up the player and camera, and initializing
        scores and other game variables.

        Parameters:
            level (int): The level number to load.
        """
        self.title_screen_loop = False
        self.level_loop = True
        
        #* assets of the game
        self.assets = {
            'player': load_image('entities/player/player_test.png'),
            'dirt': load_images('tiles/dirt'),
            'empty_dirt': load_images('tiles/empty_dirt'),
            'air': load_images('tiles/air'),
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

    def run_level(self) -> None:
        """
        Runs the main game loop for a level.

        This function handles updating and rendering game entities such as the player,
        enemies, and collectibles, as well as managing the player's input and jump mechanics.
        It continuously refreshes the display and updates the game state while the level
        is active. The function also draws a jump power gauge to visually indicate the player's
        jump charge level.

        Global Variables:
            jump (bool): A flag indicating if the jump is being charged.
            jump_time (float): The duration for which the jump has been charged.

        Attributes:
            game_overlay (pygame.Surface): An overlay surface for rendering UI elements like the jump gauge.
            scroll (list): The camera's scrolling offset, dynamically adjusted based on the player's position.
        """

        global jump, jump_time

        self.game_overlay = py.Surface((640, 360), py.SRCALPHA)

        self.start_time = time.time()

        self.reset = False

        while self.level_loop: 
            self.display.blit(py.transform.scale(self.assets['background'], self.display.get_size()), (0, 0))

            self.game_overlay.fill((0, 0, 0, 5))

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

            if self.reset == True:
                self.reset = False
                self.reset_level()

            if jump == True:
                jump_time = min(10, round(max(4, jump_time + 1/20), 2))
            
            # Draw Jump Power Gauge
            self.game_overlay.blit(py.font.Font.render(self.normal_text, "Jump Power", False, (0, 0, 0)), (25, 5))
            py.draw.rect(self.game_overlay, (150, 150, 150, 150), (15, 35, 200, 30), 0, 15) 
            py.draw.circle(self.game_overlay, (150, 0, 0, 150), (30, 50), 15, 0)
            
            if 4 < jump_time:
                py.draw.rect(self.game_overlay, (150, 0, 0, 150), (27, 35, 190*(jump_time - 4)*1/6-3, 30), 0, 15)
            if 6 < jump_time:
                py.draw.rect(self.game_overlay, (150, 150, 0, 150), (27+64, 35, 190*(jump_time - 6)*1/6-3, 30), 0, 15)
            if 8 < jump_time:
                py.draw.rect(self.game_overlay, (0, 150, 0, 150), (27+128, 35, 190*(jump_time - 8)*1/6-4, 30), 0, 15)
            
            py.draw.rect(self.game_overlay, (0, 0, 0, 150), (15, 35, 200, 30), 2, 15)

            # Draw Number of carrots & radishes - to show the player how many they've collected 

            carrot = load_image("collectibles/carrot.png")
            radish = load_image("collectibles/radish.png")

            carrot.set_alpha(200)
            radish.set_alpha(200)

            self.game_overlay.blit(carrot, (520, 15))
            self.game_overlay.blit(py.font.Font.render(self.normal_text, str(self.score), None, 'black'), (540, 12))

            self.game_overlay.blit(radish, (580, 15))
            self.game_overlay.blit(py.font.Font.render(self.normal_text, str(self.super_score), None, 'black'), (600, 12))

            # Draw the time spent in the level

            self.level_time = round(time.time() - self.start_time, 2)

            hour = '0'+str(int(self.level_time//3600)) if self.level_time//3600 < 10 else str(int(self.level_time//3600))
            minute = '0'+ str(int(self.level_time//60 - self.level_time//3600*60)) if self.level_time//60 - self.level_time//3600*60 < 10 else str(int(self.level_time//60 - self.level_time//3600*60))
            second = '0'+str(int(self.level_time - self.level_time//60*60)) if self.level_time - self.level_time//60*60 < 10 else str(int(self.level_time - self.level_time//60*60))

            self.current_time = hour+':'+minute+':'+second

            self.game_overlay.blit(py.font.Font.render(self.normal_text, str(self.current_time), None, 'black'), (530, 47))

            self.display.blit(self.game_overlay, (0,0))

            # updates the window
            self.screen.blit(py.transform.scale(self.display, self.screen.get_size()), (0, 0))
            py.display.flip()
            self.clock.tick(60) # limit FPS to 60 per second
        
    def player_input(self) -> None:
        """
        Handles player input events and updates player state accordingly.

        This function processes input events for controlling the player character.
        It updates the player's velocity and jump state based on keyboard inputs,
        such as moving left or right and charging or executing a jump. The function
        also handles exiting the game and ending the level.

        Global Variables:
            jump (bool): A flag indicating if the jump is being charged.
            jump_time (float): The duration for which the jump has been charged.

        Handles the following events:
            - QUIT: Exits the game.
            - KEYDOWN:
                - ESCAPE: Exits the game.
                - LEFT/A: Moves the player left.
                - RIGHT/D: Moves the player right.
                - UP/W: Starts charging the player's jump.
                - M: Ends the current level.
            - KEYUP:
                - LEFT/A: Stops moving the player left.
                - RIGHT/D: Stops moving the player right.
                - UP/W: Executes the player's jump if possible.
        """

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
                    self.player.jumps = 0


    def load_level(self, map_id=0) -> None:
        """
        Loads a level from a JSON file and initializes all level entities.

        Loads a level from a JSON file and sets up all level entities such as the player, collectibles, and enemies.
        It also initializes the game's projectile list and sets the current level ID.

        Global Variables:
            projectiles (dict): A dictionary containing all projectiles in the game, keyed by ID.
            projectiles_id (list): A list of all projectile IDs.

        Attributes:
            collectibles (list): A list of all collectibles in the level.
            enemies (list): A list of all enemies in the level.
            current_level (int): The ID of the currently loaded level.
        """
        try:
            self.tilemap.load(f'data/maps/{map_id}.json')
        except FileNotFoundError:
            print("Could not find the Level File(hint: it's a json file)")
            self.exit_game()

        self.current_level = map_id

        self.fastest_time = self.levels[self.current_level]['Fastest_Time']
        
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
            else: 
                self.collectibles.append(Collectible(self, collectible['pos'], (16, 16), 2))
        
        #* enemies
        self.enemies = []
        self.enemies_id = []
        for spawner in self.tilemap.extract([('spawner', 0), ('spawner', 1), ('spawner', 2)]):
            if spawner['variant'] == 0:
                self.player.pos = spawner['pos']
            elif spawner['variant'] == 1:
                self.enemies.append(TickEnemy(self, spawner['pos'], (16, 16)))
            else: 
                self.enemies.append(DungEnemy(self, spawner['pos'], (16, 16)))
    
    def end_level(self) -> None:
        """
        Ends the current level and starts the win screen loop.
        
        This function sets level_loop to False and win_screen_loop to True, 
        then calls the win_menu function to start the win screen loop. 
        It also sets title_screen_loop to True and calls the run_menu function to start the main menu loop.
        
        :return: None
        """
        self.final_time = time.time() - self.start_time
        self.level_loop = False 
        self.win_screen_loop = True
        self.win_menu()
        self.run_menu()
    
    def win_menu(self):
        self.save(self.current_level)

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

    def reset_level(self) -> None:
        self.score = 0
        self.super_score = 0
        self.load_level(self.current_level)
        self.scroll = [self.player.pos[0] - self.display.get_width()/2, self.player.pos[1] - self.display.get_height()/2]

    def exit_game(self) -> None:
        """
        Exits the game cleanly.

        Closes the pygame window and exits the game.

        :return: None
        """
        py.quit()
        sys.exit()

    def __str__(self) -> str:
        return "Game"

    def load(self, file) -> None:
        """
        Loads the save data for the given level from the save file.

        This function is used to load the save data from the save file, and
        updates the Game's levels dictionary with the loaded data.

        :param file: the number of the save file to load from
        :return: None
        """
        with open(f'data/save_data/save{file}.json', 'r') as f:
            save_data = json.load(f)
        self.levels[save_data['Level']] = {'Completed': save_data['Completed'], 
                                           'Carrots': save_data['Carrots'], 
                                           'Radishes': save_data['Radishes'], 
                                           'Score': save_data['Score'], 
                                           'Completion': save_data['Completion'], 
                                           'Time': save_data['Time'], 
                                           'Fastest_Time': save_data['Fastest_Time']}
        
    def save(self, file) -> None:
        """
        Saves the game data to a file.

        This function is used to save the game data to a file. It
        is called when the player completes a level or when the
        game is exited. The function checks if the current score is
        higher than the high score for the given level, and if so,
        it updates the high score. Then it saves the game data to
        the file.

        :param file: the number of the save file to save to
        :return: None
        """
        if self.score*10 + self.super_score*100 > self.high_scores[file][2]:
            self.high_scores[file][2] = self.score*10 + self.super_score*100
        if self.score > self.high_scores[file][0]:
            self.high_scores[file][0] = self.score
        if self.super_score > self.high_scores[file][1]:
            self.high_scores[file][1] = self.super_score
        if self.final_time < self.fastest_time:
            self.fastest_time = self.final_time

        hours = '0'+str(int(self.fastest_time//3600)) if self.fastest_time//3600 < 10 else str(int(self.fastest_time//3600))
        minutes = '0'+ str(int(self.fastest_time//60 - self.fastest_time//3600*60)) if self.fastest_time//60 - self.fastest_time//3600*60 < 10 else str(int(self.fastest_time//60 - self.fastest_time//3600*60))
        seconds = '0'+str(int(self.fastest_time - self.fastest_time//60*60)) if self.fastest_time - self.fastest_time//60*60 < 10 else str(int(self.fastest_time - self.fastest_time//60*60))

        end_time = hours + ':' + minutes + ":" + seconds
        
        with open(f'data/save_data/save{file}.json', 'w') as f:
            json.dump({"Level": self.current_level, 
                       "Completed": True, 
                       "Carrots": self.high_scores[file][0], 
                       "Radishes": self.high_scores[file][1], 
                       "Score": self.high_scores[file][2], 
                       "Completion": str(round((self.high_scores[file][0]*10 + self.high_scores[file][1]*100)*0.07692307692, 3))+"%", 
                       "Time": end_time,
                       "Fastest_Time": round(self.fastest_time, 3)}, f)
    
    def wipe_data(self) -> None:
        """
        Wipes all save data from the save files.

        This function is used to completely clear all save data from the
        save files. It is called when the player chooses to reset the
        game data from the settings menu.

        :return: None
        """
        for i in range(1, 6):
            with open(f'data/save_data/save{i}.json', 'w') as f:
                json.dump({"Level": i, "Completed": False, "Carrots": 0, "Radishes": 0, "Score": 0, "Completion": "0%", "Time": "99:59:59", "Fastest_Time": 359999}, f)


if __name__ == "__main__":
    game = Game()
    game.run_menu()