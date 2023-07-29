

import pygame
import random
import os

pygame.mixer.init()
pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)
a = (155, 175, 185)

screen_width = 1200
screen_height = 700
gamewindow = pygame.display.set_mode((screen_width, screen_height))

# Background images
welcome_bg = pygame.image.load("clear.jpg")
welcome_bg = pygame.transform.scale(welcome_bg, (screen_width, screen_height)).convert_alpha()

game_bg = pygame.image.load("snakeimg.jpg")
game_bg = pygame.transform.scale(game_bg, (screen_width, screen_height)).convert_alpha()

snake_img = pygame.image.load("line.png")
snake_head_img = pygame.image.load("rigsn.png")
food_img = pygame.image.load("aa.png")

snake_img = pygame.transform.scale(snake_img, (20, 20))
snake_head_img = pygame.transform.scale(snake_head_img, (20, 20))
food_img = pygame.transform.scale(food_img, (20, 20))

pygame.display.set_caption("Snake Game ABHINAV")
pygame.display.update()

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 55)

def text_screen(text, colour, x, y):
    screen_text = font.render(text, True, colour)
    gamewindow.blit(screen_text, [x, y])


# def plot_snake(gamewindow, snk_list, snake_size):
#     for x, y in snk_list:
#         gamewindow.blit(snake_img, (x, y))
def plot_snake(gamewindow, snk_list, snake_size):
    if len(snk_list) > 0:
        head = snk_list[-1]
        gamewindow.blit(snake_head_img, (head[0], head[1]))
        for x, y in snk_list[:-1]:
            gamewindow.blit(snake_img, (x, y))

def welcome():
    pygame.mixer.music.load("backg.mp3")
    pygame.mixer.music.play(-1)

    exit_game = False
    while not exit_game:
        gamewindow.fill(a)
        gamewindow.blit(welcome_bg, (0, 0))
        text_screen("Welcome to Snakes", black, 90, 300)
        text_screen("Press Spacebar to Play", black, 200, 390)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    gameloop()
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()
        pygame.display.update()
        clock.tick(60)

pygame.mixer.music.load("backg.mp3")
pygame.mixer.music.play(-1)
eating_sound = pygame.mixer.Sound("eating-sound-effect-36186.mp3")

def gameloop():
    exit_game = False
    game_over = False
    paused = False
    snake_x = 45
    snake_y = 55
    velocity_x = 0
    velocity_y = 0
    snk_list = []
    snk_length = 1

    if not os.path.exists("highscore.txt"):
        with open("highscore.txt", "w") as f:
            f.write("0")

    with open("highscore.txt", "r") as f:
        highscore = f.read()

    food_x = random.randint(20, screen_width / 2)
    food_y = random.randint(20, screen_height / 2)
    score = 0
    init_velocity = 5
    snake_size = 20
    fps = 60

    # box_x = 50
    # box_y = 50
    # box_width = 800
    # box_height = 600
    # Define the box size and position
    box_width = 850
    box_height = 600
    box_x = 10
    box_y = screen_height - box_height - 10




    while not exit_game:
        if game_over:
            with open("highscore.txt", "w") as f:
                f.write(str(highscore))

            gamewindow.fill(white)
            gamewindow.blit(welcome_bg, (0, 0))
            text_screen("Game Over!", black, 99, 300)
            text_screen("Press Enter to Continue", black, 300, 400)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        welcome()
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = 5
                        velocity_y = 0

                    if event.key == pygame.K_LEFT:
                        velocity_x = -5
                        velocity_y = 0

                    if event.key == pygame.K_UP:
                        velocity_y = -5
                        velocity_x = 0

                    if event.key == pygame.K_DOWN:
                        velocity_y = 5
                        velocity_x = 0

                    if event.key == pygame.K_p:
                        paused = not paused
                        if paused:
                            pygame.mixer.music.pause()
                        else:
                            pygame.mixer.music.unpause()

            if not paused:
                snake_x += velocity_x
                snake_y += velocity_y

                # Check for collision with the box boundaries
                if snake_x < box_x:
                    snake_x = box_x
                elif snake_x >= box_x + box_width - snake_size:
                    snake_x = box_x + box_width - snake_size
                elif snake_y < box_y:
                    snake_y = box_y
                elif snake_y >= box_y + box_height - snake_size:
                    snake_y = box_y + box_height - snake_size

                if abs(snake_x - food_x) < 20 and abs(snake_y - food_y) < 20:
                    score += 10
                    food_x = random.randint(box_x, box_x + box_width - snake_size)
                    food_y = random.randint(box_y, box_y + box_height - snake_size)
                    snk_length += 5
                    if score > int(highscore):
                        highscore = score

                        # Play the eating sound effect
                    eating_sound.play()

                gamewindow.fill(white)
                gamewindow.blit(game_bg, (0, 0))

                # Draw the box
                pygame.draw.rect(gamewindow, black, [box_x, box_y, box_width, box_height], 2)

                text_screen("Score:" + str(score) + "  Highscore:" + str(highscore), black, 5, box_y - 50)
                gamewindow.blit(food_img, (food_x, food_y))
                head = []
                head.append(snake_x)
                head.append(snake_y)
                snk_list.append(head)

                if len(snk_list) > snk_length:
                    del snk_list[0]

                if head in snk_list[:-1]:
                    game_over = True
                    pygame.mixer.music.load("gameover.mp3")
                    pygame.mixer.music.play()


                plot_snake(gamewindow, snk_list, snake_size)

        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()

welcome()