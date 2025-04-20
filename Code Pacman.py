# Code Pacman Br BR bR
import pygame
import copy
from Board import boards
from Board import road
import math
import random
import heapq # Import heapq for priority queue (used by UCS)
import time # To potentially limit path recalculation frequency
import tracemalloc

tracemalloc.start()

import heapq

pygame.init()

# Cấu hình màn hình
Width = 900
Height = 818
Level = copy.deepcopy(boards)
Road = copy.deepcopy(road)
Flicker = False
PI = math.pi

# Hướng đi và tốc độ
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
pinky_image = pygame.image.load("Images/Pinky.png")  # Đường dẫn đến ảnh Pinky
pinky_image = pygame.transform.scale(pinky_image, (Cell_Width, Cell_Height))  # Resize ảnh
orange_image = pygame.image.load("Images/Orange.png")  # Đường dẫn đến ảnh Orange
orange_image = pygame.transform.scale(orange_image, (Cell_Width, Cell_Height))  # Resize ảnh
blinky_image = pygame.image.load("Images/Red.jpg")  # Đường dẫn đến ảnh Blinky
blinky_image = pygame.transform.scale(blinky_image, (Cell_Width, Cell_Height))  # Resize ảnh
pacman_image = pygame.image.load("Images/Pacman.jpg")  # Đường dẫn đến ảnh Pacman
pacman_image = pygame.transform.scale(pacman_image, (Cell_Width, Cell_Height))  # Resize ảnh
blue_image = pygame.image.load("Images/Blue.png") # Đường dẫn đến ảnh Blue
blue_image = pygame.transform.scale(blue_image, (Cell_Width, Cell_Height)) # Resize ảnh

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
    # Khởi tạo font (None, 20)
    font_20 = pygame.font.Font(None, 20)
    # Render chữ ra một surface
    text_surface_1 = font_20.render("Press [ UP, DOWN, LEFT, RIGHT] on your Keyboard to move", True, White)
    # Render
    text_rect_1 = text_surface_1.get_rect(center=(Width // 2, Height - 20))
    # vẽ lên màn hình 
    Screen.blit(text_surface_1, text_rect_1)

# Hàm hiển thị Game Over 
def draw_game_over():
    font = pygame.font.Font(None, 80)
    # Khởi tạo font (None, 40)
    font_40 = pygame.font.Font(None, 40)
    # Render chữ ra một surface
    text_surface_1 = font.render("GAME OVER", True, White)
    text_surface_2 = font_40.render("Press SPACE to restart", True, White)
    # Render
    text_rect_1 = text_surface_1.get_rect(center=(Width // 2, Height // 2 - 200))
    text_rect_2 = text_surface_2.get_rect(center=(Width // 2, Height // 2))
    # Vẽ lên màn hình
    Screen.blit(text_surface_1, text_rect_1)
    Screen.blit(text_surface_2, text_rect_2)

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

# Hàm vẽ đường đi để kiểm tra các ngã rẽ và đường đi đúng số chưa trong Road 
def draw_road(Cell_Width=Cell_Width, Cell_Height=Cell_Height):
    for i in range(len(Road)):
        for j in range(len(Road[i])):
            # Hình tròn
            if Road[i][j] == 1:
                pygame.draw.circle(Screen, 'white', (j * Cell_Width + (0.5 * Cell_Width), i * Cell_Height + (0.5 * Cell_Height)), 4)
            # Hình tròn to
            if Road[i][j] == 2 and not Flicker:
                pygame.draw.circle(Screen, 'white', (j * Cell_Width + (0.5 * Cell_Width), i * Cell_Height + (0.5 * Cell_Height)), 10)
            if Road[i][j] == 3:
                pygame.draw.circle(Screen, 'white', (j * Cell_Width + (0.5 * Cell_Width), i * Cell_Height + (0.5 * Cell_Height)), 15)
            if Road[i][j] == 4:
                pygame.draw.circle(Screen, 'white', (j * Cell_Width + (0.5 * Cell_Width), i * Cell_Height + (0.5 * Cell_Height)), 20)

# # # Biến cho Pinky ---------------------------------------------------------------------------------------------------------------
global pinky_x, pinky_y, nowDirections, shuffled_Directions, visited_pink_Stack, chosen_direction
global road_Stack, pinky_state, check_road, gate_state, expanded_nodes
# Vị trí ban đầu của Pinky
# pinky_x = 420 # Đây là trường hợp Pinky ở ngoài lồng
# pinky_y = 288
pinky_x = 390 # Đây là trường hợp Pinky ở trong lồng
pinky_y = 360
# Các hướng đi
chosen_direction = random.choice(["Right", "Left"])
Directions = {
    "Up": (0, -1 * Speed),
    "Down": (0, 1 * Speed),
    "Left": (-1 * Speed, 0),
    "Right": (1 * Speed, 0)
}
# Hướng đi hiện tại của Pinky
nowDirections = (0, 0)  # Trạng thái ban đầu chưa có hướng đi
# Lấy danh sách hướng
shuffled_Directions = list(Directions.items())
# Ngăn xếp lưu các node đã đi qua để duyệt lại
visited_pink_Stack = set()  # .add() để thêm, .remove() để xóa
# Ngăn xếp lưu đường đi
road_Stack = []             # .append() để thêm, .pop() để xóa
# Trạng thái của Pinky
pinky_state = 0             # 0: bình thường, 1: back tracking
gate_state = 0              # 0: chưa qua cổng, 1: đã qua cổng
check_road = False          # Kiểm tra ngã rẽ khi đang back-tracking
expanded_nodes = 0

# Vẽ Pinky
def draw_pinky(pinky_x, pinky_y, Cell_Width, Cell_Height):
    if pinky_image:  
        Screen.blit(pinky_image, (pinky_x, pinky_y))
    else:
        pygame.draw.circle(Screen, Pink, pinky_x, pinky_y, 4)

# Pinky - DFS
def pinky_dfs(Cell_Width, Cell_Height):
    global pinky_x, pinky_y, nowDirections, shuffled_Directions, visited_pink_Stack
    global road_Stack, pinky_state, check_road, chosen_direction, gate_state, expanded_nodes
    # Nếu đang ở trong lồng, ta đi ra khỏi lồng rồi bắt Pacman
    if((pinky_x >= 360 and pinky_x <= 510) and (pinky_y > 288 and pinky_y <= 384)):
        # Trạng thái ban đầu chưa có hướng đi
        if(nowDirections == (0, 0)):
            nowDirections = Right
            if((pinky_x + nowDirections[0] * (30 // Speed), pinky_y + nowDirections[1] * (24 // Speed)) != (blue_x, blue_y)
                        and (pinky_x + nowDirections[0] * (30 // Speed), pinky_y + nowDirections[1] * (24 // Speed)) != (orange_x, orange_y)
                        and (pinky_x + nowDirections[0] * (30 // Speed), pinky_y + nowDirections[1] * (24 // Speed)) != (blinky_x, blinky_y)):
                pinky_x += nowDirections[0]
                pinky_y += nowDirections[1]
            else:
                nowDirections = (0, 0)
        # Đang ở trong lồng, đi ra ngoài
        else:
            if(((pinky_x, pinky_y) == (420, 360)) or ((pinky_x, pinky_y) == (420, 336)) or ((pinky_x, pinky_y) == (420, 384)) 
                    or ((pinky_x, pinky_y) == (450, 360)) or ((pinky_x, pinky_y) == (450, 336)) or ((pinky_x, pinky_y) == (450, 384))
                    or ((pinky_x, pinky_y) == (420, 312)) or ((pinky_x, pinky_y) == (450, 312))):
                nowDirections = Up
                if((pinky_x + nowDirections[0] * (30 // Speed), pinky_y + nowDirections[1] * (24 // Speed)) != (blue_x, blue_y)
                        and (pinky_x + nowDirections[0] * (30 // Speed), pinky_y + nowDirections[1] * (24 // Speed)) != (orange_x, orange_y)
                        and (pinky_x + nowDirections[0] * (30 // Speed), pinky_y + nowDirections[1] * (24 // Speed)) != (blinky_x, blinky_y)):
                    pinky_x += nowDirections[0]
                    pinky_y += nowDirections[1]
            else:
                if((pinky_x + nowDirections[0] * (30 // Speed), pinky_y + nowDirections[1] * (24 // Speed)) != (blue_x, blue_y)
                        and (pinky_x + nowDirections[0] * (30 // Speed), pinky_y + nowDirections[1] * (24 // Speed)) != (orange_x, orange_y)
                        and (pinky_x + nowDirections[0] * (30 // Speed), pinky_y + nowDirections[1] * (24 // Speed)) != (blinky_x, blinky_y)):
                    pinky_x += nowDirections[0]
                    pinky_y += nowDirections[1]
    # Sau khi bước qua cổng lồng thì quẹo trái hoặc phải
    elif(((pinky_x, pinky_y) == (420, 288) or (pinky_x, pinky_y) == (450, 288)) and gate_state == 0):
        chosen_direction = random.choice(["Right", "Left"])
        nowDirections = Directions[chosen_direction]
        gate_state = 1
        if((pinky_x + nowDirections[0] * (30 // Speed), pinky_y + nowDirections[1] * (24 // Speed)) != (blue_x, blue_y)
                and (pinky_x + nowDirections[0] * (30 // Speed), pinky_y + nowDirections[1] * (24 // Speed)) != (orange_x, orange_y)
                and (pinky_x + nowDirections[0] * (30 // Speed), pinky_y + nowDirections[1] * (24 // Speed)) != (blinky_x, blinky_y)):
            if (pinky_x, pinky_y) not in visited_pink_Stack:
                # Thêm ô vào danh sách đã đi qua
                visited_pink_Stack.add((pinky_x, pinky_y))
                # Thêm vào road_Stack để back-up
                road_Stack.append((pinky_x, pinky_y))
            pinky_x += nowDirections[0]
            pinky_y += nowDirections[1]
    # Kiểm tra 2 vị trí đặc biệt nối liền nhau 2 bên map
    elif(((pinky_x, pinky_y) == (0, 360)) and nowDirections == Left and pinky_state == 0):
        if (pinky_x, pinky_y) not in visited_pink_Stack:
            # Thêm ô vào danh sách đã đi qua
            visited_pink_Stack.add((pinky_x, pinky_y))
            # Thêm vào road_Stack để back-up
            road_Stack.append((pinky_x, pinky_y))
        pinky_x = 870
        pinky_y = 360
    elif(((pinky_x, pinky_y) == (870, 360)) and nowDirections == Right and pinky_state == 0):
        if (pinky_x, pinky_y) not in visited_pink_Stack:
            # Thêm ô vào danh sách đã đi qua
            visited_pink_Stack.add((pinky_x, pinky_y))
            # Thêm vào road_Stack để back-up
            road_Stack.append((pinky_x, pinky_y))
        pinky_x = 0
        pinky_y = 360
    else:
        # Kiểm tra nếu Pinky đã đi qua ô này chưa
        if (pinky_x, pinky_y) in visited_pink_Stack:
            if(Road[pinky_y // Cell_Height][pinky_x // Cell_Width] >= 2 
               and (pinky_x // Cell_Width) == (pinky_x / Cell_Width) 
               and (pinky_y // Cell_Height) == (pinky_y / Cell_Height)):
                # Kiểm tra xong quanh còn đường đi chưa đi không?
                random.shuffle(shuffled_Directions)        
                # Duyệt qua tất cả các hướng theo thứ tự ngẫu nhiên   
                for name, direction in shuffled_Directions:
                    if(Level[(pinky_y + direction[1] * (24 // Speed)) // Cell_Height][(pinky_x + direction[0] * (30 // Speed)) // Cell_Width] <= 2 
                            and (pinky_x + direction[0], pinky_y + direction[1]) not in visited_pink_Stack 
                            and (pinky_x + direction[0] * (30 // Speed), pinky_y + direction[1] * (24 // Speed)) != (blue_x, blue_y)
                            and (pinky_x + direction[0] * (30 // Speed), pinky_y + direction[1] * (24 // Speed)) != (orange_x, orange_y)
                            and (pinky_x + direction[0] * (30 // Speed), pinky_y + direction[1] * (24 // Speed)) != (blinky_x, blinky_y)):
                        nowDirections = direction
                        pinky_x += direction[0]
                        pinky_y += direction[1]
                        check_road = True
                        break
            if not check_road:
                pinky_state = 1
        else:
            # Nếu chưa đi qua, thêm ô vào danh sách đã đi qua
            visited_pink_Stack.add((pinky_x, pinky_y))
            # Thêm vào road_Stack để back-up
            road_Stack.append((pinky_x, pinky_y))

        # DFS
        if(pinky_state == 0):
            # Nếu Pinky đi đến ô Road có số >= 2
            if(Road[pinky_y // Cell_Height][pinky_x // Cell_Width] >= 2
                    and (pinky_x // Cell_Width) == (pinky_x / Cell_Width) 
                    and (pinky_y // Cell_Height) == (pinky_y / Cell_Height)):
                expanded_nodes += 1
                # Xáo trộn hướng đi cho DFS duyệt ngẫu nhiên
                random.shuffle(shuffled_Directions)          
                # Duyệt qua tất cả các hướng theo thứ tự ngẫu nhiên   
                for name, direction in shuffled_Directions:    
                    opposite = tuple(-d for d in direction)     
                    if((pinky_x + direction[0] * (30 // Speed), pinky_y + direction[1] * (24 // Speed)) == (blue_x, blue_y)
                            and (pinky_x + direction[0] * (30 // Speed), pinky_y + direction[1] * (24 // Speed)) == (orange_x, orange_y)
                            and (pinky_x + direction[0] * (30 // Speed), pinky_y + direction[1] * (24 // Speed)) == (blinky_x, blinky_y)):
                        pinky_state = 1
                    if(Level[(pinky_y + direction[1] * (24 // Speed)) // Cell_Height][(pinky_x + direction[0] * (30 // Speed)) // Cell_Width] <= 2
                            and (pinky_x + direction[0], pinky_y + direction[1]) not in visited_pink_Stack 
                            and nowDirections != opposite
                            and (pinky_x + direction[0] * (30 // Speed), pinky_y + direction[1] * (24 // Speed)) != (blue_x, blue_y)
                            and (pinky_x + direction[0] * (30 // Speed), pinky_y + direction[1] * (24 // Speed)) != (orange_x, orange_y)
                            and (pinky_x + direction[0] * (30 // Speed), pinky_y + direction[1] * (24 // Speed)) != (blinky_x, blinky_y)):
                        nowDirections = direction
                        pinky_x += direction[0]
                        pinky_y += direction[1]
                        pinky_state = 0
                        break
            # Nếu Pinky đi đến ô Road có số = 1
            elif(Road[(pinky_y) // Cell_Height][pinky_x // Cell_Width] == 1
                    and (pinky_x // Cell_Width) == (pinky_x / Cell_Width)
                    and (pinky_y // Cell_Height) == (pinky_y / Cell_Height)):
                if((pinky_x + nowDirections[0] * (30 // Speed), pinky_y + nowDirections[1] * (24 // Speed)) == (blue_x, blue_y)
                        and (pinky_x + nowDirections[0] * (30 // Speed), pinky_y + nowDirections[1] * (24 // Speed)) == (orange_x, orange_y)
                        and (pinky_x + nowDirections[0] * (30 // Speed), pinky_y + nowDirections[1] * (24 // Speed)) == (blinky_x, blinky_y)):
                    pinky_state = 1
                else:
                    pinky_x += nowDirections[0]
                    pinky_y += nowDirections[1]
            else:
                if((pinky_x + nowDirections[0], pinky_y + nowDirections[1]) != (blue_x, blue_y)
                        and (pinky_x + nowDirections[0] * (30 // Speed), pinky_y + nowDirections[1] * (24 // Speed)) != (orange_x, orange_y)
                        and (pinky_x + nowDirections[0] * (30 // Speed), pinky_y + nowDirections[1] * (24 // Speed)) != (blinky_x, blinky_y)):
                    pinky_x += nowDirections[0]
                    pinky_y += nowDirections[1]
                else:
                    pinky_state = 1
        # Back tracking
        if(pinky_state == 1):
            if len(road_Stack) > 0:
                pinky_x, pinky_y = road_Stack.pop()
            if len(road_Stack) == 0:
                visited_pink_Stack.clear()
                pinky_state = 0
                check_road = False
                gate_state = 0

        # Thiết lập lại trạng thái
        pinky_state = 0
        check_road = False

    # Vẽ Pinky
    draw_pinky(pinky_x, pinky_y, Cell_Width, Cell_Height)

# Hàm này để xem đường đi của Pinky
def Test_DFS():
    global road_Stack
    for(x, y) in road_Stack:
        pygame.draw.circle(Screen, 'pink', (x + 0.5 * Cell_Width, y + 0.5 * Cell_Height), 4)

# # # Biến cho Blue ---------------------------------------------------------------------------------------------------------------
#Vẽ Blue
def draw_blue(blue_x, blue_y, Cell_Width, Cell_Height):
    if blue_image:
        Screen.blit(blue_image, (blue_x, blue_y))
    else:
        pygame.draw.circle(Screen, Blue, blue_x, blue_y, 4)

#Vị trí ban đầu của Blue
blue_x = 390 + 30 * 3
blue_y = 360 
#bfs
global list_duongdi, blue_nowDirections, i, j, visited, x_temp, y_temp
list_duongdi = []
blue_nowDirections = (0, -2)
list_duongdi.append([((-2, 0), (450, 360))])  # tạo list 0
list_duongdi[0].append(((0, -2), (450, 288)))  # thêm vào list 0
i = 0
j = i 
visited = []
x_temp = 450
y_temp = 288

def bfs(Cell_Width, Cell_Height):
    global list_duongdi, blue_nowDirections, i, j, visited, x_temp, y_temp

    while(x_temp != (pacman_x ) or y_temp != (pacman_y) ):

        blue_nowDirections, x_temp, y_temp = list_duongdi[i][-1][0], list_duongdi[i][-1][1][0], list_duongdi[i][-1][1][1]
        opposite = tuple(-d for d in blue_nowDirections)
        if(Road[y_temp // Cell_Height][x_temp // Cell_Width] >= 1
            and x_temp // Cell_Width == x_temp / Cell_Width
            and y_temp // Cell_Height == y_temp / Cell_Height
            ):
            for direction in shuffled_Directions:
                blue_nowDirections, x_temp, y_temp = list_duongdi[i][-1][0], list_duongdi[i][-1][1][0], list_duongdi[i][-1][1][1]
                if(direction[1] == (-2, 0) and (x_temp, y_temp) == (0, 360) 
                    
                    ):
                    blue_nowDirections = direction[1]
                    x_temp = 870
                    y_temp = 360
                    visited.append((x_temp, y_temp))

                    j = j + 1
                    list_duongdi.append(copy.deepcopy(list_duongdi[i]))
                    list_duongdi[j].append((blue_nowDirections, (x_temp, y_temp)))

                    continue
                elif(direction[1] == (-2, 0) and (x_temp, y_temp) == (0, 360)
                    ):
                    continue
                if(direction[1] == (2, 0) and (x_temp, y_temp) == (870, 360) 
                    
                    ):
                    blue_nowDirections = direction[1]
                    x_temp = 0
                    y_temp = 360
                    visited.append((x_temp, y_temp))

                    j = j + 1
                    list_duongdi.append(copy.deepcopy(list_duongdi[i]))
                    list_duongdi[j].append((blue_nowDirections, (x_temp, y_temp)))
                    continue     
                elif(direction[1] == (2, 0) and (x_temp, y_temp) == (870, 360)
                     ):
                    continue
                if(direction[1] == (0, 2) and Level[(y_temp + direction[1][1] * 24 // 2) // Cell_Height][(x_temp + direction[1][0] * 30 // 2) // Cell_Width] == 9):
                    continue
                if(Level[(y_temp + direction[1][1] * 24 // 2) // Cell_Height][(x_temp + direction[1][0] * 30 // 2) // Cell_Width] <= 2
                    and ((x_temp + direction[1][0] * 30 // 2) > 0 
                         or (x_temp + direction[1][0] * 30 // 2 == 0 and y_temp + direction[1][1] * 24 // 2 == 360)
                         or (x_temp + direction[1][0] * 30 // 2 == 870 and y_temp + direction[1][1] * 24 // 2 == 360)
                         )
                    and (y_temp + direction[1][1] * 24 // 2) > 0
                    and direction[1] != opposite
                    ):
                    blue_nowDirections = direction[1]
                    x_temp += direction[1][0] * 30 // 2
                    y_temp += direction[1][1] * 24 // 2

                    visited.append((x_temp, y_temp))
                    
                    j = j + 1

                    list_duongdi.append(copy.deepcopy(list_duongdi[i]))
                    list_duongdi[j].append((blue_nowDirections, (x_temp, y_temp)))

                if(x_temp == pacman_x // Cell_Width * Cell_Width 
                   and y_temp == pacman_y // Cell_Height * Cell_Height ):
                    break
        if(x_temp == pacman_x // Cell_Width * Cell_Width
            and y_temp == pacman_y // Cell_Height * Cell_Height ):
            break
        i = i + 1 
 
# inky bfs
global k 
k = 0
def blue_bfs(Cell_Width, Cell_Height, list_duongdi):
    global blue_x, blue_y
    
    draw_blue(blue_x, blue_y, Cell_Width, Cell_Height)

    #bfs 
    global j, i, x_temp, y_temp  
    global k
    if(k <= len(list_duongdi[j]) - 1 ):

        blue_nowDirections1 = list_duongdi[j][k]

        if (
            (blue_x, blue_y) == (0, 360) 
            and blue_nowDirections1[0] == (-2, 0)
            and (pinky_x // Cell_Width, pinky_y // Cell_Height) != (870, 360)
            and (orange_x // Cell_Width, orange_y // Cell_Height) != (870, 360)
            and (blinky_x // Cell_Width, blinky_y // Cell_Height) != (870, 360)
        ):
            blue_x = 870
            blue_y = 360
            k += 1

        elif (
            (blue_x, blue_y) == (870, 360) 
            and blue_nowDirections1[0] == (2, 0)
            and (pinky_x // Cell_Width, pinky_y // Cell_Height) != (0, 360)
            and (orange_x // Cell_Width, orange_y // Cell_Height) != (0, 360)
            and (blinky_x // Cell_Width, blinky_y // Cell_Height) != (0, 360)
        ):
            blue_x = 0
            blue_y = 360
            k += 1

        elif (
            (blue_x + blue_nowDirections1[0][0]) // Cell_Width, (blue_y + blue_nowDirections1[0][1]) // Cell_Height
        ) != (pinky_x // Cell_Width, pinky_y // Cell_Height) and (
            (blue_x + blue_nowDirections1[0][0]) // Cell_Width, (blue_y + blue_nowDirections1[0][1]) // Cell_Height
        ) != (orange_x // Cell_Width, orange_y // Cell_Height) and (
            (blue_x + blue_nowDirections1[0][0]) // Cell_Width, (blue_y + blue_nowDirections1[0][1]) // Cell_Height
        ) != (blinky_x // Cell_Width, blinky_y // Cell_Height):
            
            blue_x += blue_nowDirections1[0][0]
            blue_y += blue_nowDirections1[0][1]

            if (blue_x, blue_y) == (list_duongdi[j][k][1][0], list_duongdi[j][k][1][1]):
                k += 1

        if( k == len(list_duongdi[j]) ):

            i = 0
            j = i
            k = 0
            list_duongdi.clear()
            list_duongdi.append([((0, 0), (blue_x, blue_y))])
            x_temp = blue_x
            y_temp = blue_y

            bfs(Cell_Width, Cell_Height)
           
# # # Biến cho Blinky -------------------------------------------------------------------------------------------------------------
blinky_x = 420
blinky_y = 360

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def is_walkable(x, y):
    if 0 <= y < len(boards) and 0 <= x < len(boards[0]):
        return boards[y][x] in [0, 1, 2] 
    return False

# Hàm A* để tìm đường đi:
def a_star(start, goal):
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            # reconstruct path
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path

        x, y = current
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            neighbor = (x + dx, y + dy)
            if not is_walkable(neighbor[0], neighbor[1]):
                continue

            tentative_g = g_score[current] + 1
            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + heuristic(neighbor, goal)
                heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return None

def pixel_to_cell(x, y):
    return (x // Cell_Width, y // Cell_Height)

def cell_to_pixel(cell_x, cell_y):
    return (cell_x * Cell_Width, cell_y * Cell_Height)

def astar_path(start_pixel, goal_pixel, Cell_Width, Cell_Height):
    start_cell = pixel_to_cell(start_pixel[0], start_pixel[1])
    goal_cell = pixel_to_cell(goal_pixel[0], goal_pixel[1])

    path_cells = a_star(start_cell, goal_cell)

    if path_cells:
        # Đổi các ô (cell) thành pixel
        path_pixels = [cell_to_pixel(x, y) for (x, y) in path_cells]
        return path_pixels
    else:
        return None
    
# Vẽ Blinky
def draw_blinky(blinky_x, blinky_y, Cell_Width, Cell_Height):
    if blinky_image:  
        Screen.blit(blinky_image, (blinky_x, blinky_y))
    else:
        pygame.draw.circle(Screen, Red, blinky_x, blinky_y, 4)

# Tốc độ Blinky mỗi frame (đi [Speed] pixel mỗi frame)
BLINKY_SPEED = Speed

last_pacman_pos = None
blinky_path = []
blinky_target_index = 0

def blinky_astar(Cell_Width, Cell_Height):
    global blinky_x, blinky_y, nowDirectionsBlinky, last_pacman_pos, blinky_path, blinky_target_index

    blinky_pos = (blinky_x, blinky_y)
    pacman_pos = (pacman_x, pacman_y)

    if (blinky_x >= 360 and blinky_x <= 510) and (blinky_y > 288 and blinky_y <= 384):
        nowDirectionsBlinky = Up
        blinky_x += nowDirectionsBlinky[0]
        blinky_y += nowDirectionsBlinky[1]
    else:
        # Nếu Pacman đổi vị trí hoặc đi hết đường
        if last_pacman_pos != pacman_pos or blinky_target_index >= len(blinky_path):
            path = astar_path(blinky_pos, pacman_pos, Cell_Width, Cell_Height)
            blinky_path = path if path else []
            blinky_target_index = 0
            last_pacman_pos = pacman_pos

        # Di chuyển theo từng bước pixel
        if blinky_target_index < len(blinky_path):
            target_x, target_y = blinky_path[blinky_target_index]

            # Chỉ đổi hướng khi Blinky đang ở chính giữa ô
            if blinky_x % Cell_Width == 0 and blinky_y % Cell_Height == 0:
                dx = target_x - blinky_x
                dy = target_y - blinky_y
                if dx > 0:
                    nowDirectionsBlinky = Right
                elif dx < 0:
                    nowDirectionsBlinky = Left
                elif dy > 0:
                    nowDirectionsBlinky = Down
                elif dy < 0:
                    nowDirectionsBlinky = Up

            # Di chuyển theo hướng hiện tại
            blinky_x += nowDirectionsBlinky[0]
            blinky_y += nowDirectionsBlinky[1]

            # Nếu đã đến vị trí mục tiêu thì chuyển sang mục tiêu tiếp theo
            if abs(blinky_x - target_x) < BLINKY_SPEED and abs(blinky_y - target_y) < BLINKY_SPEED:
                blinky_x = target_x
                blinky_y = target_y
                blinky_target_index += 1

    draw_blinky(blinky_x, blinky_y, Cell_Width, Cell_Height)


# # # Biến cho Orange -----------------------------------------------------------------------------------------------------------------
# Vị trí ban đầu của Orange
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
orange_delay_frames = 0  # 3 giây delay tại 60 FPS --> 180 frames

# Biến kiểm tra game đã bắt đầu hay chưa
global game_started
game_started = False

# Hàm lấy hướng ngược lại
def get_opposite_direction(direction):
    opposite = tuple(-d for d in direction)
    for name, dir in Directions.items():
        if dir == opposite:
            return dir
    return (0, 0)

# Hàm kiểm tra va chạm tường
def check_collision(next_x, next_y, exclude_self=True):
    global pinky_x, pinky_y, pacman_x, pacman_y, blue_x, blue_y, blinky_x, blinky_y, orange_x, orange_y
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
        (blinky_x, blinky_y),
        (orange_x, orange_y)
    ]
    for pos_x, pos_y in other_positions:
        if (next_x, next_y) == (pos_x, pos_y):
            if exclude_self and (next_x, next_y) == (orange_x, orange_y):
                continue
            return True
    return False

# Kiểm tra va chạm ma
def check_ghost_collision(next_x, next_y, self_x, self_y):
    global pinky_x, pinky_y, blue_x, blue_y, blinky_x, blinky_y, orange_x, orange_y
    next_tile = (int(next_y // Cell_Height), int(next_x // Cell_Width))
    self_tile = (int(self_y // Cell_Height), int(self_x // Cell_Width))

    ghost_tiles = [
        (int(pinky_y // Cell_Height), int(pinky_x // Cell_Width)),
        (int(blue_y // Cell_Height), int(blue_x // Cell_Width)),
        (int(blinky_y // Cell_Height), int(blinky_x // Cell_Width)),
        (int(orange_y // Cell_Height), int(orange_x // Cell_Width))
    ]

    for ghost_tile in ghost_tiles:
        if ghost_tile == next_tile and next_tile != self_tile:
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
                        if not check_collision(next_pixel_x, next_pixel_y) and not check_ghost_collision(next_pixel_x, next_pixel_y, orange_x, orange_y):

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
            # else:
            #     orange_path = []
            #     orange_target_pos = None 
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
                if not check_collision(next_x, next_y) and not check_ghost_collision(next_x, next_y, orange_x, orange_y):

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
             # No more path, but we still want Orange to keep chasing Pacman
                        recalculate_path = True
                    
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
                if not check_collision(next_x, next_y) and not check_ghost_collision(next_x, next_y, orange_x, orange_y):
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

# # # Biến cho Pacman ----------------------------------------------------------------------------
# Vị trí ban đầu của Pacman
global pacman_x, pacman_y, direction_command, new_direction_command, direction_type
pacman_x = 420
pacman_y = 576
# Hướng đi hiện tại của Pacman
direction_command = (0, 0)
# Hướng đi mới của Pacman - Sẽ thực thi khi đến ngã rẽ hoặc khi đi được hướng đi mới 
new_direction_command = (0, 0)
direction_type = -1

# Vẽ Pacman 
def draw_Pacman(Cell_Width, Cell_Height):
    global pacman_x, pacman_y, direction_command, new_direction_command, direction_type
    opposite = tuple(-d for d in direction_command)
    # Vị trí 2 đường thông nhau 
    if(((pacman_x, pacman_y) == (0, 360)) and direction_command == Left):
        pacman_x = 870
        pacman_y = 360
    elif(((pacman_x, pacman_y) == (870, 360)) and direction_command == Right):
        pacman_x = 0
        pacman_y = 360
    else:
        # Pacman đi đến ngã rẽ, kiểm tra có thể đi được không thì đi theo new_direction_command
        # Còn không sẽ đi tiếp hướng mặc định 
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
        # Pacman đi thẳng hoặc ngược lại 
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
    # Vẽ Pacman 
    if pacman_image:  
        Screen.blit(pacman_image,  (pacman_x, pacman_y))
    else:
        pygame.draw.circle(Screen, Yellow, (pacman_x, pacman_y), 4)

# Hàm để tính thời gian chạy và dung lượng bộ nhó sử dụng
def Calculate(target, Catched):
    global orange_x, orange_y, pinky_x, pinky_y, blinky_x, blinky_y, blue_x, blue_y, expanded_nodes
    if(target == 'Pink'):
        orange_x = 0
        orange_y = 0
        blinky_x = 0
        blinky_y = 0
        blue_x = 0
        blue_y = 0
    elif(target == 'Orange'):
        pinky_x = 0
        pinky_y = 0
        blinky_x = 0
        blinky_y = 0
        blue_x = 0
        blue_y = 0
    elif(target == 'Red'):
        orange_x = 0
        orange_y = 0
        pinky_x = 0
        pinky_y = 0
        blue_x = 0
        blue_y = 0
    elif(target == 'Blue'):
        orange_x = 0
        orange_y = 0
        pinky_x = 0
        pinky_y = 0
        blinky_x = 0
        blinky_y = 0
    if(Catched == True):
        end = time.time()
        print(f"Thời gian chạy: {end - start:.4f} giây")
        current, peak = tracemalloc.get_traced_memory()
        print(f"[Tracemalloc] Đang dùng: {current/1024**2:.2f} MB, Đỉnh: {peak/1024**2:.2f} MB")
        print(f"Số lượng ô đã đi qua: {expanded_nodes}")
        return False

# Gán key tương ứng với hướng
key_to_direction = {
    pygame.K_RIGHT: 0,
    pygame.K_d: 0,
    pygame.K_LEFT: 1,
    pygame.K_a: 1,
    pygame.K_UP: 2,
    pygame.K_w: 2,
    pygame.K_DOWN: 3,
    pygame.K_s: 3,
}

run = True
Catched = False
start = time.time()
game_started = True

# Biến hỗ trợ Blue   
global only1
only1 = 0

while run:
    Timer.tick(FPS)
    # Vẽ bản đồ
    Screen.fill((0, 0, 0))  # Vẽ lại nền đen

    # run = Calculate('Pink', Catched)

    if Catched:
        draw_game_over()
    else:
        draw_map()
        draw_instructions()

        # Vẽ Pinky
        pinky_dfs(Cell_Width, Cell_Height)

        # Vẽ Orange
        update_orange_movement()
        draw_orange(orange_x, orange_y, Cell_Width, Cell_Height)

        pinky_x = int(pinky_x)
        pinky_y = int(pinky_y)
        orange_x = int(orange_x)
        orange_y = int(orange_y)

        pinky_tile = (pinky_x // Cell_Width, pinky_y // Cell_Height)
        orange_tile = (orange_x // Cell_Width, orange_y // Cell_Height)

        dx = abs(pinky_tile[0] - orange_tile[0])
        dy = abs(pinky_tile[1] - orange_tile[1])

        if (dx + dy == 1) and gate_state == 1 and orange_gate_state == 1:
            prev_pinky_direction = nowDirections
            nowDirections = get_opposite_direction(nowDirections)
    
            # Move Pinky if new direction is safe
            new_pinky_x = pinky_x + nowDirections[0]
            new_pinky_y = pinky_y + nowDirections[1]

            # Convert to tile coords
            tile_col = new_pinky_x // Cell_Width
            tile_row = new_pinky_y // Cell_Height
            if (0 <= tile_col < Num_Cols and 0 <= tile_row < Num_Rows and 
        (Level[tile_row][tile_col] <= 2 or Level[tile_row][tile_col] == 9)):
                
                if not check_ghost_collision(new_pinky_x, new_pinky_y, pinky_x, pinky_y):
                    visited_pink_Stack.clear()
                    pinky_x = new_pinky_x
                    pinky_y = new_pinky_y
            else:
        # If invalid direction, pick random legal direction if needed
                nowDirections = (0, 0)        

        # Move Orange depending on its current direction state
            if orange_directions != (0, 0):
                new_orange_dir = get_opposite_direction(orange_directions)
                new_orange_x = orange_x + new_orange_dir[0]
                new_orange_y = orange_y + new_orange_dir[1]
                if not check_ghost_collision(new_orange_x, new_orange_y, orange_x, orange_y):
                    orange_directions = new_orange_dir
                    orange_x = new_orange_x
                    orange_y = new_orange_y
            else:
                orange_path = []
                orange_target_pos = None
                new_orange_dir = get_opposite_direction(prev_pinky_direction)
                new_orange_x = orange_x + new_orange_dir[0]
                new_orange_y = orange_y + new_orange_dir[1]
                if not check_ghost_collision(new_orange_x, new_orange_y, orange_x, orange_y):
                    orange_directions = new_orange_dir
                    orange_x = new_orange_x
                    orange_y = new_orange_y
                else:
                    orange_directions = (0, 0)

        # Vẽ Blinky
        blinky_astar(Cell_Width, Cell_Height)
        
        # #Vẽ Blue
        if(only1 == 0):
            bfs(Cell_Width, Cell_Height)
            only1 = 1
        blue_bfs(Cell_Width, Cell_Height, list_duongdi)

        # Bắt nhau trường hợp cách nhau 0 đơn vị Speed
        if(pacman_x == pinky_x and pacman_y == pinky_y):
            Catched = True
        elif(pacman_x == orange_x and pacman_y == orange_y):
            Catched = True
        elif(pacman_x == blinky_x and pacman_y == blinky_y):
            Catched = True
        elif(pacman_x == blue_x and pacman_y == blue_y):
            Catched = True

        # Vẽ Pacman
        draw_Pacman(Cell_Width, Cell_Height)

        # Bắt nhau trường hợp cách nhau 1 đơn vị Speed
        if(pacman_x == pinky_x and pacman_y == pinky_y):
            Catched = True
        elif(pacman_x == orange_x and pacman_y == orange_y):
            Catched = True
        elif(pacman_x == blinky_x and pacman_y == blinky_y):
            Catched = True
        elif(pacman_x == blue_x and pacman_y == blue_y):
            Catched = True

    # Check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        # Kiểm tra nhấn phím
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                direction_type = 4
            if event.key in key_to_direction:
                direction_type = key_to_direction[event.key]
        if event.type == pygame.KEYUP:
            if event.key in key_to_direction and direction_type == key_to_direction[event.key]:
                if direction_type == 0:
                    new_direction_command = Right
                elif direction_type == 1:
                    new_direction_command = Left
                elif direction_type == 2:
                    new_direction_command = Up
                elif direction_type == 3:
                    new_direction_command = Down
            if event.key == pygame.K_SPACE and direction_type == 4:
                Catched = False
                # Pinky
                pinky_x = 390
                pinky_y = 360
                chosen_direction = random.choice(["Right", "Left"])
                nowDirections = (0, 0)
                visited_pink_Stack.clear()
                road_Stack.clear()
                pinky_state = 0             
                gate_state = 0              
                check_road = False          
                # Orange
                orange_x = 450
                orange_y = 360
                orange_path.clear()
                orange_target_pos = None
                last_path_calc_time = 0
                orange_gate_state = 0
                orange_directions = Up
                orange_stuck_counter = 0
                orange_delay_frames = 0
                # Blue
                blue_x = 390 + 30 * 3
                blue_y = 360 
                list_duongdi.clear()
                blue_nowDirections = (0, -1 * Speed)  # Trạng thái ban đầu chưa có hướng đi
                list_duongdi.append([((-1 * Speed, 0), (450, 360))])  # tạo list 0
                list_duongdi[0].append(((0, -1 * Speed), (450, 288)))  # thêm vào list 0
                i = 0
                j = i 
                visited.clear()
                visited.append((blue_x, blue_y))
                x_temp = 450
                y_temp = 288
                k = 0
                # Blinky
                blinky_x = 420
                blinky_y = 360
                blinky_path.clear()
                nowDirectionsBlinky = (0, 0)
                # Pacman
                pacman_x = 420 
                pacman_y = 576
                direction_command = (0, 0)
                new_direction_command = (0, 0)
                direction_type = -1

    pygame.display.flip()   # Tải lại hiệu ứng mới

pygame.quit()
tracemalloc.stop()