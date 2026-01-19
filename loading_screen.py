import pygame  # type: ignore
import sys
import random
import math
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE  # type: ignore
##########################
# List of 20 unique loading text messages
LOADING_MESSAGES = [
    "Loading assets...",
    "Please wait...",
    "Patience has good results...",
    "Preparing battlefield...",
    "Loading tanks...",
    "Almost there...",
    "Initializing combat systems...",
    "Loading weapons...",
    "Setting up arena...",
    "Preparing for battle...",
    "Loading game data...",
    "Optimizing performance...",
    "Loading textures...",
    "Preparing graphics...",
    "Loading sounds...",
    "Initializing engine...",
    "Setting up controls...",
    "Loading resources...",
    "Preparing mission...",
    "Finalizing setup..."
]

def show_loading_screen(screen, size_x, size_y, images, fonts):
    """Display loading screen with progress"""
    clock = pygame.time.Clock()
    
    # Create loading screen background (use game background or solid color)
    loading_bg = pygame.Surface((size_x, size_y))
    loading_bg.fill((20, 20, 40))  # Dark blue background
    
    # Loading text
    title_font = fonts.get('title', pygame.font.Font(None, 72))
    loading_text = title_font.render('TANK ARENA', True, (255, 255, 255))
    loading_text_rect = loading_text.get_rect(center=(size_x // 2, size_y // 2 - 50))
    
    # Loading message font
    message_font = fonts.get('label', pygame.font.Font(None, 32))
    
    # Randomly select 3 different loading messages
    selected_messages = random.sample(LOADING_MESSAGES, 3)
    current_message_index = 0
    current_message = selected_messages[0]
    ##########################
    # Message timing: 2s, 2s, 3s (total 7 seconds)
    message_timings = [2000, 2000, 3000]  # milliseconds
    message_start_time = 0

    # Icon image (if provided in images dict). We'll animate this during the whole loading period.
    icon_img = None
    if isinstance(images, dict):
        icon_img = images.get('icon')
    
    # Progress bar
    progress_bar_width = 400
    progress_bar_height = 30
    progress_bar_x = (size_x - progress_bar_width) // 2
    progress_bar_y = size_y // 2 + 100
    
    # Animation variables
    loading_dots = 0
    dot_timer = 0
    progress = 0
    max_progress = 100
    
    running = True
    start_time = pygame.time.get_ticks()
    min_display_time = 7000  # Show loading screen for at least 7 seconds (to match text timing)
    extra_delay = 2000  # additional 2-second delay after existing delay
    ##########################
    while running:
        current_time = pygame.time.get_ticks()
        elapsed = current_time - start_time
        
        # Update random loading message based on elapsed time
        # Text 1: 0-2000ms (2 seconds)
        # Text 2: 2000-4000ms (2 seconds)
        # Text 3: 4000-7000ms (3 seconds)
        if elapsed < message_timings[0]:
            # First message (0-2 seconds)
            if current_message_index != 0:
                current_message_index = 0
                current_message = selected_messages[0]
                message_start_time = current_time
        elif elapsed < message_timings[0] + message_timings[1]:
            # Second message (2-4 seconds)
            if current_message_index != 1:
                current_message_index = 1
                current_message = selected_messages[1]
                message_start_time = current_time - message_timings[0]
        else:
            # Third message (4-7 seconds)
            if current_message_index != 2:
                current_message_index = 2
                current_message = selected_messages[2]
                message_start_time = current_time - (message_timings[0] + message_timings[1])
        
        # Update progress (simulate loading)
        if elapsed < min_display_time:
            progress = int((elapsed / min_display_time) * 90)  # Go to 90% during min time
        else:
            progress = min(90 + int((elapsed - min_display_time) / 500), 100)  # Complete loading
        ##########################
        # Animate loading dots
        dot_timer += 1
        if dot_timer >= 30:
            loading_dots = (loading_dots + 1) % 4
            dot_timer = 0
        
        # Draw background
        screen.blit(loading_bg, (0, 0))
        
        # Draw title
        screen.blit(loading_text, loading_text_rect)
        
        # Draw current random loading message with animated dots
        dots_text = '.' * loading_dots
        display_message = f'{current_message} {dots_text}'
        loading_message = message_font.render(display_message, True, (200, 200, 200))
        loading_message_rect = loading_message.get_rect(center=(size_x // 2, size_y // 2 + 50))
        screen.blit(loading_message, loading_message_rect)
        
        # Draw progress bar background
        pygame.draw.rect(screen, (50, 50, 50), 
                        (progress_bar_x, progress_bar_y, progress_bar_width, progress_bar_height))
        
        # Draw progress bar fill
        fill_width = int((progress / max_progress) * progress_bar_width)
        if fill_width > 0:
            # Gradient effect
            for i in range(fill_width):
                color_ratio = i / progress_bar_width
                r = int(50 + (200 * color_ratio))
                g = int(150 + (105 * color_ratio))
                b = int(255 - (155 * color_ratio))
                pygame.draw.rect(screen, (r, g, b), ##########################
                               (progress_bar_x + i, progress_bar_y, 1, progress_bar_height))
        
        # Draw progress bar border
        pygame.draw.rect(screen, (255, 255, 255), 
                        (progress_bar_x, progress_bar_y, progress_bar_width, progress_bar_height), 2)
        
        # Draw progress percentage
        percent_text = message_font.render(f'{progress}%', True, (255, 255, 255))
        percent_rect = percent_text.get_rect(center=(size_x // 2, progress_bar_y + progress_bar_height + 30))
        screen.blit(percent_text, percent_rect)

        # Draw center icon with a subtle pulse animation (runs during entire loading + extra delay)
        if icon_img:
            # Use total elapsed time so animation continues during the extra wait
            t = elapsed
            # Pulse parameters
            period = 1500.0  # milliseconds per full pulse
            amp = 0.06  # scale amplitude (6%)
            scale = 1.0 + amp * math.sin(2 * math.pi * (t % period) / period)

            base_w = icon_img.get_width()
            base_h = icon_img.get_height()
            new_w = max(1, int(base_w * scale))
            new_h = max(1, int(base_h * scale))
            try:
                scaled = pygame.transform.smoothscale(icon_img, (new_w, new_h))
            except Exception:
                scaled = pygame.transform.scale(icon_img, (new_w, new_h))

            icon_rect = scaled.get_rect(center=(size_x // 2, size_y // 2))
            screen.blit(scaled, icon_rect)
        
        # Check for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # type: ignore
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:  # type: ignore
                if event.key == pygame.K_ESCAPE:  # type: ignore
                    pygame.quit()
                    sys.exit()
        
        # Complete loading when progress reaches 100% and minimum time + extra delay has passed
        # This preserves the original minimum display time and adds the required 2s wait.
        if progress >= 100 and elapsed >= (min_display_time + extra_delay):
            # Fade out effect
            fade_surface = pygame.Surface((size_x, size_y))
            fade_alpha = 0
            fade_speed = 5

            while fade_alpha < 255:
                fade_surface.set_alpha(fade_alpha)
                fade_surface.fill((0, 0, 0))
                screen.blit(fade_surface, (0, 0))
                pygame.display.update()
                fade_alpha += fade_speed
                clock.tick(60)

            running = False
        ##########################
        pygame.display.update()
        clock.tick(60)
    
    return True

def quick_loading_screen(screen, size_x, size_y, fonts):
    """Quick loading screen without animation"""
    loading_bg = pygame.Surface((size_x, size_y))
    loading_bg.fill((20, 20, 40))
    
    title_font = fonts.get('title', pygame.font.Font(None, 72))
    loading_text = title_font.render('TANK ARENA', True, (255, 255, 255))
    loading_text_rect = loading_text.get_rect(center=(size_x // 2, size_y // 2))
    
    screen.blit(loading_bg, (0, 0))
    screen.blit(loading_text, loading_text_rect)
    pygame.display.update()
    pygame.time.wait(1000)  # Show for 1 second
    return True