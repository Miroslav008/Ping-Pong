from pygame import *
from random import randint

def tuplee(i1, i2, exp): # Tuple expression
    return eval(f'(i1[0] {exp} i2[0], i1[1] {exp} i2[1])')
def tuplees(i, s, exp): # Tuple single expression
    return eval(f'(i[0] {exp} s, i[1] {exp} s)')
def cc(coords, size): # Coordinates center
    return tuplee(coords, tuplees(size, 2, '/'), '-')
def grc(rect): # Get rect coordinates
    return [rect.x, rect.y]
def src(rect, coordinates): # Set rect coordinates
    rect.x = coordinates[0]
    rect.y = coordinates[1]
def restart_ball():
    global balltimer
    global ballvelocity
    global ballspeed
    global curround
    global pause
    global wintext
    global wintextback
    if curround < finalround:
        balltimer = 60
        ball.set_position(tuplees(winsize, 2, '/'))
        ballvelocity = Vector2(0, 0)
        ballspeed = ballstartspeed + curround // 4
    else:
        pause = True
        wintextstr = ''
        if score[0] < score[1]:
            wintextstr = 'Right wins'
        elif score[0] > score[1]:
            wintextstr = 'Left wins'
        else:
            wintextstr = 'Draw'
        wintext = winfont.render(wintextstr, True, (127, 127, 127))
        wintextback = Surface(tuplees(wintext.get_size(), 12, '+'))
        wintextback.fill((0, 0, 0))
def update_score():
    global scoretext
    global score
    for i in range(2):
        scoretext[i] = scorefont.render(str(score[i]), True, (255, 255, 255))
def define_ball_velocity():
    global ballvelocity
    ballvelocity = Vector2(ballstartvelocity * ballspeed, randint(-ballspeed, ballspeed))
def create_dir_arrows():
    global dirarrowsvisible
    global dirarrows
    global dirarrowscoords
    dirarrowsvisible = True
    rot = Vector2(0, 0).angle_to(ballvelocity)
    dirarrows = transform.rotate(dirarrowsorig.copy(), -rot - 135)
    dirarrowscoords = tuplee(grc(ball.rect), tuplees(ball.size, 2, '/'), '+') + Vector2(0, 30).rotate(rot - 90)

class GameSprite(sprite.Sprite):
    def __init__(self, texture, coordinates):
        global allsprites
        super().__init__()
        self.visible = True
        self.texture = texture
        self.size = self.texture.get_size()
        self.rect = self.texture.get_rect()
        src(self.rect, cc(coordinates, self.size))
        #self.xy = cc(coordinates, self.size)
        allsprites.append(self)
    def move(self, coordinates, min_edges, max_edges):
        #self.xy = (min(max(self.xy[0] + coordinates[0], min_edges[0]), max_edges[0]), min(max(self.xy[1] + coordinates[1], min_edges[1]), max_edges[1]))
        src(self.rect, (min(max(self.rect.x + coordinates[0], min_edges[0]), max_edges[0]), min(max(self.rect.y + coordinates[1], min_edges[1]), max_edges[1])))
    def simple_move(self, coordinates):
        #self.xy = tuplee(self.xy, coordinates, '+')
        src(self.rect, tuplee(grc(self.rect), coordinates, '+'))
    def set_position(self, coordinates):
        src(self.rect, cc(coordinates, self.size))
    def tick(self):
        if self.visible:
            w.blit(self.texture, grc(self.rect))
class StaticSprite(sprite.Sprite):
    def __init__(self, texture, coordinates):
        global allsprites
        super().__init__()
        self.visible = True
        self.texture = texture
        self.size = self.texture.get_size()
        self.rect = self.texture.get_rect()
        src(self.rect, cc(coordinates, self.size))
        #self.xy = cc(coordinates, self.size)
        allsprites.append(self)
    def tick(self):
        if self.visible:
            w.blit(self.texture, grc(self.rect))

# Window and general
winsize = (650, 450)
w = display.set_mode(winsize)
display.set_caption('Ping Pong')
clock = time.Clock()
FPS = 60
PLATFORMSPEED = round(winsize[1] / 150)

# Sprites
allsprites = []
ptexture = Surface(winsize)
ptexture.fill((0, 0, 0))
background = StaticSprite(ptexture, (winsize[0] / 2, winsize [1] / 2))

fieldlines = []
for i in range(3):
    ptexture = Surface((4 + (i % 2 * 4), winsize[1]))
    ptexture.fill((255, 255, 255))
    fieldlines.append(StaticSprite(ptexture, (winsize[0] / 4 * (i + 1), winsize[1] / 2)))

ptexturesize = (20, 70)
ptexture = Surface(ptexturesize)
ptexture.fill((255, 255, 255))
left = GameSprite(ptexture, (ptexturesize[0] * 1.5, winsize[1] / 2))
right = GameSprite(ptexture, (winsize[0] - ptexturesize[0] * 1.5, winsize[1] / 2))

ptexturesize = 30
ptexture = Surface((ptexturesize, ptexturesize))
ptexture = ptexture.convert_alpha()
ptexture.fill(Color(0, 0, 0, 0))
draw.circle(ptexture, Color(255, 255, 255), (ptexturesize / 2, ptexturesize / 2), ptexturesize / 2)
ball = GameSprite(ptexture, tuplees(winsize, 2, '/'))

dirarrows = None
dirarrowsvisible = True
dirarrowscoords = Vector2(0, 0)
ptexture = Surface((35, 35))
ptexture = ptexture.convert_alpha()
ptexture.fill((0, 0, 0, 0))
ptexture.fill((255, 255, 255), Rect(0, 0, 8, 35))
ptexture.fill((255, 255, 255), Rect(0, 0, 35, 8))
dirarrowsorig = ptexture.copy()
del ptexture, ptexturesize

# Game
game = True
pause = False
ballstartspeed = 4
ballspeed = ballstartspeed
balltimer = 60
ballvelocity = Vector2(0, 0)
ballstartvelocity = 1 - randint(0, 1) * 2
define_ball_velocity()
create_dir_arrows()
finalround = 10
curround = 0
score = [0, 0]
font.init()
scorefont = font.SysFont('arial.ttf', 50)
scoretext = [None, None]
winfont = font.SysFont('arial.ttf', 90)
update_score()
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
    if not pause:
        # Ball Control
        if balltimer > 0:
            balltimer -= 1
            if balltimer == 0:
                dirarrowsvisible = False
        else:
            # Moving Ball
            respawned = False
            if ball.rect.x + ball.size[0] <= 0:
                score[1] += 1
                curround += 1
                update_score()
                restart_ball()
                ballstartvelocity *= -1
                define_ball_velocity()
                create_dir_arrows()
                respawned = True
            elif ball.rect.x >= winsize[0]:
                score[0] += 1
                curround += 1
                update_score()
                restart_ball()
                ballstartvelocity *= -1
                define_ball_velocity()
                create_dir_arrows()
                respawned = True
            elif ball.rect.colliderect(left):
                if ball.rect.x >= left.rect.x + left.size[0] - (ballspeed + 1):  #5
                    ballvelocity.reflect_ip(Vector2(1, 0))
                else:
                    ballvelocity.reflect_ip(Vector2(0, 1))
                movoff = min(1, max(-1, (((ball.rect.y + ball.size[1] / 2) - (left.rect.y + left.size[1] / 2)) // 22)))
                ballvelocity = ballvelocity + Vector2(0, leftvelocity + movoff)
            if ball.rect.colliderect(right):
                if ball.rect.x + ball.size[0] <= right.rect.x + (ballspeed + 1):  #5
                    ballvelocity.reflect_ip(Vector2(1, 0))
                else:
                    ballvelocity.reflect_ip(Vector2(0, 1))
                movoff = min(1, max(-1, (((ball.rect.y + ball.size[1] / 2) - (right.rect.y + right.size[1] / 2)) // 22)))
                ballvelocity = ballvelocity + Vector2(0, rightvelocity + movoff)
            if ball.rect.y <= 0 or ball.rect.y + ball.size[1] >= winsize[1]:
                ballvelocity.reflect_ip(Vector2(0, 1))
            if not respawned:
                ball.simple_move(ballvelocity)
        # Moving platforms
        rightvelocity, leftvelocity = 0, 0
        keysp = key.get_pressed()
        if keysp[K_UP]:
            right.move((0, -PLATFORMSPEED), (0, 0), (winsize[0], winsize[1] - right.size[1]))
            rightvelocity -= 1
        if keysp[K_DOWN]:
            right.move((0, PLATFORMSPEED), (0, 0), (winsize[0], winsize[1] - right.size[1]))
            rightvelocity += 1
        if keysp[K_w]:
            left.move((0, -PLATFORMSPEED), (0, 0), (winsize[0], winsize[1] - left.size[1]))
            leftvelocity -= 1
        if keysp[K_s]:
            left.move((0, PLATFORMSPEED), (0, 0), (winsize[0], winsize[1] - left.size[1]))
            leftvelocity += 1
    for s in allsprites:
        s.tick()
    for i in range(2):
        w.blit(scoretext[i], cc((winsize[0] / 2 + 40 * (i * 2 - 1), 30), scoretext[i].get_size()))
    if pause:
        w.blit(wintextback, cc(tuplees(winsize, 2, '/'), wintextback.get_size()))
        w.blit(wintext, cc(tuplees(winsize, 2, '/'), wintext.get_size()))
        dirarrowsvisible = False
    if dirarrowsvisible:
        w.blit(dirarrows, cc(dirarrowscoords, dirarrows.get_size()))
    display.update()
    clock.tick(FPS)