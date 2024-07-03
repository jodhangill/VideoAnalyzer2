import pygame
import sys
import numpy as np
import cv2

# Initialize pygame
pygame.init()


# Load video and extract the first frame
video_path = 'video3.mp4'  # Replace with your video path
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

cap.release()
pygame.quit()

# Analyze Video Frames
# Path to your video file

# Get brightnesses of each point
def get_brightness(grid_points, frame):
    point_brightnesses = [[0]*6 for i in range(5)]
    for i in range(len(grid_points) - 1):
        for j in range(len(grid_points[0]) - 1):
            points = [grid_points[i][j], grid_points[i][j+1], grid_points[i+1][j], grid_points[i+1][j+1]]
            x, y = calculate_centroid(points)
            brightness = sum(frame[int(y), int(x)])
            point_brightnesses[i][j] = brightness
    return point_brightnesses
# Open the video file
cap = cv2.VideoCapture(video_path)

# Get minimum brightnesses of first 3 frames
base_brightnesses = [[799]*6 for i in range(5)]
# Check if the video opened successfully
if not cap.isOpened():
    print("Error opening video file")
    exit()
else:
    base_brightnesses = [[799]*6 for i in range(5)]
    for _ in range(3):
        ret, frame = cap.read()
        if ret:
            brightnesses = get_brightness(grid_points, frame)
            for i in range(5):
                for j in range(6):
                    base_brightnesses[i][j] = min(brightnesses[i][j], base_brightnesses[i][j])
cap.release()

# Open the video file
cap = cv2.VideoCapture(video_path)
# Check if the video opened successfully
if not cap.isOpened():
    print("Error opening video file")
    exit()

fps = 24

boxes_per_frame = 30/fps

expected_position = 1
tolerance = 1

last_lit = 1

frame_number = 0
while cap.isOpened():
    frame_number += 1
    lit = 1
    flag = False
    # Capture frame-by-frame
    ret, frame = cap.read()
    if ret:
        print(f"Frame {frame_number}: ", end="")
        for i in range(5):
                for j in range(6):
                    brightnesses = get_brightness(grid_points, frame)
                    if (brightnesses[i][j] > 1.2*base_brightnesses[i][j]):
                        lit = i*6 + j + 1
                        upper_tol = (last_lit % 30) + round(boxes_per_frame) + tolerance
                        lower_tol = (last_lit % 30) + round(boxes_per_frame) - tolerance
                        if lit >= lower_tol and lit <= upper_tol:
                            flag = True

        if flag: print("Good")
        else: print("Bad")

        last_lit = lit


        # Press 'q' to exit loop
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
        frame += 1
    else:
        break

# Release the video capture object and close all windows
cap.release()
cv2.destroyAllWindows()

# Quit pygame
pygame.quit()
sys.exit()
