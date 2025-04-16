# Code Pacman Br BR bR
import pygame
import threading
import copy
from Board import boards
from Board import road
import pygame
import math
import random
import heapq # Import heapq for priority queue (used by UCS)
import time # To potentially limit path recalculation frequency

pygame.init()

# Cấu hình màn hình
Width = 900
Height = 818
Level = copy.deepcopy(boards)
Road = copy.deepcopy(road)
Flicker = False
PI = math.pi

# Hướng đi
Speed = 2
Up = (0, -1 * Speed)
Down = (0, Speed)
Left = (-1 * Speed, 0)
Right = (Speed, 0)

# Kích thước ô
Cell_Height = ((Height - 50) // 32) # 24
Cell_Width = (Width // 30)          # 30
Num_Rows = len(Level)
Num_Cols = len(Level[0])

# Load ảnh
orange_image = pygame.image.load("Orange.png")  # Đường dẫn đến ảnh 
orange_image = pygame.transform.scale(orange_image, (Cell_Width, Cell_Height))  # Resize ảnh
pacman_image = pygame.image.load("Pacman.jpg")  # Đường dẫn đến ảnh Pacman
pacman_image = pygame.transform.scale(pacman_image, (Cell_Width, Cell_Height))  # Resize ảnh

# Khung và Tiêu đề
Screen = pygame.display.set_mode((Width, Height))
pygame.display.set_caption("Pacman")

# Khung hình
FPS = 60
Timer = pygame.time.Clock()
Font = pygame.font.SysFont("Arial", 30)

# Màu sắc
Black = (0, 0, 0)
White = (255, 255, 255)
Pink = (255, 192, 203)
Yellow = (255, 255, 0)
Blue = (0, 0, 255)
Red = (255, 0, 0)

# --- Helper Functions ---
def draw_game_over():
    font = pygame.font.Font(None, 80)
    text_surface = font.render("GAME OVER", True, Red)
    text_rect = text_surface.get_rect(center=(Width // 2, Height // 2))
    Screen.blit(text_surface, text_rect)

def draw_map(Cell_Width=Cell_Width, Cell_Height=Cell_Height, Flicker=Flicker):
    for i in range(len(Level)):
        for j in range(len(Level[i])):
            # Hình tròn
            if Level[i][j] == 1:
                pygame.draw.circle(Screen, 'white', (j * Cell_Width + (0.5 * Cell_Width), i * Cell_Height + (0.5 * Cell_Height)), 4)
            # Hình tròn to
            if Level[i][j] == 2 and not Flicker:
                pygame.draw.circle(Screen, 'white', (j * Cell_Width + (0.5 * Cell_Width), i * Cell_Height + (0.5 * Cell_Height)), 10)
            # Đường thẳng dọc
            if Level[i][j] == 3:
                pygame.draw.line(
                    Screen, Blue,
                    (j * Cell_Width + (0.5 * Cell_Width), i * Cell_Height),
                    (j * Cell_Width + (0.5 * Cell_Width), i * Cell_Height + Cell_Height),
                    3
                )
            # Đường thẳng ngang
            if Level[i][j] == 4:
                pygame.draw.line(
                    Screen, Blue,
                    (j * Cell_Width, i * Cell_Height + (0.5 * Cell_Height)),
                    (j * Cell_Width + Cell_Width, i * Cell_Height + (0.5 * Cell_Height)),
                    3
                )
            # Góc phải trên
            if Level[i][j] == 5:
                pygame.draw.arc(
                    Screen, Blue,
                    [(j * Cell_Width - (Cell_Width * 0.4)) - 2, (i * Cell_Height + (0.5 * Cell_Height)), Cell_Width, Cell_Height],
                    0,
                    PI / 2,
                    3
                )
            # Góc trái trên
            if Level[i][j] == 6:
                pygame.draw.arc(
                    Screen, Blue,
                    [(j * Cell_Width + (Cell_Width * 0.5)), (i * Cell_Height + (0.5 * Cell_Height)), Cell_Width, Cell_Height],
                    PI / 2,
                    PI,
                    3
                )
            # Góc trái dưới
            if Level[i][j] == 7:
                pygame.draw.arc(
                    Screen, Blue,
                    [(j * Cell_Width + (Cell_Width * 0.5)), (i * Cell_Height - (0.4 * Cell_Height)), Cell_Width, Cell_Height],
                    PI,
                    3 * PI / 2,
                    3
                )
            # Góc phải dưới
            if Level[i][j] == 8:
                pygame.draw.arc(
                    Screen, Blue,
                    [(j * Cell_Width - (Cell_Width * 0.4)) - 2, (i * Cell_Height - (0.4 * Cell_Height)), Cell_Width, Cell_Height],
                    3 * PI / 2,
                    2 * PI,
                    3
                )
            # Cổng ghost
            if Level[i][j] == 9:
                pygame.draw.line(
                    Screen, 'white',
                    (j * Cell_Width, i * Cell_Height + (0.5 * Cell_Height)),
                    (j * Cell_Width + Cell_Width, i * Cell_Height + (0.5 * Cell_Height)),
                    3
                )


orange_x = 420  
orange_y = 288
orange_path = [] #
orange_target_pos = None 
last_path_calc_time = 0 

# Tìm đường đi bằng UCS
def find_ucs_path(start_pos, goal_pos):
    global orange_x, orange_y
    draw_orange(orange_x,orange_y,Cell_Width, Cell_Height)
    
    start_col = start_pos[0] // Cell_Width
    start_row = start_pos[1] // Cell_Height
    goal_col = goal_pos[0] // Cell_Width
    goal_row = goal_pos[1] // Cell_Height
    start_node = (start_col, start_row)
    goal_node = (goal_col, goal_row)

    
    
    queue = [(0, start_node, [])]
    visited = {start_node} 

    while queue:
        cost, current_node, path = heapq.heappop(queue)

        # Kiểm tra xem đã đến đích chưa
        if current_node == goal_node:
            # Chuyển đổi tọa độ lưới trở lại tọa độ pixel
            pixel_path = []
            full_path = path + [current_node] 
            for node in full_path:
                 
                pixel_path.append((node[0] * Cell_Width, node[1] * Cell_Height))
            
            if pixel_path:
                 return pixel_path[1:]
            else:
                 return []

        col, row = current_node
       
        for dc, dr in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            next_col, next_row = col + dc, row + dr

            # Đường hầm
            if next_col < 0 and next_row == 14: # 
                 next_col = Num_Cols - 1
            elif next_col >= Num_Cols and next_row == 14: 
                 next_col = 0

        
            if 0 <= next_row < Num_Rows and 0 <= next_col < Num_Cols:
                 if Level[next_row][next_col] <= 2 or Level[next_row][next_col] == 9:
                     neighbor_node = (next_col, next_row)
                     if neighbor_node not in visited:
                         visited.add(neighbor_node)
                         new_cost = cost + 1
                         new_path = path + [current_node]
                         heapq.heappush(queue, (new_cost, neighbor_node, new_path))

   
    return [] 

# Cập nhật vị trí của Orange
def update_orange_movement():
    global orange_x, orange_y, orange_path, orange_target_pos, last_path_calc_time

    current_time = time.time()
    recalculate_path = False

    
    if not orange_path and orange_target_pos is None:
        recalculate_path = True
        

    
    if current_time - last_path_calc_time < 0.5 and not recalculate_path:
         pass 
    elif recalculate_path or current_time - last_path_calc_time >= 0.5: 
         
        
         pacman_current_pixel_pos = (pacman_x, pacman_y)
         orange_current_pixel_pos = (orange_x, orange_y)

        # Kiểm tra xem Pacman có trong tầm nhìn của Orange không
         if orange_current_pixel_pos != pacman_current_pixel_pos:
             
             new_path = find_ucs_path(orange_current_pixel_pos, pacman_current_pixel_pos)
             if new_path: 
                 orange_path = new_path
                 orange_target_pos = orange_path.pop(0) 
                
             else:
                 
                 orange_path = []
                 orange_target_pos = None 
             last_path_calc_time = current_time 
         else:
              
              orange_path = []
              orange_target_pos = None


    # Di chuyển đến Pacman
    if orange_target_pos:
        target_x, target_y = orange_target_pos

        
        move_x, move_y = 0, 0
        if orange_x < target_x:
            move_x = Speed
        elif orange_x > target_x:
            move_x = -Speed

        if orange_y < target_y:
            move_y = Speed
        elif orange_y > target_y:
            move_y = -Speed

        # Di chuyển Orange
        orange_x += move_x
        orange_y += move_y

        # Kiểm tra xem Orange đã đến vị trí mục tiêu chưa
        
        reached_x = (move_x > 0 and orange_x >= target_x) or \
                    (move_x < 0 and orange_x <= target_x) or \
                    (move_x == 0)
        reached_y = (move_y > 0 and orange_y >= target_y) or \
                    (move_y < 0 and orange_y <= target_y) or \
                    (move_y == 0)

        if reached_x and reached_y:
           
            orange_x = target_x
            orange_y = target_y
            
           
            if orange_path:
                orange_target_pos = orange_path.pop(0)
               
            else:
                
                orange_target_pos = None # End of path


# Vẽ orange 
def draw_orange(orange_x, orange_y, Cell_Width, Cell_Height):
    if orange_image:
        Screen.blit(orange_image, (orange_x, orange_y))
    else:
        pygame.draw.circle(Screen, Pink, orange_x, orange_y, 4)


# # # # Biến cho Pacman ----------------------------------------------------------------------------
# Vị trí ban đầu của Pacman
global pacman_x, pacman_y, direction_command, new_direction_command
pacman_x = 210
pacman_y = 576
# Hướng đi hiện tại của Pacman
direction_command = (0, 0)
new_direction_command = (0, 0)
direction_type = 0 

# Vẽ Pacman 
def draw_Pacman(Cell_Width, Cell_Height):
    global pacman_x, pacman_y, direction_command
    opposite = tuple(-d for d in direction_command)
    if (pacman_x, pacman_y) == (0, 360) and direction_command == Left:
        pacman_x = 870
        pacman_y = 360
    elif (pacman_x, pacman_y) == (870, 360) and direction_command == Right:
        pacman_x = 0
        pacman_y = 360
    else:
        if(Road[(pacman_y) // Cell_Height][pacman_x // Cell_Width] >= 2
                and (pacman_x // Cell_Width) == (pacman_x / Cell_Width)
                and (pacman_y // Cell_Height) == (pacman_y / Cell_Height)):
            if(Level[(pacman_y + new_direction_command[1] * (24 // Speed)) // Cell_Height][(pacman_x + new_direction_command[0] * (30 // Speed)) // Cell_Width] <= 2):
                direction_command = new_direction_command
                pacman_x += direction_command[0]
                pacman_y += direction_command[1]
        elif(Road[(pacman_y) // Cell_Height][pacman_x // Cell_Width] == 1
                and (pacman_x // Cell_Width) == (pacman_x / Cell_Width)
                and (pacman_y // Cell_Height) == (pacman_y / Cell_Height)
                and new_direction_command != opposite):
            if(Level[(pacman_y + new_direction_command[1] * (24 // Speed)) // Cell_Height][(pacman_x + new_direction_command[0] * (30 // Speed)) // Cell_Width] <= 2):
                direction_command = new_direction_command
                pacman_x += direction_command[0]
                pacman_y += direction_command[1]
            else:
                pacman_x += direction_command[0]
                pacman_y += direction_command[1]
        else:
            pacman_x += direction_command[0]
            pacman_y += direction_command[1]
    if pacman_image:  
        Screen.blit(pacman_image,  (pacman_x, pacman_y))
    else:
        pygame.draw.circle(Screen, Yellow, (pacman_x, pacman_y), 4)
     
    

run = True
Catched = False
while run:
    Timer.tick(FPS)
    # Vẽ bản đồ
    Screen.fill((0, 0, 0))  # Vẽ lại nền đen
    if not Catched:
        draw_map()
        # Vẽ orange
        update_orange_movement() 
        draw_orange(orange_x, orange_y, Cell_Width, Cell_Height)    

        # Vẽ Pacman
        draw_Pacman(Cell_Width, Cell_Height)
    else:
        draw_game_over()
    # Check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        # Kiểm tra nhấn phím
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT: direction_type = 0
            elif event.key == pygame.K_LEFT: direction_type = 1
            elif event.key == pygame.K_UP: direction_type = 2
            elif event.key == pygame.K_DOWN: direction_type = 3
           

        if event.type == pygame.KEYUP:
            
            if event.key == pygame.K_RIGHT and direction_type == 0: new_direction_command = Right
            elif event.key == pygame.K_LEFT and direction_type == 1: new_direction_command = Left
            elif event.key == pygame.K_UP and direction_type == 2: new_direction_command = Up
            elif event.key == pygame.K_DOWN and direction_type == 3: new_direction_command = Down

    if(pacman_x == orange_x and pacman_y == orange_y):
        Catched = True
    
    
    pygame.display.flip()   # Tải lại hiệu ứng mới

pygame.quit()