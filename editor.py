import pygame as py
import sys
from scripts.utils import load_image, load_images
from scripts.tilemap import Tilemap

RENDER_SCALE = 3.0

class Editor:
    def __init__(self) -> None:
        """
        Initializes the Editor class, setting up the required components for the
        tilemap editor, including pygame, window, clock, assets, and the tilemap.

        This constructor initializes the pygame library, sets up the display window
        and title, prepares the clock for frame rate control,
        and initializes game assets such as images for different tile types. It also
        sets up basic editor functionality such as scrolling movement, tilemap
        management, camera control, and interaction states like clicking and
        rotating.

        Attributes:
            screen (pygame.Surface): The main display surface for the editor.
            display (pygame.Surface): A secondary surface for rendering the editor's content.
            map_name (str): The name of the level being edited.
            clock (pygame.time.Clock): Used to control the frame rate of the editor.
            default_font (pygame.font.Font): The default font for rendering text.
            assets (dict): A dictionary containing loaded images for different tile types.
            movement (list): A list indicating the direction of scroll movement.
            tilemap (Tilemap): The tilemap instance used in the editor.
            scroll (list): The camera's scrolling offset.
            tile_list (list): A list of tile types available in the editor.
            tile_group (int): The index of the currently selected tile group.
            tile_variant (int): The index of the currently selected tile variant.
            clicking (bool): A flag indicating if the left mouse button is being pressed.
            right_clicking (bool): A flag indicating if the right mouse button is being pressed.
            shift (bool): A flag indicating if the shift key is held down. Used to switch current tile variant.
            rotate (bool): A flag indicating if the current tile is to be rotated.
            rotations (int): The number of rotations applied to the current tile.
            ongrid (bool): A flag indicating if the tile placement is aligned to the grid.
        """
        py.init()
        
        # window setup
        py.display.set_caption('editor')
        self.screen = py.display.set_mode((py.display.get_desktop_sizes()[0][0], py.display.get_desktop_sizes()[0][1] - 32))
        self.display = py.Surface((640, 360))
        map_name = '0'

        # clock/fps setup
        self.clock = py.time.Clock()

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
            self.tilemap.load(f'data/maps/{map_name}.json')
        except FileNotFoundError:
            print("Could not find the Level File(hint: it's a json file)")

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
        """
        Runs the editor's main loop, responsible for rendering the tilemap, handling
        scroll movement, and updating the display.

        This function is responsible for rendering the tilemap and taking into account
        the scroll offset, setting the current tile image to be displayed on the grid,
        getting the mouse position and tile position, and displaying the current tile
        on the grid or off the grid. It also handles placing and deleting tiles by
        checking if the left mouse button is being pressed and if the tile is on the
        grid. If the right mouse button is being pressed, it deletes the tile at the
        mouse position.

        :return: None
        """
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
    """
    Handles all events and inputs for the editor.

    This function processes various event types such as quitting the program, 
    mouse button actions, and keyboard inputs. It updates the editor's state 
    based on these events, including toggling the grid, rotating tiles, saving 
    maps, and handling movement.

    Mouse Events:
        - MOUSEBUTTONDOWN: Starts clicking or right-clicking actions, adds tiles 
          to on and off-grid, and scrolls through tile variants and groups.
        - MOUSEBUTTONUP: Stops clicking or right-clicking actions.

    Keyboard Events:
        - KEYDOWN: Handles quitting, movement directions, toggling grid, saving 
          maps, and tile rotations.
        - KEYUP: Stops movement actions and sets shift state to False.
    """

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
    """
    Updates the screen and controls the frame rate.

    This function updates the entire pygame display window and limits the game to 60 frames per second.

    :param clock: A pygame.time.Clock object used to control the frame rate.
    :return: None
    """
    py.display.flip()
    clock.tick(60)
# Exits the game
def exit_game() -> None:
    """
    Exits the game cleanly.

    Prints out the player's score to the console and then closes the pygame window and exits the game.

    :return: None
    """
    py.quit()
    sys.exit()
    
editor = Editor()
editor.run()