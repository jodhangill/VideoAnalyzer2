import pygame
import sys

# Initialize pygame
pygame.init()

# Set screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('5x6 Grid Animation')

# Grid dimensions
rows, cols = 5, 6  # Note: 6 rows and 5 columns
cell_width = screen_width // cols
cell_height = screen_height // rows

# Frame rate
fps = 30
clock = pygame.time.Clock()

# Initial frame count
frame_count = 0

def draw_grid(screen, rows, cols, frame_count):
    # Calculate current row and col
    total_cells = rows * cols
    current_cell = frame_count % total_cells
    current_row = current_cell // cols
    current_col = current_cell % cols

    for row in range(rows):
        for col in range(cols):
            color = (255, 255, 255) if row == current_row and col == current_col else (0, 0, 0)
            pygame.draw.rect(screen, color, (col * cell_width, row * cell_height, cell_width, cell_height))
            pygame.draw.rect(screen, (128, 128, 128), (col * cell_width, row * cell_height, cell_width, cell_height), 1)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear screen
    screen.fill((255, 255, 255))

    # Draw grid with the current frame
    draw_grid(screen, rows, cols, frame_count)

    # Update display
    pygame.display.flip()

    # Increment frame count
    frame_count += 1

    # Cap the frame rate
    clock.tick(fps)

# Quit pygame
pygame.quit()
sys.exit()
