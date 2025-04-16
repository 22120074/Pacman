import pygame
import copy
from Board import boards
from Board import road
import math
import random
import heapq
import time

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
Cell_Height = ((Height - 50) // 32) 
Cell_Width = (Width // 30)          
Num_Rows = len(Level)
Num_Cols = len(Level[0])

# Load ảnh
pinky_image = pygame.image.load("Pinky.png")
pinky_image = pygame.transform.scale(pinky_image, (Cell_Width, Cell_Height))
orange_image = pygame.image.load("Orange.png")
orange_image = pygame.transform.scale(orange_image, (Cell_Width, Cell_Height))
pacman_image = pygame.image.load("Pacman.jpg")
pacman_image = pygame.transform.scale(pacman_image, (Cell_Width, Cell_Height))

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
Orange = (255, 165, 0)

# Hàm hiển thị hướng dẫn di chuyển
def draw_instructions():
    font_20 = pygame.font.Font(None, 20)
    text_surface_1 = font_20.render("Press [ UP, DOWN, LEFT, RIGHT] on your Keyboard to move", True, White)
    text_rect_1 = text_surface_1.get_rect(center=(Width // 2, Height - 20))
    Screen.blit(text_surface_1, text_rect_1)

# Hàm vẽ game over
def draw_game_over():
    font = pygame.font.Font(None, 80)
    font_40 = pygame.font.Font(None, 40)
    text_surface_1 = font.render("GAME OVER", True, White)
    text_surface_2 = font_40.render("Press SPACE to restart", True, White)
    text_rect_1 = text_surface_1.get_rect(center=(Width // 2, Height // 2 - 200))
    text_rect_2 = text_surface_2.get_rect(center=(Width // 2, Height // 2))
    Screen.blit(text_surface_1, text_rect_1)
    Screen.blit(text_surface_2, text_rect_2)

# Hàm vẽ bản đồ
def draw_map(Cell_Width=Cell_Width, Cell_Height=Cell_Height, Flicker=Flicker):
    for i in range(len(Level)):
        for j in range(len(Level[i])):
            if Level[i][j] == 1:
                pygame.draw.circle(Screen, 'white', (j * Cell_Width + (0.5 * Cell_Width), i * Cell_Height + (0.5 * Cell_Height)), 4)
            if Level[i][j] == 2 and not Flicker:
                pygame.draw.circle(Screen, 'white', (j * Cell_Width + (0.5 * Cell_Width), i * Cell_Height + (0.5 * Cell_Height)), 10)
            if Level[i][j] == 3:
                pygame.draw.line(
                    Screen, Blue,
                    (j * Cell_Width + (0.5 * Cell_Width), i * Cell_Height),
                    (j * Cell_Width + (0.5 * Cell_Width), i * Cell_Height + Cell_Height),
                    3
                )
            if Level[i][j] == 4:
                pygame.draw.line(
                    Screen, Blue,
                    (j * Cell_Width, i * Cell_Height + (0.5 * Cell_Height)),
                    (j * Cell_Width + Cell_Width, i * Cell_Height + (0.5 * Cell_Height)),
                    3
                )
            if Level[i][j] == 5:
                pygame.draw.arc(
                    Screen, Blue,
                    [(j * Cell_Width - (Cell_Width * 0.4)) - 2, (i * Cell_Height + (0.5 * Cell_Height)), Cell_Width, Cell_Height],
                    0,
                    PI / 2,
                    3
                )
            if Level[i][j] == 6:
                pygame.draw.arc(
                    Screen, Blue,
                    [(j * Cell_Width + (Cell_Width * 0.5)), (i * Cell_Height + (0.5 * Cell_Height)), Cell_Width, Cell_Height],
                    PI / 2,
                    PI,
                    3
                )
            if Level[i][j] == 7:
                pygame.draw.arc(
                    Screen, Blue,
                    [(j * Cell_Width + (Cell_Width * 0.5)), (i * Cell_Height - (0.4 * Cell_Height)), Cell_Width, Cell_Height],
                    PI,
                    3 * PI / 2,
                    3
                )
            if Level[i][j] == 8:
                pygame.draw.arc(
                    Screen, Blue,
                    [(j * Cell_Width - (Cell_Width * 0.4)) - 2, (i * Cell_Height - (0.4 * Cell_Height)), Cell_Width, Cell_Height],
                    3 * PI / 2,
                    2 * PI,
                    3
                )
            if Level[i][j] == 9:
                pygame.draw.line(
                    Screen, 'white',
                    (j * Cell_Width, i * Cell_Height + (0.5 * Cell_Height)),
                    (j * Cell_Width + Cell_Width, i * Cell_Height + (0.5 * Cell_Height)),
                    3
                )

# Biến toàn cục
global blue_x, blue_y, red_x, red_y
blue_x = 0
blue_y = 0
red_x = 0
red_y = 0

# Biến cho Pinky
global pinky_x, pinky_y, nowDirections, shuffled_Directions, visited_pink_Stack, chosen_direction
global road_Stack, pinky_state, check_road, gate_state
pinky_x = 390
pinky_y = 360
chosen_direction = random.choice(["Right", "Left"])
Directions = {
    "Up": (0, -1 * Speed),
    "Down": (0, 1 * Speed),
    "Left": (-1 * Speed, 0),
    "Right": (1 * Speed, 0)
}
nowDirections = (0, 0)
shuffled_Directions = list(Directions.items())
visited_pink_Stack = set()
road_Stack = []
pinky_state = 0
gate_state = 0
check_road = False

# Biến cho Orange
global orange_x, orange_y, orange_path, orange_target_pos, last_path_calc_time, orange_gate_state, orange_directions
global orange_stuck_counter, orange_delay_frames
orange_x = 450
orange_y = 360
orange_path = []
orange_target_pos = None
last_path_calc_time = 0
orange_gate_state = 0
orange_directions = Up
orange_stuck_counter = 0
orange_delay_frames = 60  # 1 giây delay tại 60 FPS

# Biến cho Pacman
global pacman_x, pacman_y, direction_command, new_direction_command, direction_type
pacman_x = 420
pacman_y = 576
direction_command = (0, 0)
new_direction_command = (0, 0)
direction_type = 0

# Biến kiểm tra game đã bắt đầu hay chưa
global game_started
game_started = False

# Vẽ Pinky
def draw_pinky(pinky_x, pinky_y, Cell_Width, Cell_Height):
    if pinky_image:  
        Screen.blit(pinky_image, (pinky_x, pinky_y))
    else:
        pygame.draw.circle(Screen, Pink, pinky_x, pinky_y, 4)

# Pinky - DFS
def pinky_dfs(Cell_Width, Cell_Height):
    global pinky_x, pinky_y, nowDirections, shuffled_Directions, visited_pink_Stack
    global road_Stack, pinky_state, check_road, chosen_direction, gate_state
    
    if not game_started:
        draw_pinky(pinky_x, pinky_y, Cell_Width, Cell_Height)
        return

    if((pinky_x >= 360 and pinky_x <= 510) and (pinky_y > 288 and pinky_y <= 384)):
        if(nowDirections == (0, 0)):
            nowDirections = Right
            if not check_collision(pinky_x + nowDirections[0] * (30 // Speed), pinky_y + nowDirections[1] * (24 // Speed)):
                pinky_x += nowDirections[0]
                pinky_y += nowDirections[1]
            else:
                nowDirections = (0, 0)
        else:
            if(((pinky_x, pinky_y) == (420, 360)) or ((pinky_x, pinky_y) == (420, 336)) or ((pinky_x, pinky_y) == (420, 384)) 
                    or ((pinky_x, pinky_y) == (450, 360)) or ((pinky_x, pinky_y) == (450, 336)) or ((pinky_x, pinky_y) == (450, 384))
                    or ((pinky_x, pinky_y) == (420, 312)) or ((pinky_x, pinky_y) == (450, 312))):
                nowDirections = Up
                if not check_collision(pinky_x + nowDirections[0] * (30 // Speed), pinky_y + nowDirections[1] * (24 // Speed)):
                    pinky_x += nowDirections[0]
                    pinky_y += nowDirections[1]
            else:
                if not check_collision(pinky_x + nowDirections[0] * (30 // Speed), pinky_y + nowDirections[1] * (24 // Speed)):
                    pinky_x += nowDirections[0]
                    pinky_y += nowDirections[1]
    elif(((pinky_x, pinky_y) == (420, 288) or (pinky_x, pinky_y) == (450, 288)) and gate_state == 0):
        chosen_direction = random.choice(["Right", "Left"])
        nowDirections = Directions[chosen_direction]
        gate_state = 1
        if not check_collision(pinky_x + nowDirections[0] * (30 // Speed), pinky_y + nowDirections[1] * (24 // Speed)):
            if (pinky_x, pinky_y) not in visited_pink_Stack:
                visited_pink_Stack.add((pinky_x, pinky_y))
                road_Stack.append((pinky_x, pinky_y))
            pinky_x += nowDirections[0]
            pinky_y += nowDirections[1]
    elif(((pinky_x, pinky_y) == (0, 360)) and nowDirections == Left and pinky_state == 0):
        if (pinky_x, pinky_y) not in visited_pink_Stack:
            visited_pink_Stack.add((pinky_x, pinky_y))
            road_Stack.append((pinky_x, pinky_y))
        pinky_x = 870
        pinky_y = 360
    elif(((pinky_x, pinky_y) == (870, 360)) and nowDirections == Right and pinky_state == 0):
        if (pinky_x, pinky_y) not in visited_pink_Stack:
            visited_pink_Stack.add((pinky_x, pinky_y))
            road_Stack.append((pinky_x, pinky_y))
        pinky_x = 0
        pinky_y = 360
    else:
        if (pinky_x, pinky_y) in visited_pink_Stack:
            if(Road[pinky_y // Cell_Height][pinky_x // Cell_Width] >= 2 
               and (pinky_x // Cell_Width) == (pinky_x / Cell_Width) 
               and (pinky_y // Cell_Height) == (pinky_y / Cell_Height)):
                random.shuffle(shuffled_Directions)          
                for name, direction in shuffled_Directions:
                    opposite = tuple(-d for d in direction)     
                    if(Level[(pinky_y + direction[1] * (24 // Speed)) // Cell_Height][(pinky_x + direction[0] * (30 // Speed)) // Cell_Width] <= 2 
                            and (pinky_x + direction[0], pinky_y + direction[1]) not in visited_pink_Stack 
                            and nowDirections != opposite
                            and not check_collision(pinky_x + direction[0] * (30 // Speed), pinky_y + direction[1] * (24 // Speed))):
                        nowDirections = direction
                        pinky_x += direction[0]
                        pinky_y += direction[1]
                        check_road = True
                        break
            if not check_road:
                pinky_state = 1
        else:
            visited_pink_Stack.add((pinky_x, pinky_y))
            road_Stack.append((pinky_x, pinky_y))
        if(pinky_state == 0):
            if(Road[pinky_y // Cell_Height][pinky_x // Cell_Width] >= 2
                    and (pinky_x // Cell_Width) == (pinky_x / Cell_Width) 
                    and (pinky_y // Cell_Height) == (pinky_y / Cell_Height)):
                random.shuffle(shuffled_Directions)          
                for name, direction in shuffled_Directions:    
                    opposite = tuple(-d for d in direction)     
                    if check_collision(pinky_x + direction[0] * (30 // Speed), pinky_y + direction[1] * (24 // Speed)):
                        pinky_state = 1
                    if(Level[(pinky_y + direction[1] * (24 // Speed)) // Cell_Height][(pinky_x + direction[0] * (30 // Speed)) // Cell_Width] <= 2
                            and (pinky_x + direction[0], pinky_y + direction[1]) not in visited_pink_Stack 
                            and nowDirections != opposite
                            and not check_collision(pinky_x + direction[0] * (30 // Speed), pinky_y + direction[1] * (24 // Speed))):
                        nowDirections = direction
                        pinky_x += direction[0]
                        pinky_y += direction[1]
                        pinky_state = 0
                        break
            elif(Road[(pinky_y) // Cell_Height][pinky_x // Cell_Width] == 1
                    and (pinky_x // Cell_Width) == (pinky_x / Cell_Width)
                    and (pinky_y // Cell_Height) == (pinky_y / Cell_Height)):
                if check_collision(pinky_x + nowDirections[0] * (30 // Speed), pinky_y + nowDirections[1] * (24 // Speed)):
                    pinky_state = 1
                else:
                    pinky_x += nowDirections[0]
                    pinky_y += nowDirections[1]
            else:
                if not check_collision(pinky_x + nowDirections[0], pinky_y + nowDirections[1]):
                    pinky_x += nowDirections[0]
                    pinky_y += nowDirections[1]
                else:
                    pinky_state = 1
        if(pinky_state == 1):
            if len(road_Stack) > 0:
                pinky_x, pinky_y = road_Stack.pop()
            if len(road_Stack) == 0:
                visited_pink_Stack.clear()
                pinky_state = 0
                check_road = False
                gate_state = 0
        pinky_state = 0
        check_road = False
    draw_pinky(pinky_x, pinky_y, Cell_Width, Cell_Height)

# Hàm kiểm tra va chạm
def check_collision(next_x, next_y, exclude_self=True):
    global pinky_x, pinky_y, pacman_x, pacman_y, blue_x, blue_y, red_x, red_y, orange_x, orange_y
    # Kiểm tra xem vị trí tiếp theo có phải là cổng không
    next_row = int(next_y // Cell_Height)
    next_col = int(next_x // Cell_Width)
    is_gate = (0 <= next_row < Num_Rows and 0 <= next_col < Num_Cols and Level[next_row][next_col] == 9)
    
    # Nếu vị trí tiếp theo là cổng, bỏ qua kiểm tra va chạm với các nhân vật khác
    if is_gate:
        return False
    
    other_positions = [
        (pinky_x, pinky_y),
        (pacman_x, pacman_y),
        (blue_x, blue_y),
        (red_x, red_y),
        (orange_x, orange_y)
    ]
    for pos_x, pos_y in other_positions:
        if (next_x, next_y) == (pos_x, pos_y):
            if exclude_self and (next_x, next_y) == (orange_x, orange_y):
                continue
            return True
    return False

# Tìm đường đi bằng UCS
def find_ucs_path(start_pos, goal_pos):
    global orange_x, orange_y
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
        if current_node == goal_node:
            pixel_path = []
            full_path = path + [current_node]
            for node in full_path:
                pixel_path.append((node[0] * Cell_Width, node[1] * Cell_Height))
            return pixel_path[1:] if pixel_path else []

        col, row = current_node
        for dc, dr in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            next_col, next_row = col + dc, row + dr
            if next_col < 0 and next_row == 14:
                next_col = Num_Cols - 1
            elif next_col >= Num_Cols and next_row == 14:
                next_col = 0

            if 0 <= next_row < Num_Rows and 0 <= next_col < Num_Cols:
                if Level[next_row][next_col] <= 2 or Level[next_row][next_col] == 9:
                    neighbor_node = (next_col, next_row)
                    if neighbor_node not in visited:
                        next_pixel_x = next_col * Cell_Width
                        next_pixel_y = next_row * Cell_Height
                        if not check_collision(next_pixel_x, next_pixel_y):
                            visited.add(neighbor_node)
                            new_cost = cost + 1
                            new_path = path + [current_node]
                            heapq.heappush(queue, (new_cost, neighbor_node, new_path))
    return []

# Cập nhật vị trí của Orange
def update_orange_movement():
    global orange_x, orange_y, orange_path, orange_target_pos, last_path_calc_time, orange_gate_state, orange_directions
    global orange_stuck_counter, orange_delay_frames
    # Không di chuyển nếu game chưa bắt đầu
    if not game_started:
        return

    current_time = time.time()
    recalculate_path = False

    # Trì hoãn Orange để Pinky di chuyển trước
    if orange_delay_frames > 0:
        orange_delay_frames -= 1
        return

    # Lưu vị trí trước khi di chuyển để kiểm tra xem Orange có bị kẹt không
    prev_x, prev_y = orange_x, orange_y

    # Nếu Orange đang ở trong lồng
    if ((orange_x >= 360 and orange_x <= 510) and (orange_y > 288 and orange_y <= 384)):
        # Trạng thái ban đầu chưa có hướng đi
        if orange_directions == (0, 0):
            # Thử hướng Right trước, nếu không được thì thử Left
            if not check_collision(orange_x + Right[0] * (30 // Speed), orange_y + Right[1] * (24 // Speed)):
                orange_directions = Right
            elif not check_collision(orange_x + Left[0] * (30 // Speed), orange_y + Left[1] * (24 // Speed)):
                orange_directions = Left
            else:
                orange_directions = Up  # Nếu cả hai hướng đều bị chặn, thử đi lên
            if not check_collision(orange_x + orange_directions[0] * (30 // Speed), orange_y + orange_directions[1] * (24 // Speed)):
                orange_x += orange_directions[0]
                orange_y += orange_directions[1]
        # Đang ở trong lồng, đi ra ngoài
        else:
            # Nếu ở các vị trí cần đi lên để ra cổng
            if (((orange_x, orange_y) == (420, 360)) or ((orange_x, orange_y) == (420, 336)) or ((orange_x, orange_y) == (420, 384)) 
                    or ((orange_x, orange_y) == (450, 360)) or ((orange_x, orange_y) == (450, 336)) or ((orange_x, orange_y) == (450, 384))
                    or ((orange_x, orange_y) == (420, 312)) or ((orange_x, orange_y) == (450, 312))):
                orange_directions = Up
                if not check_collision(orange_x + orange_directions[0] * (30 // Speed), orange_y + orange_directions[1] * (24 // Speed)):
                    orange_x += orange_directions[0]
                    orange_y += orange_directions[1]
            else:
                if not check_collision(orange_x + orange_directions[0] * (30 // Speed), orange_y + orange_directions[1] * (24 // Speed)):
                    orange_x += orange_directions[0]
                    orange_y += orange_directions[1]
                else:
                    # Nếu hướng hiện tại bị chặn, thử hướng khác
                    for direction in [Up, Left, Right]:
                        if not check_collision(orange_x + direction[0] * (30 // Speed), orange_y + direction[1] * (24 // Speed)):
                            orange_directions = direction
                            orange_x += orange_directions[0]
                            orange_y += orange_directions[1]
                            break
    # Sau khi bước qua cổng lồng thì quẹo trái hoặc phải
    elif (((orange_x, orange_y) == (420, 288) or (orange_x, orange_y) == (450, 288)) and orange_gate_state == 0):
        chosen_direction = random.choice(["Right", "Left"])
        orange_directions = Directions[chosen_direction]
        orange_gate_state = 1
        if not check_collision(orange_x + orange_directions[0] * (30 // Speed), orange_y + orange_directions[1] * (24 // Speed)):
            orange_x += orange_directions[0]
            orange_y += orange_directions[1]
    # Khi đã thoát lồng, sử dụng UCS để đuổi Pacman
    else:
        # Nếu không có đường đi hoặc không có mục tiêu, cần tính lại đường đi
        if not orange_path and orange_target_pos is None:
            recalculate_path = True
        
        # Tính toán lại đường đi nếu cần hoặc sau mỗi 0.5 giây
        if current_time - last_path_calc_time < 0.5 and not recalculate_path:
            pass 
        elif recalculate_path or current_time - last_path_calc_time >= 0.5: 
            pacman_current_pixel_pos = (pacman_x, pacman_y)
            orange_current_pixel_pos = (orange_x, orange_y)
            # Tính toán lại đường đi bất kể Pacman có di chuyển hay không
            new_path = find_ucs_path(orange_current_pixel_pos, pacman_current_pixel_pos)
            if new_path: 
                orange_path = new_path
                if orange_path:
                    orange_target_pos = orange_path.pop(0) 
                else:
                    orange_target_pos = None
            else:
                orange_path = []
                orange_target_pos = None 
            last_path_calc_time = current_time 

        # Di chuyển Orange theo mục tiêu
        if orange_target_pos:
            target_x, target_y = orange_target_pos
            if (orange_x % Cell_Width == 0 and orange_y % Cell_Height == 0):
                move_x, move_y = 0, 0
                if orange_x < target_x:
                    move_x = Speed
                elif orange_x > target_x:
                    move_x = -Speed
                elif orange_y < target_y:
                    move_y = Speed
                elif orange_y > target_y:
                    move_y = -Speed

                next_x = orange_x + move_x
                next_y = orange_y + move_y
                if not check_collision(next_x, next_y):
                    orange_x = next_x
                    orange_y = next_y
                else:
                    orange_path = []
                    orange_target_pos = None
                    return

                if orange_x == target_x and orange_y == target_y:
                    if orange_path:
                        orange_target_pos = orange_path.pop(0)
                    else:
                        orange_target_pos = None
            else:
                current_direction = (0, 0)
                if orange_x % Cell_Width != 0:
                    if orange_x < target_x:
                        current_direction = (Speed, 0)
                    elif orange_x > target_x:
                        current_direction = (-Speed, 0)
                elif orange_y % Cell_Height != 0:
                    if orange_y < target_y:
                        current_direction = (0, Speed)
                    elif orange_y > target_y:
                        current_direction = (0, -Speed)
                
                next_x = orange_x + current_direction[0]
                next_y = orange_y + current_direction[1]
                if not check_collision(next_x, next_y):
                    orange_x = next_x
                    orange_y = next_y
                else:
                    orange_path = []
                    orange_target_pos = None

    

# Vẽ Orange
def draw_orange(orange_x, orange_y, Cell_Width, Cell_Height):
    if orange_image:
        Screen.blit(orange_image, (orange_x, orange_y))
    else:
        pygame.draw.circle(Screen, Orange, orange_x, orange_y, 4)

# Vẽ Pacman
def draw_Pacman(Cell_Width, Cell_Height):
    global pacman_x, pacman_y, direction_command, new_direction_command, direction_type
    opposite = tuple(-d for d in direction_command)
    if(((pacman_x, pacman_y) == (0, 360)) and direction_command == Left):
        pacman_x = 870
        pacman_y = 360
    elif(((pacman_x, pacman_y) == (870, 360)) and direction_command == Right):
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
            elif(Level[(pacman_y + direction_command[1] * (24 // Speed)) // Cell_Height][(pacman_x + direction_command[0] * (30 // Speed)) // Cell_Width] <= 2):
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
            if(new_direction_command == opposite):
                direction_command = new_direction_command
                pacman_x += direction_command[0]
                pacman_y += direction_command[1]
            else:
                pacman_x += direction_command[0]
                pacman_y += direction_command[1]
    if pacman_image:  
        Screen.blit(pacman_image,  (pacman_x, pacman_y))
    else:
        pygame.draw.circle(Screen, Yellow, (pacman_x, pacman_y), 4)

# Vòng lặp chính
run = True
Catched = False
while run:
    Timer.tick(FPS)
    Screen.fill((0, 0, 0))
    if Catched:
        draw_game_over()
    else:
        draw_map()
        draw_instructions()
        pinky_dfs(Cell_Width, Cell_Height)
        update_orange_movement()
        draw_orange(orange_x, orange_y, Cell_Width, Cell_Height)    
        if(pacman_x == pinky_x and pacman_y == pinky_y):
            Catched = True
        elif(pacman_x == orange_x and pacman_y == orange_y):
            Catched = True
        draw_Pacman(Cell_Width, Cell_Height)
        if(pacman_x == pinky_x and pacman_y == pinky_y):
            Catched = True
        elif(pacman_x == orange_x and pacman_y == orange_y):
            Catched = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                direction_type = 0
            if event.key == pygame.K_LEFT:
                direction_type = 1
            if event.key == pygame.K_UP:
                direction_type = 2
            if event.key == pygame.K_DOWN:
                direction_type = 3
            if event.key == pygame.K_SPACE:
                direction_type = 4
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT and direction_type == 0:
                new_direction_command = Right
                game_started = True  # Bắt đầu game khi nhấn phím di chuyển
            if event.key == pygame.K_LEFT and direction_type == 1:
                new_direction_command = Left
                game_started = True  # Bắt đầu game khi nhấn phím di chuyển
            if event.key == pygame.K_UP and direction_type == 2:
                new_direction_command = Up
                game_started = True  # Bắt đầu game khi nhấn phím di chuyển
            if event.key == pygame.K_DOWN and direction_type == 3:
                new_direction_command = Down
                game_started = True  # Bắt đầu game khi nhấn phím di chuyển
            if event.key == pygame.K_SPACE and direction_type == 4:
                Catched = False

                # Khởi tạo lại vị trí Pinky và Orange
                pinky_x = 390
                pinky_y = 360
                chosen_direction = random.choice(["Right", "Left"])
                nowDirections = (0, 0)
                visited_pink_Stack.clear()
                road_Stack.clear()
                pinky_state = 0             
                gate_state = 0              
                check_road = False          
                orange_x = 450 
                orange_y = 360
                orange_directions = Up
                orange_path.clear()
                orange_target_pos = None 
                last_path_calc_time = 0 
                orange_gate_state = 0
                orange_stuck_counter = 0
                orange_delay_frames = 60

                ## Khởi tạo lại vị trí Pacman
                pacman_x, pacman_y = 420, 576
                direction_command = (0, 0)
                new_direction_command = (0, 0)
                direction_type = 0
                game_started = False  # Reset trạng thái game

    pygame.display.flip()

pygame.quit()
