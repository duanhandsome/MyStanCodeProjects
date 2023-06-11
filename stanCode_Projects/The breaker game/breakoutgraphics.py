"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman, 
and Jerry Liao.

YOUR DESCRIPTION HERE
"""
from campy.graphics.gwindow import GWindow
from campy.graphics.gobjects import GOval, GRect, GLabel
from campy.gui.events.mouse import onmouseclicked, onmousemoved
import random

BRICK_SPACING = 5      # Space between bricks (in pixels). This space is used for horizontal and vertical spacing
BRICK_WIDTH = 40       # Width of a brick (in pixels)
BRICK_HEIGHT = 15      # Height of a brick (in pixels)
BRICK_ROWS = 10        # Number of rows of bricks
BRICK_COLS = 10        # Number of columns of bricks
BRICK_OFFSET = 50      # Vertical offset of the topmost brick from the window top (in pixels)
BALL_RADIUS = 10       # Radius of the ball (in pixels)
PADDLE_WIDTH = 75      # Width of the paddle (in pixels)
PADDLE_HEIGHT = 15     # Height of the paddle (in pixels)
PADDLE_OFFSET = 50     # Vertical offset of the paddle from the window bottom (in pixels)
INITIAL_Y_SPEED = 7    # Initial vertical speed for the ball
MAX_X_SPEED = 5        # Maximum initial horizontal speed for the ball


class BreakoutGraphics:

    def __init__(self, ball_radius=BALL_RADIUS, paddle_width=PADDLE_WIDTH, paddle_height=PADDLE_HEIGHT,
                 paddle_offset=PADDLE_OFFSET, brick_rows=BRICK_ROWS, brick_cols=BRICK_COLS, brick_width=BRICK_WIDTH,
                 brick_height=BRICK_HEIGHT, brick_offset=BRICK_OFFSET, brick_spacing=BRICK_SPACING, title='Breakout'):

        # Create a graphical window, with some extra space
        window_width = brick_cols * (brick_width + brick_spacing) - brick_spacing
        window_height = brick_offset + 3 * (brick_rows * (brick_height + brick_spacing) - brick_spacing)
        self.window = GWindow(width=window_width, height=window_height, title=title)

        # Create a paddle
        self.paddle = GRect(paddle_width, paddle_height)
        self.paddle.filled = True
        self.paddle.fill_color = 'lightgreen'
        self.window.add(self.paddle, x=self.window.width/2 - self.paddle.width/2,
                        y=self.window.height-self.paddle.height-paddle_offset)

        # Center a filled ball in the graphical window
        self.ball = GOval(ball_radius * 2, ball_radius * 2)
        self.ball.filled = True
        self.window.add(self.ball, x=self.window.width / 2 - ball_radius, y=self.window.height / 2 - ball_radius)

        # Default initial velocity for the ball
        self.__dx = 0
        self.__dy = INITIAL_Y_SPEED
        self.set_x_velocity()

        # Initialize our mouse listeners
        onmouseclicked(self.start_game)
        onmousemoved(self.paddle_move)

        # Argument determining if the game starts
        self.is_moving = False

        # Draw bricks
        self.brick_count = brick_cols * brick_rows
        for i in range(brick_rows):
            for j in range(brick_cols):
                self.brick = GRect(brick_width, brick_height)
                self.brick.filled = True
                if i % 5 == 1:
                    self.brick.fill_color = 'sienna'
                elif i % 5 == 2:
                    self.brick.fill_color = 'tan'
                elif i % 5 == 3:
                    self.brick.fill_color = 'olivedrab'
                elif i % 5 == 4:
                    self.brick.fill_color = 'seagreen'
                else:
                    self.brick.fill_color = 'greenyellow'
                self.window.add(self.brick, x=j*(brick_width+brick_spacing),
                                y=brick_offset+i*(brick_height+brick_spacing))

    def reset_condition(self):
        """
        This method reset condition after the user lost one HP
        """
        self.ball = GOval(BALL_RADIUS * 2, BALL_RADIUS * 2)
        self.ball.filled = True
        self.window.add(self.ball, x=self.window.width / 2 - self.ball.width/2,
                        y=self.window.height / 2 - self.ball.height/2)
        self.window.remove(self.paddle)
        self.paddle = GRect(PADDLE_WIDTH, PADDLE_HEIGHT)
        self.paddle.filled = True
        self.paddle.fill_color = 'lightgreen'
        self.window.add(self.paddle, x=self.window.width / 2 - self.paddle.width / 2,
                        y=self.window.height - self.paddle.height - PADDLE_OFFSET)
        self.is_moving = False
        self.set_x_velocity()

    def start_game(self, _):
        """
        This method determine if the game starts.
        """
        self.is_moving = True

    def paddle_move(self, event):
        """
        This method will detect the position of the mouse cursor.
        Players can control the paddle by moving the mouse, however, the paddle cannot exceed the side of the window.
        :param event: determine the position of the mouse
        """
        if self.is_moving:                              # User can only move the paddle after the game starts
            if event.x < self.paddle.width/2:
                self.paddle.x = 0
            elif event.x > self.window.width - self.paddle.width/2:
                self.paddle.x = self.window.width - self.paddle.width
            else:
                self.paddle.x = event.x - self.paddle.width/2

    def set_x_velocity(self):
        """
        This method determine the x-dimension speed of the ball, there is a 50% chance that the ball
        will bounce to the opposite side (the dx will become negative)
        """
        self.__dx = random.randint(1, MAX_X_SPEED)
        if random.random() > 0.5:
            self.__dx = -self.__dx

    def check_for_collision(self):
        """
        This method creates four corner of the pixel of the ball and check if they touch an object
        :return: True(touches an object) and False(not touching anything)
        """
        # Create four objects touching four corner of the pixel of the ball
        l_u_obj = self.window.get_object_at(self.ball.x, self.ball.y)
        r_u_obj = self.window.get_object_at(self.ball.x+self.ball.width, self.ball.y)
        l_d_obj = self.window.get_object_at(self.ball.x, self.ball.y+self.ball.height)
        r_d_obj = self.window.get_object_at(self.ball.x+self.ball.width, self.ball.y+self.ball.height)
        if self.ball.y < self.window.height/2:
            # if the ball is in the upper part of the window, and it hits an object, it must be a brick
            if l_u_obj is not None:
                self.window.remove(l_u_obj)
                self.brick_count -= 1
                return True
            elif r_u_obj is not None:
                self.window.remove(r_u_obj)
                self.brick_count -= 1
                return True
            elif l_d_obj is not None:
                self.window.remove(l_d_obj)
                self.brick_count -= 1
                return True
            elif r_d_obj is not None:
                self.window.remove(r_d_obj)
                self.brick_count -= 1
                return True
        else:
            # if the ball is in the bottom part of the window, and it hits an object, it must be a paddle
            if l_d_obj is not None or r_d_obj is not None:
                # To avoid the ball stick on the paddle
                self.ball.move(0, -BALL_RADIUS)
                return True

    def game_over(self):
        """
        This method will show "Game over" in the middle of the window after the user lost all their chances
        """
        self.window.clear()
        label = GLabel('Game Over')
        label.font = '-50-bold'
        self.window.add(label, x=45, y=self.window.height/2)

    def game_win(self):
        """
        This method will show "YOU WIN!" in the middle of the window after the user wins the game
        """
        self.window.clear()
        label = GLabel('YOU WIN!')
        label.font = '-50-bold'
        label.color = 'red'
        self.window.add(label, x=60, y=self.window.height/2)

    def get_dx(self):
        """
        Get the horizontal velocity of the ball since the user cannot get it from the user side.
        """
        return self.__dx

    def get_dy(self):
        """
        Get the vertical velocity of the ball since the user cannot get it from the user side.
        """
        return self.__dy
