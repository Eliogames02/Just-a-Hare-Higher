import pygame as py
import math, random

class PhysicsEntity:
    def __init__(self, game, e_type: str, tilemap, pos, size: tuple) -> None:
        self.game = game
        self.type = e_type
        self.tm = tilemap
        self.pos = list(pos)
        self.size = size #! Super important! - the size of the entity must be the same size as the image
        self.velocity = [0, 0]
        self.stored_velocity = [0, 0]
        self.collisions = {'up': False, 'down': False, 'left': False, 'right': False}
        self.id_options = ['0','1','2','3','4','5','6','7','8', '9', 'A','B','C','D','E','F']

        self.air_time = 0 # used to calculate when to switch between jump sprites and other sprite animations
        self.jumps = 1 # number of jumps an entity has
        self.touching_ground = False # determines whether the entity is touching the ground or not
        self.coyote_time = 0 # how long it's been since the entity last touched the ground

        self.action = '' # the current action of the entity
        self.anim_offset = (0, 0) # This offset is used to make the animation look like it collides properly
        self.flip = False # used to flip the sprite left and right so a different one doesn't need to be used

    def rect(self):
        return py.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
    
    def set_action(self, action):
        if action != self.action:
            self.action = action
            self.animation = self.game.assets[self.type + '/' + self.action].copy()

    # updates the position of the given object/entity
    def update(self, tilemap, movement=(0, 0), stored_movement=(0, 0)):
        self.collisions = {'up': False, 'down': False, 'left': False, 'right': False}

        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])

        # handle horizontal collision
        self.pos[0] += frame_movement[0] * self.game.delta_time/2
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[0] > 0:
                    entity_rect.right = rect.left
                    self.collisions['right'] = True
                if frame_movement[0] < 0:
                    entity_rect.left = rect.right
                    self.collisions['left'] = True
                self.pos[0] = entity_rect.x

        # handle vertical collision
        self.pos[1] += frame_movement[1] * self.game.delta_time/2
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[1] > 0:
                    entity_rect.bottom = rect.top
                    self.collisions['down'] = True
                if frame_movement[1] < 0:
                    entity_rect.top = rect.bottom
                    self.collisions['up'] = True
                self.pos[1] = entity_rect.y

        # gravity
        if not self.is_touching_ground(tilemap):
            if self.velocity[1] > 0:
                self.velocity[1] = round(min(5, self.velocity[1] + 0.15 * self.game.delta_time), 2)
            else: self.velocity[1] = round(min(5, self.velocity[1] + 0.1 * self.game.delta_time), 2)

        # complex jump mechanic
        if stored_movement[1] != False:
            self.stored_velocity[1] = round(max(-10, min(-2.5, self.stored_velocity[1]) - 0.1 * self.game.delta_time), 2)
        elif self.get_coyote_time() <= 0.25 and self.jumps == 1:
            self.velocity[1] += self.stored_velocity[1]
            self.stored_velocity[1] = 0
            self.jumps = 0
            self.air_time = 5
        else: self.stored_velocity[1] = 0

        #! This should be used if the entity assets are facing right to begin with.
        if movement[0] > 0: # This flips the image when moving right. 
            self.flip = False
        if movement[0] < 0: # this flips the image when moving left.
            self.flip = True

        # if the entity touches the ground or bonks it's head on something.
        if self.collisions['down'] or self.collisions['up']:
            self.velocity[1] = 0

        self.animation.update()

    # draws the image onto the screen
    def render(self, surf, offset=(0, 0)):
        surf.blit(py.transform.flip(self.animation.img(), self.flip, False), (self.pos[0] - offset[0] + self.anim_offset[0], self.pos[1] - offset[1] + self.anim_offset[1]))
    
    def is_touching_ground(self, tilemap) -> bool:
        entity_rect = self.rect()
        entity_rect.y += 1 # This moves the entity down by 1 pixel to check if it is touching the ground but doesn't acutally move the sprite.
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect) and self.velocity[1] >= 0:
                self.air_time = 0
                self.jumps = 1
                self.coyote_time = 0
                return True
        self.coyote_time += (self.game.delta_time /65)
        return False                
    
    def get_coyote_time(self) -> float:
        self.is_touching_ground(self.tm)
        return round(self.coyote_time, 5)

class Player(PhysicsEntity):
    def __init__(self, game, pos, size):
        super().__init__(game, 'player', game.tilemap, pos, size)
        self.set_action('idle') # Sets the initial action

    def update(self, movement=(0, 0), stored_movement=(0, 0)):
        super().update(self.game.tilemap, movement=movement, stored_movement=stored_movement)
        
        # Changes the current sprite of the player based on movement.
        '''if self.air_time > 4:
            self.set_action('jump')
        elif movement[0] != 0:
            self.set_action('run')
        else:
            self.set_action('idle')'''
        
class Collectible(PhysicsEntity):
    def __init__(self, game, pos, size, variant=0):
        super().__init__(game, 'collectible', game.tilemap, pos, size)
        self.is_collected = False
        self.variant = variant # 0 for carrot, 1 for radish
        if self.variant == 0:
            self.set_action('carrot')
        else: self.set_action('radish')

    def update(self):
        self.pos[1] += math.sin(py.time.get_ticks()/250) * 0.5 * self.game.delta_time
        self.collected()
    
    def collected(self):
        if self.rect().colliderect(self.game.player.rect()):
            self.game.collectibles.remove(self)
            return True
        return False

class Enemy(PhysicsEntity):
    def __init__(self, game, pos, size, enemy_type, id='00000000'):
        super().__init__(game, enemy_type, game.tilemap, pos, size)
        self.set_action('test')
        self.id = id
        self.enemy_type = enemy_type

        while self.id in game.enemies_id:
            self.id = random.choice(self.id_options) + random.choice(self.id_options) + random.choice(self.id_options) + random.choice(self.id_options) + random.choice(self.id_options) + random.choice(self.id_options) + random.choice(self.id_options) + random.choice(self.id_options)
        game.enemies_id.append(self.id)

    def update(self):

        super().update(self.game.tilemap)

        #if self.rect().colliderect(self.game.player.rect()):
         #  print('GAME OVER!')
           #self.game.exit_game()


class TickEnemy(Enemy):
    def __init__(self, game, pos, size):
        super().__init__(game, pos, size, 'tick_enemy')
        self.velocity = [2, 0]

    def update(self):
        super().update()
        if self.velocity[0] < 0:
            new_pos = (self.pos[0] - 1, self.pos[1] + 1)
            tile_rect = self.game.tilemap.physics_specific_rect(new_pos, (0, 1))
            if not py.Rect(new_pos, self.size).colliderect(tile_rect): # if the tile below where it's about to be isn't collideable it turns
                self.velocity[0] *= -1
            tile_rect = self.game.tilemap.physics_specific_rect(self.pos, (-1, 0))
            if py.Rect(new_pos, self.size).colliderect(tile_rect): # if run into wall, turn
                self.velocity[0] *= -1

        if self.velocity[0] > 0:
            new_pos = (self.pos[0] + self.size[0], self.pos[1] + 1)
            tile_rect = self.game.tilemap.physics_specific_rect(new_pos, (0, 1))
            if not py.Rect(new_pos, self.size).colliderect(tile_rect):
                self.velocity[0] *= -1
            tile_rect = self.game.tilemap.physics_specific_rect(self.pos, (1, 0))
            if py.Rect(new_pos, self.size).colliderect(tile_rect):
                self.velocity[0] *= -1

        for enemy in self.game.enemies:
            if self.rect().colliderect(enemy.rect()) and enemy.id != self.id:
               self.velocity[0] *= -1

class DungEnemy(Enemy):
    def __init__(self, game, pos, size):
        super().__init__(game, pos, size, 'dung_enemy')
        self.x_player_offset = self.pos[0] - self.game.player.pos[0]
        self.y_player_offset = self.pos[1] - self.game.player.pos[1]
        self.projectile_id = '00000000'
        self.time_since_throw = 0
        
        
    def update(self):
        super().update()
        self.x_player_offset = self.pos[0] - self.game.player.pos[0]
        self.y_player_offset = self.pos[1] - self.game.player.pos[1]
        if self.distance_to_player() <= 240 and self.time_since_throw >= 2:
            self.throw_projectile()
            self.time_since_throw = 0
        else: self.time_since_throw += self.game.delta_time/60
    
    def throw_projectile(self):
        while self.projectile_id in self.game.projectiles_id:
            self.projectile_id = random.choice(self.id_options) + random.choice(self.id_options) + random.choice(self.id_options) + random.choice(self.id_options) + random.choice(self.id_options) + random.choice(self.id_options) + random.choice(self.id_options) + random.choice(self.id_options)
        self.game.projectiles_id.append(self.projectile_id)
        self.game.projectiles[self.projectile_id] = Projectile(self.game, self.pos, (4, 4), self.x_player_offset, self.y_player_offset, self.projectile_id)

    def distance_to_player(self):
        return ((self.x_player_offset)**2 + (self.y_player_offset)**2)**0.5

class Projectile(PhysicsEntity):
    def __init__(self, game, pos, size, x_distance_to_player, y_distance_to_player, id):
        super().__init__(game, 'projectile', game.tilemap, pos, size)
        self.set_action('poop')
        self.id = id
        self.falling = -1 # 1 is falling, -1 isn't falling
        self.velocity = [x_distance_to_player/self.game.tilemap.tile_size/2 * -1, (-1 * abs(y_distance_to_player)/self.game.tilemap.tile_size)/2 - 6]
    def update(self):
        super().update(self.game.tilemap)

        if self.velocity[1] > 0:
            self.velocity[1] = round(min(5, self.velocity[1] + 0.15 * self.game.delta_time), 2)
        else:self.velocity[1] = round(min(5, self.velocity[1] + 0.1 * self.game.delta_time), 2)
        

        if self.velocity[1] > 0:
            self.falling = 1
        
        projectile_rect = self.rect()
        for collision in self.collisions.values():
            if collision == True:
                self.game.projectiles_to_delete.append(self.id)
                return
        for enemy in self.game.enemies:
            if projectile_rect.colliderect(enemy.rect()) and enemy.enemy_type != 'dung_enemy':
                self.game.projectiles_to_delete.append(self.id)
                return
        if projectile_rect.colliderect(self.game.player.rect()):
            self.game.projectiles_to_delete.append(self.id)
            return