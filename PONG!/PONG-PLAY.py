import pygame
import sys
import random
def initialize_pygame(): # Initialize Pygame
    pygame.init()
    pygame.font.init()

def setup_game_window(): # Set up the game window
    screen_width, screen_height = 800, 600
    window = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Pong Game")
    return screen_width, screen_height, window

def setup_game_variables(): # Initialize game variables such as paddles, ball, and their initial positions and speeds
    paddle1 = pygame.Rect(50, 250, 10, 100)
    paddle2 = pygame.Rect(740, 250, 10, 100)

    ball, ball_speed_x, ball_speed_y = initialize_ball()

    paddle_speed = 12

    return paddle1, paddle2, ball, ball_speed_x, ball_speed_y, paddle_speed

def initialize_ball(): # Initialize the ball with random initial direction and speed
    initial_direction = random.choice([-1, 1])
    ball_speed_x = initial_direction * random.randint(5, 8)

    initial_angle = random.choice([-1, 1])
    ball_speed_y = initial_angle * random.randint(5, 8)

    ball = pygame.Rect(395, 295, 10, 10)

    return ball, ball_speed_x, ball_speed_y

def setup_scores_and_clock(): # Set up scores and the game clock
    left_score = 0
    right_score = 0
    max_score = 5
    clock = pygame.time.Clock()
    return left_score, right_score, max_score, clock

def reset_ball(): # Reset the ball to its initial state
    ball, ball_speed_x, ball_speed_y = initialize_ball()
    return ball, ball_speed_x, ball_speed_y

def display_game_paused(): # Display the "Game Paused" message
    global game_paused
    game_paused_text = game_font.render("Game Paused", True, (255, 255, 255))
    text_rect = game_paused_text.get_rect()
    text_rect.center = (screen_width // 2, screen_height // 2)

    while game_paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_paused = False
        window.fill((0, 0, 0))
        window.blit(game_paused_text, text_rect)
        pygame.display.flip()

def display_game_over(): # Display the game over screen
    game_over_image = pygame.image.load("Game Over.PNG")
    image_rect = game_over_image.get_rect()
    image_rect.center = (screen_width // 2, screen_height // 2)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

        window.fill((0, 0, 0))
        window.blit(game_over_image, image_rect)

        # Add text "Press Q to Quit"
        quit_text = game_font.render("Press Q to Quit...", True, (255, 255, 255))
        text_rect = quit_text.get_rect()
        text_rect.center = (screen_width // 2, screen_height // 2 + 100)
        window.blit(quit_text, text_rect)

        pygame.draw.rect(window, (255, 255, 255), paddle1)
        pygame.draw.rect(window, (255, 255, 255), paddle2)
        pygame.draw.ellipse(window, (255, 255, 255), ball)
        pygame.display.flip()
        clock.tick(60)

# Initialize Pygame
initialize_pygame()

# Set the game font
game_font = pygame.font.Font(None, 36)

# Initialize the game state variables
game_paused = False
screen_width, screen_height, window = setup_game_window()
paddle1, paddle2, ball, ball_speed_x, ball_speed_y, paddle_speed = setup_game_variables()
left_score, right_score, max_score, clock = setup_scores_and_clock()
running = False

#Main Game Loop
pygame.mixer.music.load("Undertale OST_ 036 - Dummy!.wav")
pygame.mixer.music.play(-1)

# Display the welcome message before starting the game
start_text_lines = [
    "Welcome to my first big Python Project!",

    "I hope you enjoy!",

    "Press SPACE to start"
]

# Calculate the total height of the text lines
text_height = 0
for line in start_text_lines:
    text_height += game_font.size(line)[1]

# Display the text lines one below the other
y_pos = (screen_height - text_height) // 2
for line in start_text_lines:
    line_surface = game_font.render(line, True, (255, 255, 255))
    text_rect = line_surface.get_rect()
    text_rect.centerx = screen_width // 2
    text_rect.top = y_pos
    window.blit(line_surface, text_rect)
    y_pos += text_rect.height

pygame.display.flip()

# Wait for the SPACE key to be pressed to start the game
waiting_for_start = True

while waiting_for_start:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                waiting_for_start = False

# The main game loop starts here
running = False
start_game = False
hit_counter = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not start_game:
                    start_game = True
                    running = True
            elif event.key == pygame.K_ESCAPE:
                game_paused = not game_paused

    if game_paused:
        display_game_paused()

    keys = pygame.key.get_pressed()
    if start_game:
        if keys[pygame.K_w] and paddle1.top > 0:
            paddle1.y -= paddle_speed
        if keys[pygame.K_s] and paddle1.bottom < screen_height:
            paddle1.y += paddle_speed
        if keys[pygame.K_UP] and paddle2.top > 0:
            paddle2.y -= paddle_speed
        if keys[pygame.K_DOWN] and paddle2.bottom < screen_height:
            paddle2.y += paddle_speed

    if running:
        ball.x += ball_speed_x
        ball.y += ball_speed_y

        # Collision with top and bottom walls
        if ball.top <= 0 or ball.bottom >= screen_height:
            ball_speed_y = -ball_speed_y

            # Collision with paddles
        if ball.colliderect(paddle1):
            ball_speed_x = -ball_speed_x  # Reverse the ball's direction

        if ball.colliderect(paddle2):
            hit_counter += 1
            if hit_counter % 3 == 0:  # Increase speed every 3 hits
                ball_speed_x *= 1.2  # Increase the speed factor as needed
                ball_speed_y *= 1.2  # Increase the speed factor as needed
            ball_speed_x = -ball_speed_x  # Reverse the ball's direction

        # Reset the counter when it reaches a multiple of 3
        if hit_counter % 3 == 0:
            hit_counter = 0
        # Ball out of bounds
        if ball.x < 0 or ball.x > screen_width:
            left_score += 1 if ball.x < 0 else 0
            right_score += 1 if ball.x > screen_width else 0
            if left_score >= max_score or right_score >= max_score:
                # Display the end screen
                start_time = pygame.time.get_ticks()
                limit = 4000
                display_game_over()
            else:
                ball, ball_speed_x, ball_speed_y = reset_ball()

    window.fill((0, 0, 0))

    pygame.draw.rect(window, (255, 255, 255), paddle1)
    pygame.draw.rect(window, (255, 255, 255), paddle2)
    pygame.draw.ellipse(window, (255, 255, 255), ball)

    font = pygame.font.Font(None, 36)
    left_score_text = font.render(str(right_score), True, (255, 255, 255))
    right_score_text = font.render(str(left_score), True, (255, 255, 255))
    screen_width, screen_height = window.get_size()
    window.blit(left_score_text, (screen_width // 4, 50))
    window.blit(right_score_text, (3 * screen_width // 4, 50))

    pygame.display.flip()

    clock.tick(60)
