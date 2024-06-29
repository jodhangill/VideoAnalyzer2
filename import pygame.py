import pygame
import sys

# Initialize pygame
pygame.init()

# Set screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Click Two Points on the Image')

# Load an image
image_path = './2024-06-28 17.03.41.png'  # Replace with your image path
try:
    img = pygame.image.load(image_path)
except pygame.error as e:
    print(f"Unable to load image: {image_path}")
    print(e)
    sys.exit()

# Get image dimensions
img_width, img_height = img.get_rect().size

# Resize image if it's larger than the screen
if img_width > screen_width or img_height > screen_height:
    img = pygame.transform.scale(img, (min(img_width, screen_width), min(img_height, screen_height)))

# Main loop
running = True
points = []
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Check if left mouse button clicked
            if event.button == 1:
                # Get mouse position
                mouse_x, mouse_y = event.pos
                # Store the point
                points.append((mouse_x, mouse_y))
                # Print point coordinates
                print(f"Point {len(points)} clicked at: ({mouse_x}, {mouse_y})")

                # If two points have been clicked, exit the loop
                if len(points) == 2:
                    running = False

    # Draw image on screen
    screen.blit(img, ((screen_width - img.get_width()) // 2, (screen_height - img.get_height()) // 2))

    # Update display
    pygame.display.flip()

# Quit pygame
pygame.quit()

# Print final points
print("Final points:")
for i, (x, y) in enumerate(points, 1):
    print(f"Point {i}: ({x}, {y})")
