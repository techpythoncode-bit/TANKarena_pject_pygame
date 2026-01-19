import pygame  # type: ignore

def load_images():
    """Load all game images"""
    images = {
        'background': pygame.image.load('media/bgtwn.jpg'),
        'background_level2': pygame.image.load('media/bg2.jpg'),
        'background_level3': pygame.image.load('media/bg3.jpg'),
        'player': pygame.image.load('media/tnk1.png').convert_alpha(),
        'opponent': pygame.image.load('media/tnk2.png').convert_alpha(),
        'bullet_player': pygame.image.load('media/bombbullet_ply.png'),
        'bullet_opponent': pygame.image.load('media/bombbullet_opt.png'),
        'collision': pygame.image.load('media/collide_img.png'),
        'collision_tank': pygame.image.load('media/collide_for_tank.png'),
        'first_kill_opponent': pygame.image.load('media/killgot_opt.png').convert_alpha(),
        'first_kill_player': pygame.image.load('media/killgot_ply.jpg').convert_alpha(),
        'player_win': pygame.image.load('media/pl_win.png').convert_alpha(),
        'player_lost': pygame.image.load('media/pl_lost.png').convert_alpha(),
        'icon': pygame.image.load('media/icon.jpg')
    }
    return images

def load_sounds():
    """Load all game sounds"""
    sounds = {
        'fire': pygame.mixer.Sound('sounds/fire.wav'),
        'first_kill': pygame.mixer.Sound('sounds/firstkill.mp3'),
        'another_kill': pygame.mixer.Sound('sounds/anotherkill.mp3'),
        'megakill': pygame.mixer.Sound('sounds/megakill.mp3'),
        'win': pygame.mixer.Sound('sounds/wn.wav'),
        'lose': pygame.mixer.Sound('sounds/lse.mp3')
    }
    return sounds

def load_fonts():
    """Load all game fonts"""
    fonts = {
        'title': pygame.font.Font('fnts/fnt.ttf', 48),
        'kills': pygame.font.Font(None, 16),
        'label': pygame.font.Font(None, 32),
        'message': pygame.font.Font('fnts/msgfnt.ttf', 36)
    }
    return fonts

def load_music():
    """Load background music"""
    pygame.mixer.music.load('sounds/gmbgm.mp3')
    return True