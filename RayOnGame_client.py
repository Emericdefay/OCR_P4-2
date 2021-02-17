import pygame
import math
import sys
import random as rd



# Constants :
WIDTH = 1800
HEIGHT = 900
RAD2DEG = 2 * math.pi / 360
COMPUTERS = 100


class Ray:
    global WIDTH
    global HEIGHT

    def __init__(self, identity, pos=(100, 100), angle=0):
        # Display Surface:
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))

        # Identity :
        self.identity = identity

        # Coordinates :
        self.x = pos[0]
        self.y = pos[1]
        self.angle = angle
        self.xWeapon = 0
        self.yWeapon = 0

        # Sprite original :
        self.sprite = pygame.image.load("RaySprite{}.png".format(rd.randint(0, 3))).convert_alpha()
        self.size = self.sprite.get_size()
        self.scale = 3
        self.sprite = pygame.transform.scale(self.sprite, ((int(self.size[0] / self.scale)), int(self.size[1] / self.scale)))

        # Sprites used :
        self.sprite_rot = pygame.transform.rotate(self.sprite, 0)
        self.weapon = pygame.image.load("Missile.png").convert_alpha()
        self.weapon_rot = pygame.transform.rotate(self.weapon, 0)

        # Radius :
        self.rayRadius = 73
        self.scannerRadius = 500
        self.missileRadius = 22

        # Speed Properties :
        self.vel = 5
        self.velWeapon = 50
        self.range = 500 ** 2
        self.accel = 0

        # Gear Properties :
        self.dmgWeapon = 1
        self.hp = 10

        # Status :
        self.shot = False
        self.alive = True
        self.touched = False
        self.hit = False

    def move(self, accel, rot):
        self.angle += rot
        self.accel += accel

        if 0 <= self.accel <= 1.5:# and -10 <= self.y <= HEIGHT+10:
            self.x += self.vel * (math.cos(self.angle * RAD2DEG)) * self.accel
            self.y -= self.vel * (math.sin(self.angle * RAD2DEG)) * self.accel
            self.x = self.x % WIDTH
            self.y = self.y % HEIGHT
        elif self.accel > 1.5:
            self.accel = 1.5
        else:
            self.accel = 0

        self.sprite_rot = pygame.transform.rotate(self.sprite, self.angle)

    def shoot(self, xOrigin, yOrigin, angle):
        self.weapon_rot = pygame.transform.rotate(self.weapon, angle - 90)

        self.xWeapon += self.velWeapon * (math.cos(angle * RAD2DEG))
        self.yWeapon -= self.velWeapon * (math.sin(angle * RAD2DEG))

        if self.xWeapon < 0 or self.yWeapon < 0 or self.xWeapon > WIDTH or self.yWeapon > HEIGHT:
            self.xWeapon = -1000
            self.yWeapon = -1000
            self.shot = True
            self.reload()

        if ((self.xWeapon - xOrigin) ** 2 + (self.yWeapon - yOrigin) ** 2) > self.range:
            self.xWeapon = -1000
            self.yWeapon = -1000
            self.shot = True
            self.reload()
           
        if self.hit:
            self.xWeapon = -1000
            self.yWeapon = -1000
            self.shot = True
            self.reload()

    def reload(self):
        if self.shot:
            self.xWeapon = self.x
            self.yWeapon = self.y
            self.shot = False

    def died(self):
        self.alive = False
        self.x = -1000
        self.y = -1000
        self.xWeapon = -1000
        self.yWeapon = -1000

    def get_pos(self):
        # print(self.x, self.y) #DEBUG
        return self.x, self.y

    def get_angle(self):
        return self.angle

    def get_hp(self):
        # print(self.hp) #DEBUG
        return self.hp

    def get_touched(self):
        self.hp -= self.dmgWeapon
        if self.hp <= 0:
            self.died()

    def scan(self, group):
        for objectDetected in group:
            for typeDetected in objectDetected:
                if ((typeDetected[0] - self.x) ** 2 + (typeDetected[1] - self.y) ** 2) < self.scannerRadius ** 2:
                    # print(typeDetected[2], (typeDetected[0], typeDetected[1])) #DEBUG
                    return typeDetected[2], typeDetected[0], typeDetected[1]


class Control:

    def __init__(self, identity, ennemies):
        self.ID = identity
        self.moving = False
        self.turnRight = False
        self.turnLeft = False
        self.shooting = False
        self.scanning = False
        self.group = ennemies

    def move(self):
        self.moving = True
        return self.moving

    def stop(self):
        self.moving = False
        return self.moving

    def right(self):
        self.turnRight = True
        self.turnLeft = False
        return self.turnRight

    def left(self):
        self.turnRight = False
        self.turnLeft = True
        return self.turnLeft

    def unturn(self):
        self.turnRight = False
        self.turnLeft = False

    def shoot(self):
        self.shooting = True
        return self.shooting

    def unshoot(self):
        self.shooting = False
        return self.shooting

    def scan(self):
        self.scanning = True
        return self.ID.scan(self.group)

    def unscan(self):
        self.scanning = False
        return self.scanning

    def pos(self):
        return self.ID.get_pos()

    def angle(self):
        return self.ID.get_angle()


def behaviorBot(ray):
    """

    :param ray:
    # Commands & associate Status

    ## Movements :
    ray.move() - ray.moving
    ray.stop() - ray.moving
    ray.right() - ray.turnRight
    ray.left() - ray.turnLeft
    ray.unturn() - X

    ## Localisation :
    ray.scan() - ray.scanning
    ray.pos() - X
    ray.angle() - X
    ## Actions :
    ray.shoot() - ray.shooting


    :return:
    """

    ray.move()
    ray.scan()
    if ray.scanning:
        if ray.scan():
            if ray.scan()[0] == "ray":
                angle = math.atan2(ray.scan()[2] - ray.pos()[1], ray.scan()[1] - ray.pos()[0])
                angle = abs(int(angle / RAD2DEG))
                if angle - 10 <= int(ray.angle() % 360) <= angle + 10:
                    ray.unturn()
                    ray.shoot()
                elif angle + 10 < int(ray.angle() % 360) <= angle + 100:
                    ray.right()
                    ray.unshoot()
                else:
                    ray.left()
                    ray.unshoot()

            if ray.scan()[0] == "missile":
                ray.move()
                ray.left()
            else:
                ray.unturn()


def groupEnnemies(group, identity):
    groupEnnemies = []
    for k in range(len(group)):
        if k != identity:
            groupEnnemies.append(group[k])
    return groupEnnemies


def drive(joueur, controleur, ennemies, window, xShot, yShot, angleShot):
    if joueur.alive:
        # Movements :
        if controleur.turnLeft and not controleur.turnRight:
            joueur.move(0, 3)
        if controleur.moving:
            joueur.move(0.2, 0)
        if controleur.turnRight and not controleur.turnLeft:
            joueur.move(0, -3)

        # Scan :
        if controleur.scanning:
            joueur.scan(ennemies)

        # Shoot
        xStatic = joueur.xWeapon
        yStatic = joueur.yWeapon

        if controleur.shooting:
            joueur.reload()
            angleShot = joueur.angle
            xShot = joueur.x
            yShot = joueur.y
            joueur.shoot(xShot, yShot, angleShot)
        if joueur.shot:
            joueur.reload()

        # Updates :
        # Collisions :
        for k in range(len(ennemies)):
            if (ennemies[k][1][0] - joueur.x)**2 + (ennemies[k][1][1] - joueur.y)**2 < joueur.rayRadius**2:
                joueur.get_touched()
        # Deceleration :
        joueur.move(-0.01, 0)

        # Display :
        if not (xStatic is joueur.xWeapon and yStatic is joueur.yWeapon):
            window.blit(joueur.weapon_rot, joueur.weapon_rot.get_rect(center=(joueur.xWeapon, joueur.yWeapon)))
        window.blit(joueur.sprite_rot, joueur.sprite_rot.get_rect(center=(joueur.x, joueur.y)))
        return True
    else:
        return False


def main():
    # Initialization :
    pygame.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("RayOnGame")
    clock = pygame.time.Clock()

    # Init global variables:
    global COMPUTERS
    run = True
    survivors = COMPUTERS

    # Adding bot(s) :
    rays = [Ray(i+1, (WIDTH//2+(WIDTH//3)*math.cos(i/(RAD2DEG*COMPUTERS)), HEIGHT//2+(HEIGHT//3)*math.sin(i/(COMPUTERS*RAD2DEG))), (45-i*90)) for i in range(COMPUTERS)]

    # Group of sprites:
    groupAll = [[(-1000, -1000, "ray"), (-1000, -1000, "missile")] for i in range(COMPUTERS)]

    # Init bots:
    bots = [Control(rays[i], groupEnnemies(groupAll, i)) for i in range(COMPUTERS)]

    # init bot(s) variables:
    """
    liste : [0,0,0] -> [xShot, yShot, angleShot]
    """
    paramBots = [[0, 0, 0] for i in range(COMPUTERS)]

    # Init background:
    win.fill((0, 6, 60))

    while run:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
                sys.exit()

        win.fill((0, 6, 60))

        # BOT players :
        # A ajouter ID du joueur ici
        bots = [Control(rays[i], groupEnnemies(groupAll, i)) for i in range(len(rays))]

        # L'ID viendra dans le behaviorBot -> behaviorBot(ID, bot)
        for bot in bots:
            behaviorBot(bot)

        for i in range(len(rays)):
            if not (drive(rays[i], bots[i], groupEnnemies(groupAll, i), win, paramBots[i][0], paramBots[i][1], paramBots[i][2])):
                del rays[i]
                del bots[i]
                del groupAll[i]
                del paramBots[i]
                survivors -= 1
                break

        # Actualize data :
        groupAll = [[(rays[i].x, rays[i].y, "ray"), (rays[i].xWeapon, rays[i].yWeapon, "missile")] for i in range(len(rays))]

        font = pygame.font.SysFont("comicsans", 60)
        text = font.render("Rays {} vivantes".format(survivors), 1, (255, 0, 0))
        win.blit(text, (100, 100))

        # Survivors :
        if survivors < 2:
            font = pygame.font.SysFont("comicsans", 60)
            text = font.render("Ray {} WIN".format(rays[0].identity), 1, (255, 0, 0))
            win.blit(text, (WIDTH//2, HEIGHT//2))

        # UPDATES :
        pygame.display.flip()


if __name__ == '__main__':
    main()