import pygame  # type: ignore
import sys
import math
from pygame.locals import QUIT, MOUSEBUTTONDOWN, KEYDOWN, K_ESCAPE  # type: ignore
import save_system
##########################

def draw_button(screen, rect, text_surf, hover=False):
    color = (180, 180, 180) if hover else (140, 140, 140)
    pygame.draw.rect(screen, color, rect)
    pygame.draw.rect(screen, (255, 255, 255), rect, 2)
    text_rect = text_surf.get_rect(center=rect.center)
    screen.blit(text_surf, text_rect)
####################################################

def fade_screen(screen, size_x, size_y, direction='out', duration=500):
    """Fade the screen in or out over a duration in milliseconds"""
    clock = pygame.time.Clock()
    fade_surface = pygame.Surface((size_x, size_y))
    fade_surface.fill((0, 0, 0))

    start_time = pygame.time.get_ticks()
    while True:
        elapsed = pygame.time.get_ticks() - start_time
        if elapsed >= duration:
            break

        if direction == 'out':
            alpha = int((elapsed / duration) * 255)
        else:  # 'in'
            alpha = int((1 - elapsed / duration) * 255)

        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface, (0, 0))
        pygame.display.update()
        clock.tick(60)


def show_text_screen(screen, size_x, size_y, fonts, title, lines):
    clock = pygame.time.Clock()
    title_font = fonts.get('title', pygame.font.Font(None, 72))
    label_font = fonts.get('label', pygame.font.Font(None, 28))
    small_font = pygame.font.Font('fnts/msgfnt.ttf', 22)

    # Scrolling variables
    scroll_offset = 0
    scroll_speed = 20
    max_scroll = 0

    # Calculate total height needed for all text
    total_height = 100  # Start after title
    for line in lines:
        if line.startswith('   '):  # Indented lines (sub-items)
            total_height += 28
        elif line.endswith(':') or line == '':  # Section headers or empty lines
            if line:
                total_height += 40
            else:
                total_height += 20  # Extra space for empty lines
        else:  # Regular lines
            total_height += 32
    
    # Calculate maximum scroll offset
    max_scroll = max(0, total_height - (size_y - 100))  # Leave space for title and back hint
##########################
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # type: ignore
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:  # type: ignore
                if event.key == K_ESCAPE:  # type: ignore
                    return
                # Keyboard scrolling
                if event.key == pygame.K_UP:
                    scroll_offset = max(0, scroll_offset - scroll_speed)
                elif event.key == pygame.K_DOWN:
                    scroll_offset = min(max_scroll, scroll_offset + scroll_speed)
                elif event.key == pygame.K_HOME:
                    scroll_offset = 0
                elif event.key == pygame.K_END:
                    scroll_offset = max_scroll
            elif event.type == pygame.MOUSEWHEEL:  # Mouse wheel scrolling
                if event.y > 0:  # Scroll up
                    scroll_offset = max(0, scroll_offset - scroll_speed)
                else:  # Scroll down
                    scroll_offset = min(max_scroll, scroll_offset + scroll_speed)
##########################
        screen.fill((20, 20, 40))
        title_surf = title_font.render(title, True, (255, 255, 255))
        screen.blit(title_surf, title_surf.get_rect(center=(size_x // 2, 50)))

        # Create a clipping surface for the scrollable area
        clip_rect = pygame.Rect(0, 100, size_x, size_y - 130)  # Leave space for title and back hint
        screen.set_clip(clip_rect)

        y = 100 - scroll_offset  # Start with scroll offset
        for line in lines:
            if line.startswith('   '):  # Indented lines (sub-items)
                surf = small_font.render(line.strip(), True, (180, 180, 180))
                screen.blit(surf, surf.get_rect(center=(size_x // 2, y)))
                y += 28
            elif line.endswith(':') or line == '':  # Section headers or empty lines
                if line:
                    surf = label_font.render(line, True, (255, 215, 0))  # Gold color for headers
                    screen.blit(surf, surf.get_rect(center=(size_x // 2, y)))
                    y += 40
                else:
                    y += 20  # Extra space for empty lines
            else:  # Regular lines
                surf = label_font.render(line, True, (220, 220, 220))
                screen.blit(surf, surf.get_rect(center=(size_x // 2, y)))
                y += 32

        # Reset clipping
        screen.set_clip(None)

        # Back hint
        back_surf = small_font.render('Press ESC to go back | Use ↑↓ or Mouse Wheel to scroll', True, (150, 150, 150))
        screen.blit(back_surf, (20, size_y - 30))

        # Show scroll indicator if content is scrollable
        if max_scroll > 0:
            # Draw scroll bar
            bar_width = 10
            bar_height = 60
            bar_x = size_x - bar_width - 20
            bar_y = 100 + (scroll_offset / max_scroll) * ((size_y - 200) - bar_height)
            
            pygame.draw.rect(screen, (80, 80, 80), (bar_x, 100, bar_width, size_y - 200))
            pygame.draw.rect(screen, (200, 200, 200), (bar_x, bar_y, bar_width, bar_height))

        pygame.display.update()
        clock.tick(60)


def show_level_selection(screen, size_x, size_y, fonts, unlocked_level):
    """Display level selection screen with buttons"""
    clock = pygame.time.Clock()

    title_font = fonts.get('title', pygame.font.Font(None, 72))
    label_font = fonts.get('label', pygame.font.Font(None, 28))

    level1_surf = label_font.render('Level 1 - Easy', True, (0, 0, 0))
    level2_surf = label_font.render('Level 2 - Medium', True, (0, 0, 0))
    level3_surf = label_font.render('Level 3 - Hard', True, (0, 0, 0))
    back_surf = label_font.render('Back', True, (0, 0, 0))

    # Button rects
    btn_w = 240
    btn_h = 56
    spacing = 24
    total_h = btn_h * 4 + spacing * 3
    start_y = (size_y - total_h) // 2 + 80

    level1_rect = pygame.Rect((size_x // 2 - btn_w // 2, start_y, btn_w, btn_h))
    level2_rect = pygame.Rect((size_x // 2 - btn_w // 2, start_y + btn_h + spacing, btn_w, btn_h))
    level3_rect = pygame.Rect((size_x // 2 - btn_w // 2, start_y + (btn_h + spacing) * 2, btn_w, btn_h))
    back_rect = pygame.Rect((size_x // 2 - btn_w // 2, start_y + (btn_h + spacing) * 3, btn_w, btn_h))

    # Warning message variables
    warning_text = None
    warning_start_time = 0
    warning_duration = 2000  # 2 seconds

    running = True
    while running:
        current_time = pygame.time.get_ticks()
        mx, my = pygame.mouse.get_pos()
        clicked = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # type: ignore
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:  # type: ignore
                clicked = True
                click_pos = event.pos
            if event.type == KEYDOWN:  # type: ignore
                if event.key == K_ESCAPE:  # type: ignore
                    return

        screen.fill((20, 20, 40))

        # Draw title
        title_surf = title_font.render('Select Level', True, (255, 255, 255))
        screen.blit(title_surf, title_surf.get_rect(center=(size_x // 2, 80)))

        # Draw buttons with hover
        draw_button(screen, level1_rect, level1_surf, hover=level1_rect.collidepoint((mx, my)))
        draw_button(screen, level2_rect, level2_surf, hover=level2_rect.collidepoint((mx, my)))
        draw_button(screen, level3_rect, level3_surf, hover=level3_rect.collidepoint((mx, my)))
        draw_button(screen, back_rect, back_surf, hover=back_rect.collidepoint((mx, my)))

        # Draw warning message if active
        if warning_text and current_time - warning_start_time < warning_duration:
            # Blinking effect using sine wave
            blink_factor = (math.sin((current_time - warning_start_time) * 0.01) + 1) / 2  # 0 to 1
            red = int(255 * blink_factor)
            white = int(255 * (1 - blink_factor))
            color = (red, white, white)
            warning_surf = title_font.render(warning_text, True, color)
            warning_rect = warning_surf.get_rect(center=(size_x // 2, size_y // 2))
            screen.blit(warning_surf, warning_rect)
        elif warning_text and current_time - warning_start_time >= warning_duration:
            warning_text = None  # Clear warning after duration

        pygame.display.update()
        clock.tick(60)

        if clicked:
            if level1_rect.collidepoint(click_pos):
                fade_screen(screen, size_x, size_y, 'out')
                return 1
            if level2_rect.collidepoint(click_pos):
                if 2 <= unlocked_level:
                    fade_screen(screen, size_x, size_y, 'out')
                    return 2
                else:
                    warning_text = "⚠ Complete Level 1 First!"
                    warning_start_time = current_time
            if level3_rect.collidepoint(click_pos):
                if 3 <= unlocked_level:
                    fade_screen(screen, size_x, size_y, 'out')
                    return 3
                else:
                    warning_text = "⚠ Complete Level 2 First!"
                    warning_start_time = current_time
            if back_rect.collidepoint(click_pos):
                return


def show_menu(screen, size_x, size_y, images, fonts, unlocked_level=1, username=None):
    """Display main menu with Play, Credits, Instructions, and user profile at top-right"""
    clock = pygame.time.Clock()

    title_font = fonts.get('title', pygame.font.Font(None, 72))
    label_font = fonts.get('label', pygame.font.Font(None, 28))

    play_surf = label_font.render('Play', True, (0, 0, 0))
    credits_surf = label_font.render('Credits', True, (0, 0, 0))
    instr_surf = label_font.render('Instructions', True, (0, 0, 0))
    levels_surf = label_font.render('Levels', True, (0, 0, 0))

    # Button rects
    btn_w = 240
    btn_h = 56
    spacing = 24
    total_h = btn_h * 4 + spacing * 3
    start_y = (size_y - total_h) // 2 + 80

    play_rect = pygame.Rect((size_x // 2 - btn_w // 2, start_y, btn_w, btn_h))
    credits_rect = pygame.Rect((size_x // 2 - btn_w // 2, start_y + btn_h + spacing, btn_w, btn_h))
    instr_rect = pygame.Rect((size_x // 2 - btn_w // 2, start_y + (btn_h + spacing) * 2, btn_w, btn_h))
    levels_rect = pygame.Rect((size_x // 2 - btn_w // 2, start_y + (btn_h + spacing) * 3, btn_w, btn_h))

    # Optional center icon
    icon = None
    if isinstance(images, dict):
        icon = images.get('icon')

    # Profile button in menu
    profile_button_rect = pygame.Rect(0, 0, 220, 44)

    running = True
    profile_panel_visible = False
    while running:
        mx, my = pygame.mouse.get_pos()
        clicked = False

        # Place profile button top-right
        profile_button_rect.top = 10
        profile_button_rect.right = size_x - 10

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # type: ignore
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:  # type: ignore
                clicked = True
                if profile_button_rect.collidepoint(event.pos):
                    profile_panel_visible = not profile_panel_visible
                else:
                    if profile_panel_visible:
                        pw, ph = 260, 140
                        panel_rect = pygame.Rect(profile_button_rect.right - pw, profile_button_rect.bottom + 8, pw, ph)
                        if not panel_rect.collidepoint(event.pos):
                            profile_panel_visible = False
            if event.type == KEYDOWN:  # type: ignore
                if event.key == K_ESCAPE:  # type: ignore
                    pygame.quit()
                    sys.exit()

        screen.fill((20, 20, 40))

        # Draw title
        title_surf = title_font.render('TANK ARENA', True, (255, 255, 255))
        screen.blit(title_surf, title_surf.get_rect(center=(size_x // 2, 80)))

        # Draw optional icon above buttons
        if icon:
            icon_rect = icon.get_rect(center=(size_x // 2, 130))
            screen.blit(icon, icon_rect)

        # Draw buttons with hover
        draw_button(screen, play_rect, play_surf, hover=play_rect.collidepoint((mx, my)))
        draw_button(screen, credits_rect, credits_surf, hover=credits_rect.collidepoint((mx, my)))
        draw_button(screen, instr_rect, instr_surf, hover=instr_rect.collidepoint((mx, my)))
        draw_button(screen, levels_rect, levels_surf, hover=levels_rect.collidepoint((mx, my)))

        # Draw profile button
        btn_hover = profile_button_rect.collidepoint((mx, my))
        btn_color = (200, 200, 220) if btn_hover else (160, 160, 180)
        pygame.draw.rect(screen, btn_color, profile_button_rect, border_radius=8)
        pygame.draw.rect(screen, (255, 255, 255), profile_button_rect, 2, border_radius=8)
        # Avatar circle
        avatar_center = (profile_button_rect.left + 20, profile_button_rect.centery)
        pygame.draw.circle(screen, (50, 120, 220), avatar_center, 12)
        # Username
        uname = username or 'Player'
        name_surf = label_font.render(uname, True, (0, 0, 0))
        name_rect = name_surf.get_rect(midleft=(profile_button_rect.left + 40, profile_button_rect.centery))
        screen.blit(name_surf, name_rect)

        # Panel
        if profile_panel_visible:
            pw, ph = 260, 140
            px = profile_button_rect.right - pw
            py = profile_button_rect.bottom + 8
            panel_rect = pygame.Rect(px, py, pw, ph)
            shadow = panel_rect.move(3, 3)
            pygame.draw.rect(screen, (0, 0, 0), shadow, border_radius=8)
            pygame.draw.rect(screen, (245, 245, 255), panel_rect, border_radius=8)
            pygame.draw.rect(screen, (100, 100, 120), panel_rect, 2, border_radius=8)

            # contents: username and unlocked level
            u_surf = label_font.render(f'Username: {uname}', True, (20, 20, 40))
            u_rect = u_surf.get_rect(topleft=(px + 12, py + 12))
            screen.blit(u_surf, u_rect)

            hi = save_system.load_progress()
            h_surf = label_font.render(f'Unlocked Up To: {hi}', True, (20, 20, 40))
            h_rect = h_surf.get_rect(topleft=(px + 12, py + 50))
            screen.blit(h_surf, h_rect)

        pygame.display.update()
        clock.tick(60)

        if clicked:
            if play_rect.collidepoint((mx, my)):
                return  # Start game (return to caller which will proceed to main loop)
            if credits_rect.collidepoint((mx, my)):
                # Show credits screen
                lines = [
                    '\n'
                    'DEVELOPMENT TEAM:',
                    'Programmer: Shravan Acharya',
                    'Designer & Team Partner: Rahul Chetry',
                    '',
                    'ASSETS & CREDITS:',
                    '',
                    'Font:',
                    '   Chrusty by Cove 703',
                    '',
                    'Icons & Images:',
                    '   Bullet Image – Missile icons by Those Icons (Flaticon)',
                    '   Collision Effects – Explosion icons by Freepik (Flaticon)',
                    '   Player Win Image – Instagram: @spartafc_reddingca',
                    '   Player Lose Image – Adobe Stock',
                    '   Level 2 Tank – Thelonitemonk (Pinterest)',
                    '   Level 3 Tank – pattonkesselring (Pinterest)',
                    '   Other Images – Created using AI',
                    '',
                    'Voice & Audio:',
                    '   Voice Generation – luvvoice.com, voicemode.com',
                    '   Background Music – Epic Chase Music by MaxKoMusic (chosic.com)',
                    '   Additional Audio – mixit.com, uppbeat.com',
                    '   Sound Effects – myinstants.com',
                    '',
                    'Backgrounds:',
                    'desert bg by top graphics and svg bundles pinterest',
                    'icy place bg by WallpapersHome pinterest',
                    'adobestock for level 1 bg',
                    'Thank you for playing TANK Arena!'
                ]
                show_text_screen(screen, size_x, size_y, fonts, 'Credits', lines)
            if instr_rect.collidepoint((mx, my)):
                # Show instructions screen
                lines = [
                    '\nInstructions:',
                    '- Move and aim your tank',
                    '- Press SPACE to fire',
                    '- Destroy opponent tanks to score',
                    '',
                    'Good luck!'
                ]
                show_text_screen(screen, size_x, size_y, fonts, 'Instructions', lines)
            if levels_rect.collidepoint((mx, my)):
                # Show levels screen with buttons
                selected_level = show_level_selection(screen, size_x, size_y, fonts, unlocked_level)
                if selected_level:
                    return selected_level
