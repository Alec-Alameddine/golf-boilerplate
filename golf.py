import math
import pygame as pg

SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 800
WINDOW_COLOR = (100, 100, 100)
LINE_COLOR = (0, 0, 255)
ALINE_COLOR = (0, 0, 0)
BARRIER = 1
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

speedMultiplierFont = pg.font.SysFont("courier new", 13)
SPEEDMULTIPLIERCOLOR = (255, 0, 0)

powerMultiplierFont = pg.font.SysFont("courier new", 13)
POWERMULTIPLIERCOLOR = (255, 0, 0)


class Ball(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 10
        self.color = (255, 255, 255)
        self.outlinecolor = (255, 0, 0)

    def show(self, window):
        pg.draw.circle(window, self.outlinecolor, (self.x, self.y), self.radius)
        pg.draw.circle(window, self.color, (self.x, self.y), self.radius - int(.4 * self.radius))

    @staticmethod
    def path(x, y, p, a, t, bounce=False):
        vx, vy = p * math.cos(a), p * math.sin(a)  #Velocities
        dx, dy = vx * t, vy * t - gravity(t)  #Distances Traveled

        if bounce: pass

        print(f'    x-pos: {dx + x:.0f}px')
        print(f'    y-pos: {abs(dy - y):.0f}px')

        return round(dx + x), round(y - dy)

    @staticmethod
    def quadrant(x,y,xm,ym):
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
        penalty_text = 'Out of Bounds! +1 Stroke'
        penalty_label = penaltyFont.render(penalty_text, 1, PENALTYCOLOR)
        penalty_rect = penalty_label.get_rect(center=(SCREEN_WIDTH/2, .225*SCREEN_HEIGHT))
        window.blit(penalty_label, penalty_rect)

    speed_multiplier_text = 'Speed: {:2.2f} m/s'.format(speed_multiplier)
    speed_multiplier_label = speedMultiplierFont.render(speed_multiplier_text, 1, SPEEDMULTIPLIERCOLOR)
    window.blit(speed_multiplier_label, (.91*SCREEN_WIDTH,.98*SCREEN_HEIGHT))

    power_multiplier_text = f'Strength: {int(power_multiplier*100)}%'
    power_multiplier_label = powerMultiplierFont.render(power_multiplier_text, 1, POWERMULTIPLIERCOLOR)
    window.blit(power_multiplier_label, (.01*SCREEN_WIDTH,.98*SCREEN_HEIGHT))

    #strength

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

def gravity(t):
    return 4.9*t**2


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
x, y, time, power, ang, strokes = 0, 0, 0, 0, 0, 0
xb, yb = None, None
shoot, penalty = False, False
p_ticks = 0

ball = Ball(START_X, START_Y)
quit = False

strength_dict = {0: .01, 1: .02, 2: .04, 3: .08, 4: .16, 5: .25, 6: .50, 7: .75, 8: 1}; stkey = 6
speed_dict = {0: .25, 1: .5, 2: 1, 3: 1.5, 4: 2, 5: 2.5, 6: 3, 7: 3.5, 8: 4, 9: 5, 10: 7.5, 11: 10}; spkey = 4

window = initialize()
try:
    while not quit:
        power_multiplier = strength_dict[stkey]
        speed_multiplier = speed_dict[spkey]

        seconds = (pg.time.get_ticks()-p_ticks)/1000
        if seconds > 1.2: penalty = False

        cursor_pos = pg.mouse.get_pos()
        line = [(ball.x, ball.y), cursor_pos]
        line_ball_x, line_ball_y = cursor_pos[0] - ball.x, cursor_pos[1] - ball.y

        aline = [(ball.x, ball.y), (ball.x + .015 * SCREEN_WIDTH, ball.y)]

        if not shoot:
            power_display = round(
                distance(line_ball_x, line_ball_y) * power_multiplier/6)

            angle_display = round(angle(cursor_pos) * deg)

        if shoot:
            time += .3 * speed_multiplier
            print('\n   time: %ss' % round(time, 2))
            if ball.y <= START_Y:
                if BARRIER < ball.x < SCREEN_WIDTH:
                    po = ball.path(x, y, power, ang, time)
                    ball.x, ball.y = po[0], po[1]
                else:
                    print('Out of Bounds!')
                    penalty = True
                    p_ticks = pg.time.get_ticks()
                    strokes += 1
                    shoot = False
                    if BARRIER < xb < SCREEN_WIDTH:
                        ball.x = xb
                    else:
                        ball.x = START_X
                    ball.y = yb
            else:
                shoot = False
                ball.y = START_Y

        for event in pg.event.get():
            if event.type == pg.QUIT:
                quit = True

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    quit = True

                if event.key == pg.K_RIGHT:
                    if speed_multiplier != 10:
                        spkey += 1

                if event.key == pg.K_LEFT:
                    if speed_multiplier != .25:
                        spkey -= 1

                if event.key == pg.K_UP:
                    if power_multiplier != 1:
                        stkey += 1

                if event.key == pg.K_DOWN:
                    if power_multiplier != .01:
                        stkey -= 1

            if event.type == pg.MOUSEBUTTONDOWN:
                if not shoot:
                    shoot = True
                    x, y = ball.x, ball.y
                    xb, yb = ball.x, ball.y
                    time, power = 0, (
                        distance(line_ball_x, line_ball_y)) * power_multiplier/6
                    print('\n\nBall Hit!')
                    print('\npower: %sN' % round(power, 2))
                    ang = angle(cursor_pos)
                    print('angle: %s°' % round(ang * deg, 2))
                    print('cos(a): %s' % round(math.cos(ang), 2)), print('sin(a): %s' % round(math.sin(ang), 2))
                    strokes += 1

        draw_window()

    print("\nShutting down...")
    pg.quit()

except Exception as error:
    print(f'A fatal error ({error}) has occurred. The program is shutting down.')
    pg.quit()
