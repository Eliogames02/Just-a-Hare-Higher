import pygame as py
import math, random

class PhysicsEntity:
    def __init__(self, game, entity_type:str, pos, size):
        self.game = game
        self.tilemap = game.tilemap
        self.entity_type = entity_type
        self.pos = list(pos)
        self.size = size #! Super important! - the size of the entity must be the same size as the image
        self.velocity = [0, 0]
        self.collisions = {'up': False, 'down': False, 'left': False, 'right': False} # all directional collisions
        self.id_options = ['0','1','2','3','4','5','6','7','8', '9', 'A','B','C','D','E','F'] # the options for each position of the id
        self.flip = False # whether the direction of the entity is flipped
        self.action = '' # the current action of the entity
        self.anim_offset = (0, 0) # the offset of the animation from the entity's position

        self.NULL_RECT = py.Rect(-1000, -1000, 1, 1) #! THE NULL RECT IS REAL

    def update(self, gravity_force=[0.125, True, 0.2]) -> None:
        """
        Updates the entity's state.

        Updates the entity's position based on the velocity, handles gravity, horizontal and 
        vertical collisions, normal force, sprite flipping, and the animation getting updated.
        """
        self.collisions = {'up': False, 'down': False, 'left': False, 'right': False} # resets the collisions for the new frame

        # frame movement of the entity to change the position based on the velocity
        frame_movement = [self.velocity[0], self.velocity[1]]

        # handles horizontal collisions
        self.horizontal_collision(frame_movement[0])

        # handles vertical collisions
        self.vertical_collision(frame_movement[1])
        
        # handles gravity
        self.gravity(*gravity_force)

        # handles normal force
        if self.collisions['down'] or self.collisions['up']:
            self.velocity[1] = 0

        # handles sprite flipping based on velocity's direction
        if self.velocity[0] > 0:
            self.flip = False
        elif self.velocity[0] < 0:
            self.flip = True

        # handles the animation getting updated
        self.animation.update()

    # handles horizontal collisions
    def horizontal_collision(self, x_movement) -> bool:
        self.pos[0] += x_movement
        entity_rect = self.rect()
        for rect in self.tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if x_movement > 0:
                    entity_rect.right = rect.left
                    self.collisions['right'] = True
                if x_movement < 0:
                    entity_rect.left = rect.right
                    self.collisions['left'] = True
                self.pos[0] = entity_rect.x
        return (self.collisions['right'] or self.collisions['left'])

    # handles vertical collisions
    def vertical_collision(self, y_movement) -> bool:
        self.pos[1] += y_movement
        entity_rect = self.rect()
        for rect in self.tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if y_movement > 0:
                    entity_rect.bottom = rect.top
                    self.collisions['down'] = True
                if y_movement < 0:
                    entity_rect.top = rect.bottom
                    self.collisions['up'] = True
                self.pos[1] = entity_rect.y
        return (self.collisions['down'] or self.collisions['up'])

    # handles gravity
    def gravity(self, falling_speed, slow_descent=True, descent_multiplier=0.2) -> None:
        if not self.is_touching_ground():
            if self.velocity[1] > 0:
                self.velocity[1] = round(min(5, self.velocity[1] + falling_speed*descent_multiplier if slow_descent else self.velocity[1] + falling_speed), 2)
            else: self.velocity[1] = round(min(5, self.velocity[1] + falling_speed), 2)

    def is_touching_ground(self) -> bool:
        entity_rect = self.rect()
        entity_rect.y += 1
        rect1 = self.tilemap.physics_specific_rect(self.pos, (0, 0))
        rect2 = self.tilemap.physics_specific_rect(self.pos, (0, 1))
        rect3 = self.tilemap.physics_specific_rect(self.pos, (1, 1))
        if entity_rect.colliderect(rect1) or entity_rect.colliderect(rect2) or entity_rect.colliderect(rect3):
            return True
        return False    

    def render(self, surface, offset=(0,0)) -> None:
        surface.blit(py.transform.flip(self.animation.img(), self.flip, False), (self.pos[0] - offset[0] + self.anim_offset[0], self.pos[1] - offset[1] + self.anim_offset[1]))

    def rect(self) -> py.Rect:
        return py.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
    
    def set_action(self, action: str) -> None:
        if action != self.action:
            self.action = action
            self.animation = self.game.assets[self.entity_type + '/' + action].copy()

class Player(PhysicsEntity):
    def __init__(self, game, pos, size):
        super().__init__(game, 'player', pos, size)
        self.COYOTE_TIME = 0.125 # the time the player can jump after leaving the ground while they have a jump left
        self.air_time = 0 # the time since the player left the ground
        self.jumps = 1
        self.set_action('idle')

    def update(self):
        super().update()

    def is_touching_ground(self) -> bool:
        answer = super().is_touching_ground()
        if answer:
            self.air_time = 0
            self.jumps = 1
            return answer
        self.air_time += (1/60) # should add 1 second for every second the player doesn't touch the ground
        if self.air_time > self.COYOTE_TIME:
            self.jumps = 0
        return False
    
class Collectible(PhysicsEntity):
    def __init__(self, game, pos, size, variant=0):
        super().__init__(game, 'collectible', pos, size)
        self.is_collected = False
        self.variant = variant # 0 for carrot, 1 for radish
        if self.variant == 0:
            self.set_action('carrot')
        else: self.set_action('radish')

    def update(self):
        self.pos[1] += math.sin(py.time.get_ticks()/250) * 0.5
        self.collected()
    
    def collected(self):
        if self.rect().colliderect(self.game.player.rect()):
            if self.variant == 0:
                self.game.score += 1
            else: self.game.super_score += 1
            self.game.collectibles.remove(self)
            return True
        return False
    
class Enemy(PhysicsEntity):
    def __init__(self, game, enemy_type, pos, size, id='00000000'):
        super().__init__(game, enemy_type, pos, size)
        self.set_action('idle')
        self.id = id
        self.enemy_type = enemy_type

        while self.id in game.enemies_id:
            self.id = random.choice(self.id_options) + random.choice(self.id_options) + random.choice(self.id_options) + random.choice(self.id_options) + random.choice(self.id_options) + random.choice(self.id_options) + random.choice(self.id_options) + random.choice(self.id_options)
        game.enemies_id.append(self.id)

class TickEnemy(Enemy):
    def __init__(self, game, pos, size):
        super().__init__(game, 'tick_enemy', pos, size)
        self.velocity = [2, 0]

    def update(self):
        super().update()
        if self.velocity[0] < 0:
            new_pos = (self.pos[0] - 1, self.pos[1] + 1)
            tile_rect = self.tilemap.physics_specific_rect(new_pos, (0, 1)) # collision underneath
            if not py.Rect(new_pos, self.size).colliderect(tile_rect): # if the tile below where it's about to be isn't collideable it turns
                self.velocity[0] *= -1
            tile_rect = self.tilemap.physics_specific_rect(self.pos, (-1, 0)) # collision to the left
            if py.Rect(new_pos, self.size).colliderect(tile_rect): # if run into wall, turn
                self.velocity[0] *= -1

        if self.velocity[0] > 0:
            new_pos = (self.pos[0] + self.size[0], self.pos[1] + 1)
            tile_rect = self.tilemap.physics_specific_rect(new_pos, (0, 1)) # collision underneath
            if not py.Rect(new_pos, self.size).colliderect(tile_rect):
                self.velocity[0] *= -1
            tile_rect = self.tilemap.physics_specific_rect(self.pos, (1, 0)) # collision to the right
            if py.Rect(new_pos, self.size).colliderect(tile_rect):
                self.velocity[0] *= -1

        for enemy in self.game.enemies:
            if self.rect().colliderect(enemy.rect()) and enemy.id != self.id:
               self.velocity[0] *= -1

class DungEnemy(Enemy):
    def __init__(self, game, pos, size):
        super().__init__(game, 'dung_enemy', pos, size)
        self.x_player_offset = self.pos[0] - self.game.player.pos[0]
        self.y_player_offset = self.pos[1] - self.game.player.pos[1]
        self.projectile_id = '00000000'
        self.time_since_throw = 0
        
    def update(self):
        super().update()
        self.x_player_offset = self.pos[0] - self.game.player.pos[0] # updates the x offset between the enemy and the player
        self.y_player_offset = self.pos[1] - self.game.player.pos[1] # updates the y offset between the enemy and the player
        if self.distance_to_player() <= 240 and self.time_since_throw >= 2:
            self.throw_projectile()
            self.time_since_throw = 0
        else: self.time_since_throw += 1/60

    def throw_projectile(self):
        while self.projectile_id in self.game.projectiles_id:
            self.projectile_id = random.choice(self.id_options) + random.choice(self.id_options) + random.choice(self.id_options) + random.choice(self.id_options) + random.choice(self.id_options) + random.choice(self.id_options) + random.choice(self.id_options) + random.choice(self.id_options)
        self.game.projectiles_id.append(self.projectile_id)
        self.game.projectiles[self.projectile_id] = Projectile(self.game, (self.pos[0] + (self.size[0]/2), self.pos[1] - 4), (4, 4), self.x_player_offset, self.y_player_offset, self.projectile_id)

    def distance_to_player(self):
        return ((self.x_player_offset)**2 + (self.y_player_offset)**2)**0.5 # pythagorean theorem used to calculate distance

class Projectile(PhysicsEntity):
    def __init__(self, game, pos, size, x_distance_to_player, y_distance_to_player, id):
        super().__init__(game, 'projectile', pos, size)
        self.set_action('idle')
        self.id = id
        self.y_player_offset = y_distance_to_player
        self.falling = -1 # 1 is falling, 0 isn't falling
        self.velocity = [-1/60 * x_distance_to_player, (-1/60 * y_distance_to_player) - 3.151592653589793]
    def update(self):
        if self.y_player_offset != 0:
            gravity = [0.125, True, 0.5]
        else: gravity = [0.125, False, 1]
        super().update(gravity)

        if self.velocity[1] > 0:
            self.velocity[1] = round(min(5, max(-5, self.velocity[1])), 2)
        else:  
            self.velocity[1] = round(min(5, max(-5, self.velocity[1])), 2)

        if self.velocity[1] > 0:
            self.falling = 1
        
        projectile_rect = self.rect()
        for collision in self.collisions.values():
            if collision == True: # if the projectile is colliding with anything
                self.game.projectiles_to_delete.append(self.id) 
                return
        for enemy in self.game.enemies:
            if projectile_rect.colliderect(enemy.rect()) and enemy.enemy_type != 'dung_enemy': #* Could damage enemies
                self.game.projectiles_to_delete.append(self.id) 
                return
        if projectile_rect.colliderect(self.game.player.rect()): #* Needs to send some signal to player or the game to end it, or deal damage to player
            self.game.projectiles_to_delete.append(self.id) 
            return