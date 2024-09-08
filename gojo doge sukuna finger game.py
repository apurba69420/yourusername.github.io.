import pygame
import random
import sys
import time
import asyncio  # Import asyncio

# Initialize Pygame
pygame.init()

# Get screen dimensions from the display
info = pygame.display.Info()
SCREEN_WIDTH, SCREEN_HEIGHT = info.current_w, info.current_h

# Setup the screen for fullscreen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Gojo's Dodge")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Load images
try:
    background = pygame.image.load('pexels-minan1398-813269.jpg')  # Load your night background image
    gojo_image = pygame.image.load('d19bbd51-5224-468c-8690-0de0986df06d.png')  # Load Gojo image
    finger_image = pygame.image.load('kjR1r_H__400x400.png')  # Load Sukuna finger image
except pygame.error as e:
    print(f"Unable to load images: {e}")
    sys.exit()

# Resize images to fit fullscreen
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Dimensions in pixels (approximations based on the given heights)
gojo_height = 150  # Height of Gojo in pixels (6 feet 7 cm)
finger_height = 50  # Height of Sukuna's finger in pixels (6 feet)

# Resize images
gojo_image = pygame.transform.scale(gojo_image, (80, gojo_height))  # Resize Gojo image
finger_image = pygame.transform.scale(finger_image, (40, finger_height))  # Resize Sukuna finger image

# Character setup
gojo = {
    "x": SCREEN_WIDTH // 2,
    "y": SCREEN_HEIGHT - gojo_height,
    "speed": 10
}

# Falling fingers setup
fingers = [{"x": random.randint(0, SCREEN_WIDTH - 40), "y": -40, "speed": random.randint(25, 25)}for _ in range(15)]

# Game variables
clock = pygame.time.Clock()
running = True
rounds = 0
start_time = time.time()  # Record start time

def draw():
    """Draw all elements on the screen."""
    screen.blit(background, (0, 0))  # Draw the background
    screen.blit(gojo_image, (gojo["x"], gojo["y"]))  # Draw Gojo character
    for finger in fingers:
        screen.blit(finger_image, (finger["x"], finger["y"]))  # Draw each falling Sukuna finger
    pygame.display.flip()

def update_fingers():
    """Update the position of falling Sukuna fingers."""
    global rounds, running
    for finger in fingers:
        finger["y"] += finger["speed"]
        if finger["y"] > SCREEN_HEIGHT:
            finger["x"] = random.randint(0, SCREEN_WIDTH - 40)
            finger["y"] = -40
            rounds += 1
            print(f"Finger reset. Rounds: {rounds}")  # Debugging print
        # Check collision
        if gojo["x"] < finger["x"] < gojo["x"] + 80 and gojo["y"] < finger["y"] + finger_height < gojo["y"] + gojo_height:
            print("Hit! Game Over.")  # Debugging print
            running = False

def handle_movement():
    """Handle Gojo's left and right movement."""
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        gojo["x"] -= gojo["speed"]
    if keys[pygame.K_RIGHT]:
        gojo["x"] += gojo["speed"]

    # Boundary checking
    gojo["x"] = max(0, min(gojo["x"], SCREEN_WIDTH - 80))

def final_battle():
    """Final battle against Sukuna with 'Purple' attacks."""
    print("Final round against Sukuna! Dodge the Purple attacks.")  # Debugging print

async def game_loop():
    """Asynchronous game loop."""
    global running
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(BLACK)
        draw()
        update_fingers()
        handle_movement()

        # Check if 10 hours have passed
        elapsed_time = time.time() - start_time
        if elapsed_time > 10 * 3600:  # 10 hours in seconds
            print("10 hours have passed. Game Over.")
            running = False

        pygame.display.update()
        await asyncio.sleep(0)  # Yield control back to the event loop
        clock.tick(30)

async def main():
    """Main asynchronous entry point for the game."""
    await game_loop()

if __name__ == "__main__":
    asyncio.run(main())
    print("Exited game loop")  # Debugging print
    pygame.quit()