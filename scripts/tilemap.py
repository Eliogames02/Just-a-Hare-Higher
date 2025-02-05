import pygame as py
import json

NEIGHBOR_OFFSETS = [(-1, -1), (0, -1), (1, -1), (-1,0), (0, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
PHYSICS_TILES = {'dirt', 'air'}

class Tilemap:
    def __init__(self, game, tile_size=16):
        """
        Initializes a Tilemap instance.

        Args:
            game: The game instance to which this tilemap belongs.
            tile_size (int, optional): The size of each tile. Defaults to 16.

        Attributes:
            game: The game instance to which this tilemap belongs.
            tile_size (int): The size of each tile.
            tilemap (dict): A dictionary storing the on-grid tiles.
            offgrid_tiles (list): A list storing the off-grid tiles.
        """

        self.game = game
        self.tile_size = tile_size
        self.tilemap = {}
        self.offgrid_tiles = []

    def extract(self, id_pairs:list, keep=False):
        """
        Extracts tiles from the tilemap and offgrid tiles that match the specified id pairs.

        Args:
            id_pairs (list): A list of tuples, where each tuple contains a tile type and variant to match.
            keep (bool, optional): If True, the matching tiles will not be removed from the tilemap or offgrid tiles. Defaults to False.

        Returns:
            list: A list of copies of the matching tiles. The positions of the tiles from the tilemap are scaled by the tile size.
        """
        matches = []
        for tile in self.offgrid_tiles.copy():
            if (tile['type'], tile['variant']) in id_pairs: 
                matches.append(tile.copy())
                if not keep:
                    self.offgrid_tiles.remove(tile)

        for location in list(self.tilemap):
            tile = self.tilemap[location]
            if (tile['type'], tile['variant']) in id_pairs:
                matches.append(tile.copy())
                matches[-1]['pos'] = matches[-1]['pos'].copy()
                matches[-1]['pos'][0] *= self.tile_size
                matches[-1]['pos'][1] *= self.tile_size
                if not keep:
                    del self.tilemap[location]
        return matches

    def render(self, surface, offset=(0, 0)):
        """
        Renders the tiles onto the given surface, applying an offset for scrolling.

        This function iterates through both off-grid and on-grid tiles, drawing each tile
        onto the provided surface. Off-grid tiles are rendered directly at their specified
        positions, while on-grid tiles are rendered based on the visible region determined
        by the surface size and the provided offset. 

        Args:
            surface (pygame.Surface): The surface to render the tiles onto.
            offset (tuple, optional): The offset used to adjust the tile positions for
                                    scrolling, given as (x, y) coordinates.
        """
        for tile in self.offgrid_tiles:
            surface.blit(py.transform.rotate(self.game.assets[tile['type']][tile['variant']], -90 * tile['rotations']), (tile['pos'][0] - offset[0], tile['pos'][1] - offset[1]))

        for x in range(offset[0] // self.tile_size, (offset[0] + surface.get_width()) // self.tile_size + 1):
            for y in range(offset[1] // self.tile_size, (offset[1] + surface.get_height()) // self.tile_size + 1):
                location = str(x) + ';' + str(y)
                if location in self.tilemap:
                    tile = self.tilemap[location]
                    if tile['variant'] != 3: 
                        surface.blit(py.transform.rotate(self.game.assets[tile['type']][tile['variant']], -90 * tile['rotations']), (tile['pos'][0] * self.tile_size - offset[0], tile['pos'][1] * self.tile_size - offset[1]))
                    else:
                        try:
                            if self.game.current_level == 1: 
                                self.game.display.blit(py.font.Font.render(self.game.normal_text, "WAD - Arrow Keys - Space", True, (0, 0, 0)), (tile['pos'][0] * self.tile_size - offset[0], tile['pos'][1] * self.tile_size - offset[1]))
                                self.game.display.blit(py.font.Font.render(self.game.normal_text, "Get to the Star", True, (0, 0, 0)), (tile['pos'][0] * self.tile_size - offset[0], (tile['pos'][1]+2) * self.tile_size - offset[1]))
                            if self.game.current_level == 2: 
                                self.game.display.blit(py.font.Font.render(self.game.normal_text, "They're Not Nice", True, (0, 0, 0)), (tile['pos'][0] * self.tile_size - offset[0], tile['pos'][1] * self.tile_size - offset[1]))
                            if self.game.current_level == 3: 
                                self.game.display.blit(py.font.Font.render(self.game.normal_text, "Look Out from Above", True, (0, 0, 0)), (tile['pos'][0] * self.tile_size - offset[0], tile['pos'][1] * self.tile_size - offset[1]))
                            if self.game.current_level == 4: 
                                self.game.display.blit(py.font.Font.render(self.game.normal_text, "Watch the Ground for Moles", True, (0, 0, 0)), (tile['pos'][0] * self.tile_size - offset[0], tile['pos'][1] * self.tile_size - offset[1]))
                            if self.game.current_level == 5: 
                                self.game.display.blit(py.font.Font.render(self.game.normal_text, "Just One Hare Higher", True, (0, 0, 0)), (tile['pos'][0] * self.tile_size - offset[0], tile['pos'][1] * self.tile_size - offset[1]))
                        except AttributeError:
                            pass
    def tiles_around(self, pos):
        """
        Returns a list of tiles surrounding the given position in the tilemap.

        The function checks each neighboring position around the given position
        based on predefined offsets and collects tiles that are present in the tilemap.

        Args:
            pos (tuple): The position to check around, given as a tuple of (x, y) coordinates.

        Returns:
            list: A list of tiles found around the specified position.
        """
        tiles = []
        tile_location = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size))
        for offset in NEIGHBOR_OFFSETS:
            check_location = str(tile_location[0] + offset[0]) + ';' + str(tile_location[1] + offset[1])
            if check_location in self.tilemap:
                tiles.append(self.tilemap[check_location])
        return tiles
    
    def tile_around(self, pos, tile_offset):
        """
        Returns the tile at the position tile_offset from the given position in the tilemap.

        If the tile at the offset position is not found, it returns None.
        If the tile is of a type included in PHYSICS_TILES, it returns the tile's properties.
        """
        tile_location = (str(int(pos[0] // self.tile_size) + tile_offset[0]) + ';' + str(int(pos[1] // self.tile_size) + tile_offset[1]))
        if tile_location in self.tilemap: 
            return self.tilemap[tile_location]
        return None
    
    def physics_rects_around(self, pos):
        """
        Returns a list of pygame.Rects of the physics tiles around the given position in the tilemap.
        
        Only tiles of type in PHYSICS_TILES are included in the list.
        
        Args:
            pos (tuple): The position to check around.
        
        Returns:
            list: A list of pygame.Rects of the physics tiles around the position.
        """
        rects = []
        for tile in self.tiles_around(pos):
            if tile['type'] in PHYSICS_TILES:   
                rects.append(py.Rect(tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size, self.tile_size, self.tile_size))
        return rects
    
    def physics_specific_rect(self, pos, tile_offset):
        """
        Returns the pygame.Rect of a specific tile with a given offset from the provided tilemap position.

        If the tile at the offset position is not found, it returns a dummy Rect at (-1000, -1000).
        If the tile is of a type included in PHYSICS_TILES, it returns the Rect based on the tile's position and the tile size.
        
        Args:
            pos (tuple): The position to check around.
            tile_offset (tuple): The offset from the position to check for the specific tile.
        
        Returns:
            py.Rect: The rectangle of the specific tile or a dummy rectangle if no valid tile is found.
        """
        tile = self.tile_around(pos, tile_offset)
        if tile == None: return py.Rect(-1000, -1000, 1, 1) #! THE NULL RECT IS REAL
        if tile['type'] in PHYSICS_TILES:
            return py.Rect(tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size, self.tile_size, self.tile_size)
        return py.Rect(-1000, -1000, 1, 1) #! THE NULL RECT IS REAL

    def save(self, path):
        """
        Saves the current tilemap to the given path as a json file.
        
        The json file will contain a dictionary with the following keys:
        - 'tilemap': the tilemap as a dictionary of dictionaries, where the keys are the 
            coordinates of the tiles in the format 'x;y' and the values are dictionaries
            with the following keys:
            - 'type': the type of the tile
            - 'variant': the variant of the tile
            - 'rotations': the number of times the tile has been rotated clockwise
            - 'pos': the position of the tile in the format (x, y)
        - 'tile_size': the size of the tiles as an integer
        - 'offgrid_tiles': a dictionary with the same format as 'tilemap', but for the
            tiles that are not part of the main tilemap (i.e. the tiles that are not
            aligned with the grid)
        """
        with open(path, 'w') as f:
            json.dump({'tilemap': self.tilemap, 'tile_size': self.tile_size, 'offgrid_tiles': self.offgrid_tiles}, f)
    
    def load(self, path):
        """
        Loads a tilemap from the given path. The tilemap is expected to be in the following format:
        {
            'tilemap': {'x_pos;y_pos': {'type': str, 'variant': int, 'rotations': int, 'pos': (int, int)}}, 
            'tile_size': int, 
            'offgrid_tiles': {'x_pos;y_pos': {'type': str, 'variant': int, 'rotations': int, 'pos': (int, int)}}
        }
        """
    
        with open(path, 'r') as f:
            map_data = json.load(f)
        
        self.tilemap = map_data['tilemap']
        self.tile_size = map_data['tile_size']
        self.offgrid_tiles = map_data['offgrid_tiles']