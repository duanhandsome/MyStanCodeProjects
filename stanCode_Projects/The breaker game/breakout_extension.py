"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman,
and Jerry Liao.

The program will run the game Breakout. The user get 3 chances to clear all the bricks in the window.

Game rules:
1. The game will automatically stop if all the bricks are eliminated(win) or if you lose all 3 chances(lose).
2. Users can see their lives in the right bottom corner of the window.
3. The game allows users to enter their name.
4. Users will get 1000 points when hitting the first 25% bricks, 2000 points for hitting the next 25% bricks,
   3000 points for the next 25% bricks and 4000 points for the last 25% bricks.
5. The vertical speed of the ball will increase randomly after the user successfully hits a brick.
6. If users win the game, the window will show "YOU WIN", YOUR SCORE: 250000.
7. If users lost the game, the window will show if he breaks the previous record.
8. After hitting every 10 bricks, a bonus ball will drop, and there are four different kinds effect if the user uses
   the paddle to touch the bonus:
   (1) paddle will become longer
   (2) user will gain one HP
   (3) paddle will become shorter
   (4) user will lose one HP
   Note: there will only be one bonus on the screen, if the player hasn't gotten previous bonus, no more bonus
   will be dropped even he hits other bricks.
"""

from campy.gui.events.timer import pause
from breakoutgraphics_extension import BreakoutGraphics
import random

FRAME_RATE = 10         # 100 frames per second
SPEED_CHANGE = 0.2      # Maximum speed change after the ball touches the paddle or the bricks


def main():
    graphics = BreakoutGraphics()

    # Add the animation loop here!
    while True:
        if graphics.is_moving and graphics.chance > 0 and graphics.brick_count > 0:
            # Make sure if the game starts
            dx = graphics.get_dx()
            dy = graphics.get_dy()
            graphics.ball.move(dx, dy)
            # Check if the ball touches the wall
            if graphics.ball.x < 0 or graphics.ball.x > graphics.window.width - graphics.ball.width:
                graphics.set_dx(-dx)
            if graphics.ball.y < 0:
                graphics.set_dy(-dy)
            # Check if the ball touches a brick
            if graphics.check_for_collision_brick():
                # The velocity of the ball will increase everytime it hits a paddle or a brick
                if dy > 0:
                    float(graphics.set_dy(-dy)) - random.random() * SPEED_CHANGE
                elif dy < 0:
                    float(graphics.set_dy(-dy)) + random.random() * SPEED_CHANGE
            # Check if the ball touches a paddle
            if graphics.check_for_collision_paddle():
                graphics.set_dy(-dy)
            # Check the condition of the bonus
            if graphics.bonus_is_moving:
                graphics.bonus_condition()
            # Check if the user lose one HP
            if graphics.ball.y >= graphics.window.height:
                graphics.life_decrease()
                graphics.reset_condition()
        elif graphics.chance <= 0 or graphics.paddle.width <= 0:
            # The user used all the HP
            graphics.game_over()
            break
        elif graphics.brick_count <= 0:
            # The user win the game by breaking all the bricks
            graphics.game_win()
            break
        pause(FRAME_RATE)


if __name__ == '__main__':
    main()
