import pygame
import sys
import numpy as np
import cv2

# Initialize pygame
pygame.init()


# Load video and extract the first frame
video_path = 'your_video.mp4'  # Replace with your video path
cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    print("Error opening video file")
    exit()

# Read the first frame
ret, frame_bgr = cap.read()
if not ret:
    print("Error reading video frame")
    exit()

# Convert BGR to RGB format
frame = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)

# Now 'frame_rgb' is a numpy array representing the first frame in RGB format
# You can manipulate and process 'frame_rgb' as needed

# Release the video capture object
cap.release()

# Get frame dimensions
frame_width, frame_height = frame.shape[1], frame.shape[0]

# Set screen dimensions to match frame size
screen_width, screen_height = frame_width, frame_height
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Transform the Polygon on the Video Frame')

# Convert frame to pygame surface
img = pygame.image.frombuffer(frame.tobytes(), frame.shape[1::-1], 'RGB')

# Initial polygon coordinates (a rectangle for example)
polygon = [(150, 150), (650, 150), (650, 450), (150, 450)]
dragging_corner = None

def calculate_centroid(points):
    x_coords = [p[0] for p in points]
    y_coords = [p[1] for p in points]
    centroid_x = sum(x_coords) / len(points)
    centroid_y = sum(y_coords) / len(points)
    return (centroid_x, centroid_y)

def interpolate_points(p1, p2, steps):
    return [(p1[0] + (p2[0] - p1[0]) * i / steps, p1[1] + (p2[1] - p1[1]) * i / steps) for i in range(steps + 1)]

def calculate_grid_points(polygon, rows, cols):
    top_edge = interpolate_points(polygon[0], polygon[1], cols)
    bottom_edge = interpolate_points(polygon[3], polygon[2], cols)
    left_edge = interpolate_points(polygon[0], polygon[3], rows)
    right_edge = interpolate_points(polygon[1], polygon[2], rows)
    
    grid_points = []
    for i in range(rows + 1):
        row = interpolate_points(left_edge[i], right_edge[i], cols)
        grid_points.append(row)
    
    return grid_points

def draw_grid(screen, rows, cols, frame_count):
    # Calculate current row and col
    total_cells = rows * cols
    current_cell = frame_count % total_cells
    current_row = current_cell // cols
    current_col = current_cell % cols

def draw_dots(screen, grid_points):
    for i in range(len(grid_points) - 1):
        for j in range(len(grid_points[0]) - 1):
            points = [grid_points[i][j], grid_points[i][j+1], grid_points[i+1][j], grid_points[i+1][j+1]]
            pygame.draw.circle(screen, (0, 255, 0), calculate_centroid(points), 3)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for i, corner in enumerate(polygon):
                    if pygame.Rect(corner[0] - 10, corner[1] - 10, 20, 20).collidepoint(event.pos):
                        dragging_corner = i
                        break
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                dragging_corner = None
        elif event.type == pygame.MOUSEMOTION:
            if dragging_corner is not None:
                mouse_x, mouse_y = event.pos
                polygon[dragging_corner] = (mouse_x, mouse_y)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                print("Polygon corners confirmed at coordinates:")
                for i, corner in enumerate(polygon):
                    print(f"Corner {i+1}: {corner}")
                running = False

    # Clear screen
    screen.fill((0, 0, 0))

    # Draw image
    screen.blit(img, ((screen_width - img.get_width()) // 2, (screen_height - img.get_height()) // 2))

    # Draw the polygon
    pygame.draw.polygon(screen, (255, 0, 0), polygon, 2)

    # Draw polygon Corners
    for corner in polygon:
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(corner[0] - 10, corner[1] - 10, 20, 20), 1)

    # Calculate and draw centroid
    centroid = calculate_centroid(polygon)
    pygame.draw.circle(screen, (0, 0, 255), (int(centroid[0]), int(centroid[1])), 5)

    # Calculate and draw grid points
    grid_points = calculate_grid_points(polygon, 5, 6)

    # Draw dots in the center of each grid cell
    draw_dots(screen, grid_points)

    # Draw grid lines
    for row in grid_points:
        pygame.draw.lines(screen, (0, 255, 0), False, row, 1)
    for col in range(6 + 1):
        col_points = [grid_points[row][col] for row in range(5 + 1)]
        pygame.draw.lines(screen, (0, 255, 0), False, col_points, 1)

    # Update display
    pygame.display.flip()

# Analyze Video Frames
# Path to your video file
video_path = 'your_video.mp4'

# Open the video file
cap = cv2.VideoCapture(video_path)

# Check if the video opened successfully
if not cap.isOpened():
    print("Error opening video file")
    exit()

while cap.isOpened():
    # Capture frame-by-frame
    ret, frame = cap.read()

    point_brightnesses = [[0]*6 for i in range(5)]

    grid_points = calculate_grid_points(polygon, 5, 6)
    for i in range(len(grid_points) - 1):
        for j in range(len(grid_points[0]) - 1):
            points = [grid_points[i][j], grid_points[i][j+1], grid_points[i+1][j], grid_points[i+1][j+1]]
            x, y = calculate_centroid(points)
            brightness = sum(frame[int(y), int(x)])
            point_brightnesses[i][j] = brightness

    if ret:
        point_brightnesses = [[0]*6 for i in range(5)]

        # Get brightnesses of each point
        grid_points = calculate_grid_points(polygon, 5, 6)
        for i in range(len(grid_points) - 1):
            for j in range(len(grid_points[0]) - 1):
                points = [grid_points[i][j], grid_points[i][j+1], grid_points[i+1][j], grid_points[i+1][j+1]]
                x, y = calculate_centroid(points)
                brightness = sum(frame[int(y), int(x)])
                point_brightnesses[i][j] = brightness
        
        print(point_brightnesses)

        # Press 'q' to exit loop
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
    else:
        break
# Read a single frame
ret, frame = cap.read()

# Check if the frame was successfully read
if not ret:
    print("Error reading frame")
    exit()

# Specify the pixel coordinates (x, y) you want to get brightness from
x = 100  # Example x-coordinate
y = 150  # Example y-coordinate

# Get the brightness (grayscale value) of the pixel at (x, y)
brightness = sum(frame[y, x])

print(f"Brightness of pixel ({x}, {y}): {brightness}")

# Release the video capture object and close all windows
cap.release()
cv2.destroyAllWindows()

# Quit pygame
pygame.quit()
sys.exit()
