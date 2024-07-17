import pygame as py
import json

NEIGHBOR_OFFSETS = [(-1, -1), (0, -1), (1, -1), (-1,0), (0, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
PHYSICS_TILES = {'dirt'}
#AUTOTILE_TILES = {'dirt'} autotiling isn't helpful here because the tiles srites aren't finished yet

class Tilemap:
    def __init__(self, game, tile_size=16):
        self.game = game
        self.tile_size = tile_size
        self.tilemap = {}
        self.offgrid_tiles = []

    def extract(self, id_pairs:list, keep=False):
        matches = []
        for tile in self.offgrid_tiles.copy():
            if (tile['type'], tile['variant']) in id_pairs: 
                matches.append(tile.copy())
                if not keep:
                    self.offgrid_tiles.remove(tile)

        for location in self.tilemap:
            tile = self.tilemap[location]
            if (tile['type'], tile['variant']) in id_pairs:
                matches.append(tile.copy())
                matches[-1]['pos'] = matches[-1]['pos'].copy()
                matches[-1]['pos'][0] *= self.tile_size
                matches[-1]['pos'][1] *= self.tile_size
                if not keep:
                    del self.tilemap[location]
        
        return matches

    def tiles_around(self, pos):
        tiles = []
        tile_location = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size))
        for offset in NEIGHBOR_OFFSETS:
            check_location = str(tile_location[0] + offset[0]) + ';' + str(tile_location[1] + offset[1])
            if check_location in self.tilemap:
                tiles.append(self.tilemap[check_location])
        return tiles
    
    def save(self, path):
        with open(path, 'w') as f:
            json.dump({'tilemap': self.tilemap, 'tile_size': self.tile_size, 'offgrid_tiles': self.offgrid_tiles}, f)

    def load(self, path):
        with open(path, 'r') as f:
            map_data = json.load(f)
        
        self.tilemap = map_data['tilemap']
        self.tile_size = map_data['tile_size']
        self.offgrid_tiles = map_data['offgrid_tiles']

    def physics_rects_around(self, pos):
        rects = []
        for tile in self.tiles_around(pos):
            if tile['type'] in PHYSICS_TILES:
                rects.append(py.Rect(tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size, self.tile_size, self.tile_size))
        return rects
    
    #* Autotiling isn't helpful here because the tiles srites aren't finished yet
    #def autotile(self):
    #    for location in self.tilemap:
    #        tile = self.tilemap[location]
    #        neighbors = set()
    #        for shift in [(1,0), (0,1), (-1,0), (0,-1)]:
    #            check_location = str(tile['pos'][0] + shift[0]) + ';' + str(tile['pos'][1] + shift[1])
    #            if check_location in self.tilemap:
    #                pass

    def render(self, surf, offset=(0, 0)):
        for tile in self.offgrid_tiles:
            surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] - offset[0], tile['pos'][1] - offset[1]))

        for x in range(offset[0] // self.tile_size, (offset[0] + surf.get_width()) // self.tile_size + 1):
            for y in range(offset[1] // self.tile_size, (offset[1] + surf.get_height()) // self.tile_size + 1):
                location = str(x) + ';' + str(y)
                if location in self.tilemap:
                    tile = self.tilemap[location]
                    if tile['type'] != 'collectible' or str(type(self.game)) == "<class '__main__.Editor'>":
                        surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] * self.tile_size - offset[0], tile['pos'][1] * self.tile_size - offset[1]))