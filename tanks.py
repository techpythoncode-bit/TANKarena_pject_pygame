import math
import pygame

def is_collision(x1, y1, x2, y2, radius=45):
    """Check if two points are within collision radius"""
    return math.hypot(x2 - x1, y2 - y1) < radius

def draw_players(screen, player_img, opponent_img, pl_x, pl_y, op_x, op_y):
    """Draw player and opponent tanks"""
    screen.blit(player_img, (pl_x, pl_y))
    screen.blit(opponent_img, (op_x, op_y))

def draw_bullet(screen, bullet_img, x, y):
    """Draw player bullet"""
    screen.blit(bullet_img, (x, y))

def draw_bullet_op(screen, bullet_img, x, y):
    """Draw opponent bullet"""
    screen.blit(bullet_img, (x, y))

def collision_show(screen, collision_img, x, y):
    """Show collision effect for bullet collisions"""
    screen.blit(collision_img, (x - 32, y - 32))

def collision_tank_show(screen, collision_img, x, y):
    """Show collision effect for tank collisions"""
    screen.blit(collision_img, (x, y))

def respawn_player(pl_max_health, pl_x_start, pl_y_start):
    """Reset player to starting position"""
    return {
        'pl_hlth': pl_max_health,
        'pl_x': pl_x_start,
        'bullt_state': 'ready',
        'bullt_x': pl_x_start + 20,
        'bullt_y': pl_y_start + 100
    }

def respawn_opponent(op_max_health, op_x, op_y):
    """Reset opponent to starting position"""
    return {
        'op_hlth': op_max_health,
        'op_x': op_x,
        'bullt_state_op': 'ready',
        'bullt_x_op': op_x,
        'bullt_y_op': op_y + 100
    }

def update_player_bullet(bullt_state, bullt_x, bullt_y, bullt_speed, size_x, pl_x, pl_y):
    """Update player bullet position and state"""
    if bullt_state == 'fire':
        # Check if bullet is off screen
        if bullt_x >= size_x:
            return {
                'bullt_state': 'ready',
                'bullt_x': pl_x + 20,
                'bullt_y': pl_y + 100,
                'draw_x': bullt_x,
                'draw_y': bullt_y,
                'draw': False
            }
        # Draw at current position, then update for next frame
        draw_x = bullt_x
        draw_y = bullt_y
        new_x = bullt_x + bullt_speed
        
        if new_x >= size_x:
            return {
                'bullt_state': 'ready',
                'bullt_x': pl_x + 20,
                'bullt_y': pl_y + 100,
                'draw_x': draw_x,
                'draw_y': draw_y,
                'draw': True
            }
        return {
            'bullt_state': 'fire',
            'bullt_x': new_x,
            'bullt_y': bullt_y,
            'draw_x': draw_x,
            'draw_y': draw_y,
            'draw': True
        }
    return {
        'bullt_state': bullt_state,
        'bullt_x': bullt_x,
        'bullt_y': bullt_y,
        'draw_x': bullt_x,
        'draw_y': bullt_y,
        'draw': False
    }

def update_opponent_bullet(bullt_state_op, bullt_x_op, bullt_y_op, bullt_speed_op, op_x, op_y):
    """Update opponent bullet position and state"""
    if bullt_state_op == 'fire':
        # Check if bullet is off screen
        if bullt_x_op <= 0:
            return {
                'bullt_state_op': 'ready',
                'bullt_x_op': op_x,
                'bullt_y_op': op_y + 100,
                'draw_x': bullt_x_op,
                'draw_y': bullt_y_op,
                'draw': False
            }
        # Draw at current position, then update for next frame
        draw_x = bullt_x_op
        draw_y = bullt_y_op
        new_x = bullt_x_op - bullt_speed_op
        
        if new_x <= 0:
            return {
                'bullt_state_op': 'ready',
                'bullt_x_op': op_x,
                'bullt_y_op': op_y + 100,
                'draw_x': draw_x,
                'draw_y': draw_y,
                'draw': True
            }
        return {
            'bullt_state_op': 'fire',
            'bullt_x_op': new_x,
            'bullt_y_op': bullt_y_op,
            'draw_x': draw_x,
            'draw_y': draw_y,
            'draw': True
        }
    return {
        'bullt_state_op': bullt_state_op,
        'bullt_x_op': bullt_x_op,
        'bullt_y_op': bullt_y_op,
        'draw_x': bullt_x_op,
        'draw_y': bullt_y_op,
        'draw': False
    }

def check_bullet_tank_collision(bullt_x, bullt_y, tank_x, tank_y, tank_width, tank_height):
    """Check if bullet collides with tank"""
    tank_center_x = tank_x + tank_width // 2
    tank_center_y = tank_y + tank_height // 2
    return is_collision(bullt_x, bullt_y, tank_center_x, tank_center_y)

def check_bullet_bullet_collision(bullt_x, bullt_y, bullt_x_op, bullt_y_op, radius=25):
    """Check if two bullets collide"""
    return is_collision(bullt_x, bullt_y, bullt_x_op, bullt_y_op, radius)