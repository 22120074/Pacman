# Code Pacman Br BR bR
import pygame
import threading
import copy
from Board import boards
from Board import road
import pygame
import math
import random

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
Cell_Height = ((Height - 50) // 32) # 24 pixel
Cell_Width = (Width // 30)          # 30 pixel

# Load ảnh
pinky_image = pygame.image.load("Pinky.png")  # Đường dẫn đến ảnh Pinky
pinky_image = pygame.transform.scale(pinky_image, (Cell_Width, Cell_Height))  # Resize ảnh



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

# Hàm hiển thị dòng chữ Game Over
def draw_game_over():
    # Khởi tạo font (None = dùng font mặc định, 80 là cỡ chữ)
    font = pygame.font.Font(None, 80)

    # Render chữ ra một surface
    text_surface = font.render("GAME OVER", True, Red)

    # Lấy vị trí để căn giữa
    text_rect = text_surface.get_rect(center=(Width // 2, Height // 2))

    # Vẽ lên màn hình
    Screen.blit(text_surface, text_rect)

# Hàm vẽ bản đồ
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

# Vẽ Pinky
def draw_pinky(pinky_x, pinky_y, Cell_Width, Cell_Height):
    if pinky_image:  
        Screen.blit(pinky_image, (pinky_x, pinky_y))
    else:
        pygame.draw.circle(Screen, Pink, pinky_x, pinky_y, 4)


# # # Biến cho Ghost khác -----------------------------------------------------------------------
global blue_x, blue_y, orange_x, orange_y, red_x, red_y
blue_x = 0
blue_y = 0
orange_x = 0
orange_y = 0
red_x = 0
red_y = 0
# # # Biến cho Pinky ----------------------------------------------------------------------------
global pinky_x, pinky_y, nowDirections, shuffled_Directions, visited_pink_Stack, chosen_direction
global road_Stack, pinky_state, check_road, gate_state
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

# Pinky - DFS
def pinky_dfs(Cell_Width, Cell_Height):
    global pinky_x, pinky_y, nowDirections, shuffled_Directions, visited_pink_Stack
    global road_Stack, pinky_state, check_road, chosen_direction, gate_state
    # Vẽ Pinky
    draw_pinky(pinky_x, pinky_y, Cell_Width, Cell_Height)
    # Nếu đang ở trong lồng, ta đi ra khỏi lồng rồi bắt Pacman
    if((pinky_x >= 360 and pinky_x <= 510) and (pinky_y > 288 and pinky_y <= 384)):
        # Trạng thái ban đầu chưa có hướng đi
        if(nowDirections == (0, 0)):
            nowDirections = Right
            if((pinky_x + nowDirections[0], pinky_y + nowDirections[1]) != (blue_x, blue_y)
                        and (pinky_x + nowDirections[0], pinky_y + nowDirections[1]) != (orange_x, orange_y)
                        and (pinky_x + nowDirections[0], pinky_y + nowDirections[1]) != (red_x, red_y)):
                pinky_x += nowDirections[0]
                pinky_y += nowDirections[1]
        # Đang ở trong lồng, đi ra ngoài
        else:
            if(((pinky_x, pinky_y) == (420, 360)) or ((pinky_x, pinky_y) == (420, 336)) or ((pinky_x, pinky_y) == (420, 384)) 
                    or ((pinky_x, pinky_y) == (450, 360)) or ((pinky_x, pinky_y) == (450, 336)) or ((pinky_x, pinky_y) == (450, 384))
                    or ((pinky_x, pinky_y) == (420, 312)) or ((pinky_x, pinky_y) == (450, 312))):
                nowDirections = Up
                if((pinky_x + nowDirections[0], pinky_y + nowDirections[1]) != (blue_x, blue_y)
                        and (pinky_x + nowDirections[0], pinky_y + nowDirections[1]) != (orange_x, orange_y)
                        and (pinky_x + nowDirections[0], pinky_y + nowDirections[1]) != (red_x, red_y)):
                    pinky_x += nowDirections[0]
                    pinky_y += nowDirections[1]
            else:
                if((pinky_x + nowDirections[0], pinky_y + nowDirections[1]) != (blue_x, blue_y)
                        and (pinky_x + nowDirections[0], pinky_y + nowDirections[1]) != (orange_x, orange_y)
                        and (pinky_x + nowDirections[0], pinky_y + nowDirections[1]) != (red_x, red_y)):
                    pinky_x += nowDirections[0]
                    pinky_y += nowDirections[1]
    # Sau khi bước qua cổng lồng thì quẹo trái hoặc phải
    elif(((pinky_x, pinky_y) == (420, 288) or (pinky_x, pinky_y) == (450, 288)) and gate_state == 0):
        chosen_direction = random.choice(["Right", "Left"])
        nowDirections = Directions[chosen_direction]
        gate_state = 1
        if((pinky_x + nowDirections[0], pinky_y + nowDirections[1]) != (blue_x, blue_y)
                and (pinky_x + nowDirections[0], pinky_y + nowDirections[1]) != (orange_x, orange_y)
                and (pinky_x + nowDirections[0], pinky_y + nowDirections[1]) != (red_x, red_y)):
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
                    opposite = tuple(-d for d in direction)     
                    if(Level[(pinky_y + direction[1] * (24 // Speed)) // Cell_Height][(pinky_x + direction[0] * (30 // Speed)) // Cell_Width] <= 2 
                            and (pinky_x + direction[0], pinky_y + direction[1]) not in visited_pink_Stack 
                            and nowDirections != opposite
                            and (pinky_x + direction[0], pinky_y + direction[1]) != (blue_x, blue_y)
                            and (pinky_x + direction[0], pinky_y + direction[1]) != (orange_x, orange_y)
                            and (pinky_x + direction[0], pinky_y + direction[1]) != (red_x, red_y)):
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

        # # Nếu chưa có hướng đi nhất định, chọn ngẫu nhiên một hướng đi, này dành cho th ở bên ngoài lồng
        # if(nowDirections == (0, 0)):
        #     # Xáo trộn hướng đi cho DFS duyệt ngẫu nhiên
        #     random.shuffle(shuffled_Directions)          
        #     # Duyệt qua tất cả các hướng theo thứ tự ngẫu nhiên   
        #     for name, direction in shuffled_Directions:     
        #         if(Level[(pinky_y + direction[1] * (24 // Speed)) // Cell_Height][(pinky_x + direction[0] * (30 // Speed)) // Cell_Width] <= 2):
        #             nowDirections = direction
        #             pinky_x += direction[0]
        #             pinky_y += direction[1]
        #             break            

        # DFS
        if(pinky_state == 0):
            # Nếu Pinky đi đến ô Road có số >= 2
            if(Road[pinky_y // Cell_Height][pinky_x // Cell_Width] >= 2
                    and (pinky_x // Cell_Width) == (pinky_x / Cell_Width) 
                    and (pinky_y // Cell_Height) == (pinky_y / Cell_Height)):
                # Xáo trộn hướng đi cho DFS duyệt ngẫu nhiên
                random.shuffle(shuffled_Directions)          
                # Duyệt qua tất cả các hướng theo thứ tự ngẫu nhiên   
                for name, direction in shuffled_Directions:    
                    opposite = tuple(-d for d in direction)     
                    if(Level[(pinky_y + direction[1] * (24 // Speed)) // Cell_Height][(pinky_x + direction[0] * (30 // Speed)) // Cell_Width] <= 2
                            and (pinky_x + direction[0], pinky_y + direction[1]) not in visited_pink_Stack 
                            and nowDirections != opposite
                            and (pinky_x + direction[0], pinky_y + direction[1]) != (blue_x, blue_y)
                            and (pinky_x + direction[0], pinky_y + direction[1]) != (orange_x, orange_y)
                            and (pinky_x + direction[0], pinky_y + direction[1]) != (red_x, red_y)):
                        nowDirections = direction
                        pinky_x += direction[0]
                        pinky_y += direction[1]
                        break
            # Nếu Pinky đi đến ô Road có số = 1
            elif(Road[(pinky_y) // Cell_Height][pinky_x // Cell_Width] == 1
                    and (pinky_x // Cell_Width) == (pinky_x / Cell_Width)
                    and (pinky_y // Cell_Height) == (pinky_y / Cell_Height)
                    and (pinky_x + nowDirections[0], pinky_y + nowDirections[1]) != (blue_x, blue_y)
                    and (pinky_x + nowDirections[0], pinky_y + nowDirections[1]) != (orange_x, orange_y)
                    and (pinky_x + nowDirections[0], pinky_y + nowDirections[1]) != (red_x, red_y)):
                pinky_x += nowDirections[0]
                pinky_y += nowDirections[1]
            else:
                if((pinky_x + nowDirections[0], pinky_y + nowDirections[1]) != (blue_x, blue_y)
                        and (pinky_x + nowDirections[0], pinky_y + nowDirections[1]) != (orange_x, orange_y)
                        and (pinky_x + nowDirections[0], pinky_y + nowDirections[1]) != (red_x, red_y)):
                    pinky_x += nowDirections[0]
                    pinky_y += nowDirections[1]
        # Back tracking
        elif(pinky_state == 1):
            if len(road_Stack) > 0:
                pinky_x, pinky_y = road_Stack.pop()
            if(len(road_Stack) == 0):
                visited_pink_Stack.clear()
                pinky_state = 0
                check_road = False
                gate_state = 0
                print(1)

        # Thiết lập lại trạng thái
        pinky_state = 0
        check_road = False 
#Load anh Blue
blue_image = pygame.image.load("Blue.png")
blue_image = pygame.transform.scale(blue_image, (Cell_Width, Cell_Height))

#Vẽ Blue
def draw_blue(blue_x, blue_y, Cell_Width, Cell_Height):
    if blue_image:
        Screen.blit(blue_image, (blue_x, blue_y))
    else:
        pygame.draw.circle(Screen, Blue, blue_x, blue_y, 4)

#Vị trí ban đầu của Blue
blue_x = 390 + 30
blue_y = 360 
#bfs
global list_duongdi, blue_nowDirections, i, j, visited, x_temp, y_temp
list_duongdi = []
blue_nowDirections = (0, 0)
list_duongdi.append([((0, - 2), (blue_x, 288))])
i = 0
j = i 
visited = []
visited.append((blue_x, blue_y))
x_temp = 420
y_temp = 288

def bfs(Cell_Width, Cell_Height):
    global list_duongdi, blue_nowDirections, i, j, visited, x_temp, y_temp



    while(x_temp != pacman_x or y_temp != pacman_y):
        blue_nowDirections, x_temp, y_temp = list_duongdi[i][-1][0], list_duongdi[i][-1][1][0], list_duongdi[i][-1][1][1]
        opposite = tuple(-d for d in blue_nowDirections)
        if(Road[y_temp // Cell_Height][x_temp // Cell_Width] >= 1
            and x_temp // Cell_Width == x_temp / Cell_Width
            and y_temp // Cell_Height == y_temp / Cell_Height
            ):
            for direction in shuffled_Directions:
                blue_nowDirections, x_temp, y_temp = list_duongdi[i][-1][0], list_duongdi[i][-1][1][0], list_duongdi[i][-1][1][1]
                if(direction[0] == "Left" and (x_temp, y_temp) == (0, 360) 
                    and (870, 360) not in visited
                    ):
                    blue_nowDirections = direction[1]
                    x_temp = 870
                    y_temp = 360
                    visited.append((x_temp, y_temp))

                    j = j + 1
                    list_duongdi.append(copy.deepcopy(list_duongdi[i]))
                    list_duongdi[j].append((blue_nowDirections, (x_temp, y_temp)))

                    continue
                elif(direction[0] == "Left" and (x_temp, y_temp) == (0, 360)
                     and (870, 360) in visited):
                    continue
                if(direction[0] == "Right" and (x_temp, y_temp) == (870, 360) 
                    and (0, 360) not in visited
                    ):
                    blue_nowDirections = direction[1]
                    x_temp = 0
                    y_temp = 360
                    visited.append((x_temp, y_temp))

                    j = j + 1
                    list_duongdi.append(copy.deepcopy(list_duongdi[i]))
                    list_duongdi[j].append((blue_nowDirections, (x_temp, y_temp)))
                    continue     
                elif(direction[0] == "Right" and (x_temp, y_temp) == (870, 360)
                     and (0, 360) in visited):
                    continue
                if(direction[0] == "Down" and Level[(y_temp + direction[1][1] * 24 // 2) // Cell_Height][(x_temp + direction[1][0] * 30 // 2) // Cell_Width] == 9):
                    continue
                if(Level[(y_temp + direction[1][1] * 24 // 2) // Cell_Height][(x_temp + direction[1][0] * 30 // 2) // Cell_Width] <= 2
                    and (x_temp + direction[1][0] * 30 // 2, y_temp + direction[1][1] * 24 // 2) not in visited 
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

                if(x_temp == pacman_x and y_temp == pacman_y):
                    print("Pacman caught")
                    break
        if(x_temp == pacman_x and y_temp == pacman_y):
            print("Pacman caught")
            break
        i = i + 1 
 
# inky bfs
global k 
k = 1
def inky_bfs(Cell_Width, Cell_Height, list_duongdi):
    global blue_x, blue_y
    blue_nowDirections = (0, 0)
    
    draw_blue(blue_x, blue_y, Cell_Width, Cell_Height)

    while((blue_x >= 360 and blue_x <= 510) and (blue_y > 288 and blue_y <= 384)):
        # Trạng thái ban đầu chưa có hướng đi
        if(blue_nowDirections == (0, 0)):
            blue_nowDirections = Up
            if((blue_x + blue_nowDirections[0], blue_y + blue_nowDirections[1]) != (pinky_x, pinky_y)
                        and (blue_x + blue_nowDirections[0], blue_y + blue_nowDirections[1]) != (orange_x, orange_y)
                        and (blue_x + blue_nowDirections[0], blue_y + blue_nowDirections[1]) != (red_x, red_y)):
                # print("Hello world")
                blue_x += blue_nowDirections[0]
                blue_y += blue_nowDirections[1]
        # Đang ở trong lồng, đi ra ngoài
        else:
            if(((blue_x, blue_y) == (420, 384)) or ((blue_x, blue_y) == (420, 360)) or ((blue_x, blue_y) == (420, 336)) 
                    or ((blue_x, blue_y) == (450, 384)) or ((blue_x, blue_y) == (450, 360)) or ((blue_x, blue_y) == (450, 336))
                    or ((blue_x, blue_y) == (420, 312)) or ((blue_x, blue_y) == (450, 312))):
                # print("blue_x: ", blue_x, "blue_y: ", blue_y)
                blue_nowDirections = Up
                if((blue_x + blue_nowDirections[0], blue_y + blue_nowDirections[1]) != (pinky_x, pinky_y)
                        and (blue_x + blue_nowDirections[0], blue_y + blue_nowDirections[1]) != (orange_x, orange_y)
                        and (blue_x + blue_nowDirections[0], blue_y + blue_nowDirections[1]) != (red_x, red_y)):
                    blue_x += blue_nowDirections[0]
                    blue_y += blue_nowDirections[1]
                    # print("blue_x: ", blue_x, "blue_y: ", blue_y)
            else:
                if((blue_x + blue_nowDirections[0], blue_y + blue_nowDirections[1]) != (pinky_x, pinky_y)
                        and (blue_x + blue_nowDirections[0], blue_y + blue_nowDirections[1]) != (orange_x, orange_y)
                        and (blue_x + blue_nowDirections[0], blue_y + blue_nowDirections[1]) != (red_x, red_y)):
                    blue_x += blue_nowDirections[0]
                    blue_y += blue_nowDirections[1]


    #bfs 
    global j  
    global k
    if(k <= len(list_duongdi[j]) - 1 ):


        blue_nowDirections1 = list_duongdi[j][k]

        if (blue_x, blue_y) == (0, 360) and blue_nowDirections1[0] == (-2, 0):
            blue_x = 870
            blue_y = 360
            k += 1
        elif(blue_x, blue_y) == (870, 360) and blue_nowDirections1[0] == (2, 0):
            blue_x = 0
            blue_y = 360
            k += 1
        else:
            blue_x += blue_nowDirections1[0][0]
            blue_y += blue_nowDirections1[0][1]

            if( (blue_x, blue_y) == (list_duongdi[j][k][1][0], list_duongdi[j][k][1][1])):
                k += 1
    



# # # # Biến cho Pacman ----------------------------------------------------------------------------
# Vị trí ban đầu của Pacman
global pacman_x, pacman_y, direction_command, new_direction_command, direction_type
pacman_x = 660 + 5 * 30 - 25 * 30
pacman_y = 360 + 24 * 15
# Hướng đi hiện tại của Pacman
direction_command = (0, 0)
new_direction_command = (0, 0)
direction_type = 0
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
            pacman_x += direction_command[0]
            pacman_y += direction_command[1]
    if pacman_image:  
        Screen.blit(pacman_image,  (pacman_x, pacman_y))
    else:
        pygame.draw.circle(Screen, Yellow, (pacman_x, pacman_y), 4)
    
run = True
Catched = False
global old_pacman_post
old_pacman_post = (pacman_x, pacman_y)  
global only1
only1 = 0
while run:
    Timer.tick(FPS)
    # Vẽ bản đồ
    Screen.fill((0, 0, 0))  # Vẽ lại nền đen
    if not Catched:
        draw_map()
        # # Vẽ Pinky
        pinky_dfs(Cell_Width, Cell_Height)

        

        # #Vẽ Inky
        inky_bfs(Cell_Width, Cell_Height, list_duongdi)
        # Vẽ Pacman
        draw_Pacman(Cell_Width, Cell_Height)
        if(only1 == 0):
            bfs(Cell_Width, Cell_Height)
            only1 = 1

        # if(old_pacman_post != (pacman_x, pacman_y)):
        #     pacman_x = pacman_x // Cell_Width
        #     pacman_y = pacman_y // Cell_Height
        #     list_duongdi.clear()
        #     i = 0
        #     j = i
        #     visited.clear()
        #     visited.append((pacman_x, pacman_y))
        #     x_temp = pacman_x
        #     y_temp = pacman_y
        #     list_duongdi.append([((0, - 2), (pacman_x, pacman_y))])
        #     bfs(Cell_Width, Cell_Height)
        # old_pacman_post = (pacman_x, pacman_y)
    else:
        draw_game_over()
    # Check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        # Kiểm tra nhấn phím
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                direction_type = 0
            if event.key == pygame.K_LEFT:
                direction_type = 1
            if event.key == pygame.K_UP:
                direction_type = 2
            if event.key == pygame.K_DOWN:
                direction_type = 3
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT and direction_type == 0:
                new_direction_command = Right   
            if event.key == pygame.K_LEFT and direction_type == 1:
                new_direction_command = Left
            if event.key == pygame.K_UP and direction_type == 2:
                new_direction_command = Up
            if event.key == pygame.K_DOWN and direction_type == 3:
                new_direction_command = Down

    if(pacman_x == pinky_x and pacman_y == pinky_y):
        Catched = True
    
    if(pacman_x == blue_x and pacman_y == blue_y):
        Catched = True
    # pygame.time.delay(100)  # Delay để dễ dàng xem chuyển động
    pygame.display.flip()   # Tải lại hiệu ứng mới

pygame.quit()