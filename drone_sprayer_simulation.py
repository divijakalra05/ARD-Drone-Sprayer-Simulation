import pygame
import random
import math

pygame.init()

WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Advanced Drone Pesticide Sprayer Simulation")

clock = pygame.time.Clock()

# Drone properties
drone_x = WIDTH // 2
drone_y = 180
drone_speed = 4
spray_on = False
spray_flow = 2      # 1 = low, 2 = medium, 3 = high
propeller_angle = 0 # rotates for animation
tilt = 0            # left/right tilt

# Spray particles
particles = []

# Crop objects
crops = []
for x in range(0, WIDTH, 25):
    crops.append({"x": x, "health": 50})  # 0–100 health

# Create spray particles
def generate_spray():
    for _ in range(spray_flow * 4):
        particles.append({
            "x": drone_x + random.randint(-10, 10),
            "y": drone_y + 30,
            "speed": random.uniform(2.5, 4),
            "size": random.randint(2, 4)
        })

# Draw crops with color based on health
def draw_crops():
    for c in crops:
        green = int(80 + (c["health"] * 1.4))  # greener = healthier
        green = min(green, 255)

        # crop stem
        pygame.draw.line(screen, (30, green, 30),
                         (c["x"], HEIGHT * 0.8),
                         (c["x"] + 5, HEIGHT * 0.8 - 30), 3)

# Update spray particles + crop interaction
def update_particles():
    for p in particles[:]:
        p["y"] += p["speed"]
        p["speed"] += 0.04

        pygame.draw.circle(screen, (120, 200, 255),
                           (int(p["x"]), int(p["y"])),
                           p["size"])

        # Check collision with crops
        if p["y"] > HEIGHT * 0.8 - 30:
            for c in crops:
                if abs(p["x"] - c["x"]) < 15:
                    c["health"] = min(100, c["health"] + spray_flow * 0.7)
            particles.remove(p)

# Draw drone with propeller animation, tilt, shadow
def draw_drone():
    global propeller_angle

    # SHADOW
    shadow_y = drone_y + 80 + drone_y * 0.05
    pygame.draw.ellipse(screen, (0, 0, 0, 60), (drone_x - 40, shadow_y, 80, 15))

    # DRONE BODY WITH TILT
    tilt_offset = tilt * 4
    body_rect = pygame.Rect(drone_x - 25 - tilt_offset, drone_y - 15, 50, 30)
    pygame.draw.rect(screen, (200, 200, 200), body_rect)

    # PROPELLER BAR
    pygame.draw.line(screen, (100, 100, 100),
                     (drone_x - 35 - tilt_offset, drone_y - 25),
                     (drone_x + 35 - tilt_offset, drone_y - 25), 6)

    # ROTATING PROPELLER (just a line spinning)
    length = 40
    px = drone_x - tilt_offset
    py = drone_y - 25

    end_x = px + math.cos(propeller_angle) * length
    end_y = py + math.sin(propeller_angle) * length

    pygame.draw.line(screen, (30, 30, 30), (px, py), (end_x, end_y), 4)

    propeller_angle += 0.4  # rotation speed

    # Nozzles
    pygame.draw.circle(screen, (50, 50, 50), (drone_x - 20 - tilt_offset, drone_y + 20), 6)
    pygame.draw.circle(screen, (50, 50, 50), (drone_x + 20 - tilt_offset, drone_y + 20), 6)


running = True

while running:
    screen.fill((135, 206, 250))  # sky blue background
    dt = clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Spray toggle
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                spray_on = not spray_on

            # Spray flow control
            if event.key == pygame.K_1:
                spray_flow = 1
            if event.key == pygame.K_2:
                spray_flow = 2
            if event.key == pygame.K_3:
                spray_flow = 3

    keys = pygame.key.get_pressed()

    # Movement
    if keys[pygame.K_LEFT] and drone_x > 40:
        drone_x -= drone_speed
        tilt = -1
    elif keys[pygame.K_RIGHT] and drone_x < WIDTH - 40:
        drone_x += drone_speed
        tilt = 1
    else:
        tilt = 0

    if keys[pygame.K_UP] and drone_y > 80:
        drone_y -= drone_speed
    if keys[pygame.K_DOWN] and drone_y < HEIGHT * 0.6:
        drone_y += drone_speed

    # Spray
    if spray_on:
        generate_spray()

    update_particles()
    draw_crops()
    draw_drone()

    pygame.display.update()

pygame.quit()
