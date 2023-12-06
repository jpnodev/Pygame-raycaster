import pygame
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 320
screen_height = 240
res = 25
screen = pygame.display.set_mode((screen_width, screen_height))

bloc_size = 16

# Player position, direction, and movement speed
player_x = 4*bloc_size
player_y = 3*bloc_size
player_angle = 0  # Angle in radians
player_speed = bloc_size
player_rotation_speed = 1
fov = math.pi / 2 # Default FOV (60 degrees)


# Map representing walls (1s) and empty spaces (0s)
# Different numbers will correspond to different colors
color_palette = [(44, 33, 55), (118, 68, 98), (169, 104, 104), (237, 180, 161)]
textures = {
    0: [[0] * 16 for _ in range(16)],  # Empty space texture
    1: [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 3, 0, 3, 3, 3, 3, 3, 3, 0, 3, 3, 3],
        [0, 3, 3, 3, 2, 0, 2, 2, 2, 2, 2, 2, 0, 2, 2, 2],
        [0, 2, 2, 2, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 3, 3, 3, 3, 3, 3, 0, 3, 3, 3, 0, 3, 3, 3, 3],
        [0, 2, 2, 2, 2, 2, 2, 0, 2, 2, 2, 0, 2, 2, 2, 2],
        [0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [3, 3, 3, 3, 0, 3, 3, 3, 3, 3, 3, 0, 3, 3, 3, 0],
        [2, 2, 2, 2, 0, 2, 2, 2, 2, 2, 2, 0, 2, 2, 2, 0],
        [0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [3, 3, 0, 0, 0, 0, 0, 0, 3, 3, 0, 0, 3, 3, 3, 0],
        [2, 2, 3, 3, 3, 3, 0, 2, 2, 2, 0, 2, 2, 2, 2, 0],
        [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0]],  # Wall texture 1
        
    2: [[2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2]]  # Wall texture 2
    # Add textures for other values in the map as needed
}

map_grid = [
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 2, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 1],
    [1, 0, 0, 1, 1, 0, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 1],
    [1, 0, 0, 1, 1, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1]
]

def is_wall(x, y):
    map_x = math.floor(x / bloc_size)
    map_y = math.floor(y / bloc_size)
    return map_grid[map_y][map_x] > 0  # Detect collisions for values strictly higher than 0

def distance(x1, y1, x2, y2):
    return math.sqrt((x2-x1)**2 + (y2-y1)**2)

def cast_rays(player_x, player_y, player_angle):
    num_rays = int(screen_width*res/100)  # Set the number of rays to screen width

    # Calculate the starting and ending angles for the rays based on FOV
    start_angle = player_angle - fov / 2
    angle_increment = fov / num_rays  # Angle increment for each ray

    for i in range(num_rays):
        ray_angle = start_angle + i * angle_increment

        # Ray direction components
        ray_dx = math.cos(ray_angle)
        ray_dy = math.sin(ray_angle)

        # Initialize ray position to the player's position
        ray_x = player_x
        ray_y = player_y

        hit_wall = False
        is_side = False
        wall_distance = 0
        max_distance = 8 * bloc_size

        # DDA variables for step and initial side distance
        if ray_dx != 0:
            delta_x = math.sqrt(1 + (ray_dy / ray_dx) ** 2)
        else:
            delta_x = float('inf')  # Assign infinity if ray_dx is zero

        if ray_dy != 0:
            delta_y = math.sqrt(1 + (ray_dx / ray_dy) ** 2)
        else:
            delta_y = float('inf')  # Assign infinity if ray_dy is zero

        step_x = 0
        step_y = 0

        if ray_dx < 0:
            step_x = -1
            side_x = (player_x - ray_x) * delta_x
        else:
            step_x = 1
            side_x = (ray_x + 1 - player_x) * delta_x

        if ray_dy < 0:
            step_y = -1
            side_y = (player_y - ray_y) * delta_y
        else:
            step_y = 1
            side_y = (ray_y + 1 - player_y) * delta_y

        # DDA algorithm
        while not hit_wall and wall_distance < max_distance:
            if side_x < side_y:
                side_x += delta_x
                ray_x += step_x
                is_side = False
            else:
                side_y += delta_y
                ray_y += step_y
                is_side = True

            # Check for collision
            if is_wall(ray_x, ray_y):
                hit_wall = True
                if not is_side:
                    wall_distance = (ray_x - player_x + (1 - step_x) / 2) / ray_dx
                else:
                    wall_distance = (ray_y - player_y + (1 - step_y) / 2) / ray_dy

        if hit_wall:
            # Calculate height of wall slice on the screen
            if wall_distance == 0:
                wall_distance = 1
            wall_slice_height = int(screen_height * (screen_height // bloc_size) / wall_distance)
            map_x = int(ray_x//bloc_size)
            map_y = int(ray_y//bloc_size)

            map_value = map_grid[map_y][map_x]
            brightness = 1 - (wall_distance / max_distance)  # Faster shading based on distance

            if (is_side):
                texture_u = int((ray_x % bloc_size) / bloc_size*16)
            else:
                texture_u = int((ray_y % bloc_size) / bloc_size*16)

            # Render the texture column on the wall slice
            for texture_v in range(16):
                # Calculate the texture pixel to render
                #texture_y = int((y / wall_slice_height) * 16)  # Assuming textures are 16 pixels high
                color = color_palette[textures[map_value][texture_v][texture_u]]  # Adjust brightness if needed
                screen_color = tuple(max(int(c * brightness), 0) for c in color)

                # Calculate the position on the screen to render
                wall_slice_pixel = wall_slice_height/16
                screen_y = screen_height/2 - wall_slice_height/2 + texture_v*wall_slice_pixel
                uvRect = pygame.Rect(i*screen_width/num_rays, screen_y, screen_width/num_rays+1, wall_slice_pixel+1)
                pygame.draw.rect(screen, screen_color, uvRect)
                #*
                # pygame.draw.line(screen, screen_color, (i*screen_width/num_rays, screen_y), ((i+0)*screen_width/num_rays, screen_y+wall_slice_pixel))


# Variables to handle time
clock = pygame.time.Clock()
last_time = pygame.time.get_ticks()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    new_x = player_x
    new_y = player_y

    # Get the current time
    current_time = pygame.time.get_ticks()

    # Calculate the elapsed time since the last frame
    delta_time = (current_time - last_time) / 1000.0  # Convert to seconds

    # Update last_time for the next frame
    last_time = current_time

    # Adjust the player's movement speed based on the elapsed time
    movement_speed = player_speed * delta_time
    rotation_speed = player_rotation_speed * delta_time

    if keys[pygame.K_UP]:
        new_x += movement_speed * math.cos(player_angle)
        new_y += movement_speed * math.sin(player_angle)
    if keys[pygame.K_DOWN]:
        new_x -= movement_speed * math.cos(player_angle)
        new_y -= movement_speed * math.sin(player_angle)
    if keys[pygame.K_LEFT]:
        player_angle -= rotation_speed
    if keys[pygame.K_RIGHT]:
        player_angle += rotation_speed

    if not is_wall(new_x, new_y):
        player_x = new_x
        player_y = new_y

    pygame.draw.rect(screen, color_palette[3], pygame.Rect(0, 0, screen_width, screen_height//2))
    pygame.draw.rect(screen, color_palette[0], pygame.Rect(0, screen_height//2, screen_width, screen_height))
    cast_rays(player_x, player_y, player_angle)
    pygame.display.flip()

pygame.quit()