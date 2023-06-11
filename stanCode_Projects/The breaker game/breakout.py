"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman,
and Jerry Liao.

The program will run the game Breakout. You get 3 chances to clear all the bricks in the window.
The game will automatically stop if all the bricks are eradicated or if you lose all 3 chances.
"""

from campy.gui.events.timer import pause
from breakoutgraphics import BreakoutGraphics

FRAME_RATE = 10         # 100 frames per second
NUM_LIVES = 3			# Number of attempts


def main():
    graphics = BreakoutGraphics()
    dx = graphics.get_dx()
    dy = graphics.get_dy()
    chances = NUM_LIVES

    # Add the animation loop here!
    while True:
        pause(FRAME_RATE)
        # Make sure if the game starts (is_moving == True)
        if graphics.is_moving and graphics.brick_count > 0 and chances > 0:
            graphics.ball.move(dx, dy)
            # Check if the ball touches the wall
            if graphics.ball.x < 0 or graphics.ball.x > graphics.window.width - graphics.ball.width:
                dx = -dx
            if graphics.ball.y < 0:
                dy = -dy
            # Check if the ball touches other objects
            if graphics.check_for_collision():
                dy = -dy
            # Check if the user lose one HP
            if graphics.ball.y >= graphics.window.height:
                chances -= 1
                graphics.reset_condition()
        # The user consumes all the HP
        elif chances <= 0:
            graphics.game_over()
            break
        # The user wins the game by breaking all the bricks
        elif graphics.brick_count <= 0:
            graphics.game_win()
            break


if __name__ == '__main__':
    main()
