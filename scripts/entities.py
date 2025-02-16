import pygame as py
import math, random

class PhysicsEntity:
    def __init__(self, game, entity_type:str, pos, size):
        """
        Initializes a PhysicsEntity instance with the given parameters.

        Args:
            game: The game instance to which this entity belongs.
            entity_type (str): The type of the entity, used for identifying it.
            pos (tuple): The initial position of the entity as a (x, y) tuple.
            size (tuple): The size of the entity as a (width, height) tuple.

        Attributes:
            game: The game instance to which this entity belongs.
            tilemap: The tilemap associated with the game.
            entity_type (str): The type of the entity.
            pos (list): The current position of the entity.
            size (tuple): The size of the entity.
            velocity (list): The current velocity of the entity.
            collisions (dict): A dictionary tracking collision states in four directions.
            id_options (list): Possible characters for generating entity IDs.
            flip (bool): Indicates whether the entity's direction is flipped. True for left, False for right.
            action (str): The current action of the entity. Used for handling sprites easier.
            anim_offset (tuple): The offset of the animation from the entity's position.
            NULL_RECT (py.Rect): A constant representing a null rectangle.
        """
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
        self.offscreen_offset = 256 # the amount of pixels offscreen before the entity isn't updated

        self.NULL_RECT = py.Rect(-1000, -1000, 1, 1) #! THE NULL RECT IS REAL

    def update(self, gravity_force=[0.125, True, 0.2]) -> None:
        """
        Updates the physics entity's state for the current frame.

        This function resets collision states, calculates the frame movement based on
        the entity's velocity, and handles horizontal and vertical collisions. It applies
        gravity to the entity, adjusts the velocity based on normal forces, and updates
        the entity's sprite flip direction based on its horizontal movement. Additionally,
        it updates the entity's animation state.

        Args:
            gravity_force (list, optional): A list containing gravity parameters.
                Defaults to [0.125, True, 0.2].
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

    
    def horizontal_collision(self, x_movement) -> bool:
        """
        Handles horizontal collisions for the entity.

        Moves the entity by the given x movement and checks for collisions with
        the physics tiles around its position. If a collision is found, the
        entity's position is adjusted to be exactly at the collision point and
        the corresponding collision state is set to True.

        Args:
            x_movement (float): The amount of horizontal movement to apply to the entity.

        Returns:
            bool: Whether any horizontal collision was detected.
        """

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
        """
        Handles vertical collisions for the entity.

        Moves the entity by the given y movement and checks for collisions with
        the physics tiles around its position. If a collision is found, the
        entity's position is adjusted to be exactly at the collision point and
        the corresponding collision state is set to True.

        Args:
            y_movement (float): The amount of vertical movement to apply to the entity.

        Returns:
            bool: Whether any vertical collision was detected.
        """

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
        """
        Applies gravity to the entity.

        If the entity is not touching the ground, increases the entity's vertical
        velocity by the given falling speed. If the entity's vertical velocity is
        positive (i.e. it is falling), it will be increased by the falling speed
        multiplied by the descent multiplier if slow_descent is True, otherwise
        it will be increased by the falling speed directly. If the entity's
        vertical velocity is negative (i.e. it is jumping), it will be increased
        by the falling speed directly. The entity's vertical velocity is capped
        at 5.

        Args:
            falling_speed (float): The speed at which the entity falls.
            slow_descent (bool, optional): Whether to slow down the entity's
                descent. Defaults to True.
            descent_multiplier (float, optional): The multiplier to apply to the
                falling speed when slow_descent is True. Defaults to 0.2.
        """
        if not self.is_touching_ground():
            if self.velocity[1] > 0:
                self.velocity[1] = round(min(5, self.velocity[1] + falling_speed*descent_multiplier if slow_descent else self.velocity[1] + falling_speed), 2)
            else: self.velocity[1] = round(min(5, self.velocity[1] + falling_speed), 2)

    def is_touching_ground(self) -> bool:
        """
        Checks if the entity is currently touching the ground.

        Returns True if the entity is currently standing on a physics tile, False otherwise.

        The check is done by offsetting the entity's rect by one pixel down and checking if it collides with any of the three
        tiles below it (center, left, and right). If any collision is found, the function returns True, otherwise it returns False.
        """
        entity_rect = self.rect()
        entity_rect.y += 1
        rect1 = self.tilemap.physics_specific_rect(self.pos, (0, 0))
        rect2 = self.tilemap.physics_specific_rect(self.pos, (0, 1))
        rect3 = self.tilemap.physics_specific_rect(self.pos, (1, 1))
        if entity_rect.colliderect(rect1) or entity_rect.colliderect(rect2) or entity_rect.colliderect(rect3):
            return True
        return False    

    def render(self, surface, offset=(0,0)) -> None:
        '''
        Renders the entity's current animation onto the given surface at the given offset, with the animation flipped horizontally if the entity is facing left.
        
        Args:
            surface (pygame.Surface): The surface to render the entity onto.
            offset (tuple, optional): The offset from the top left corner of the surface to render the entity at, given as a tuple of (x, y) coordinates. Defaults to (0, 0).
        '''
        surface.blit(py.transform.flip(self.animation.img(), self.flip, False), (self.pos[0] - offset[0] + self.anim_offset[0], self.pos[1] - offset[1] + self.anim_offset[1]))

    def rect(self) -> py.Rect:
        """
        Returns the pygame.Rect representation of the entity's position and size.

        This rectangle is used for collision detection and rendering.

        Returns:
            py.Rect: A rectangle with the entity's current position and size.
        """

        return py.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
    
    def set_action(self, action: str) -> None:
        """
        Sets the current action of the entity and updates its animation accordingly.

        If the specified action is different from the current action, the entity's
        action is updated and the animation is reset based on the new action.

        Args:
            action (str): The new action to set for the entity.
        """

        if action != self.action:
            self.action = action
            self.animation = self.game.assets[self.entity_type + '/' + action].copy()

class Player(PhysicsEntity):
    def __init__(self, game, pos, size):
        """
        Initializes a Player instance.

        Args:
            game: The game instance to which this player belongs.
            pos (tuple): The initial position of the player as a (x, y) tuple.
            size (tuple): The size of the player as a (width, height) tuple.

        Attributes:
            COYOTE_TIME (float): The time the player can jump after leaving the ground while they have a jump left.
            air_time (float): The time since the player left the ground.
            jumps (int): The number of jumps the player has left.
        """

        super().__init__(game, 'player', pos, size)
        self.COYOTE_TIME = 0.25 # the time the player can jump after leaving the ground while they have a jump left
        self.air_time = 0 # the time since the player left the ground
        self.jumps = 1
        self.set_action('idle')

    def update(self):
        """
        Updates the player's state for the current frame.

        Calls the parent class's update method and updates the player's jump state accordingly.
        """
        if self.game.debug == False:
            super().update()
        else:
            self.pos[0] += self.velocity[0]
            self.pos[1] += self.velocity[1]

        # if collide with enemy / projectile, reset level

    def is_touching_ground(self) -> bool:
        """
        Checks if the player is currently touching the ground.

        Checks if the player is touching the ground by calling the parent class's is_touching_ground method.
        If the player is touching the ground, resets the air time and sets the number of jumps to 1.
        If the player is not touching the ground, increments the air time and sets the number of jumps to 0 if the air time exceeds the COYOTE_TIME.
        """
        
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
        """
        Initializes a Collectible instance with the given parameters.

        Args:
            game: The game instance to which this collectible belongs.
            pos (tuple): The initial position of the collectible as a (x, y) tuple.
            size (tuple): The size of the collectible as a (width, height) tuple.
            variant (int, optional): The variant of the collectible. Defaults to 0.
                - 0: Carrot
                - 1: Radish
                - 2: Finish(the end of the level)

        Attributes:
            is_collected (bool): Indicates whether the collectible has been collected.
            variant (int): The variant of the collectible, used to determine the action.
        """
        super().__init__(game, 'collectible', pos, size)
        self.is_collected = False
        self.variant = variant # 0 for carrot, 1 for radish
        if self.variant == 0:
            self.set_action('carrot')
        elif self.variant == 1:
            self.set_action('radish')
        else: self.set_action('finish')

    def update(self):
        """
        Updates the collectible's position and checks for collection.

        This method adjusts the collectible's vertical position to create a floating effect
        and calls the `collected` method to check if the player has collected the item.
        """

        self.pos[1] += math.sin(py.time.get_ticks()/250) * 0.5
        self.collected()
    
    def collected(self):
        """
        Checks if the player has collected the item.

        This method checks if the player's rectangle is colliding with the
        collectible's rectangle. If so, it increments the game's score or
        super score, depending on the variant of the collectible, and removes
        the collectible from the game. If the variant is 2, it ends the level.

        Returns:
            bool: Whether the collectible was collected.
        """
        if self.rect().colliderect(self.game.player.rect()):
            if self.variant == 0:
                self.game.score += 1
            elif self.variant == 1: 
                self.game.super_score += 1
            else: 
                self.game.end_level()
            self.game.collectibles.remove(self)
            return True
        return False
    
class Enemy(PhysicsEntity):
    def __init__(self, game, enemy_type, pos, size, id='00000000'):
        """
        Initializes an Enemy instance with the given parameters.

        Args:
            game: The game instance to which this enemy belongs.
            enemy_type (str): The type of the enemy, used for identifying it.
            pos (tuple): The initial position of the enemy as a (x, y) tuple.
            size (tuple): The size of the enemy as a (width, height) tuple.
            id (str, optional): The ID of the enemy. Defaults to '00000000'.
        """

        super().__init__(game, enemy_type, pos, size)
        self.set_action('idle')
        self.id = id
        self.enemy_type = enemy_type

        while self.id in game.enemies_id:
            self.id = random.choice(self.id_options) + random.choice(self.id_options) + random.choice(self.id_options) + random.choice(self.id_options) + random.choice(self.id_options) + random.choice(self.id_options) + random.choice(self.id_options) + random.choice(self.id_options)
        game.enemies_id.append(self.id)
    
    def update(self):
        """
        Updates the enemy's position and handles collisions.

        This method updates the position of the enemy by checking its velocity
        and adjusting its direction when necessary. It checks for collisions with
        tiles below and beside the enemy to determine if it should turn around. If
        the enemy is about to move off a platform or run into a wall, its
        horizontal velocity is reversed. Additionally, the method checks for
        collisions with other enemies, and reverses direction upon collision to
        prevent overlap.
        """
        if self.pos[0] + self.size[0] < self.game.scroll[0]-self.offscreen_offset or self.pos[0] > self.game.scroll[0] + self.game.width + self.offscreen_offset or self.pos[1] + self.size[1] < self.game.scroll[1]-self.offscreen_offset or self.pos[1] > self.game.scroll[1] + self.game.height + self.offscreen_offset:
            return
        super().update()

class TickEnemy(Enemy):
    def __init__(self, game, pos, size):
        """
        Initializes a TickEnemy instance with the given parameters.

        Args:
            game: The game instance to which this enemy belongs.
            pos (tuple): The initial position of the enemy as a (x, y) tuple.
            size (tuple): The size of the enemy as a (width, height) tuple.

        Attributes:
            velocity (list): The initial velocity of the tick enemy.
        """
        super().__init__(game, 'tick_enemy', pos, size)
        self.velocity = [random.choice([-1.2,-1,-0.8,0.8,1,1.2])*2.5, 0]

    def update(self):
        """
        Updates the TickEnemy's position and handles collisions.

        This method updates the position of the TickEnemy by checking its velocity
        and adjusting its direction when necessary. It checks for collisions with
        tiles below and beside the enemy to determine if it should turn around. If
        the TickEnemy is about to move off a platform or run into a wall, its
        horizontal velocity is reversed. Additionally, the method checks for
        collisions with other enemies, and reverses direction upon collision to
        prevent overlap.
        """

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
            if self.rect().colliderect(enemy.rect()) and enemy.id != self.id and enemy.enemy_type == 'tick_enemy':
               self.velocity[0] *= -1

        if self.rect().colliderect(self.game.player.rect()):
            self.game.reset_level()

class DungEnemy(Enemy):
    def __init__(self, game, pos, size):
        """
        Initializes a DungEnemy instance with the given parameters.

        Args:
            game: The game instance to which this enemy belongs.
            pos (tuple): The initial position of the enemy as a (x, y) tuple.
            size (tuple): The size of the enemy as a (width, height) tuple.

        Attributes:
            x_player_offset (float): The horizontal offset between the enemy and the player.
            y_player_offset (float): The vertical offset between the enemy and the player.
            projectile_id (str): The ID of the projectile to be thrown by the enemy.
            time_since_throw (float): The time elapsed since the last projectile was thrown.
        """

        super().__init__(game, 'dung_enemy', pos, size)
        self.x_player_offset = self.pos[0] - self.game.player.pos[0]
        self.y_player_offset = self.pos[1] - self.game.player.pos[1]
        self.projectile_id = '00000000'
        self.time_since_throw = 0
        
    def update(self):
        """
        Updates the DungEnemy's state for the current frame.

        This method updates the position offsets between the DungEnemy and the player,
        checks the distance to the player, and throws a projectile if within range
        and enough time has passed since the last throw. The time since the last
        projectile throw is incremented each frame.
        """

        super().update()
        self.x_player_offset = self.pos[0] - self.game.player.pos[0] # updates the x offset between the enemy and the player
        self.y_player_offset = self.pos[1] - self.game.player.pos[1] # updates the y offset between the enemy and the player
        if self.distance_to_player() <= 200 and self.time_since_throw >= 2.5:
            self.throw_projectile()
            self.time_since_throw = 0
        else: self.time_since_throw += 1/60

        if self.rect().colliderect(self.game.player.rect()):
            self.game.reset_level()

    def throw_projectile(self):
        """
        Throws a projectile from the DungEnemy's position towards the player.

        This function generates a new ID for the projectile, appends it to the game's projectile IDs,
        and creates a new Projectile instance with the player as the target and the DungEnemy's position
        as the start position.
        """
        while self.projectile_id in self.game.projectiles_id:
            self.projectile_id = random.choice(self.id_options) + random.choice(self.id_options) + random.choice(self.id_options) + random.choice(self.id_options) + random.choice(self.id_options) + random.choice(self.id_options) + random.choice(self.id_options) + random.choice(self.id_options)
        self.game.projectiles_id.append(self.projectile_id)
        self.game.projectiles[self.projectile_id] = Projectile(self.game, (self.pos[0] + (self.size[0]/2), self.pos[1] - 4), (4, 4), self.x_player_offset, self.y_player_offset, self.projectile_id)

    def distance_to_player(self):
        """
        Calculates the distance between the enemy and the player.

        The distance is calculated using the pythagorean theorem, taking into
        account the x and y offsets between the enemy and the player.

        Returns:
            float: The distance between the enemy and the player.
        """
        
        return ((self.x_player_offset)**2 + (self.y_player_offset)**2)**0.5 # pythagorean theorem used to calculate distance

class Projectile(PhysicsEntity):
    def __init__(self, game, pos, size, x_distance_to_player, y_distance_to_player, id):
        """
        Initializes a Projectile instance with the given parameters.

        Args:
            game: The game instance to which this projectile belongs.
            pos (tuple): The initial position of the projectile as a (x, y) tuple.
            size (tuple): The size of the projectile as a (width, height) tuple.
            x_distance_to_player (float): The x offset between the projectile and the player.
            y_distance_to_player (float): The y offset between the projectile and the player.
            id (str): The ID of the projectile.

        Attributes:
            game: The game instance to which this projectile belongs.
            id (str): The ID of the projectile.
            y_player_offset (float): The y offset between the projectile and the player.
            falling (int): 1 if falling, 0 if not falling.
            velocity (list): The initial velocity of the projectile as a [x, y] list.
        """
        super().__init__(game, 'projectile', pos, size)
        self.set_action('idle')
        self.id = id
        self.y_player_offset = y_distance_to_player
        self.falling = -1 # 1 is falling, 0 isn't falling
        self.velocity = [-1/60 * x_distance_to_player, (-1/60 * y_distance_to_player) - 3.151592653589793]
    def update(self):
        """
        Updates the Projectile's state for the current frame.

        This function updates the gravity force based on whether the projectile is
        falling or not, and updates the projectile's position with the new gravity.
        It also checks for collisions with other objects, and if a collision is
        detected, it marks the projectile to be deleted.

        """
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
        if projectile_rect.colliderect(self.game.player.rect()): #* Needs to send some signal to player or the game to end it, or deal damage to player 
            self.game.reset_level()
            return
        for collision in self.collisions.values():
            if collision == True: # if the projectile is colliding with anything
                self.game.projectiles_to_delete.append(self.id) 
                return
        for enemy in self.game.enemies:
            if projectile_rect.colliderect(enemy.rect()) and enemy.enemy_type != 'dung_enemy': #* Could damage enemies
                self.game.projectiles_to_delete.append(self.id) 
                return
        

class MoleEnemy(Enemy):
    def __init__(self, game, pos, size):
        super().__init__(game, 'mole_enemy', [pos[0], pos[1]-1], size)
    
    def update(self):
        self.anim_offset = [0, 1]
        if self.rect().colliderect(self.game.player.rect()):
            self.game.player.pos[1] += 48