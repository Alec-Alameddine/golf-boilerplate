import math

import pygame as pg
from scipy.constants import g as gravity


SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 800
WINDOW_COLOR = (100, 100, 100)

TICKRATE = 60
GAME_SPEED = .35

LINE_COLOR = (0, 0, 255)
ALINE_COLOR = (0, 0, 0)

BARRIER = 1
BOUNCE_FUZZ = 0

START_X = int(.5 * SCREEN_WIDTH)
START_Y = int(.99 * SCREEN_HEIGHT)


pg.font.init()
strokeFont = pg.font.SysFont("monospace", 50)
STROKECOLOR = (255, 255, 0)

powerFont = pg.font.SysFont("arial", 15, bold=True)
POWERCOLOR = (0, 255, 0)

angleFont = pg.font.SysFont("arial", 15, bold=True)
ANGLECOLOR = (0, 255, 0)

penaltyFont = pg.font.SysFont("georgia", 40, bold=True)
PENALTYCOLOR = (255, 0, 0)

resistMultiplierFont = pg.font.SysFont("courier new", 13)
RESISTMULTIPLIERCOLOR = (255, 0, 0)

powerMultiplierFont = pg.font.SysFont("courier new", 13)
POWERMULTIPLIERCOLOR = (255, 0, 0)


class Ball(object):
    def __init__(self, x, y, dx = 0, dy = 0, bounce = .8, radius = 10):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.bounce = bounce
        self.radius = radius
        self.mass = 4/3 * math.pi * self.radius**3
        self.color = (255, 255, 255)
        self.outlinecolor = (255, 0, 0)

    def show(self, window):
        pg.draw.circle(window, self.outlinecolor, (int(self.x), int(self.y)), self.radius)
        pg.draw.circle(window, self.color, (int(self.x), int(self.y)), self.radius - int(.4 * self.radius))

    def update(self, update_frame):
        update_frame += 1

        ax = 0
        ay = gravity

        dt = GAME_SPEED
        self.vx += ax * dt
        self.vy += ay * dt

        if resist_multiplier:
            drag = 6*math.pi * self.radius * resist_multiplier
            air_resist_x = -drag * self.vx / self.mass
            air_resist_y = -drag * self.vy / self.mass

            ax += air_resist_x
            ay += air_resist_y
            self.vx += air_resist_x
            self.vy += air_resist_y

        self.x += self.vx * dt
        self.y += self.vy * dt

        bounced = False
        if self.y + self.radius > SCREEN_HEIGHT:
            self.y = SCREEN_HEIGHT - self.radius
            self.vy = -self.vy
            bounced = True

        # if (self.x - self.radius < BARRIER):
        #     self.x = BARRIER + self.radius
        #     self.vx = -self.vx
        #     bounced = True

        # if (self.x + self.radius > SCREEN_WIDTH - BARRIER):
        #     self.x = SCREEN_WIDTH - BARRIER - self.radius
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

        return update_frame

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
    clock.tick(TICKRATE)

    window.fill(WINDOW_COLOR)
    ball.show(window)

    if not shoot:
        pg.draw.arrow(window, ALINE_COLOR, ALINE_COLOR, aline[0], aline[1], 5)
        pg.draw.arrow(window, LINE_COLOR, LINE_COLOR, line[0], line[1], 5)

    stroke_text = 'Strokes: %s' % strokes
    stroke_label = strokeFont.render(stroke_text, 1, STROKECOLOR)
    if not strokes:
        window.blit(stroke_label, (SCREEN_WIDTH - .21 * SCREEN_WIDTH, SCREEN_HEIGHT - .985 * SCREEN_HEIGHT))
    else:
        window.blit(stroke_label, (SCREEN_WIDTH - (.21+.02*math.floor(math.log10(strokes))) * SCREEN_WIDTH, SCREEN_HEIGHT - .985 * SCREEN_HEIGHT))

    power_text = 'Shot Strength: %sN' % power_display
    power_label = powerFont.render(power_text, 1, POWERCOLOR)
    if not shoot: window.blit(power_label, (cursor_pos[0] + .008 * SCREEN_WIDTH, cursor_pos[1]))

    angle_text = 'Angle: %s°' % angle_display
    angle_label = angleFont.render(angle_text, 1, ANGLECOLOR)
    if not shoot: window.blit(angle_label, (ball.x - .06 * SCREEN_WIDTH, ball.y - .01 * SCREEN_HEIGHT))

    if penalty:
        penalty_text = f'Out of Bounds! +1 Stroke'
        penalty_label = penaltyFont.render(penalty_text, 1, PENALTYCOLOR)
        penalty_rect = penalty_label.get_rect(center=(SCREEN_WIDTH/2, .225*SCREEN_HEIGHT))
        window.blit(penalty_label, penalty_rect)

    resist_multiplier_text = 'Air Resistance: {:2.2f} m/s'.format(resist_multiplier)
    resist_multiplier_label = resistMultiplierFont.render(resist_multiplier_text, 1, RESISTMULTIPLIERCOLOR)
    window.blit(resist_multiplier_label, (.89*SCREEN_WIDTH, .98*SCREEN_HEIGHT))

    power_multiplier_text = f'Strength: {int(power_multiplier*100)}%'
    power_multiplier_label = powerMultiplierFont.render(power_multiplier_text, 1, POWERMULTIPLIERCOLOR)
    window.blit(power_multiplier_label, (.005*SCREEN_WIDTH, .98*SCREEN_HEIGHT))

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


def arrow(screen, lcolor, tricolor, start, end, trirad):
    pg.draw.line(screen, lcolor, start, end, 2)
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

def initialize():
    pg.init()
    pg.display.set_caption('Golf')
    window = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pg.event.set_grab(True)
    pg.mouse.set_cursor((8, 8), (0, 0), (0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0))

    return window

rad, deg = math.pi/180, 180/math.pi
x, y, power, ang, strokes = [0]*5
xb, yb = None, None
shoot, penalty = False, False
p_ticks, update_frame = 0, 0

ball = Ball(START_X, START_Y)
quit = False

clock = pg.time.Clock()

strength_dict = {0: .01, 1: .02, 2: .04, 3: .08, 4: .16, 5: .25, 6: .50, 7: .75, 8: 1}; stkey = 6
resist_dict = {0: 0, 1: .01, 2: .02, 3: .03, 4: .04, 5: .05, 6: .1, 7: .2, 8: .3, 9: .4, 10: .5, 11: .6, 12: .7, 13: .8, 14: .9, 15: 1}; spkey = 7

window = initialize()
while not quit:
    power_multiplier = strength_dict[stkey]
    resist_multiplier = resist_dict[spkey]

    seconds = (pg.time.get_ticks()-p_ticks)/1000
    if seconds > 1.2: penalty = False

    cursor_pos = pg.mouse.get_pos()
    line = [(ball.x, ball.y), cursor_pos]
    line_ball_x, line_ball_y = cursor_pos[0] - ball.x, cursor_pos[1] - ball.y

    aline = [(ball.x, ball.y), (ball.x + .015 * SCREEN_WIDTH, ball.y)]

    if not shoot:
        power_display = round(
            distance(line_ball_x, line_ball_y) * power_multiplier/5)

        angle_display = round(angle(cursor_pos) * deg)

    else:
        if (abs(ball.vy) < 5 and abs(ball.vx) < 1 and abs(ball.y - (START_Y - 2)) <= BOUNCE_FUZZ): #or (round(ball.vy) == -9 and not ball.vx):
            shoot = False
            ball.y = START_Y
            print('\nThe ball has come to a rest!')
            update_frame = 0
        else:
            update_frame = ball.update(update_frame)

        if not BARRIER < ball.x < SCREEN_WIDTH:
            shoot = False
            print(f'\nOut of Bounds! ({round(ball.x), round(ball.y)})')
            penalty = True
            p_ticks = pg.time.get_ticks()
            strokes += 1

            if BARRIER < xb < SCREEN_WIDTH:
                ball.x = xb
            else:
                ball.x = START_X
            ball.y = yb

    for event in pg.event.get():
        if event.type == pg.QUIT:
            quit = True

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                quit = True

            if event.key == pg.K_RIGHT:
                if spkey != max(resist_dict):
                    spkey += 1

            if event.key == pg.K_LEFT:
                if spkey != min(resist_dict):
                    spkey -= 1

            if event.key == pg.K_UP:
                if stkey != max(strength_dict):
                    stkey += 1

            if event.key == pg.K_DOWN:
                if stkey != min(strength_dict):
                    stkey -= 1

        if event.type == pg.MOUSEBUTTONDOWN:
            if not shoot:
                shoot = True
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

    draw_window()

print("\nShutting down...")
pg.quit()
