"""
File: skeet.py
Original Author: Lucas Monteiro

import arcade
import math
import random

# These are Global constants to use throughout the game
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 500

RIFLE_WIDTH = 100
RIFLE_HEIGHT = 20
RIFLE_COLOR = arcade.color.DARK_RED

BULLET_RADIUS = 3
BULLET_COLOR = arcade.color.BLACK_OLIVE
BULLET_SPEED = 10

TARGET_RADIUS = 20
TARGET_COLOR = arcade.color.CARROT_ORANGE
TARGET_SAFE_COLOR = arcade.color.AIR_FORCE_BLUE
TARGET_SAFE_RADIUS = 15

SPRITE_SCALING_PLAYER = 0.5
SPRITE_SCALING_COIN = .25
COIN_COUNT = 50
SCREEN_TITLE = "Skeet, by Lucas Monteiro"

class Point:
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        
class Velocity:
    def __init__(self):
        self.dx = 0.0
        self.dy = 0.0

class Base:
    def __init__(self):
        self.center = Point()
        self.velocity = Velocity()
        self.radius = 0.0
        self.alive = True
        
    def advance(self):
        self.center.x += self.velocity.dx
        self.center.y += self.velocity.dy
        
    def is_off_screen(self, SCREEN_WIDTH, SCREEN_HEIGHT):
        if self.center.x > SCREEN_WIDTH or self.center.y > SCREEN_HEIGHT:
            return True
        if self.center.x < 0 or self.center.y < 0:
            return True
        
class Bullet(Base):
    def __init__(self):
        super().__init__()
        self.radius = BULLET_RADIUS
        self.velocity.dx = BULLET_SPEED
        self.velocity.dy = BULLET_SPEED
        
    def draw(self):
        arcade.draw_circle_filled(self.center.x, self.center.y, BULLET_RADIUS, BULLET_COLOR)
    
    def fire(self, angle):
        self.velocity.dx = math.cos(math.radians(angle)) * BULLET_SPEED
        self.velocity.dy = math.sin(math.radians(angle)) * BULLET_SPEED
            
class Target(Base):
    def __init__(self):
        super().__init__()
        self.radius = TARGET_RADIUS
        self.center.x = random.uniform(0, SCREEN_WIDTH // 2)
        self.center.y = random.uniform(SCREEN_HEIGHT // 2, SCREEN_HEIGHT)
        self.velocity.dx = random.uniform(1, 5)
        self.velocity.dy = random.uniform(-2, 5)

    def draw(self):
        arcade.draw_circle_filled(self.center.x, self.center.y, TARGET_RADIUS, TARGET_COLOR)  
        
    def bounce_horizontal (self):
        self.velocity.dx *= -1
        
    def bounce_vertical (self):
        self.velocity.dy *= -1
        
class Standard_Target(Target):
    def __init__(self):
        self.check_hit = 1
        super().__init__()
        
    def hit(self):
        self.check_hit -= 1
        self.alive = False
        return 1
    
class Standard_Target_Hard(Standard_Target):
    def __init__(self):
        super().__init__()
        
    def hit(self):
        return super().hit()
    
    def draw(self):
        arcade.draw_circle_filled(self.center.x, self.center.y, 10, arcade.color.RED)
        
class Average_Target(Target):
    def __init__(self):
        super().__init__()
        self.velocity.dx = random.uniform(1, 3)
        self.velocity.dy = random.uniform(-2, 3)
        self.check_hit = 2
    
    def hit(self):
        self.check_hit -= 1
        if self.check_hit < 3 and self.check_hit > 0:
            return 1
        else:
            self.alive = False
            return 2
        
    def draw(self):
        arcade.draw_circle_filled(self.center.x, self.center.y, self.radius, arcade.color.DARK_BYZANTIUM)
        text_x = self.center.x - (self.radius / 2)
        text_y = self.center.y - (self.radius / 2)
        arcade.draw_text(repr(self.check_hit), text_x, text_y, arcade.color.WHITE, font_size=20)    
    
class Strong_Target(Target):
    def __init__(self):
        super().__init__()
        self.velocity.dx = random.uniform(1, 3)
        self.velocity.dy = random.uniform(-2, 3)
        self.check_hit = 3
        
    def hit(self):
        self.check_hit -= 1
        if self.check_hit < 3 and self.check_hit > 0:
            return 1
        else:
            self.alive = False
            return 5
        
    def draw(self):
        arcade.draw_circle_filled(self.center.x, self.center.y, self.radius, arcade.color.BABY_BLUE)
        text_x = self.center.x - (self.radius / 2)
        text_y = self.center.y - (self.radius / 2)
        arcade.draw_text(repr(self.check_hit), text_x, text_y, arcade.color.BLACK, font_size=20)
        
class Strong_Target_Hard(Strong_Target):
    def __init__(self):
        super().__init__()
        
    def hit(self):
        super().hit()

    def draw(self):
        arcade.draw_circle_filled(self.center.x, self.center.y, 8, arcade.color.BABY_BLUE)
        text_x = self.center.x - (8 / 2)
        text_y = self.center.y - (8 / 2)
        arcade.draw_text(repr(self.check_hit), text_x, text_y, arcade.color.BLACK, font_size=10)      
        
class Safe_Target(Target):
    def __init__(self):
        super().__init__()
        self.check_hit = 0
        
    def hit(self):
        self.check_hit -= 1
        if self.check_hit < 0:
            self.alive = False          
        return -10
        
    def draw(self):
        arcade.draw_rectangle_filled(self.center.x, self.center.y, 40, 40, arcade.color.BLACK)
        
class Safe_Target_Hard(Safe_Target):
    def __init__(self):
        super().__init__()
        
    def hit(self):
        super().hit()
        
    def draw(self):
        super().draw()
        
class Rifle:
    """
    The rifle is a rectangle that tracks the mouse.
    """
    def __init__(self):
        self.center = Point()
        self.center.x = 0
        self.center.y = 0

        self.angle = 45

    def draw(self):
        arcade.draw_rectangle_filled(self.center.x, self.center.y, RIFLE_WIDTH, RIFLE_HEIGHT, RIFLE_COLOR, 360-self.angle)

class Game(arcade.View):
    """
    This class handles all the game callbacks and interaction
    It assumes the following classes exist:
        Rifle
        Target (and it's sub-classes)
        Point
        Velocity
        Bullet

    This class will then call the appropriate functions of
    each of the above classes.

    You are welcome to modify anything in this class, but mostly
    you shouldn't have to. There are a few sections that you
    must add code to.
    """

    def __init__(self, width, height):
        #pylint: disable=unused-argument"
        """
        Sets up the initial conditions of the game
        :param width: Screen width
        :param height: Screen height
        """
        super().__init__()

        self.rifle = Rifle()
        self.score = 0

        self.bullets = []

        # TODO: Create a list for your targets (similar to the above bullets)
        self.targets = []

        arcade.set_background_color(arcade.color.WHITE)
        self.window.set_mouse_visible(True)
        
        self.target = Safe_Target()
        self.target_hard = Safe_Target_Hard()

    def on_draw(self):
        """
        Called automatically by the arcade framework.
        Handles the responsibility of drawing all elements.
        """

        # clear the screen to begin drawing
        arcade.start_render()

        # draw each object
        self.rifle.draw()

        for bullet in self.bullets:
            bullet.draw()

        # TODO: iterate through your targets and draw them...
        for target in self.targets:
            target.draw()

        self.draw_score()
        
        self.draw_level()

    def draw_score(self):
        """
        Puts the current score on the screen
        """
        score_text = "Score: {}".format(self.score)
        start_x = 10
        start_y = SCREEN_HEIGHT - 20
        arcade.draw_text(score_text, start_x=start_x, start_y=start_y, font_size=12, color=arcade.color.BLACK)
    
    def draw_level(self):
        
        """
        Puts the current level on the screen
        """
        level_info = ""      
 
        if self.score >= 0 and self.score < 30:
            level_info = "LEVEL 1"
        elif self.score >= 30 and self.score < 70:
            level_info = "LEVEL 2"
        elif self.score >= 70 and self.score < 100:
            level_info = "LEVEL 3"                
            
        start_x = SCREEN_WIDTH // 2
        start_y = SCREEN_HEIGHT - 20
        
        arcade.draw_text(level_info, start_x=start_x, start_y=start_y, font_size=12, color=arcade.color.BLACK)       
    
    def update(self, delta_time):
        """
        Update each object in the game.
        :param delta_time: tells us how much time has actually elapsed
        """
        self.check_collisions()
        self.check_off_screen()

        # decide if we should start a target
        if self.score <= 25:
            if random.randint(1, 100) == 1:
                self.create_target()
        elif self.score <= 50:
            if random.randint(1, 75) == 1:
                self.create_target()
        else:
            if random.randint(1, 50) == 1:
                self.create_target()   

        for bullet in self.bullets:
            bullet.advance()

        # TODO: Iterate through your targets and tell them to advance
        for target in self.targets:
            target.advance()
        
        self.check_bounce()
        
        self.draw_level()
        
        if self.score < 0:
            view = GameOverView()
            self.window.show_view(view)
        elif self.score >= 100:
            view = WinView()
            self.window.show_view(view) 

    def create_target(self):
        """
        Creates a new target of a random type and adds it to the list.
        :return:
        """

        # TODO: Decide what type of target to create and append it to the list
        new_target = random.randint(1,4)
        
        if new_target == 1 and self.score < 30:
            target = Standard_Target()
            self.targets.append(target)
        elif new_target == 1 and self.score >= 30:
            target = Standard_Target_Hard()
            self.targets.append(target)
        elif new_target == 2 and self.score < 30:
            target = Strong_Target()
            self.targets.append(target)
        elif new_target == 2 and self.score >= 30:
            target = Strong_Target_Hard()
            self.targets.append(target)   
        elif new_target == 3 and self.score < 30:
            target = Safe_Target()
            self.targets.append(target)
        elif new_target == 3 and self.score >= 30:
            target = Safe_Target_Hard()
            self.targets.append(target)
        elif new_target == 4:
            target = Average_Target()
            self.targets.append(target)    
            

    def check_collisions(self):
        """
        Checks to see if bullets have hit targets.
        Updates scores and removes dead items.
        :return:
        """

        # NOTE: This assumes you named your targets list "targets"

        for bullet in self.bullets:
            for target in self.targets:

                # Make sure they are both alive before checking for a collision
                if bullet.alive and target.alive:
                    too_close = bullet.radius + target.radius
                    
                    if (abs(bullet.center.x - target.center.x) < too_close and
                                abs(bullet.center.y - target.center.y) < too_close):
                        # its a hit!
                        bullet.alive = False
                        self.score += target.hit()

                        # We will wait to remove the dead objects until after we
                        # finish going through the list

        # Now, check for anything that is dead, and remove it
        self.cleanup_zombies()       
      

    def cleanup_zombies(self):
        """
        Removes any dead bullets or targets from the list.
        :return:
        """
        for bullet in self.bullets:
            if not bullet.alive:
                self.bullets.remove(bullet)

        for target in self.targets:
            if not target.alive:
                self.targets.remove(target)

    def check_off_screen(self):
        """
        Checks to see if bullets or targets have left the screen
        and if so, removes them from their lists.
        :return:
        """
        for bullet in self.bullets:
            if bullet.is_off_screen(SCREEN_WIDTH, SCREEN_HEIGHT):
                self.bullets.remove(bullet)

        for target in self.targets:
            if target.is_off_screen(SCREEN_WIDTH, SCREEN_HEIGHT):                self.targets.remove(target)

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        # set the rifle angle in degrees
        self.rifle.angle = self._get_angle_degrees(x, y)

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        # Fire!
        angle = self._get_angle_degrees(x, y)

        bullet = Bullet()
        
        bullet.fire(angle)
        self.bullets.append(bullet)
            

    def _get_angle_degrees(self, x, y):
        """
        Gets the value of an angle (in degrees) defined
        by the provided x and y.

        Note: This could be a static method, but we haven't
        discussed them yet...
        """
        # get the angle in radians
        angle_radians = math.atan2(y, x)

        # convert to degrees
        angle_degrees = math.degrees(angle_radians)

        return angle_degrees
    
    def check_bounce(self):
        """
        Checks to see if the ball has hit the borders
        of the screen and if so, calls its bounce methods.
        """
        for target in self.targets:
            if target.center.x > (SCREEN_WIDTH - TARGET_RADIUS) and target.velocity.dx > 0:
                target.bounce_horizontal()
            if target.center.y < TARGET_RADIUS and target.velocity.dy < 0:
                target.bounce_vertical()
            if target.center.y > (SCREEN_HEIGHT - TARGET_RADIUS) and target.velocity.dy > 0:
                target.bounce_vertical()
                
class InstructionView(arcade.View):
    def __init__(self):
        super().__init__()
    
    def on_show(self):
        """ This is run once when we switch to this view """
        arcade.set_background_color(arcade.csscolor.DARK_GREEN)

        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, SCREEN_WIDTH - 1, 0, SCREEN_HEIGHT - 1)
    
    def on_draw(self):
        """ Draw this view """
        arcade.start_render()
        arcade.draw_text("You score by destroying the ball targets.\nIf you hit any square target, you'll lose a \nlife and score.", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                         arcade.color.WHITE, font_size=15, anchor_x="center")
        arcade.draw_text("Click to PLAY", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2-75,
                         arcade.color.WHITE, font_size=20, anchor_x="center")
   
   
    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """ If the user presses the mouse button, start the game. """
        game_view = Game(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.window.show_view(game_view)
        
class GameOverView(arcade.View):
    """ View to show when game is over """

    def __init__(self):
        """ This is run once when we switch to this view """
        super().__init__()
        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, SCREEN_WIDTH - 1, 0, SCREEN_HEIGHT - 1)

    def on_show(self):
        """ This is run once when we switch to this view """
        arcade.set_background_color(arcade.csscolor.DARK_RED)

        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, SCREEN_WIDTH - 1, 0, SCREEN_HEIGHT - 1)
    
    def on_draw(self):
        """ Draw this view """
        arcade.start_render()
        arcade.draw_text("I'm sorry", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 1.5,
                         arcade.color.WHITE, font_size=15, anchor_x="center")
        arcade.draw_text("GAME OVER :(", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                         arcade.color.WHITE, font_size=50, anchor_x="center")
        arcade.draw_text("Press to PLAY AGAIN", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2-75,
                         arcade.color.WHITE, font_size=20, anchor_x="center")
   
   
    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """ If the user presses the key button, start the game. """
        game_view = Game(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.window.show_view(game_view)

class WinView(arcade.View):
    """ View to show when game is over """

    def __init__(self):
        """ This is run once when we switch to this view """
        super().__init__()
        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, SCREEN_WIDTH - 1, 0, SCREEN_HEIGHT - 1)

    def on_show(self):
        """ This is run once when we switch to this view """
        arcade.set_background_color(arcade.csscolor.DARK_BLUE)

        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, SCREEN_WIDTH - 1, 0, SCREEN_HEIGHT - 1)
    
    def on_draw(self):
        """ Draw this view """
        arcade.start_render()
        arcade.draw_text("You Win !!!", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                         arcade.color.WHITE, font_size=50, anchor_x="center")
        arcade.draw_text("Press to PLAY AGAIN", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2-75,
                         arcade.color.WHITE, font_size=20, anchor_x="center")
   
   
    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """ If the user presses the key button, start the game. """
        game_view = Game(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.window.show_view(game_view)
 

# Creates the game and starts it going
def main():
    """ Main method """

    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    start_view = InstructionView()
    window.show_view(start_view)
    arcade.run()
    
main()    