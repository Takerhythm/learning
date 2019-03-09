import sys
import pygame
import pygame.locals
import random
# 定义常量
WINDOW_WIDTH = 512
WINDOW_HEIGHT = 768
WINDOW_ICON = pygame.image.load("res/app.ico")
WINDOW_CAPTION = "飞机大战"
BACKGROUND_IMG = pygame.image.load("res/img_bg_level_" + str(random.randint(1, 5)) + ".jpg")
PLAYERPLANE_IMG = pygame.image.load("res/hero.png")
Bullets_IMG = pygame.image.load("res/bullet_12.png")


class Models:  # 定义模型父类
    WINDOW = None

    def __init__(self, img, x, y):  # 初始化模型
        self.img = img
        self.x = x
        self.y = y

    def blit_display(self):  # 模型贴图
        Models.WINDOW.blit(self.img, (self.x, self.y))

    @staticmethod  # 碰撞检测
    def coll_check(rect1, rect2):
        return pygame.Rect.colliderect(rect1, rect2)


class BackGround(Models):
    def move(self):  # 背景移动
        if self.y <= WINDOW_HEIGHT:
            self.y += 1
        else:
            self.y = 0

    def blit_display(self):  # 重写父类贴图,为背景以及辅助背景贴图
        super().blit_display()
        Models.WINDOW.blit(self.img, (self.x, self.y - WINDOW_HEIGHT))  # 定义辅助背景


class PlayerPlane(Models):
    def __init__(self, img, x, y):
        super().__init__(img, x, y)
        self.bullets = []  # 定义子弹列表
        self.boom = Boom()
        self.life = 100

    def blit_display(self, enemys):  # 子弹贴图及碰撞处理
        super().blit_display()
        remove_bullets = []
        for bullet in self.bullets:
            if bullet.y < -29:  # 超出屏幕处理
                remove_bullets.append(bullet)
            else:
                bullet_model = pygame.locals.Rect(bullet.x, bullet.y, 20, 29)  # 建立子弹模型
                for enemy in enemys:
                    enemyplane_model = pygame.locals.Rect(enemy.x, enemy.y, 100, 68)  # 建立 敌机模型
                    if Models.coll_check(bullet_model, enemyplane_model):
                        remove_bullets.append(bullet)
                        enemy.status = True  # 碰撞状态开启
                        enemy.boom.is_boom = True  # 爆炸效果开启
                        enemy.boom.x = enemy.x  # 爆炸坐标开启
                        enemy.boom.y = enemy.y
                        sound = pygame.mixer.Sound("res/bomb.wav")
                        sound.play()
                        Game.score += 1
                        break
        for bullet in remove_bullets:  # 玩家碰撞检测
            self.bullets.remove(bullet)
        playerplane_model = pygame.locals.Rect(self.x, self.y, 120, 68)
        for enemy in enemys:
            enemyplane_model = pygame.locals.Rect(enemy.x, enemy.y, 100, 68)
            enemyplane__bullet_model = pygame.locals.Rect(enemy.enemyplane_bullet[0].x, enemy.enemyplane_bullet[0].y, 20, 29)
            if Models.coll_check(enemyplane_model, playerplane_model) or Models.coll_check(playerplane_model, enemyplane__bullet_model):
                # enemy.status = True
                # enemy.boom.is_boom = True
                # pygame.mixer.music.load("res/gameover.wav")
                # pygame.mixer.music.play(loops=1)
                self.life -= 1
                if self.life <= 0:
                    pygame.mixer.music.load("res/gameover.wav")
                    pygame.mixer.music.play(loops=1)
                    return 2
        return 1


class EnemyPlane(Models):
    def __init__(self):
        self.img = pygame.image.load("res/img-plane_" + str(random.randint(1, 7)) + ".png")
        self.x = random.randint(0, WINDOW_WIDTH - 100)
        self.y = -random.randint(68, WINDOW_HEIGHT)
        self.status = False  # 设置敌机状态
        self.boom = Boom()
        self.enemyplane_bullet = []

    def move(self):
        if self.y <= WINDOW_HEIGHT and not self.status:
            self.y += 2
        else:  # 敌机重置
            if self.enemyplane_bullet[0].y > WINDOW_HEIGHT + 29:
                self.enemyplane_bullet.pop(0)
            self.img = pygame.image.load("res/img-plane_" + str(random.randint(1, 7)) + ".png")
            self.y = -random.randint(68, WINDOW_HEIGHT)
            self.x = random.randint(0, WINDOW_WIDTH - 100)
            self.status = False
            self.boom.is_boom = False
            bullet = Bullets(pygame.image.load("res/bullet_1.png"), self.x + 40, self.y + 34)
            self.enemyplane_bullet.append(bullet)
            self.enemyplane_bullet[0].move(Bullets.enemyplane_move_speed)

    def blit_display(self, enemyplane):
        super().blit_display()
        Bullets.blit_display(self.enemyplane_bullet[0], enemyplane)
        if self.boom.is_boom:
            Boom.blit_display(self.boom)


class Bullets(Models):
    playerplane_move_speed = -12
    enemyplane_move_speed = 2.5

    def move(self, move_speed,):  # 子弹移动
        self.y += move_speed

    def blit_display(self, enemyplane):
        super().blit_display()


class Boom(Models):  # 定义爆炸效果类
    def __init__(self):
        self.x = None  # 爆炸坐标默认关闭
        self.y = None
        self.imgs = [pygame.image.load("res/bomb-" + str(i) + ".png") for i in range(1, 8)]
        self.is_boom = False  # 定义是否爆炸属性
        self.times = 0  # 定义爆炸动画播放次序

    def blit_display(self):  # 重写定义单独爆炸效果
        if self.is_boom and self.times < len(self.imgs) * 10000:
            Models.WINDOW.blit(self.imgs[self.times//10000], (self.x, self.y))
            self.times += 1
        else:
            self.times = 0
            self.is_boom = False


class Game:
    score = 0

    def __init__(self):
        self.status = 1
    # 定义主程序
    def run(self):
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load("res/bg.wav")
        pygame.mixer.music.play()
        self.window_init()
        self.model_init()
        while True:
            self.background.move()
            self.background.blit_display()
            if self.status == 0:
                pass
            elif self.status == 1:
                for enemyplane in self.enemyplanes:  # 敌机贴图及移动
                    enemyplane.blit_display(enemyplane)
                    enemyplane.move()
                    enemyplane.enemyplane_bullet[0].move(Bullets.enemyplane_move_speed)
                self.status = self.playerplane.blit_display(self.enemyplanes)
                for bullet in self.playerplane.bullets:  # 子弹贴图及移动
                    bullet.blit_display(enemyplane)
                    bullet.move(Bullets.playerplane_move_speed)
            elif self.status == 2:
                font_over = pygame.font.Font("res/DENGB.TTF", 40)
                text_obj = font_over.render("GAMEOVER\n得分:"+str(Game.score), 1, (255, 0, 0))
                self.window.blit(text_obj, pygame.locals.Rect(43, 300, 226, 43))
            pygame.display.update()  # 窗体更新
            self.events_init()

    def window_init(self):  # 窗体初始化
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        Models.WINDOW = self.window
        pygame.display.set_icon(WINDOW_ICON)
        pygame.display.set_caption(WINDOW_CAPTION)

    def events_init(self):  # 事件监听
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:  # 窗体退出
                sys.exit()
            if event.type == pygame.locals.MOUSEMOTION:  # 鼠标位置获取
                mouse_position = pygame.mouse.get_pos()
                self.playerplane.x = mouse_position[0] - 100/2
                self.playerplane.y = mouse_position[1] - 68/2 + 5
        press_status = pygame.mouse.get_pressed()  # 鼠标按压获取
        if press_status[0] == 1 and self.status == 1:
            mouse_position = pygame.mouse.get_pos()
            bullet = Bullets(Bullets_IMG, mouse_position[0] - 20 / 2, mouse_position[1] - 78 / 2 - 29)
            self.playerplane.bullets.append(bullet)

    def model_init(self):  # 模型初始化
        self.background = BackGround(BACKGROUND_IMG, 0, 0)  # 生成背景
        self.enemyplanes = []
        for _ in range(5):  # 生成5架敌机
            enemyplane = EnemyPlane()
            bullet = Bullets(pygame.image.load("res/bullet_1.png"), enemyplane.x + 40, enemyplane.y + 30)
            enemyplane.enemyplane_bullet.append(bullet)
            self.enemyplanes.append(enemyplane)
        self.playerplane = PlayerPlane(PLAYERPLANE_IMG, 200, 500)  # 生成玩家飞机


if __name__ == "__main__":
    Game().run()
