# Code Pacman Br BR bR
import pygame
import threading
import copy
from Board import boards
import pygame
import math

pygame.init()

# Cấu hình màn hình
Width = 900
Height = 800
Level = copy.deepcopy(boards)
Flicker = False
PI = math.pi

# Hướng đi
Up = (1, 0) 
Down = (-1, 0)
Left = (-1, 0)
Right = (0, 1)

# Kichs thước ô
Cell_Height = ((Height - 50) // 32)
Cell_Width = (Width // 30)

# Load ảnh
pinky_image = pygame.image.load("Pinky.png")  # Đường dẫn đến ảnh Pinky
pinky_image = pygame.transform.scale(pinky_image, (Cell_Width, Cell_Height))  # Resize ảnh

# Vị trí ban đầu của Pinky
pinky_x = 13
pinky_y = 15

# Khung và Tiêu đề
Screen = pygame.display.set_mode((Width, Height))
pygame.display.set_caption("Pacman")

# Khung hình
FPS = 60
Timer = pygame.time.Clock()
Font = pygame.font.SysFont("Arial", 30)

# Blues
Black = (0, 0, 0)
White = (255, 255, 255)
Pink = (255, 192, 203)
Yellow = (255, 255, 0)
Blue = (0, 0, 255)

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

# Vẽ Pinky
def draw_pinky(pinky_x=pinky_x, pinky_y=pinky_y, Cell_Width=Cell_Width, Cell_Height=Cell_Height):
    if pinky_image:  
        Screen.blit(
            pinky_image, 
            (pinky_x * Cell_Width + (Cell_Width - pinky_image.get_width()) // 2, 
            pinky_y * Cell_Height + (Cell_Height - pinky_image.get_height()) // 2)
        )
    else:
        pygame.draw.circle(Screen, Pink, (pinky_x + Cell_Width // 2, pinky_y + Cell_Height // 2), 4)

run = True
while run:
    Timer.tick(FPS)

    # Vẽ bản đồ
    draw_map()
    # Vẽ Pinky
    draw_pinky(pinky_x=pinky_x, pinky_y=pinky_y)
    # Check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False



    # Update the display
    pygame.display.flip()
pygame.quit()