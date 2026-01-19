##########################
import pygame  # type: ignore
import sys
import random
from pygame.locals import QUIT, KEYDOWN, K_SPACE  # type: ignore
import load
import tanks
import level1
import level2
import level3
import loading_screen
import menu
import save_system

# ---------------- INIT ---------------- 
pygame.init()
sound_enabled = True
try:
    pygame.mixer.init()
except Exception as e:
    print('Warning: audio disabled -', e)
    sound_enabled = False

# ---------------- VARIABLES ---------------- 
size_x = 1350
size_y = 463
##########################
# Current level (default to level 1, can be changed)
current_level_module = level1
current_level_num = 1

def load_level(level_num):
    """Load level configuration and reset game state"""
    global current_level_module, current_level_num, current_level
    global PL_MAX_HLTH, OP_MAX_HLTH, pl_hlth, op_hlth
    global pl_x, pl_y, op_x, op_y
    global bullt_speed, bullt_speed_op
    global WIN_TARGET, DAMAGE_PER_HIT
    global pl_kills, op_kills, game_over, winner, game_over_played
    global bullt_state, bullt_state_op, bullt_x, bullt_y, bullt_x_op, bullt_y_op
    global hit_feedback_list, first_kill_done, first_kill_show, kill_banner_show
    global title_text, gm_bg  # Add title_text and gm_bg to globals

    # Load level module
    if level_num == 1:
        current_level_module = level1
        gm_bg = images['background']
    elif level_num == 2:
        current_level_module = level2
        gm_bg = images['background_level2']
    elif level_num == 3:
        current_level_module = level3
        gm_bg = images['background_level3']
    else:
        current_level_module = level1  # Default to level 1
        gm_bg = images['background']

    current_level_num = level_num
    current_level = current_level_module

    # Update title text for new level
    title_text = title_font.render(current_level.LEVEL_NAME, True, 'blue')


def reset_game_state():
    """Reset all transient game state to match the currently loaded level"""
    global PL_MAX_HLTH, OP_MAX_HLTH, pl_hlth, op_hlth
    global pl_x, pl_y, op_x, op_y
    global bullt_speed, bullt_speed_op, WIN_TARGET, DAMAGE_PER_HIT
    global pl_kills, op_kills, game_over, winner, game_over_played
    global bullt_state, bullt_state_op, bullt_x, bullt_y, bullt_x_op, bullt_y_op
    global hit_feedback_list, first_kill_done, first_kill_show, kill_banner_show
    global op_last_fire, op_fire_delay, first_kill_by_player

    PL_MAX_HLTH = current_level.PL_MAX_HLTH
    OP_MAX_HLTH = current_level.OP_MAX_HLTH
    pl_hlth = PL_MAX_HLTH
    op_hlth = OP_MAX_HLTH

    pl_x = current_level.PL_START_X
    pl_y = current_level.PL_START_Y
    op_x = current_level.OP_START_X
    op_y = current_level.OP_START_Y

    bullt_speed = current_level.PL_BULLET_SPEED
    bullt_speed_op = current_level.OP_BULLET_SPEED
    WIN_TARGET = current_level.WIN_TARGET
    DAMAGE_PER_HIT = current_level.DAMAGE_PER_HIT

    pl_kills = 0
    op_kills = 0
    game_over = False
    winner = None
    game_over_played = False

    bullt_state = 'ready'
    bullt_state_op = 'ready'
    bullt_x = pl_x + 20
    bullt_y = pl_y + 100
    bullt_x_op = op_x
    bullt_y_op = op_y + 100

    hit_feedback_list = []
    first_kill_done = False
    first_kill_show = False
    first_kill_by_player = False
    kill_banner_show = False
####################################################
    # Reset opponent fire timing
    op_last_fire = 0
    op_fire_delay = random.randint(current_level.OP_FIRE_DELAY_MIN, current_level.OP_FIRE_DELAY_MAX)

# ---------------- USERNAME PROMPT ----------------

def show_username_prompt(screen, size_x, size_y, fonts):
    """Show a simple modal to enter username and return it."""
    clock = pygame.time.Clock()
    title_font = fonts.get('title', pygame.font.Font(None, 72))
    label_font = fonts.get('label', pygame.font.Font(None, 28))

    username = ''
    active = True

    # Semi-transparent overlay
    overlay = pygame.Surface((size_x, size_y))
    overlay.set_alpha(180)
    overlay.fill((10, 10, 20))

    # Input box rect
    box_w, box_h = 520, 56
    box_rect = pygame.Rect((size_x - box_w) // 2, (size_y - box_h) // 2, box_w, box_h)

    while active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # Accept
                    final_name = username.strip() or 'Player'
                    return final_name
                elif event.key == pygame.K_ESCAPE:
                    # Cancel with default
                    return 'Player'
                elif event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                else:
                    ch = event.unicode
                    # Allow letters, numbers, underscore, space and hyphen
                    if (ch.isalnum() or ch in ['_', ' ', '-']) and len(username) < 16:
                        username += ch

        # Draw overlay on top of current frame
        screen.blit(overlay, (0, 0))

        # Title
        title_surf = title_font.render('Enter Your Username', True, (255, 255, 255))
        title_rect = title_surf.get_rect(center=(size_x // 2, size_y // 2 - 80))
        screen.blit(title_surf, title_rect)

        # Input box
        pygame.draw.rect(screen, (230, 230, 240), box_rect, border_radius=8)
        pygame.draw.rect(screen, (120, 120, 140), box_rect, 2, border_radius=8)

        # Caret blink
        caret_visible = (pygame.time.get_ticks() // 500) % 2 == 0
        display_text = username if len(username) > 0 else ''
        text_surf = label_font.render(display_text, True, (10, 10, 30))
        text_rect = text_surf.get_rect(midleft=(box_rect.left + 12, box_rect.centery))
        screen.blit(text_surf, text_rect)

        # Placeholder
        if len(username) == 0:
            ph_surf = label_font.render('Type here (max 16 chars) ...', True, (130, 130, 150))
            ph_rect = ph_surf.get_rect(midleft=(box_rect.left + 12, box_rect.centery))
            screen.blit(ph_surf, ph_rect)

        # Caret drawing at end of text
        if caret_visible:
            caret_x = text_rect.right + 4
            caret_y = box_rect.top + 12
            caret_h = box_rect.height - 24
            pygame.draw.rect(screen, (60, 60, 80), (caret_x, caret_y, 2, caret_h))

        # Helper text
        help_surf = label_font.render('Press Enter to confirm, Esc for default', True, (200, 200, 220))
        help_rect = help_surf.get_rect(center=(size_x // 2, box_rect.bottom + 32))
        screen.blit(help_surf, help_rect)

        pygame.display.update()
        clock.tick(60)

# ---------------- COUNTDOWN ----------------

def show_countdown(screen, size_x, size_y, fonts, bg_surface):
    """Display a 3-2-1 countdown with fade-out animation before level starts.
    Uses default system font to guarantee numeric glyphs and a dim backdrop for contrast.
    """
    clock = pygame.time.Clock()
    # Use default font to ensure digits always render
    big_font = pygame.font.Font(None, 160)

    numbers = ['3', '2', '1']
    duration = 900  # ms per number for better visibility

    for num in numbers:
        start = pygame.time.get_ticks()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            elapsed = pygame.time.get_ticks() - start
            if elapsed > duration:
                break

            # Fade out alpha from 255 -> 0 over duration
            t = max(0.0, min(1.0, elapsed / duration))
            alpha = int(255 * (1.0 - t))

            # Redraw background
            screen.blit(bg_surface, (0, 0))

            # Dimmer for contrast
            dim = pygame.Surface((size_x, size_y), pygame.SRCALPHA)
            dim.fill((0, 0, 0, 120))
            screen.blit(dim, (0, 0))

            # Create a transparent overlay for the number and fade the whole overlay
            overlay = pygame.Surface((size_x, size_y), pygame.SRCALPHA)
            # Add a subtle shadow to the number for readability
            num_surf_shadow = big_font.render(num, True, (0, 0, 0))
            num_rect = num_surf_shadow.get_rect(center=(size_x // 2 + 3, size_y // 2 + 3))
            overlay.blit(num_surf_shadow, num_rect)
            num_surf = big_font.render(num, True, (255, 255, 255))
            num_rect = num_surf.get_rect(center=(size_x // 2, size_y // 2))
            overlay.blit(num_surf, num_rect)
            overlay.set_alpha(alpha)
            screen.blit(overlay, (0, 0))

            pygame.display.update()
            clock.tick(60)

# ---------------- SCREEN ---------------- 
# Set display mode FIRST before loading images (needed for convert_alpha)
screen = pygame.display.set_mode((size_x, size_y))
pygame.display.set_caption('TANKArena')

# ---------------- LOAD ASSETS ---------------- 
images = load.load_images()
fonts = load.load_fonts()
if sound_enabled:
    sounds = load.load_sounds()
    try:
        load.load_music()
    except Exception as e:
        print('Warning: load_music failed -', e)
        sound_enabled = False
else:
    class AltSilentSound:
        def play(self):
            return None
    sounds = {
        'fire': AltSilentSound(),
        'first_kill': AltSilentSound(),
        'another_kill': AltSilentSound(),
        'megakill': AltSilentSound(),
        'win': AltSilentSound(),
        'lose': AltSilentSound(),
    }

# Set icon after images are loaded
pygame.display.set_icon(images['icon'])

# Extract fonts (needed before level loading)
title_font = fonts['title']
kills_font = fonts['kills']
label_font = fonts['label']
message_font = fonts['message']

# Load level configuration (now that fonts are available)
load_level(1)

# Initialize level variables after loading
PL_MAX_HLTH = current_level.PL_MAX_HLTH
OP_MAX_HLTH = current_level.OP_MAX_HLTH
pl_hlth = PL_MAX_HLTH
op_hlth = OP_MAX_HLTH

pl_x = current_level.PL_START_X
pl_y = current_level.PL_START_Y
op_x = current_level.OP_START_X
op_y = current_level.OP_START_Y

bullt_speed = current_level.PL_BULLET_SPEED
bullt_speed_op = current_level.OP_BULLET_SPEED
WIN_TARGET = current_level.WIN_TARGET
DAMAGE_PER_HIT = current_level.DAMAGE_PER_HIT

# Health bar visual settings
HEALTH_BAR_WIDTH = 300
HEALTH_BAR_HEIGHT = 20
SMALL_HEALTH_BAR_WIDTH = 80
SMALL_HEALTH_BAR_HEIGHT = 8
HEALTH_BAR_OFFSET_Y = 0

# Kills
pl_kills = 0
op_kills = 0

# Player bullet
bullt_x = pl_x + 20
bullt_y = pl_y + 100
bullt_speed = current_level.PL_BULLET_SPEED
bullt_state = 'ready'

# Opponent bullet
bullt_x_op = op_x
bullt_y_op = op_y + 100
bullt_speed_op = current_level.OP_BULLET_SPEED
bullt_state_op = 'ready'

# Opponent fire timing
op_last_fire = 0
op_fire_delay = random.randint(current_level.OP_FIRE_DELAY_MIN, current_level.OP_FIRE_DELAY_MAX)

FPS_val = 60
gm_is_running = True

# Collision effect
collision_x = 0
collision_y = 0
show_collision = False
collision_time = 0
collision_type = ''

# First kill banner
first_kill_done = False
first_kill_show = False
first_kill_time = 0
FIRST_KILL_DURATION = 1500
first_kill_by_player = False
# Multi-kill banner (player)
kill_banner_show = False
kill_banner_time = 0
KILL_BANNER_DURATION = 1500
kill_banner_text = ''
game_over = False
winner = None
game_over_played = False

# Hit feedback text system
hit_feedback_list = []

# Extract images
# gm_bg is now set in load_level function
player = images['player']
oponent = images['opponent']
bullt = images['bullet_player']
bullt_op = images['bullet_opponent']
cllson_img = images['collision']
cllson_img_tnk = images['collision_tank']
first_kill_img_opt = images['first_kill_opponent']
first_kill_img_ply = images['first_kill_player']
pl_win_img = images['player_win']
pl_lost_img = images['player_lost']

# Extract sounds
fire_snd = sounds['fire']
first_kill_snd = sounds['first_kill']
another_kill_snd = sounds['another_kill']
megakill_snd = sounds['megakill']
win_snd = sounds['win']
lose_snd = sounds['lose']

# Update title text dynamically
title_text = title_font.render(current_level.LEVEL_NAME, True, 'blue')

# Start music
if sound_enabled:
    try:
        pygame.mixer.music.play(-1)
    except Exception:
        pass

clock = pygame.time.Clock()

# ---------------- LOADING SCREEN ----------------
# Show loading screen before starting the game
loading_screen.show_loading_screen(screen, size_x, size_y, images, fonts)
# Acquire username: load if saved, else prompt once and save
username = save_system.load_username()
if not username:
    username = show_username_prompt(screen, size_x, size_y, fonts)
    try:
        save_system.save_username(username)
    except Exception:
        pass
# Load progress
unlocked_level = save_system.load_progress()
# Show main menu (Play / Credits / Instructions) immediately after loading
selected_level = menu.show_menu(screen, size_x, size_y, images, fonts, unlocked_level, username)
if selected_level:
    load_level(selected_level)
    # Ensure all state is reinitialized for the chosen level
    reset_game_state()
    # Fade in to the new level
    screen.blit(gm_bg, (0, 0))
    menu.fade_screen(screen, size_x, size_y, 'in')
    # Show 3-2-1 countdown with fade animation
    show_countdown(screen, size_x, size_y, fonts, gm_bg)
    # Restart background music for the level (if mixer is available)
    try:
        pygame.mixer.music.play(-1)
    except Exception:
        pass
else:
    # If Play was clicked (no specific level selected), still show countdown for the current level
    screen.blit(gm_bg, (0, 0))
    show_countdown(screen, size_x, size_y, fonts, gm_bg)

# ---------------- GAME LOOP ---------------- 
# -------- USER PROFILE UI STATE --------
profile_button_rect = pygame.Rect(0, 0, 120, 36)
profile_panel_visible = False

# -------- PAUSE UI STATE --------
is_paused = False
pause_button_rect = pygame.Rect(0, 0, 90, 32)

while gm_is_running:
    screen.blit(gm_bg, (0, 0))
    current_time = pygame.time.get_ticks()

    # Position profile button at top-right each frame (below top HUD)
    profile_button_rect.top = 70
    profile_button_rect.right = size_x - 10
    # Position pause button near top-left (below top HUD)
    pause_button_rect.top = 70
    pause_button_rect.left = 10

    mx, my = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # type: ignore
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
           if event.key == pygame.K_ESCAPE:
            game_over = True
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:  # type: ignore
            if event.key == pygame.K_SPACE and bullt_state == 'ready' and pl_hlth > 0 and bullt_x <= size_x + 80 and not game_over:  # type: ignore
                bullt_x = pl_x + 260
                bullt_y = pl_y + 100
                bullt_state = 'fire'
                try:
                    fire_snd.play()
                except Exception:
                    pass
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if profile_button_rect.collidepoint(event.pos):
                profile_panel_visible = not profile_panel_visible
            else:
                # hide if clicking outside panel area when visible
                if profile_panel_visible:
                    # compute panel rect to test outside clicks
                    panel_w, panel_h = 260, 140
                    panel_rect = pygame.Rect(profile_button_rect.right - panel_w, profile_button_rect.bottom + 8, panel_w, panel_h)
                    if not panel_rect.collidepoint(event.pos):
                        profile_panel_visible = False
            # Pause button toggle
            if pause_button_rect.collidepoint(event.pos):
                is_paused = not is_paused

    # Short-circuit update section when paused
    if is_paused:
        pygame.display.update()
        clock.tick(FPS_val)
        continue

    # -------- PLAYER BULLET -------- 
    bullet_update = tanks.update_player_bullet(bullt_state, bullt_x, bullt_y, bullt_speed, size_x, pl_x, pl_y)
    bullt_state = bullet_update.get('bullt_state', 'ready')
    bullt_x = bullet_update.get('bullt_x', pl_x + 20)
    bullt_y = bullet_update.get('bullt_y', pl_y + 100)
    if bullet_update.get('draw', False):
        tanks.draw_bullet(screen, bullt, bullet_update.get('draw_x', bullt_x), bullet_update.get('draw_y', bullt_y))

    # -------- OPPONENT FIRE -------- 
    if bullt_state_op == 'ready' and op_hlth > 0:
        if current_time - op_last_fire >= op_fire_delay:
            bullt_x_op = op_x
            bullt_y_op = op_y + 100
            bullt_state_op = 'fire'
            try:
                fire_snd.play()
            except Exception:
                pass
            op_last_fire = current_time
            op_fire_delay = random.randint(current_level.OP_FIRE_DELAY_MIN, current_level.OP_FIRE_DELAY_MAX)

    # -------- OPPONENT BULLET -------- 
    bullet_op_update = tanks.update_opponent_bullet(bullt_state_op, bullt_x_op, bullt_y_op, bullt_speed_op, op_x, op_y)
    bullt_state_op = bullet_op_update.get('bullt_state_op', 'ready')
    bullt_x_op = bullet_op_update.get('bullt_x_op', op_x)
    bullt_y_op = bullet_op_update.get('bullt_y_op', op_y + 100)
    if bullet_op_update.get('draw', False):
        tanks.draw_bullet_op(screen, bullt_op, bullet_op_update.get('draw_x', bullt_x_op), bullet_op_update.get('draw_y', bullt_y_op))

    # -------- COLLISIONS -------- 
    # Check collisions using the draw positions
    if bullet_update.get('draw', False):
        bullet_collision_x = bullet_update.get('draw_x', bullt_x)
        bullet_collision_y = bullet_update.get('draw_y', bullt_y)
        if tanks.check_bullet_tank_collision(bullet_collision_x, bullet_collision_y, op_x, op_y, oponent.get_width(), oponent.get_height()):
            show_collision = True
            collision_type = 'tank'
            collision_x = op_x + (oponent.get_width() - cllson_img_tnk.get_width()) // 2
            collision_y = op_y + (oponent.get_height() - cllson_img_tnk.get_height()) // 2
            collision_time = current_time
            bullt_state = 'ready'
            bullt_x = pl_x + 20
            bullt_y = pl_y + 100
            # Apply per-level damage for player hitting opponent
            op_hlth -= DAMAGE_PER_HIT
            
            # Add hit feedback text
            feedback_messages = ['Excellent!', 'Great!', 'Perfect!', 'Nice Shot!', 'Amazing!']
            feedback_text = random.choice(feedback_messages)
            hit_feedback_list.append({
                'text': feedback_text,
                'x': op_x + oponent.get_width() // 2,
                'y': op_y - 20,
                'time': current_time,
                'duration': 1500,
                'velocity_y': -2  # Floating upward
            })

            if op_hlth <= 0:
                pl_kills += 1
                # First kill handling
                if pl_kills == 1:
                    first_kill_by_player = True
                    if not first_kill_done:
                        first_kill_done = True
                        first_kill_show = True
                        first_kill_time = current_time
                        try:
                            first_kill_snd.play()
                        except Exception:
                            pass
                else:
                    # Play different sound for subsequent kills
                    if pl_kills >= WIN_TARGET:  # Last kill of the level - play megakill
                        try:
                            megakill_snd.play()
                        except Exception:
                            pass
                    elif pl_kills < WIN_TARGET and pl_kills > 1:  # Regular subsequent kills
                        try:
                            another_kill_snd.play()
                        except Exception:
                            pass
                    
                    # Choose message for subsequent kills
                    if pl_kills == 2:
                        kill_banner_text = 'Excellent!'
                    elif pl_kills == 3:
                        kill_banner_text = 'Great!'
                    elif pl_kills == 4:
                        kill_banner_text = 'Super!'
                    elif pl_kills >= 5:
                        kill_banner_text = 'Unstoppable!'
                    else:
                        kill_banner_text = ''

                    if kill_banner_text:
                        kill_banner_show = True
                        kill_banner_time = current_time

                # Check if this kill reaches the win target and end game
                if pl_kills >= WIN_TARGET:
                    game_over = True
                    winner = 'player'
                    # Save progress: unlock next level
                    save_system.save_progress(current_level_num + 1)
                    # Stop all sounds and background music at end of level
                    pygame.mixer.stop()
                    pygame.mixer.music.stop()
                else:
                    # Only respawn if game is not over
                    respawn_data = tanks.respawn_opponent(OP_MAX_HLTH, current_level.OP_START_X, current_level.OP_START_Y)
                    op_hlth = respawn_data.get('op_hlth', OP_MAX_HLTH)
                    op_x = respawn_data.get('op_x', current_level.OP_START_X)
                    bullt_state_op = respawn_data.get('bullt_state_op', 'ready')
                    bullt_x_op = respawn_data.get('bullt_x_op', op_x)
                    bullt_y_op = respawn_data.get('bullt_y_op', op_y + 100)
 
    if bullet_op_update.get('draw', False):
        bullet_op_collision_x = bullet_op_update.get('draw_x', bullt_x_op)
        bullet_op_collision_y = bullet_op_update.get('draw_y', bullt_y_op)
        if tanks.check_bullet_tank_collision(bullet_op_collision_x, bullet_op_collision_y, pl_x, pl_y, player.get_width(), player.get_height()):
            show_collision = True
            collision_type = 'tank'
            collision_x = pl_x + (player.get_width() - cllson_img_tnk.get_width()) // 2
            collision_y = pl_y + (player.get_height() - cllson_img_tnk.get_height()) // 2
            collision_time = current_time
            bullt_state_op = 'ready'
            bullt_x_op = op_x
            bullt_y_op = op_y + 100
            pl_hlth -= current_level.DAMAGE_PER_HIT

            if pl_hlth <= 0:
                op_kills += 1
                first_kill_by_player = False
                if not first_kill_done:
                    first_kill_done = True
                    first_kill_show = True
                    first_kill_time = current_time
                    try:
                        first_kill_snd.play()
                    except Exception:
                        pass

                if op_kills >= WIN_TARGET:
                    game_over = True
                    winner = 'opponent'
                    # Stop all sounds and background music at end of level
                    pygame.mixer.stop()
                    pygame.mixer.music.stop()
                else:
                    # Only respawn if game is not over
                    respawn_data = tanks.respawn_player(PL_MAX_HLTH, current_level.PL_START_X, current_level.PL_START_Y)
                    pl_hlth = respawn_data.get('pl_hlth', PL_MAX_HLTH)
                    pl_x = respawn_data.get('pl_x', current_level.PL_START_X)
                    bullt_state = respawn_data.get('bullt_state', 'ready')
                    bullt_x = respawn_data.get('bullt_x', pl_x + 20)
                    bullt_y = respawn_data.get('bullt_y', pl_y + 100)

    # Bullet vs Bullet
    if bullet_update.get('draw', False) and bullet_op_update.get('draw', False):
        bullet_collision_x = bullet_update.get('draw_x', bullt_x)
        bullet_collision_y = bullet_update.get('draw_y', bullt_y)
        bullet_op_collision_x = bullet_op_update.get('draw_x', bullt_x_op)
        bullet_op_collision_y = bullet_op_update.get('draw_y', bullt_y_op)
        if tanks.check_bullet_bullet_collision(bullet_collision_x, bullet_collision_y, bullet_op_collision_x, bullet_op_collision_y):
            show_collision = True
            collision_x = (bullet_collision_x + bullet_op_collision_x) // 2
            collision_y = (bullet_collision_y + bullet_op_collision_y) // 2
            collision_type = 'bullet'
            collision_time = current_time
            bullt_state = 'ready'
            bullt_x = pl_x + 20
            bullt_y = pl_y + 100
            bullt_state_op = 'ready'
            bullt_x_op = op_x
            bullt_y_op = op_y + 100

    # (Collision rendering moved below so collisions draw on top of tanks)

    # -------- UI -------- 
    pl_kills_fnt = kills_font.render(f'YOUR KILLS: {pl_kills}', True, 'black')
    op_kills_fnt = kills_font.render(f'OPONENT KILLS: {op_kills}', True, 'black')

    tanks.draw_players(screen, player, oponent, pl_x, pl_y, op_x, op_y)
    screen.blit(title_text, (530, 10))

    # Pause button
    pb_hover = pause_button_rect.collidepoint((mx, my))
    pb_color = (230, 200, 100) if pb_hover else (200, 170, 70)
    pygame.draw.rect(screen, pb_color, pause_button_rect, border_radius=6)
    pygame.draw.rect(screen, (255, 255, 255), pause_button_rect, 2, border_radius=6)
    pb_label = kills_font.render('PAUSE' if not is_paused else 'RESUME', True, (0, 0, 0))
    pb_rect = pb_label.get_rect(center=pause_button_rect.center)
    screen.blit(pb_label, pb_rect)

    # Dim overlay and paused text if paused
    if is_paused and not game_over:
        dim = pygame.Surface((size_x, size_y))
        dim.set_alpha(120)
        dim.fill((0, 0, 0))
        screen.blit(dim, (0, 0))
        ptxt = title_font.render('Paused', True, (255, 255, 255))
        screen.blit(ptxt, ptxt.get_rect(center=(size_x // 2, size_y // 2)))

    # Collision effect (draw after tanks so the collision image appears on top)
    if show_collision:
        if collision_type == 'bullet':
            tanks.collision_show(screen, cllson_img, collision_x, collision_y)
        else:
            tanks.collision_tank_show(screen, cllson_img_tnk, collision_x, collision_y)

        if current_time - collision_time > 300:
            show_collision = False

    # Draw small health bars close to each tank
    sb_w = SMALL_HEALTH_BAR_WIDTH
    sb_h = SMALL_HEALTH_BAR_HEIGHT
    off = HEALTH_BAR_OFFSET_Y   

    # Player small bar
    pl_bar_x = pl_x + (player.get_width() - sb_w) // 2
    pl_bar_y = pl_y + off
    pygame.draw.rect(screen, (255, 0, 0), (pl_bar_x, pl_bar_y, sb_w, sb_h))
    pl_green_w = int(sb_w * max(pl_hlth, 0) / PL_MAX_HLTH)
    if pl_green_w > 0:
        pygame.draw.rect(screen, (0, 255, 0), (pl_bar_x, pl_bar_y, pl_green_w, sb_h))

    # Opponent small bar
    op_bar_x = op_x + (oponent.get_width() - sb_w) // 2
    op_bar_y = op_y + off
    pygame.draw.rect(screen, (255, 0, 0), (op_bar_x, op_bar_y, sb_w, sb_h))
    op_green_w = int(sb_w * max(op_hlth, 0) / OP_MAX_HLTH)
    if op_green_w > 0:
        pygame.draw.rect(screen, (0, 255, 0), (op_bar_x, op_bar_y, op_green_w, sb_h))

    # Health labels
    pl_label = label_font.render(f'YOUR HEALTH: {pl_hlth}', True, (0, 255, 0))
    op_label = label_font.render(f'OPONENT HEALTH: {op_hlth}', True, (255, 0, 0))
    screen.blit(pl_label, (0, 0))
    screen.blit(op_label, (size_x - op_label.get_width(), 0))

    screen.blit(pl_kills_fnt, (0, 30))
    screen.blit(op_kills_fnt, (1202, 30))

    # -------- USER PROFILE BUTTON & PANEL --------
    # Button
    btn_hover = profile_button_rect.collidepoint((mx, my))
    btn_color = (200, 200, 220) if btn_hover else (160, 160, 180)
    pygame.draw.rect(screen, btn_color, profile_button_rect, border_radius=6)
    pygame.draw.rect(screen, (255, 255, 255), profile_button_rect, width=2, border_radius=6)
    # Avatar circle
    avatar_center = (profile_button_rect.left + 18, profile_button_rect.centery)
    pygame.draw.circle(screen, (50, 120, 220), avatar_center, 10)
    # Name text
    name_surf = kills_font.render('PROFILE', True, (0, 0, 0))
    name_rect = name_surf.get_rect(midleft=(profile_button_rect.left + 36, profile_button_rect.centery))
    screen.blit(name_surf, name_rect)

    # Panel
    if profile_panel_visible:
        panel_w, panel_h = 260, 140
        panel_x = profile_button_rect.right - panel_w
        panel_y = profile_button_rect.bottom + 8
        panel_rect = pygame.Rect(panel_x, panel_y, panel_w, panel_h)
        # Background with shadow
        shadow = panel_rect.move(3, 3)
        pygame.draw.rect(screen, (0, 0, 0), shadow, border_radius=8)
        pygame.draw.rect(screen, (245, 245, 255), panel_rect, border_radius=8)
        pygame.draw.rect(screen, (100, 100, 120), panel_rect, 2, border_radius=8)
        # Content: username, current level, unlocked
        name_surf = label_font.render(f'Username: {username}', True, (20, 20, 40))
        name_rect = name_surf.get_rect(topleft=(panel_x + 12, panel_y + 12))
        screen.blit(name_surf, name_rect)

        lvl_surf = label_font.render(f'Current Level: {current_level_num}', True, (20, 20, 40))
        lvl_rect = lvl_surf.get_rect(topleft=(panel_x + 12, panel_y + 50))
        screen.blit(lvl_surf, lvl_rect)
        # Also show highest unlocked from save
        try:
            highest = save_system.load_progress()
        except Exception:
            highest = 1
        hi_surf = label_font.render(f'Unlocked Up To: {highest}', True, (20, 20, 40))
        hi_rect = hi_surf.get_rect(topleft=(panel_x + 12, panel_y + 86))
        screen.blit(hi_surf, hi_rect)

    # -------- FIRST KILL BANNER -------- 
    if first_kill_show:
        if current_time - first_kill_time < FIRST_KILL_DURATION:
            x = (size_x - first_kill_img_opt.get_width()) // 2
            if first_kill_by_player:
                screen.blit(first_kill_img_ply, (x, 15))
            else:
                screen.blit(first_kill_img_opt, (x, 15))
        else:
            first_kill_show = False
    # Multi-kill banner (player)
    if kill_banner_show:
        if current_time - kill_banner_time < KILL_BANNER_DURATION:
            kb_surf = title_font.render(kill_banner_text, True, (255, 215, 0))
            kb_rect = kb_surf.get_rect(center=(size_x // 2, 60))
            screen.blit(kb_surf, kb_rect)
        else:
            kill_banner_show = False
    
    # -------- HIT FEEDBACK TEXT --------
    # Update and render hit feedback text
    feedback_to_remove = []
    for i, feedback in enumerate(hit_feedback_list):
        elapsed = current_time - feedback['time']
        if elapsed < feedback['duration']:
            # Update position (floating upward)
            feedback['y'] += feedback['velocity_y']
            
            # Fade out effect
            alpha = max(0, 255 - (elapsed * 255 // feedback['duration']))
            
            # Create text surface with alpha
            feedback_surface = message_font.render(feedback['text'], True, (255, 215, 0))
            feedback_surface.set_alpha(alpha)
            
            # Center the text horizontally on the opponent
            text_rect = feedback_surface.get_rect(center=(feedback['x'], feedback['y']))
            screen.blit(feedback_surface, text_rect)
        else:
            feedback_to_remove.append(i)
    
    # Remove expired feedback
    for i in reversed(feedback_to_remove):
        hit_feedback_list.pop(i)
    
    # If game over, show final image and play sound once
    if game_over:
        if not game_over_played:
            pygame.mixer.music.stop()
            pygame.mixer.stop()
            if winner == 'player':
                try:
                    win_snd.play()
                except Exception:
                    pass
            else:
                try:
                    lose_snd.play()
                except Exception:
                    pass
            game_over_played = True

        if winner == 'player':
            img = pl_win_img
            # Show level complete message
            level_text = f'Level {current_level_num} Complete!'
            if current_level_num < 3:
                next_text = 'Press ENTER for next level'
            else:
                next_text = 'You completed all levels! Press ENTER to exit'
        else:
            img = pl_lost_img
            level_text = f'Level {current_level_num} Failed!'
            next_text = 'Press ENTER to retry level'

        x = (size_x - img.get_width()) // 2
        y = (size_y - img.get_height()) // 2
        screen.blit(img, (x, y))
        
        # Render level text
        level_surf = title_font.render(level_text, True, (255, 255, 255))
        level_rect = level_surf.get_rect(center=(size_x // 2, 50))
        screen.blit(level_surf, level_rect)
        
        # Render instruction text
        inst_surf = label_font.render(next_text, True, (255, 215, 0))
        inst_rect = inst_surf.get_rect(center=(size_x // 2, size_y - 50))
        screen.blit(inst_surf, inst_rect)
        
        pygame.display.update()
        clock.tick(FPS_val)
        
        # Wait for any key press or quit event after showing win/lose screen
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # ENTER key
                    if winner == 'player' and current_level_num < 3:
                        # Load next level
                        next_level = current_level_num + 1
                        load_level(next_level)
                        
                        # Reinitialize game state for new level
                        reset_game_state()
                        # Draw bg and show 3-2-1 countdown before resuming
                        screen.blit(gm_bg, (0, 0))
                        show_countdown(screen, size_x, size_y, fonts, gm_bg)
                        # Restart background music
                        try:
                            pygame.mixer.music.play(-1)
                        except Exception:
                            pass
                        continue  # Skip to next game loop iteration
                    else:
                        # Exit or retry
                        pygame.quit()
                        sys.exit()
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
    pygame.display.update()
    clock.tick(FPS_val)
    
#Programmer: Shravan Acharya
#Designer: Rahul Chetry

##Thanks!!!