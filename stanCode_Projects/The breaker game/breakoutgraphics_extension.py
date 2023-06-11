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

BRICK_SPACING = 5           # Space between bricks (in pixels). This space is used for horizontal and vertical spacing
BRICK_WIDTH = 40            # Width of a brick (in pixels)
BRICK_HEIGHT = 15           # Height of a brick (in pixels)
BRICK_ROWS = 10             # Number of rows of bricks
BRICK_COLS = 10             # Number of columns of bricks
BRICK_OFFSET = 50           # Vertical offset of the topmost brick from the window top (in pixels)
BALL_RADIUS = 10            # Radius of the ball (in pixels)
HP_RADIUS = 7.5             # HP ball radius
PADDLE_WIDTH = 75           # Width of the paddle (in pixels)
PADDLE_HEIGHT = 15          # Height of the paddle (in pixels)
PADDLE_OFFSET = 50          # Vertical offset of the paddle from the window bottom (in pixels)
INITIAL_Y_SPEED = 7         # Initial vertical speed for the ball
MAX_X_SPEED = 5             # Maximum initial horizontal speed for the ball
NUM_LIVES = 3               # Number of attempts
BONUS_BRICKS = 10           # Number of bricks needed to hit for a bonus
BONUS_CHANCE = 0.5          # The chance of dropping a bonus when hitting a brick
PADDLE_WIDTH_CHANGE = 15    # Paddle wide increase/decrease after eating the bonus


class BreakoutGraphics:

    def __init__(self, ball_radius=BALL_RADIUS, paddle_width=PADDLE_WIDTH, paddle_height=PADDLE_HEIGHT,
                 paddle_offset=PADDLE_OFFSET, brick_rows=BRICK_ROWS, brick_cols=BRICK_COLS, brick_width=BRICK_WIDTH,
                 brick_height=BRICK_HEIGHT, brick_offset=BRICK_OFFSET, brick_spacing=BRICK_SPACING, chance=NUM_LIVES,
                 title='Breakout'):

        # User enters his name
        self.player_name = input('Please enter your name: ')

        # Create a graphical window, with some extra space
        window_width = brick_cols * (brick_width + brick_spacing) - brick_spacing
        window_height = brick_offset + 3 * (brick_rows * (brick_height + brick_spacing) - brick_spacing)
        self.window = GWindow(width=window_width, height=window_height, title=title)

        # Create HP balls
        self.chance = chance
        for i in range(self.chance):
            hp = GOval(HP_RADIUS*2, HP_RADIUS*2)
            hp.filled = True
            hp.fill_color = 'red'
            hp.color = 'red'
            self.window.add(hp, x=self.window.width-25*(self.chance-i), y=self.window.height-19)

        # Create a player name label
        self.name = GLabel(f'Gamer: {self.player_name}')
        self.name.font = '-12-bold'
        self.window.add(self.name, 0, BRICK_OFFSET-20)

        # Create score board
        self.score = 0
        self.score_board = GLabel(f'Score: {self.score}')
        self.score_board.font = '-12-bold'
        self.window.add(self.score_board, 0, self.window.height)

        # Create the welcome, introduction and click to start label
        self.welcome = GLabel("Welcome to the brick breaker!")
        self.welcome.font = '-12-bold'
        self.window.add(self.welcome, self.window.width/2-110, self.window.height/2+50)
        self.introduction = GLabel("You have three chances to break all the bricks.")
        self.introduction.font = '-12-bold'
        self.window.add(self.introduction, self.window.width/2-170, self.window.height/2+70)
        self.click_intro = GLabel("Click to start!")
        self.click_intro.font = '-12-bold'
        self.window.add(self.click_intro, self.window.width/2-55, self.window.height/2+90)

        # Create a paddle
        self.paddle_width = PADDLE_WIDTH
        self.paddle_height = PADDLE_HEIGHT
        self.paddle = GRect(paddle_width, paddle_height)
        self.paddle.filled = True
        self.paddle.fill_color = 'lightgreen'
        self.paddle.color = 'lightgreen'
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

        # Attribute controlling if the game starts
        self.is_moving = False

        # Attributes related to bonus
        self.bonus_is_moving = False
        self.bonus_ready_dropping = True
        self.bonus = GRect(15, 15)
        self.bonus.filled = True
        self.bonus.fill_color = 'mediumseagreen'
        self.bonus.color = 'mediumseagreen'

        # Paddle movement and click to start the game
        onmouseclicked(self.start_game)
        onmousemoved(self.paddle_move)

        # Draw bricks
        self.brick_sum = brick_cols * brick_rows
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

    def life_increase(self):
        """
        This method will be executed after the user gain one HP.
        One HP ball will be added.
        """
        self.chance += 1
        hp = GOval(HP_RADIUS * 2, HP_RADIUS * 2)
        hp.filled = True
        hp.fill_color = 'red'
        hp.color = 'red'
        self.window.add(hp, x=self.window.width-25*self.chance, y=self.window.height-19)

    def life_decrease(self):
        """
        This method will be executed after the user lost one HP.
        One HP ball will be removed.
        """
        self.chance -= 1
        hp = self.window.get_object_at(x=self.window.width-25*(self.chance+1)+HP_RADIUS,
                                       y=self.window.height-19+HP_RADIUS)
        self.window.remove(hp)

    def reset_condition(self):
        """
        This method reset condition after the user lost one HP
        """
        self.window.remove(self.bonus)
        self.ball = GOval(BALL_RADIUS * 2, BALL_RADIUS * 2)
        self.ball.filled = True
        self.window.add(self.ball, x=self.window.width / 2 - self.ball.width/2,
                        y=self.window.height / 2 - self.ball.height/2)
        self.window.remove(self.paddle)
        self.paddle = GRect(self.paddle_width, self.paddle_height)
        self.paddle.filled = True
        self.paddle.fill_color = 'lightgreen'
        self.paddle.color = 'lightgreen'
        self.window.add(self.paddle, x=self.window.width / 2 - self.paddle.width / 2,
                        y=self.window.height - self.paddle.height - PADDLE_OFFSET)
        self.is_moving = False
        self.set_x_velocity()

    def start_game(self, _):
        """
        This method determines if the game starts.
        """
        self.is_moving = True
        self.window.remove(self.welcome)
        self.window.remove(self.introduction)
        self.window.remove(self.click_intro)

    def paddle_move(self, event):
        """
        This method will detect the position of the mouse cursor.
        Users can control the paddle by moving the mouse, however, the paddle cannot exceed the side of the window.
        :param event: determine the position of the mouse
        """
        if self.is_moving:                              # User can only move the paddle after the game starts
            if event.x > self.window.width - self.paddle.width/2:
                self.paddle.x = self.window.width - self.paddle.width
            elif event.x < self.paddle.width/2:
                self.paddle.x = 0
            else:
                self.paddle.x = event.x - self.paddle.width/2

    def set_x_velocity(self):
        """
        This method determines the x-dimension speed of the ball, there is a 50% chance that the ball
        will bounce to the opposite side (the dx will become negative)
        """
        self.__dx = random.randint(2, MAX_X_SPEED)
        if random.random() > 0.5:
            self.__dx = -self.__dx

    def check_for_collision_brick(self):
        """
        This method creates four corner of the pixel of the ball and check if they touch a brick
        (But if the ball touches the scoreboard or the HP ball, nothing will happen)
        In addition, this method checks if the bonus can be dropped.
        :return: True(touches a brick) and False(not touching anything)
        """
        # Create four objects touching four corner of the pixel of the ball
        l_u_obj = self.window.get_object_at(self.ball.x, self.ball.y)
        r_u_obj = self.window.get_object_at(self.ball.x+self.ball.width, self.ball.y)
        l_d_obj = self.window.get_object_at(self.ball.x, self.ball.y+self.ball.height)
        r_d_obj = self.window.get_object_at(self.ball.x+self.ball.width, self.ball.y+self.ball.height)
        if self.ball.y < self.window.height / 2:
            # if the ball is in the upper part of the window, and it hits an object, it must be a brick
            if l_u_obj is not None and l_u_obj is not self.name and l_u_obj is not self.bonus:
                self.window.remove(l_u_obj)
                self.brick_count -= 1
                self.renew_scoreboard()
                self.check_bonus_drop()
                return True
            elif r_u_obj is not None and r_u_obj is not self.name and r_u_obj is not self.bonus:
                self.window.remove(r_u_obj)
                self.brick_count -= 1
                self.renew_scoreboard()
                self.check_bonus_drop()
                return True
            elif l_d_obj is not None and l_d_obj is not self.name and l_d_obj is not self.bonus:
                self.window.remove(l_d_obj)
                self.brick_count -= 1
                self.renew_scoreboard()
                self.check_bonus_drop()
                return True
            elif r_d_obj is not None and r_d_obj is not self.name and r_d_obj is not self.bonus:
                self.window.remove(r_d_obj)
                self.brick_count -= 1
                self.renew_scoreboard()
                self.check_bonus_drop()
                return True

    def check_for_collision_paddle(self):
        """
        This method creates four corner of the pixel of the ball and check if they touch a paddle
        (But if the ball touches the scoreboard or the HP ball, nothing will happen)
        :return: True(touches a paddle) and False(not touching anything)
        """
        l_d_obj = self.window.get_object_at(self.ball.x, self.ball.y + self.ball.height)
        r_d_obj = self.window.get_object_at(self.ball.x + self.ball.width, self.ball.y + self.ball.height)
        if self.window.height / 2 <= self.ball.y <= self.window.height - self.paddle.height - PADDLE_OFFSET:
            # if the ball is in the bottom part of the window, and it hits an object, it must be a paddle
            if l_d_obj is not None or r_d_obj is not None:
                # To avoid the ball stick on the paddle
                if self.__dy > 0:
                    self.ball.move(0, -BALL_RADIUS)
                    return True

    def check_bonus_drop(self):
        """
        This method will check if the bonus can be dropped.
        (The chance is equal to BONUS_CHANCE and there is only on bonus allowed in the window.)
        """
        if self.bonus_ready_dropping and random.random() < BONUS_CHANCE:
            self.window.add(self.bonus, self.ball.x, self.ball.y)
            self.bonus_is_moving = True

    def bonus_condition(self):
        """
        This method checks the condition of the bonus:
        1. The bonus effect will be activated
        2. Check if the bonus falls out of the window
        """
        self.bonus_ready_dropping = False
        self.bonus.move(0, 5)
        # The user catches the bonus
        if self.window.get_object_at(self.bonus.x, self.bonus.y+18) is self.paddle\
                or self.window.get_object_at(self.bonus.x+15, self.bonus.y+18) is self.paddle:
            self.window.remove(self.bonus)
            self.bonus_effect()
            self.bonus_ready_dropping = True
            self.bonus_is_moving = False
        # The user fails to catch the bonus
        if self.bonus.y + 18 >= self.window.height:
            self.window.remove(self.bonus)
            self.bonus_ready_dropping = True
            self.bonus_is_moving = False

    def bonus_effect(self):
        """
        This method determines the effect of a bonus.
        There are four bonus effects:
        1. paddle will become longer (positive effect, with prob=0.6)
        2. user will gain one HP (positive effect, with prob=0.1)
        3. paddle will become shorter (negative effect, with prob=0.2)
        4. user will lose one HP (negative effect, with prob=0.1)
        """
        ran_effect = random.randint(1, 10)
        # paddle becomes longer
        if ran_effect <= 6:
            x = self.paddle.x + self.paddle_width/2
            y = self.paddle.y
            self.window.remove(self.paddle)
            self.paddle_width += PADDLE_WIDTH_CHANGE
            self.paddle = GRect(self.paddle_width, self.paddle_height)
            self.paddle.filled = True
            self.paddle.fill_color = 'lightgreen'
            self.paddle.color = 'lightgreen'
            self.window.add(self.paddle, x - self.paddle.width / 2, y)
        # paddle becomes shorter
        elif 6 < ran_effect <= 8:
            x = self.paddle.x + self.paddle_width / 2
            y = self.paddle.y
            self.window.remove(self.paddle)
            self.paddle_width -= PADDLE_WIDTH_CHANGE
            self.paddle = GRect(self.paddle_width, self.paddle_height)
            self.paddle.filled = True
            self.paddle.fill_color = 'lightgreen'
            self.paddle.color = 'lightgreen'
            self.window.add(self.paddle, x - self.paddle.width / 2, y)
        # Gain one HP
        elif ran_effect == 9:
            self.life_increase()
        else:
            self.life_decrease()

    def renew_scoreboard(self):
        """
        This method renews the scoreboard and calculating new scores
        """
        if 3 / 4 * self.brick_sum <= self.brick_count < self.brick_sum:
            self.score += 1000
            self.window.remove(self.score_board)
            self.score_board = GLabel(f'Score: {self.score}')
            self.score_board.font = '-12-bold'
            self.window.add(self.score_board, 0, self.window.height)
        elif 1 / 2 * self.brick_sum <= self.brick_count < 3 / 4 * self.brick_sum:
            self.score += 2000
            self.window.remove(self.score_board)
            self.score_board = GLabel(f'Score: {self.score}')
            self.score_board.font = '-12-bold'
            self.window.add(self.score_board, 0, self.window.height)
        elif 1 / 4 * self.brick_sum <= self.brick_count < 1 / 2 * self.brick_sum:
            self.score += 3000
            self.window.remove(self.score_board)
            self.score_board = GLabel(f'Score: {self.score}')
            self.score_board.font = '-12-bold'
            self.window.add(self.score_board, 0, self.window.height)
        elif 0 <= self.brick_count < 1 / 4 * self.brick_sum:
            self.score += 4000
            self.window.remove(self.score_board)
            self.score_board = GLabel(f'Score: {self.score}')
            self.score_board.font = '-12-bold'
            self.window.add(self.score_board, 0, self.window.height)

    def game_over(self):
        """
        This method will show "Game over" and the user's score after you use all the chances
        """
        self.window.clear()
        label = GLabel('Game Over')
        label.font = '-50-bold'
        self.window.add(label, x=45, y=self.window.height/2)
        # Show the score
        score_label = GLabel(f'Your score: {self.score}')
        score_label.font = '-30-bold'
        if self.score == 0:
            self.window.add(score_label, x=90, y=self.window.height/2+40)
        elif 1000 <= self.score < 9999:
            self.window.add(score_label, x=70, y=self.window.height/2+40)
        elif 10000 <= self.score < 99999:
            self.window.add(score_label, x=55, y=self.window.height/2+40)
        else:
            self.window.add(score_label, x=35, y=self.window.height/2+40)
        # Check if this is the highest score
        with open('Highest score.txt', 'r') as f:
            old_score = f.read()
        if self.score < int(old_score):
            highest_score_label = GLabel(f'Highest score: {old_score}')
            highest_score_label.font = '-30-bold'
            self.window.add(highest_score_label, x=20, y=self.window.height / 2 + 80)
        else:
            break_record_label = GLabel(f'You break the record!')
            break_record_label.font = '-30-bold'
            self.window.add(break_record_label, x=20, y=self.window.height / 2 + 80)
            with open('Highest score.txt', 'w') as f:
                f.write(str(self.score))

    def game_win(self):
        """
        This method will show "YOU WIN!" in the middle of the window after the user wins the game
        """
        self.window.clear()
        label = GLabel('YOU WIN!')
        label.font = '-50-bold'
        label.color = 'red'
        self.window.add(label, x=60, y=self.window.height/2)
        # Show the score
        score_label = GLabel(f'YOUR SCORE: {self.score}')
        score_label.font = '-30-bold'
        score_label.color = 'red'
        self.window.add(score_label, x=15, y=self.window.height/2+50)
        # Record the highest score
        with open('Highest score.txt', 'w') as f:
            f.write(str(self.score))

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

    def set_dx(self, new_dx):
        """
        Setter function to update dx and bounce the ball.
        :param new_dx: the new dx value passed from the server side to the coder side.
        :return: None, this function does not return anything.
        """
        self.__dx = new_dx

    def set_dy(self, new_dy):
        """
        Setter function to update dy and bounce the ball.
        :param new_dy: the new dy value passed from the server side to the coder side.
        :return: None, this function does not return anything.
        """
        self.__dy = new_dy
        return self.__dy

