# Simple Tetris Game in Python
# @JellyAce-69
import pygame
import random

pygame.init()
screen = pygame.display.set_mode((300, 600))
clock = pygame.time.Clock()
# 20 x 10 Grid
grid = [[0 for _ in range(10)] for _ in range(20)]
shapes = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[1, 1, 1], [0, 1, 0]],
    [[1, 1, 1], [1, 0, 0]],
    [[1, 1, 1], [0, 0, 1]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1, 0]],
]
RED = (255, 0, 0)

colors = [
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (255, 255, 0),
    (255, 0, 255),
    (0, 255, 255),
    (255, 165, 0),
]

current_shape = random.choice(shapes)
current_color = random.choice(colors)
shape_x, shape_y = 3, 0
shape_x_left = False
shape_x_right = False
shape_y_down = False
score = 0
font = pygame.font.Font(None, 36)


# Determine if the shape can move, within the boundaries
def can_move(shape, x, y):
    for i, row in enumerate(shape):
        for j, cell in enumerate(row):
            if cell and (
                x + j < 0
                or x + j >= 10
                or y + i >= 20
                or (y + i >= 0 and grid[y + i][x + j])
            ):
                return False
    return True


def place_shape():
    global current_shape, current_color, shape_x, shape_y, score, running, game_over

    # Record the shape position in the grid
    for i, row in enumerate(current_shape):
        for j, cell in enumerate(row):
            if cell:
                grid[shape_y + i][shape_x + j] = current_color

    # If cleared
    empty = 0

    for i in range(19, -1, -1):
        if all(grid[i]):
            del grid[i]
            empty += 1

    for i in range(empty):
        grid.insert(0, [0 for _ in range(10)])
        score += 100

    empty = 0

    current_shape = random.choice(shapes)
    current_color = random.choice(colors)
    shape_x, shape_y = 3, 0
    if can_move(current_shape, shape_x, shape_y) == False:
        print("Game Over!")
        running = False
        game_over = True


# Proper Game Over Inspired Glitchy Ewan
def draw_game_over_glitch():
    for i, row in enumerate(grid):
        for j, _ in enumerate(row):
            glitch_bool = random.choice([True, False])
            if glitch_bool:
                pygame.draw.rect(screen, RED, (j * 30, i * 30, 30, 30))
                pygame.display.flip()
                pygame.time.wait(10)


# Nilagay ko lang to para di ko na kailangan mag tap kaso mabilis, need to modify
def check_movement():
    global shape_x, shape_y
    if shape_x_left == True and can_move(current_shape, shape_x - 1, shape_y):
        shape_x -= 1
    elif shape_x_right == True and can_move(current_shape, shape_x + 1, shape_y):
        shape_x += 1
    elif shape_y_down == True and can_move(current_shape, shape_x, shape_y + 1):
        shape_y += 1


def rotate(shape):
    return [list(row) for row in zip(*shape[::-1])]


running = True
fall_time = 0
game_over = False

while running:
    # Handles key events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                shape_x_left = True
            elif event.key == pygame.K_RIGHT:
                shape_x_right = True
            elif event.key == pygame.K_DOWN:
                shape_y_down = True
            elif event.key == pygame.K_UP:
                rotated_shape = rotate(current_shape)
                if can_move(rotated_shape, shape_x, shape_y):
                    current_shape = rotated_shape
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                shape_x_left = False
            elif event.key == pygame.K_RIGHT:
                shape_x_right = False
            elif event.key == pygame.K_DOWN:
                shape_y_down = False

    check_movement()

    # After a certain time, drop the shape
    fall_time += clock.get_time()
    if fall_time >= 500:
        if can_move(current_shape, shape_x, shape_y + 1):
            shape_y += 1
        else:
            place_shape()
        fall_time = 0
    screen.fill((0, 0, 0))

    # If game over, red pixels of death muwahahahah
    if running == False and game_over == True:
        # Kung gusto mo nung effect sa baba, uncomment this.
        # for i, row in enumerate(grid):
        #     for j, cell in enumerate(row):
        #         if cell:
        #             pygame.draw.rect(screen, cell, (j * 30, i * 30, 30, 30))
        draw_game_over_glitch()
        pygame.time.wait(2000)
        break

    # Draw the grid
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, cell, (j * 30, i * 30, 30, 30))

    # Draw the current shape current position
    for i, row in enumerate(current_shape):
        for j, cell in enumerate(row):
            if cell:
                pygame.draw.rect(
                    screen,
                    current_color,
                    ((shape_x + j) * 30, (shape_y + i) * 30, 30, 30),
                )
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
