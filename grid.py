import pygame
import sys

# Initialize pygame
pygame.init()

# Set screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Colors
white = (255, 255, 255)
black = (0, 0, 0)

# Define grid parameters
grid_size = 30  # Number of squares in the grid
square_size = screen_width // grid_size  # Size of each square

# Counter to track frames
frame_counter = 0

# Main loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear screen
    screen.fill(white)

    # Calculate current position of the black square
    current_square = frame_counter % grid_size

    # Draw grid squares
    for i in range(grid_size):
        rect = pygame.Rect(i * square_size, 0, square_size, screen_height)
        if i == current_square:
            pygame.draw.rect(screen, black, rect)
        pygame.draw.rect(screen, black, rect, 1)  # Draw grid lines

    # Update display
    pygame.display.flip()

    # Increment frame counter
    frame_counter += 1

    # Cap the frame rate
    pygame.time.Clock().tick(30)

# Quit pygame
pygame.quit()
sys.exit()
