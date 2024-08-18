import pygame as py
import sys
from scripts.utils import load_image, load_images
from scripts.tilemap import Tilemap

RENDER_SCALE = 2.0

class Editor:
    def __init__(self) -> None:
        # pygame setup
        py.init()
        
        # window setup
        py.display.set_caption('editor')
        self.screen = py.display.set_mode((1280, 960))
        self.display = py.Surface((640, 480))
        map_name = ''

        # clock/fps setup
        self.clock = py.time.Clock()

        # font setup
        self.default_font = py.font.SysFont("Time New Roman", 24)

        # assets setup
        self.assets = {
            'dirt': load_images('tiles/dirt'),
            'empty_dirt': load_images('tiles/empty_dirt'),
            'collectible': load_images('tiles/collectible'),
            'spawner': load_images('tiles/spawners'),
        }

        # scroll movement setup
        self.movement = [False, False, False, False]

        #tilemap
        self.tilemap = Tilemap(self, tile_size=16)
        try:
            self.tilemap.load(f'data/maps/0.json')
        except FileNotFoundError:
            pass

        #camera setup
        self.scroll = [0, 0]

        # editor setup
        self.tile_list = list(self.assets)
        self.tile_group = 0
        self.tile_variant = 0
        self.clicking = False
        self.right_clicking = False
        self.shift = False
        self.rotate = False
        self.rotations = 0
        self.ongrid = True

    def run(self) -> None:
        while True:
            self.display.fill((0, 0, 0))

            # Scroll handling
            self.scroll[0] += (self.movement[1] - self.movement[0]) * 5 # multiply movement to speed up scrolling
            self.scroll[1] += (self.movement[3] - self.movement[2]) * 5
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            # renders the tilemap and takes into account the scroll
            self.tilemap.render(self.display, offset=render_scroll)

            # sets the current tile image to be displayed on the grid
            current_tile_img = py.transform.rotate(self.assets[self.tile_list[self.tile_group]][self.tile_variant].copy(), -90 * self.rotations)
            current_tile_img.set_alpha(100)

            if self.rotate == True:
                if self.rotations > 2:
                    self.rotations = 0
                else: self.rotations += 1
                self.rotate = False

            # Get the mous position and tile position
            self.mouse_pos = py.mouse.get_pos()
            self.mouse_pos = (self.mouse_pos[0] // RENDER_SCALE, self.mouse_pos[1] // RENDER_SCALE)
            tile_pos = (int(self.mouse_pos[0] + self.scroll[0]) // self.tilemap.tile_size, int(self.mouse_pos[1] + self.scroll[1]) // self.tilemap.tile_size)

            # Displays the current tile on the grid or off the grid
            if self.ongrid:
                self.display.blit(current_tile_img, (tile_pos[0] * self.tilemap.tile_size - self.scroll[0], tile_pos[1] * self.tilemap.tile_size - self.scroll[1]))
            else:
                self.display.blit(current_tile_img, self.mouse_pos)

            
            if self.clicking and self.ongrid:
                self.tilemap.tilemap[str(tile_pos[0]) + ';' + str(tile_pos[1])] = {'type': self.tile_list[self.tile_group], 'variant': self.tile_variant, 'pos': (tile_pos[0], tile_pos[1]), 'rotations': (self.rotations)}
            if self.right_clicking:
                tile_location = str(tile_pos[0]) + ';' + str(tile_pos[1])
                if tile_location in self.tilemap.tilemap and self.ongrid == True:
                    del self.tilemap.tilemap[tile_location]
                for tile in self.tilemap.offgrid_tiles.copy():
                    tile_img = self.assets[tile['type']][tile['variant']]
                    tile_r = py.Rect(tile['pos'][0] - self.scroll[0], tile['pos'][1] - self.scroll[1], tile_img.get_width(), tile_img.get_height())
                    if tile_r.collidepoint(self.mouse_pos) and self.ongrid == False:
                        self.tilemap.offgrid_tiles.remove(tile)

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
        
        # Handles all mouse input events
        if event.type == py.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.clicking = True
                if not self.ongrid:
                    self.tilemap.offgrid_tiles.append({'type': self.tile_list[self.tile_group], 'variant': self.tile_variant, 'pos': (self.mouse_pos[0] + self.scroll[0], self.mouse_pos[1] + self.scroll[1]), 'rotations': self.rotations})
            if event.button == 3:
                self.right_clicking = True
            
            if self.shift:
                if event.button == 4:
                    self.tile_variant = (self.tile_variant - 1) % len(self.assets[self.tile_list[self.tile_group]])
                if event.button == 5:
                    self.tile_variant = (self.tile_variant + 1) % len(self.assets[self.tile_list[self.tile_group]])
            else:
                if event.button == 4:
                    self.tile_group = (self.tile_group - 1) % len(self.tile_list)
                    self.tile_variant = 0
                if event.button == 5:
                    self.tile_group = (self.tile_group + 1) % len(self.tile_list)
                    self.tile_variant = 0

        if event.type == py.MOUSEBUTTONUP:    
            if event.button == 1:
                self.clicking = False
            if event.button == 3:
                self.right_clicking = False

        # Handles all keyboard input events
        if event.type == py.KEYDOWN:
            if event.key == py.K_ESCAPE:
                exit_game()

            if event.key == py.K_LEFT or event.key == py.K_a:
                self.movement[0] = True
            if event.key == py.K_RIGHT or event.key == py.K_d:
                self.movement[1] = True

            if event.key == py.K_UP or event.key == py.K_w:
                self.movement[2] = True
            if event.key == py.K_DOWN or event.key == py.K_s:
                self.movement[3] = True

            if event.key == py.K_g:
                self.ongrid = not self.ongrid

            if event.key == py.K_LSHIFT:
                self.shift = True
            if event.key == py.K_LCTRL:
                self.rotate = True

            if event.key == py.K_o:
                map_name = input('Enter level name -> ')
                self.tilemap.save(f'data/maps/{map_name}.json')
                print('Map Saved')


        if event.type == py.KEYUP:
            if event.key == py.K_LEFT or event.key == py.K_a:
                self.movement[0] = False
            if event.key == py.K_RIGHT or event.key == py.K_d:
                self.movement[1] = False

            if event.key == py.K_UP or event.key == py.K_w:
                self.movement[2] = False
            if event.key == py.K_DOWN or event.key == py.K_s:
                self.movement[3] = False

            if event.key == py.K_LSHIFT:
                self.shift = False

# Handles updating the screen and fps
def update_screen(clock) -> None:
    py.display.flip()
    clock.tick(60)
# Exits the game
def exit_game() -> None:
    py.quit()
    sys.exit()
    
editor = Editor()
editor.run()