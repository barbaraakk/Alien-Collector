import os
os.environ['SDL_VIDEO_CENTERED'] = '1'
import pgzrun
import math, random
from pygame import Rect

#CONFIGURAÇÕES
WIDTH, HEIGHT = 800, 600
TITLE = "Alien - Coletador"

#VARIAVEIS GLOBAIS
game_state = "menu"
transition_timer = 0

score = 0
level = 1
MAX_LEVEL = 2

sound_on = True

#BOTOES MENU
btn_start = Rect((300, 200), (200, 50))
btn_sound = Rect((300, 270), (200, 50))
btn_exit  = Rect((300, 340), (200, 50))

#NIVEIS
LEVEL_DATA = {
    1: {
        'bg': (255, 200, 150),
        
        'bees': [
            {
                'x': 100,
                'y': 450,
                'min_x': 50,
                'max_x': 350,
                'speed': 2.5
            },
            {
                'x': 600,
                'y': 300,
                'min_x': 400,
                'max_x': 750,
                'speed': 2.5
            },
        ],
        
        'crystals': [
            (200, 200),
            (650, 500),
            (100, 100),
            (500, 50)
        ]
    },
    
    2: {
        'bg': (150, 220, 180),
        
        'bees': [
            {
                'x': 150,
                'y': 400,
                'min_x': 50,
                'max_x': 400,
                'speed': 3.0
            },
            {
                'x': 550,
                'y': 250,
                'min_x': 350,
                'max_x': 750,
                'speed': 3.0
            },
            {
                'x': 350,
                'y': 150,
                'min_x': 100,
                'max_x': 600,
                'speed': 2.8
            },
        ],
        
        'crystals': [
            (150, 150),
            (700, 450),
            (80, 80),
            (450, 100),
            (600, 550)
        ]
    }
}

#CLASSES DE SPRITES ANIMADOS
class AnimatedSprite:
    def __init__(self, x, y, idle_frames, active_frames):
        self.x, self.y = x, y
        self.idle_frames = idle_frames
        self.active_frames = active_frames
        self.frame_index = 0
        self.frame_timer = 0
        self.is_active = False
        self.actor = Actor(idle_frames[0], center=(x, y))

    def animate(self, speed=8):
        self.frame_timer += 1
        if self.frame_timer >= speed:
            self.frame_timer = 0
            frames = self.active_frames if self.is_active else self.idle_frames
            self.frame_index = (self.frame_index + 1) % len(frames)
            self.actor.image = frames[self.frame_index]

    def draw(self):
        self.actor.center = (self.x, self.y)
        self.actor.draw()


#Classe do Jogador
class Player(AnimatedSprite):
    def __init__(self):
        super().__init__(
            400, 550,
            idle_frames=['alien_idle1', 'alien_idle2'],
            active_frames=['alien_walk1', 'alien_walk2']
        )
        self.target_x = self.x
        self.target_y = self.y
        self.speed = 4


    def update(self):
        dx, dy = self.target_x - self.x, self.target_y - self.y
        dist = math.hypot(dx, dy)
        if dist > 1:
            self.is_active = True
            self.x += (dx / dist) * self.speed
            self.y += (dy / dist) * self.speed
        else:
            self.is_active = False
        self.actor.center = (self.x, self.y)
        self.animate(8)


# Classe da Abelha
class Bee(AnimatedSprite):
    def __init__(self, x, y, min_x, max_x, speed):
        super().__init__(x, y, ['bee_idle1', 'bee_idle2'], ['bee_fly1', 'bee_fly2'])
        self.min_x, self.max_x = min_x, max_x
        self.base_y = y
        self.speed = speed
        self.direction = random.choice([-1, 1])
        self.is_active = True
        self.wave_time = random.uniform(0, math.pi * 2)  # fase inicial diferente pra cada abelha

    def update(self):
        self.wave_time += 0.1
        self.y = self.base_y + math.sin(self.wave_time) * 20  # sobe/desce
        self.x += self.speed * self.direction

        if self.x < self.min_x or self.x > self.max_x:
            self.direction *= -1

        self.animate(10)


#CRISTAIS
class Crystal(AnimatedSprite):
    def __init__(self, x, y):
        super().__init__(x, y, ['crystal1', 'crystal2'], ['crystal1', 'crystal2'])
        self.is_active = True

    def update(self):
        self.animate(15)


#VAR JOGO
player = Player()
bees = []
crystals = []


#CORES
COLORS = {
    "bg": (22, 22, 28),
    "panel": (36, 36, 48),
    "accent": (140, 180, 255),
    "text": (230, 230, 235),
    "muted": (150, 150, 160),
    "danger": (255, 100, 100),
    "success": (100, 255, 160),
}

#DESENHAR TEXTOS E BOTOES
def draw_text(text, center, size=32, color=None, bold=False):
    if color is None:
        color = COLORS["text"]

    screen.draw.text(
        text,
        center=center,
        fontsize=size,
        color=color,
        bold=bold
    )

def draw_button(rect, label):
    screen.draw.filled_rect(rect, COLORS["panel"])
    screen.draw.rect(rect, COLORS["accent"])
    draw_text(label, rect.center, 26, COLORS["text"])

def draw():
    screen.clear()
    screen.fill(COLORS["bg"])

    if game_state == "menu":
        draw_text(TITLE, (WIDTH / 2, 140), 64, COLORS["accent"], bold=True)
        draw_button(btn_start, "INICIAR")
        draw_button(btn_sound, f"SOM: {'ON' if sound_on else 'OFF'}")
        draw_button(btn_exit, "SAIR")

    elif game_state == "playing":
        screen.fill(COLORS["bg"])
        for obj in crystals + bees + [player]:
            obj.draw()
        draw_text(f"Level {level}", (70, 30), 26, COLORS["muted"])
        draw_text(f"Score: {score}", (WIDTH - 100, 30), 26, COLORS["muted"])

    elif game_state == "level_end":
        screen.fill(COLORS["bg"])
        draw_text("Level concluído", (WIDTH / 2, HEIGHT / 2 - 20), 48, COLORS["success"], bold=True)
        draw_text("Aguarde para continuar", (WIDTH / 2, HEIGHT / 2 + 40), 26, COLORS["muted"])

    elif game_state == "over":
        screen.fill(COLORS["bg"])
        draw_text("Game Over", (WIDTH / 2, HEIGHT / 2 - 20), 48, COLORS["danger"], bold=True)
        draw_text(f"Score: {score}", (WIDTH / 2, HEIGHT / 2 + 30), 28, COLORS["muted"])
        draw_text("Clique para jogar novamente", (WIDTH / 2, HEIGHT / 2 + 70), 24, COLORS["muted"])

    elif game_state == "win":
        screen.fill(COLORS["bg"])
        draw_text("VOCÊ VENCEU!!", (WIDTH / 2, HEIGHT / 2 - 20), 48, COLORS["accent"], bold=True)
        draw_text(f"Pontos finais: {score}", (WIDTH / 2, HEIGHT / 2 + 30), 28, COLORS["muted"])
        draw_text("Clique para voltar", (WIDTH / 2, HEIGHT / 2 + 70), 24, COLORS["muted"])


#ATUALIZAÇÃO DO JOGO
def update():

    global game_state, score, transition_timer
    
    if game_state == "playing":
        player.update()

        for bee in bees:
            bee.update()
            if player.actor.colliderect(bee.actor):
                play_sound('hurt.ogg')
                game_state = "over"
                return

        for crystal in crystals[:]:
            crystal.update()
            if player.actor.colliderect(crystal.actor):
                crystals.remove(crystal)
                score += 1
                play_sound('pickup.ogg')

        if not crystals:
            play_sound('win.ogg')
            game_state = "level_end"
            transition_timer = 90

    elif game_state == "level_end":
        transition_timer -= 1
        if transition_timer <= 0:
            next_level()


#MOUSE CONTROLES
def on_mouse_down(pos):
    global game_state, sound_on

    if game_state == "menu":
        if btn_start.collidepoint(pos):
            reset_game()
            game_state = "playing"
        elif btn_sound.collidepoint(pos):
            sound_on = not sound_on
            update_music()
        elif btn_exit.collidepoint(pos):
            exit()

    elif game_state == "playing":
        player.target_x, player.target_y = pos

    elif game_state in ("over", "win"):
        game_state = "menu"


#FUNCOES DO JOGO
def reset_game():
    global score, level
    score, level = 0, 1
    load_level(level)
    update_music()


def next_level():
    global level, game_state
    level += 1
    if level <= MAX_LEVEL:
        load_level(level)
        game_state = "playing"
    else:
        game_state = "win"


def load_level(n):
    player.x = player.target_x = 400
    player.y = player.target_y = 550
    bees.clear()
    crystals.clear()

    level_cfg = LEVEL_DATA[n]
    for bee_data in level_cfg['bees']:
        bees.append(Bee(bee_data['x'], bee_data['y'], bee_data['min_x'], bee_data['max_x'], bee_data['speed']))
    for c in level_cfg['crystals']:
        crystals.append(Crystal(c[0], c[1]))


def play_sound(name):
    if sound_on:
        try:
            getattr(sounds, name).play()
        except Exception as e:
            print(f"[ERRO DE SOM] '{name}': {e}")


def update_music():
    if sound_on:
        if not music.is_playing('bg_loop.wav'):
            try:
                music.play('bg_loop.wav')
                music.set_volume(0.4)
            except:
                pass
    else:
        music.stop()


#INICIO
update_music()
reset_game()
game_state = "menu"

pgzrun.go()
