import math

import pygame as pg


class Colors:

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)

    YELLOW = (255, 255, 0)
    MOON = (245, 243, 206)


class Constants:

    SCREEN_WIDTH = 1500
    SCREEN_HEIGHT = 800
    WINDOW_COLOR = (100, 100, 100)

    TICKRATE = 60
    GAME_SPEED = .35

    LINE_COLOR = (0, 0, 255)
    ALINE_COLOR = Colors.BLACK

    X_BOUNDS_BARRIER = 1
    Y_BOUNDS_BARRIER = 1
    BOUNCE_FUZZ = 0

    START_X = int(.5 * SCREEN_WIDTH)
    START_Y = int(.99 * SCREEN_HEIGHT)

    AIR_DRAG = .3
    GRAVITY = 9.80665


class Fonts:

    pg.font.init()
    strokeFont = pg.font.SysFont("monospace", 50)
    STROKECOLOR = Colors.YELLOW

    powerFont = pg.font.SysFont("arial", 15, bold=True)
    POWERCOLOR = Colors.GREEN

    angleFont = pg.font.SysFont("arial", 15, bold=True)
    ANGLECOLOR = Colors.GREEN

    penaltyFont = pg.font.SysFont("georgia", 40, bold=True)
    PENALTYCOLOR = Colors.RED

    resistMultiplierFont = pg.font.SysFont("courier new", 13)
    RESISTMULTIPLIERCOLOR = Colors.RED

    powerMultiplierFont = pg.font.SysFont("courier new", 13)
    POWERMULTIPLIERCOLOR = Colors.RED


class Ball(object):
    def __init__(self, x, y, dx = 0, dy = 0, bounce = .8, radius = 10):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.bounce = bounce
        self.radius = radius
        self.mass = 4/3 * math.pi * self.radius**3
        self.color = Colors.WHITE
        self.outlinecolor = Colors.RED

    def show(self, window):
        pg.draw.circle(window, self.outlinecolor, (int(self.x), int(self.y)), self.radius)
        pg.draw.circle(window, self.color, (int(self.x), int(self.y)), self.radius - int(.4 * self.radius))

    def update(self, update_frame):
        update_frame += 1

        ax = 0
        ay = Constants.GRAVITY

        dt = Constants.GAME_SPEED
        self.vx += ax * dt
        self.vy += ay * dt

        if resist_multiplier:
            drag = 6*math.pi * self.radius * resist_multiplier * Constants.AIR_DRAG
            air_resist_x = -drag * self.vx / self.mass
            air_resist_y = -drag * self.vy / self.mass

            self.vx += air_resist_x/dt
            self.vy += air_resist_y/dt

        self.x += self.vx * dt
        self.y += self.vy * dt

        bounced, stop, shoot = False, False, True

        # Top & Bottom
        if self.y + self.radius > Constants.SCREEN_HEIGHT:
            self.y = Constants.SCREEN_HEIGHT - self.radius
            self.vy = -self.vy
            bounced = True
            print('    Bounce!')

        if self.y - self.radius < Constants.Y_BOUNDS_BARRIER:
            self.y = Constants.Y_BOUNDS_BARRIER + self.radius
            self.vy = -self.vy
            bounced = True
            print('    Bounce!')

        # Speed/Resistance Rectangles
        if (self.x >= .875*Constants.SCREEN_WIDTH + self.radius) and (self.y + self.radius >= .98*Constants.SCREEN_HEIGHT):
            self.x = .88*Constants.SCREEN_WIDTH + self.radius
            self.y = .98*Constants.SCREEN_HEIGHT - self.radius
            self.x = .87*Constants.SCREEN_WIDTH + self.radius
            self.vy, self.vx = -self.vy, -abs(self.vx)
            bounced = True

        if (self.x <= .1175*Constants.SCREEN_WIDTH + self.radius) and (self.y + self.radius >= .98*Constants.SCREEN_HEIGHT):
            self.x = .118*Constants.SCREEN_WIDTH + self.radius
            self.y = .98*Constants.SCREEN_HEIGHT - self.radius
            self.x = .119*Constants.SCREEN_WIDTH + self.radius
            self.vy, self.vx = -self.vy, abs(self.vx)
            bounced = True

        # if (self.x - self.radius < Constants.X_BOUNDS_BARRIER):
        #     self.x = X_BOUNDS_BARRIER + self.radius
        #     self.vx = -self.vx
        #     bounced = True

        # if (self.x + self.radius > Constants.SCREEN_WIDTH - Constants.X_BOUNDS_BARRIER):
        #     self.x = Constants.SCREEN_WIDTH - Constants.X_BOUNDS_BARRIER - self.radius
        #     self.vx = -self.vx
        #     bounced = True

        if bounced:
            self.vx *= self.bounce
            self.vy *= self.bounce

        print(f'\n    Update Frame: {update_frame}',
               '        x-pos: %spx' % round(self.x),
               '        y-pos: %spx' % round(self.y),
               '        x-vel: %spx/u' % round(self.vx),
               '        y-vel: %spx/u' % round(self.vy),
               sep='\n', end='\n\n')

        return update_frame, shoot, stop

    @staticmethod
    def quadrant(x, y, xm, ym):
        if ym < y and xm > x:
            return 1
        elif ym < y and xm < x:
            return 2
        elif ym > y and xm < x:
            return 3
        elif ym > y and xm > x:
            return 4
        else:
            return False


def draw_window():
    clock.tick(Constants.TICKRATE)

    window.fill(Constants.WINDOW_COLOR)

    resist_multiplier_text = 'Air Resistance: {:2.2f} m/s'.format(resist_multiplier)
    resist_multiplier_label = Fonts.resistMultiplierFont.render(resist_multiplier_text, 1, Fonts.RESISTMULTIPLIERCOLOR)
    pg.draw.rect(window, Colors.BLACK, (.8875*Constants.SCREEN_WIDTH, .98*Constants.SCREEN_HEIGHT, Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT))
    pg.draw.arrow(window, Colors.MOON, Colors.GREEN, (.8875*Constants.SCREEN_WIDTH, .99*Constants.SCREEN_HEIGHT), (.88*Constants.SCREEN_WIDTH, .99*Constants.SCREEN_HEIGHT), 3, 3)
    pg.draw.arrow(window, Colors.MOON, Colors.GREEN, (Constants.SCREEN_WIDTH, .975*Constants.SCREEN_HEIGHT), (.88*Constants.SCREEN_WIDTH, .975*Constants.SCREEN_HEIGHT), 3)
    window.blit(resist_multiplier_label, (.8925*Constants.SCREEN_WIDTH, .98*Constants.SCREEN_HEIGHT))

    power_multiplier_text = f'Swing Strength: {int(power_multiplier*100)}%'
    power_multiplier_label = Fonts.powerMultiplierFont.render(power_multiplier_text, 1, Fonts.POWERMULTIPLIERCOLOR)
    pg.draw.rect(window, Colors.BLACK, (10**-4*Constants.SCREEN_WIDTH, .98*Constants.SCREEN_HEIGHT, .1125*Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT))
    window.blit(power_multiplier_label, (.005*Constants.SCREEN_WIDTH, .98*Constants.SCREEN_HEIGHT))

    if not shoot:
        pg.draw.arrow(window, Constants.ALINE_COLOR, Constants.ALINE_COLOR, aline[0], aline[1], 5)
        pg.draw.arrow(window, Constants.LINE_COLOR, Constants.LINE_COLOR, line[0], line[1], 5)

    stroke_text = 'Strokes: %s' % strokes
    stroke_label = Fonts.strokeFont.render(stroke_text, 1, Fonts.STROKECOLOR)
    if not strokes:
        window.blit(stroke_label, (Constants.SCREEN_WIDTH - .21 * Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT - .985 * Constants.SCREEN_HEIGHT))
    else:
        window.blit(stroke_label, (Constants.SCREEN_WIDTH - (.21+.02*math.floor(math.log10(strokes))) * Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT - .985 * Constants.SCREEN_HEIGHT))

    power_text = 'Shot Strength: %sN' % power_display
    power_label = Fonts.powerFont.render(power_text, 1, Fonts.POWERCOLOR)
    if not shoot: window.blit(power_label, (cursor_pos[0] + .008 * Constants.SCREEN_WIDTH, cursor_pos[1]))

    angle_text = 'Angle: %s°' % angle_display
    angle_label = Fonts.angleFont.render(angle_text, 1, Fonts.ANGLECOLOR)
    if not shoot: window.blit(angle_label, (ball.x - .06 * Constants.SCREEN_WIDTH, ball.y - .01 * Constants.SCREEN_HEIGHT))

    if penalty:
        penalty_text = f'Out of Bounds! +1 Stroke'
        penalty_label = Fonts.penaltyFont.render(penalty_text, 1, Fonts.PENALTYCOLOR)
        penalty_rect = penalty_label.get_rect(center=(Constants.SCREEN_WIDTH/2, .225*Constants.SCREEN_HEIGHT))
        window.blit(penalty_label, penalty_rect)

    ball.show(window)

    pg.display.flip()


def angle(cursor_pos):
    x, y, xm, ym = ball.x, ball.y, cursor_pos[0], cursor_pos[1]
    if x-xm:
        angle = math.atan((y - ym) / (x - xm))
    elif y > ym:
        angle = math.pi/2
    else:
        angle = 3*math.pi/2

    q = ball.quadrant(x,y,xm,ym)
    if q: angle = math.pi*math.floor(q/2) - angle

    if round(angle*deg) == 360:
        angle = 0

    if x > xm and not round(angle*deg):
        angle = math.pi

    return angle


def arrow(screen, lcolor, tricolor, start, end, trirad, thickness=2):
    pg.draw.line(screen, lcolor, start, end, thickness)
    rotation = (math.atan2(start[1] - end[1], end[0] - start[0])) + math.pi/2
    pg.draw.polygon(screen, tricolor, ((end[0] + trirad * math.sin(rotation),
                                        end[1] + trirad * math.cos(rotation)),
                                       (end[0] + trirad * math.sin(rotation - 120*rad),
                                        end[1] + trirad * math.cos(rotation - 120*rad)),
                                       (end[0] + trirad * math.sin(rotation + 120*rad),
                                        end[1] + trirad * math.cos(rotation + 120*rad))))
setattr(pg.draw, 'arrow', arrow)


def distance(x, y):
    return math.sqrt(x**2 + y**2)


def update_values(quit, rkey, stkey, shoot, xb, yb, strokes):
    for event in pg.event.get():
        if event.type == pg.QUIT:
            quit = True

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                quit = True

            if event.key == pg.K_RIGHT:
                if rkey != max(resist_dict):
                    rkey += 1

            if event.key == pg.K_LEFT:
                if rkey != min(resist_dict):
                    rkey -= 1

            if event.key == pg.K_UP:
                if stkey != max(strength_dict):
                    stkey += 1

            if event.key == pg.K_DOWN:
                if stkey != min(strength_dict):
                    stkey -= 1

        if event.type == pg.MOUSEBUTTONDOWN:
            if not shoot:
                shoot, stop = True, False
                strokes, xb, yb = hit_ball(strokes)

    return quit, rkey, stkey, shoot, xb, yb, strokes


def hit_ball(strokes):
    x, y = ball.x, ball.y
    xb, yb = ball.x, ball.y
    power = power_multiplier/4 * distance(line_ball_x, line_ball_y)
    print('\n\nBall Hit!')
    print('\npower: %sN' % round(power, 2))
    ang = angle(cursor_pos)
    print('angle: %s°' % round(ang * deg, 2))
    print('cos(a): %s' % round(math.cos(ang), 2)), print('sin(a): %s' % round(math.sin(ang), 2))

    ball.vx, ball.vy = power * math.cos(ang), -power * math.sin(ang)

    strokes += 1

    return strokes, xb, yb


def initialize():
    pg.init()
    pg.display.set_caption('Golf')
    window = pg.display.set_mode((Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT))
    pg.event.set_grab(True)
    pg.mouse.set_cursor((8, 8), (0, 0), (0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0))

    return window


rad, deg = math.pi/180, 180/math.pi
x, y, power, ang, strokes = [0]*5
xb, yb = None, None
shoot, penalty, stop, quit = [False]*4
p_ticks, update_frame = 0, 0

ball = Ball(Constants.START_X, Constants.START_Y)

clock = pg.time.Clock()

strength_dict = {0: .01, 1: .02, 2: .04, 3: .08, 4: .16, 5: .25, 6: .50, 7: .75, 8: 1}; stkey = 6
resist_dict = {0: 0, 1: .01, 2: .02, 3: .03, 4: .04, 5: .05, 6: .1, 7: .2, 8: .3, 9: .4, 10: .5, 11: .6, 12: .7,
               13: .8, 14: .9, 15: 1, 16: 1.25, 17: 1.5, 18: 1.75, 19: 2, 20: 2.5, 21: 3, 22: 3.5, 23: 4, 24: 4.5,
               25: 5}; rkey = 7

window = initialize()
while not quit:
    power_multiplier = strength_dict[stkey]
    resist_multiplier = resist_dict[rkey]

    seconds = (pg.time.get_ticks()-p_ticks)/1000
    if seconds > 1.2: penalty = False

    cursor_pos = pg.mouse.get_pos()
    line = [(ball.x, ball.y), cursor_pos]
    line_ball_x, line_ball_y = cursor_pos[0] - ball.x, cursor_pos[1] - ball.y

    aline = [(ball.x, ball.y), (ball.x + .015 * Constants.SCREEN_WIDTH, ball.y)]

    if not shoot:
        power_display = round(
            distance(line_ball_x, line_ball_y) * power_multiplier/5)

        angle_display = round(angle(cursor_pos) * deg)

    else:
        if stop or (abs(ball.vy) < 5 and abs(ball.vx) < 1 and abs(ball.y - (Constants.START_Y - 2)) <= Constants.BOUNCE_FUZZ):
            shoot = False
            #ball.y = Constants.START_Y
            print('\nThe ball has come to a rest!')
            update_frame = 0
        else:
            update_frame, shoot, stop = ball.update(update_frame)

        if not Constants.X_BOUNDS_BARRIER < ball.x < Constants.SCREEN_WIDTH:
            shoot = False
            print(f'\nOut of Bounds! Pos: {round(ball.x), round(ball.y)}')
            penalty = True
            p_ticks = pg.time.get_ticks()
            strokes += 1

            if Constants.X_BOUNDS_BARRIER < xb < Constants.SCREEN_WIDTH:
                ball.x = xb
            else:
                ball.x = Constants.START_X
            ball.y = yb

    quit, rkey, stkey, shoot, xb, yb, strokes = update_values(quit, rkey, stkey, shoot, xb, yb, strokes)

    draw_window()

print("\nShutting down...")
pg.quit()
