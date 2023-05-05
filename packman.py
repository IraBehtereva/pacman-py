import time
import random

gui = True
if not gui:
    import keyboard
else:
    import pygame

PACKMAN_X = 0
PACKMAN_Y = 0
enemy_x = 6
enemy_y = 4
WIDTH = 30
HEIGHT = 20
score = 0
update = True

block_size = 40

symbol = " "
pacman = "@"
packman_open = False
pacman_direction = "left"

food_s = "+"
food_count_to_generate = 15
block_count_to_generate = 50
food_count = 0

enemy = "&"
enemy_count_to_generate = 5
enemy_time = 0
enemy_step = 0.1

MENU, GAME, GAME_OVER, SETTINGS = range(4)
state = MENU

pole = []
points = []
buttons = []
settings_buttons = []

runing = True


def generate_food():
    global food_count
    points_local = points.copy()
    points_local.remove([PACKMAN_X, PACKMAN_Y])
    points_local.remove([enemy_x, enemy_y])

    for i in range(food_count_to_generate):
        point = random.choice(points_local)
        pole[point[1]][point[0]] = food_s
        food_count += 1
        points_local.remove(point)


def generate_block():
    coords = []
    for x in range(WIDTH):
        for y in range(HEIGHT):
            coords.append([x, y])
    for y in range(HEIGHT):
        coords.remove([0, y])
        coords.remove([WIDTH - 1, y])

    for x in range(1, WIDTH - 1):
        coords.remove([x, 0])
        coords.remove([x, HEIGHT - 1])

    for i in range(block_count_to_generate):
        point = random.choice(coords)
        wall = random.choice(["|", "|", "|", "-", "-", "-", "-"])
        pole[point[1]][point[0]] = wall
        coords.remove(point)


def generate_pole():
    for y in range(HEIGHT):
        line = []
        for x in range(WIDTH):
            line.append(symbol)
            points.append([x, y])
        pole.append(line)


def print_pole_gui(screen):
    screen.fill((0, 0, 0))

    for y, line in enumerate(pole):
        for x, item in enumerate(line):
            if item == pacman:
                print_pacman(x * block_size, y * block_size)
            if item == food_s:
                pygame.draw.circle(screen, (0, 255, 0),
                                   (x * block_size + block_size // 2, y * block_size + block_size // 2),
                                   block_size // 4)
            if item == "|":
                pygame.draw.rect(
                    screen,
                    (0, 255, 255),
                    (
                        (x * block_size),
                        y * block_size,
                        block_size,
                        block_size
                    )
                )
            if item == "-":
                pygame.draw.rect(
                    screen,
                    (255, 0, 255),
                    (
                        x * block_size,
                        y * block_size,
                        block_size,
                        block_size
                    )
                )
            if item == enemy:
                draw_enemy(x * block_size, y * block_size)


def start():
    global state, pole, PACKMAN_X, PACKMAN_Y, enemy_x, enemy_y, food_count, score
    state = GAME
    pole = []
    food_count = 0
    PACKMAN_X = 0
    PACKMAN_Y = 0
    enemy_x = 6
    enemy_y = 4
    score = 0

    generate_pole()
    generate_block()
    generate_food()



def setting():
    global state
    state = SETTINGS


def exit():
    global runing
    runing = False


def print_menu(screen, first=False):
    screen_w = WIDTH * block_size
    screen_h = HEIGHT * block_size

    menu_w = screen_w // 3
    menu_h = screen_h // 2

    x = screen_w // 2 - menu_w // 2
    y = screen_h // 2 - menu_h // 2

    pygame.draw.rect(
        screen,
        (255, 255, 255),
        (
            x, y,
            menu_w, menu_h
        )
    )

    padding = 20
    button_w = menu_w - padding * 2
    button_h = menu_h // 3 - padding * 1.5
    font = pygame.font.SysFont('Calibri', 42)

    def print_button(bx, by, text, fun):
        pygame.draw.rect(
            screen,
            (50, 255, 255),
            (
                bx + padding, by + padding,
                button_w, button_h
            )
        )

        text_surface = font.render(text, False, (255, 255, 255))
        screen.blit(text_surface, (bx + padding + button_w // 2 - text_surface.get_width() // 2,
                                   by + padding + button_h // 2 - text_surface.get_height() // 2))
        if first:
            buttons.append((
                bx + padding, by + padding,
                bx + padding + button_w, by + padding + button_h,
                fun
            ))

    print_button(x, y, 'Start', start)
    print_button(x, y + button_h + padding, 'Setting', setting)
    print_button(x, y + (button_h + padding) * 2, 'Exit', exit)


def change_food_count(plus=True):
    global food_count_to_generate
    if not plus:
        if food_count_to_generate > 0:
            food_count_to_generate -= 1
        return
    food_count_to_generate += 1


def change_enemy_step(plus=True):
    global enemy_step
    if not plus:
        if enemy_step > 0:
            enemy_step -= 0.1
        return
    enemy_step += 0.1


def change_block_count(plus=True):
    global block_count_to_generate
    if not plus:
        if block_count_to_generate > 0:
            block_count_to_generate -= 1
        return
    block_count_to_generate += 1


def go_to_menu():
    global state
    state = MENU

def print_sattings(first=False):
    screen_w = WIDTH * block_size
    screen_h = HEIGHT * block_size

    menu_w = screen_w // 3
    menu_h = screen_h // 2 + 140

    x = screen_w // 2 - menu_w // 2
    y = screen_h // 2 - menu_h // 2

    pygame.draw.rect(
        screen,
        (255, 255, 255),
        (
            x, y,
            menu_w, menu_h
        )
    )
    font = pygame.font.SysFont('Calibri', 40)
    padding = 30

    def print_button(bx, by, text, value, up, down):
        text_surface = font.render(text, False, (0, 0, 0))
        screen.blit(text_surface, (bx + padding, by + padding))

        value_surface = font.render(f"{value}", False, (0, 0, 0))
        screen.blit(value_surface, (bx + menu_w - value_surface.get_width() - padding, by + padding))

        up_x = bx + menu_w - value_surface.get_width() - padding
        up_y = by + padding // 2

        b_w = value_surface.get_width()
        b_h = value_surface.get_height() // 4

        pygame.draw.rect(
            screen,
            (0, 255, 255),
            (
                up_x,
                up_y,
                b_w, b_h
            )
        )
        if first:
            settings_buttons.append((
                up_x,
                up_y,
                up_x + b_w,
                up_y + b_h,
                up
            ))
        pygame.draw.polygon(
            screen, (11, 22, 33), [
                (up_x + b_w // 2, up_y + (b_h * 0.2)),
                (up_x + b_w - (b_w * 0.2), up_y + b_h - (b_h * 0.2)),
                (up_x + (b_w * 0.2), up_y + b_h - (b_h * 0.2))
            ]
        )

        bot_x = up_x
        bot_y = by + padding + value_surface.get_height()

        pygame.draw.rect(
            screen,
            (0, 255, 255),
            (
                bot_x,
                bot_y,
                b_w, b_h
            )
        )
        if first:
            settings_buttons.append((
                bot_x,
                bot_y,
                bot_x + b_w,
                bot_y + b_h,
                down
            ))

        pygame.draw.polygon(
            screen, (11, 22, 33), [
                (bot_x + (b_w * 0.2), bot_y + (b_h * 0.2)),
                (bot_x + b_w - (b_w * 0.2), bot_y + (b_h * 0.2)),
                (bot_x + b_w // 2, bot_y + b_h - (b_h * 0.2))
            ]
        )
        return bot_y + b_h

    last_y = print_button(x, y, "Кол-во еды", food_count_to_generate, change_food_count,
                          lambda: change_food_count(False))
    last_y = print_button(x, last_y, "Кол-во стен", block_count_to_generate, change_block_count,
                          lambda: change_block_count(False))
    print_button(x, last_y, "Скорость злодея", int(enemy_step * 10), change_enemy_step,
                 lambda: change_enemy_step(False))

    large_button_padding = 20
    large_button_w = menu_w - large_button_padding * 2
    large_button_h = menu_h // 5 - large_button_padding * 2
    large_button_y = y + menu_h - large_button_h - padding

    pygame.draw.rect(
        screen,
        (50, 255, 255),
        (
            x + large_button_padding, large_button_y + large_button_padding,
            large_button_w, large_button_h
        )
    )

    text_surface = font.render("Назад", False, (255, 255, 255))
    screen.blit(text_surface, (x + large_button_padding + large_button_w // 2 - text_surface.get_width() // 2,
                               large_button_y + large_button_padding + large_button_h // 2 - text_surface.get_height() // 2))
    if first:
        settings_buttons.append((
            x + large_button_padding, large_button_y + large_button_padding,
            x + large_button_padding + large_button_w, large_button_y + large_button_padding + large_button_h,
            go_to_menu
        ))


def print_pole():
    global update

    if not update:
        return

    print()
    print("-" * (WIDTH + 2))
    for line in pole:
        print("|" + "".join(line) + "|")
    print("-" * (WIDTH + 2))
    print(end="")

    update = False
    print(food_count)


def move(x, y, hero, prev_x, prev_y):
    global update, food_s, food_count, score

    if y >= HEIGHT:
        y = 0

    if x >= WIDTH:
        x = 0

    if y < 0:
        y = HEIGHT - 1

    if x < 0:
        x = WIDTH - 1

    if pole[y][x] == food_s:
        food_count -= 1

        if hero == pacman:
            score += 1

    if pole[y][x] == "|" or pole[y][x] == "-":
        return prev_x, prev_y

    pole[y][x] = hero
    pole[prev_y][prev_x] = symbol
    update = True
    return x, y


def move_pacman(x, y):
    global PACKMAN_X, PACKMAN_Y
    PACKMAN_X, PACKMAN_Y = move(x, y, pacman, PACKMAN_X, PACKMAN_Y)


def move_enemy(x, y):
    global enemy_x, enemy_y
    enemy_x, enemy_y = move(x, y, enemy, enemy_x, enemy_y)


def get_pos_by_dir(dir, x, y):
    if dir == 'left':
        return x - 1, y
    elif dir == 'right':
        return x + 1, y
    elif dir == 'up':
        return x, y - 1
    elif dir == 'down':
        return x, y + 1


def go(direction):
    global pacman_direction
    pacman_direction = direction
    x, y = get_pos_by_dir(direction, PACKMAN_X, PACKMAN_Y)
    move_pacman(x, y)


def go_enemy():
    global enemy_time
    en_time = float(f'{time.perf_counter() - start_time}'[:4])

    if en_time == enemy_time or f'{en_time / enemy_step}'[2] == 0:
        return
    enemy_time = en_time

    dir = random.choice(["up", "down", "left", "right"])
    x, y = get_pos_by_dir(dir, enemy_x, enemy_y)
    move_enemy(x, y)


def print_pacman(x, y):
    sureface = pygame.Surface((block_size, block_size))
    pygame.draw.circle(sureface, (255, 0, 0), (block_size // 2, block_size // 2), block_size // 2)
    pygame.draw.circle(sureface, (0, 0, 0), (block_size // 2 + (block_size // 2 * 0.2), block_size // 2 * 0.3),
                       block_size // 10)
    if (pacman_direction in ["left", "right"] and PACKMAN_X % 2 == 0) or (
            pacman_direction in ["up", "down"] and PACKMAN_Y % 2 == 0):
        pygame.draw.line(sureface, (0, 0, 0), (block_size // 2, block_size // 2), (block_size, block_size // 2))
    else:
        pygame.draw.polygon(sureface, (0, 0, 0), [(block_size // 2, block_size // 2), (block_size, block_size // 4),
                                                  (block_size, block_size // 2 + (block_size // 4))])

    if pacman_direction == 'up':
        sureface = pygame.transform.rotate(sureface, 90)
    elif pacman_direction == 'down':
        sureface = pygame.transform.rotate(sureface, -90)
    elif pacman_direction == 'left':
        sureface = pygame.transform.flip(sureface, True, False)

    screen.blit(sureface, (x, y))


def draw_enemy(x, y):
    surface = pygame.Surface((block_size, block_size))
    pygame.draw.polygon(
        surface, (175, 0, 255),
        [(block_size // 4, 0), (block_size // 4 * 3, 0),
         (block_size, block_size), (0, block_size)])
    pygame.draw.circle(surface, (0, 0, 0), (block_size // 2 - (block_size // 2 * 0.2), block_size // 2 * 0.3),
                       block_size // 10)
    pygame.draw.circle(surface, (0, 0, 0), (block_size // 2 + (block_size // 2 * 0.2), block_size // 2 * 0.3),
                       block_size // 10)

    screen.blit(surface, (x, y))


def check_game_over():
    global state
    if PACKMAN_X == enemy_x and PACKMAN_Y == enemy_y:
        state = GAME_OVER


if __name__ == '__main__':

    generate_pole()
    generate_block()
    generate_food()

    if not gui:
        keyboard.add_hotkey("w", lambda: go('up'))
        keyboard.add_hotkey("s", lambda: go('down'))
        keyboard.add_hotkey("a", lambda: go('left'))
        keyboard.add_hotkey("d", lambda: go('right'))
    else:
        pygame.init()
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((WIDTH * block_size + block_size, HEIGHT * block_size + block_size))
        print_menu(screen, True)
        print_sattings(True)

    start_time = time.perf_counter()
    runing = True
    while runing:
        screen.fill((0, 0, 0))
        if state == GAME:
            go_enemy()
            if not gui:
                print_pole()
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        runing = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            go('up')
                        if event.key == pygame.K_DOWN:
                            go('down')
                        if event.key == pygame.K_LEFT:
                            go('left')
                        if event.key == pygame.K_RIGHT:
                            go('right')
                        if event.key == pygame.K_ESCAPE:
                            state = MENU

                check_game_over()
                print_pole_gui(screen)

                font = pygame.font.SysFont('Calibri', 18)
                text_surface = font.render(f"score: {score}", False, (255, 255, 255))
                screen.blit(text_surface, (10, 10))

            if food_count == 0:
                generate_food()
        if state == MENU:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    runing = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = event.pos

                    for button in buttons:
                        x, y, x1, y1, fun = button

                        if x < mx < x1 and y < my < y1:
                            fun()

            print_menu(screen)

        if state == SETTINGS:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    runing = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = event.pos

                    for button in settings_buttons:
                        x, y, x1, y1, fun = button

                        if x < mx < x1 and y < my < y1:
                            fun()
            print_sattings()

        if state == GAME_OVER:
            font = pygame.font.SysFont('Calibly', 42)
            text_surface = font.render("Game Over", False, (255, 255, 255))
            screen.blit(text_surface, (WIDTH * block_size // 2 - (text_surface.get_width() // 2),
                                       HEIGHT * block_size // 2 - (text_surface.get_height() // 2)))
            pygame.display.update()
            time.sleep(3)
            state = MENU

        if gui:
            pygame.display.update()
            clock.tick(10)
