import blessed
import time


term = blessed.Terminal()

# Initial position
x, y = term.width // 2, term.height // 2


class Ball():
    def __init__(self, x, y, dx, dy, term):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.term = term

    def move(self):
        self.x += self.dx
        self.y += self.dy
        self.x = int(self.x)
        self.y = int(self.y)

    def draw(self):
        print(self.term.move(self.y, self.x) + 'o')

    def clear(self):
        print(self.term.move(self.y, self.x) + ' ')

    def bounce(self):
        if self.x == 0 or self.x >= self.term.width - 1:
            self.dx *= -1
        if self.y == 0 or self.y >= self.term.height - 2:
            self.dy *= -1


class Paddle():
    def __init__(self, x, y, term):
        self.x = x
        self.y = y
        self.term = term

    def draw(self):
        print(self.term.move(self.y, self.x) + '========')

    def clear(self):
        print(self.term.move(self.y, self.x) + '        ')

    def move(self, dx):
        self.x += dx
        if self.x < 0:
            self.x = 0
        if self.x > self.term.width - 5:
            self.x = self.term.width - 5


frames_per_second = 30

with term.cbreak(), term.hidden_cursor():
    # Clear the screen
    print(term.home + term.clear)

    the_ball = Ball(x, y, 1, 1, term)
    the_paddle = Paddle(term.width // 2, term.height - 5, term)
    the_paddle.draw()

    # Main loop
    while True:

        start_time = time.time()

        if the_ball.y == the_paddle.y and \
                the_ball.x >= the_paddle.x and \
                the_ball.x <= the_paddle.x + 8:
            the_ball.dy *= -1

        the_ball.clear()
        the_ball.move()
        the_ball.bounce()
        the_ball.draw()

        # Quit
        if term.inkey(timeout=0) == 'q':
            break
        
        key = term.inkey(timeout=0.1)
        if key.code == term.KEY_LEFT:
            the_paddle.clear()
            the_paddle.move(-2)
            the_paddle.draw()

        if key.code == term.KEY_RIGHT:
            the_paddle.clear()
            the_paddle.move(2)
            the_paddle.draw()

        end_time = time.time()

        delay_time = 1.0 / frames_per_second - (end_time - start_time)

        if delay_time > 0:
            # Sleep
            time.sleep(delay_time)

# Clear the screen on exit
print(term.clear)
