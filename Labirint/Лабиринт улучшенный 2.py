import pygame
from copy import *
pygame.init()
size = (601, 601)
size_for_end = (300, 300)
screen = pygame.display.set_mode(size)

font = pygame.font.SysFont("Arial", 30)
buttons_names = pygame.font.SysFont("Arial", 17)
results_name = pygame.font.SysFont("Arial", 30, italic=True)
rules_name = pygame.font.SysFont("Arial", 15, italic=True)

distance = 1
count = 0
end = False
s1 = 0
s2 = 0
f1 = 0
f2 = 0
way = []
a = [[0 for i in range(12)] for j in range(12)]
check_countless = [[0 for i in range(12)] for j in range(12)]

red = (255, 0, 0)
white = (255, 255, 255)
green = (50, 205, 50)
violet = (138, 43, 226)
black = (0, 0, 0)
lime = (0, 255, 0)
blue = (0, 255, 255)
green_yellow = (173, 255, 47)
pink = (255, 20, 147)
orange = (255, 127, 80)
dark_red = (220, 20, 60)
lavander = (230, 230, 250)

happy_smile_dowland = pygame.image.load('Счастливый смайл.png').convert_alpha()
sad_smile_dowland = pygame.image.load('Грустный смайл.png').convert_alpha()
happy_smile = pygame.transform.scale(happy_smile_dowland, (50, 50))
sad_smile = pygame.transform.scale(sad_smile_dowland, (50, 50))


def clean():
    global a
    global distance
    global count
    global f1
    global f2
    global s1
    global s2
    f1 = 0
    s1 = 0
    f2 = 0
    s2 = 0
    count = 0
    distance = 0
    a = [[0 for i in range(12)] for j in range(12)]
    screen.fill(violet)
    pygame.draw.rect(screen, white, (50, 50, 500, 500), 0)
    pygame.draw.rect(screen, red, (551, 0, 49, 51), 0)
    pygame.draw.rect(screen, lime, (551, 50, 49, 51), 0)
    cleaner = buttons_names.render("Clean", True, black)
    screen.blit(cleaner, [551, 20])
    start_program = buttons_names.render("Start", True, black)
    screen.blit(start_program, [551, 73])
    for i in range(0, 601, 50):
        if i < 550:
            text = font.render(str(i // 50), True, black)
            screen.blit(text, [i + 10, 10])
            screen.blit(text, [10, i + 10])
        pygame.draw.line(screen, black, (0, i), (600, i), 2)
        pygame.draw.line(screen, black, (i, 0), (i, 600), 2)
    pygame.draw.rect(screen, lavander, (2, 552, 597, 48), 0)
    first_rule = rules_name.render('Чтобы построить стену, нажмите левую кнопку мыши.', True, black)
    second_rule = rules_name.render('Чтобы обозначить начало или конец, нажмите правую кнопку мыши.', True, black)
    screen.blit(first_rule, [80, 555])
    screen.blit(second_rule, [10, 575])


def start(s1, s2, f1, f2):
    global a
    global distance
    way = []
    x_start = f1
    y_start = f2
    count_countless = 0
    distance = 1
    if s1 == 0 and s2 == 0 or f1 == 0 and f2 == 0:
        quit()
    else:
        first_step(s1, s2)
        while a[f1][f2] == -3 and count_countless < 144:      
            count_countless += 1
            trace(s1, s2)                
            distance += 1
        if count_countless == 144:        
            bad_end()
        else:
            while (x_start != s1 or y_start != s2):
                answer = finish(x_start, y_start, s1, s2)
                way.append(answer)
                x_start = answer[0]
                y_start = answer[1]
            for ix in range(len(way) - 1):
                paint(way[ix][0], way[ix][1])
            happy_end()
            
            
def checkCell(x1, x2):
    global a

    if 0 < x1 < 11 and 0 < x2 < 11: 
        if a[x1][x2] == 0 or a[x1][x2] < -1:
            return True
        else:
            return False


def checkCell2(x, y):
    global a
    if 0 < x < 11 and 0 < y < 11: 
        if a[x][y] != -1 or a[x][y] < -1:
            return True
    return False


def mark(x, y):
    global check_countless
    check_countless[x][y] = 1


def paint(x, y):
    if 0 < x < 11 and 0 < y < 11:
        pygame.draw.rect(screen, orange, (x * 50 + 1, y * 50 + 1, 49, 49), 0)


def trace(s1, s2):
    global a
    global distance
    global previous_countless
    global now_countless
    global check_countless
    x = []
    for i in range(1, 11):
        for j in range(1, 11):
            if a[i][j] == distance:               
                if a[i - 1][j] == 0 or a[i - 1][j] == -3:
                    x.append([i - 1, j])
                if a[i + 1][j] == 0 or a[i + 1][j] == -3:
                    x.append([i + 1, j])
                if a[i][j + 1] == 0 or a[i][j + 1] == -3:
                    x.append([i, j + 1])
                if a[i][j - 1] == 0 or a[i][j - 1] == -3:
                    x.append([i, j - 1])
    for n in range(len(x)):
        a[x[n][0]][x[n][1]] = distance + 1


def first_step(s1, s2):
    global a
    if a[s1 - 1][s2] == 0 or a[s1 - 1][s2] == -3:
        a[s1 - 1][s2] = 1
    if a[s1 + 1][s2] == 0 or a[s1 + 1][s2] == -3:
        a[s1 + 1][s2] = 1
    if a[s1][s2 - 1] == 0 or a[s1][s2 - 1] == -3:
        a[s1][s2 - 1] = 1   
    if a[s1][s2 + 1] == 0 or a[s1][s2 + 1] == -3:
        a[s1][s2 + 1] = 1      


def finish(x, y, s1, s2):
    global a
    cells_around = cell_around(x, y)
    a1 = cells_around[0]
    a2 = cells_around[1]
    a3 = cells_around[2]
    a4 = cells_around[3]
    if checkCell2(x - 1, y) and a1 <= a2 and a1 <= a3 and a1 <= a4:
        return [x - 1, y]
    elif checkCell2(x, y - 1) and a2 <= a1 and a2 <= a3 and a2 <= a4:
        return [x, y - 1]
    elif checkCell2(x + 1, y) and a3 <= a1 and a3 <= a2 and a3 <= a4:
        return [x + 1, y]
    elif checkCell2(x, y + 1) and a4 <= a1 and a4 <= a2 and a4 <= a3:
        return [x, y + 1]
    else:
        return [s1, s2]
        
    
def cell_around(x, y):
    global a
    a1 = a[x - 1][y]
    a2 = a[x][y - 1]
    a3 = a[x + 1][y]
    a4 = a[x][y + 1]    
    if a1 == 0 or a1 == -1:
        a1 = 101
    if a2 == 0 or a2 == -1:
        a2 = 101
    if a3 == 0 or a3 == -1:
        a3 = 101
    if a4 == 0 or a4 == -1:
        a4 = 101    
    return [a1, a2, a3, a4]


def bad_end():
    pygame.draw.rect(screen, lavander, (2, 552, 597, 48), 0)
    screen.blit(sad_smile, (52, 551))
    error = results_name.render("Ошибка. Вы проиграли.", True, red)
    screen.blit(error, [150, 565])
    
    
def happy_end():
    pygame.draw.rect(screen, lavander, (2, 552, 597, 48), 0)
    screen.blit(happy_smile, (52, 551))
    success = results_name.render("Вы выиграли! Поздравляем!", True, green)
    screen.blit(success, [130, 565])    


clean()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            position = event.pos
            x = position[0] 
            y = position[1]
            if event.button == 1:
                if x // 50 == 11 and y // 50 == 0:
                    clean()
                elif x // 50 == 11 and y // 50 == 1:
                    start(s1, s2, f1, f2)
                elif 0 < x // 50 < 11 and 0 < y // 50 < 11:
                    pygame.draw.rect(screen, blue, ((x // 50) * 50 + 1, (y // 50) * 50 + 1, 49, 49), 0)
                    a[x // 50][y // 50] = -1
            elif event.button == 3:
                if count == 0:
                    pygame.draw.rect(screen, dark_red, ((x // 50) * 50 + 1, (y // 50) * 50 + 1, 49, 49), 0)
                    s1 = x // 50
                    s2 = y // 50
                    a[s1][s2] = -2
                elif count == 1:
                    f1 = x // 50
                    f2 = y // 50
                    a[f1][f2] = -3
                    pygame.draw.rect(screen, dark_red, ((x // 50) * 50 + 1, (y // 50) * 50 + 1, 49, 49), 0)
                count += 1
    pygame.display.update()