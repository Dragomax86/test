import pygame

NEIGHBOR_OFFSETS = [(0, 0), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1)]
PHYSICS_TILES = {"grass","dirt"}

class TileMap:
   
    def __init__(self, game, tile_size):

        self.game = game
        self.tile_size = list(tile_size)
        self.tilemap = {}
        self.offgrid_tiles = []
    
    def mapping(self):
        #Position, type, variant of the entire tiles of the map

        for y in range(self.game.assets["map_tuto"].get_height()):
            for x in range(self.game.assets["map_tuto"].get_width()):
                if self.game.assets["map_tuto"].get_at((x,y)) == self.game.color_code["grass"]:
                    self.tilemap[str(x) + ";" + str(y)] = {"type": "grass", "variant": 0, "position": (x,y)}
                if self.game.assets["map_tuto"].get_at((x,y)) == self.game.color_code["dirt"]:
                    self.tilemap[str(x) + ";" + str(y)] = {"type": "dirt", "variant": 0, "position": (x,y)}

    def tiles_around(self, position):
        tiles = []
        tile_location = (int(position[0] // self.tile_size[0]), int(position[1] // self.tile_size[1]))
        for offset in NEIGHBOR_OFFSETS:
            check_loc = str(tile_location[0] + offset[0]) + ";" + str(tile_location[1] + offset[1])
            if check_loc in self.tilemap:
                tiles.append(self.tilemap[check_loc])
        return tiles

    def physics_rects_around(self, position):
        rects = []
        for tile in self.tiles_around(position):
            if tile["type"] in PHYSICS_TILES:
                rects.append(pygame.Rect(tile["position"][0] * self.tile_size[0], tile["position"][1] * self.tile_size[1], self.tile_size[0], self.tile_size[1]))
        return rects

    def solide_check(self, position):
        tile_location = str(int(position[0] // self.tile_size[0])) + ";" + str(int(position[1] // self.tile_size[1]))
        if tile_location in self.tilemap:
            if self.tilemap[tile_location]["type"] in PHYSICS_TILES:
                return self.tilemap[tile_location]

    def render(self, surface, offset=[0,0]):
        for tile in self.offgrid_tiles:
            surface.blit(self.game.assets[tile["type"]][tile["variant"]], (tile["position"][0] - offset[0], tile["position"][1] - offset[1]))

        for location in self.tilemap:
            tile = self.tilemap[location]
            surface.blit(self.game.assets[tile["type"]][tile["variant"]], (tile["position"][0] * self.tile_size[0] - offset[0], tile["position"][1] * self.tile_size[1] - offset[1]))