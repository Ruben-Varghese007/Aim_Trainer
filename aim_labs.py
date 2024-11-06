import math
import random
import time
import pygame

pygame.init()

WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Aim Trainer")

TARGET_PADDING = 30
BG_COLOR = (0, 25, 40)
LIVES = 3  
TOP_BAR_HEIGHT = 50

LABEL_FONT = pygame.font.SysFont("comicsans", 24)
BUTTON_FONT = pygame.font.SysFont("comicsans", 28)
HEADING_FONT = pygame.font.SysFont("comicsans", 50)

class Target:
    SIZE = 30
    COLOR = "white"

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, win):
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), int(self.SIZE))
        pygame.draw.circle(win, BG_COLOR, (self.x, self.y), int(self.SIZE * 0.8))
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), int(self.SIZE * 0.6))
        pygame.draw.circle(win, BG_COLOR, (self.x, self.y), int(self.SIZE * 0.4))

        pygame.draw.line(win, self.COLOR, (self.x - self.SIZE, self.y), (self.x + self.SIZE, self.y), 2)
        pygame.draw.line(win, self.COLOR, (self.x, self.y - self.SIZE), (self.x, self.y + self.SIZE), 2)

    def collide(self, x, y):
        dis = math.sqrt((x - self.x)**2 + (y - self.y)**2)
        return dis <= self.SIZE

def draw(win, target):
    win.fill(BG_COLOR)
    if target:
        target.draw(win)

def format_time(secs):
    milli = math.floor(int(secs * 1000 % 1000) / 100)
    seconds = int(round(secs % 60, 1))
    minutes = int(secs // 60)
    return f"{minutes:02d}:{seconds:02d}.{milli}"

def draw_top_bar(win, countdown, targets_pressed, misses, elapsed_time):
    pygame.draw.rect(win, "grey", (0, 0, WIDTH, TOP_BAR_HEIGHT))
    timer_label = LABEL_FONT.render(f"Timer: {format_time(countdown)}", 1, "black")
    speed = round(targets_pressed / elapsed_time, 1) 
    speed_label = LABEL_FONT.render(f"Speed: {speed} t/s", 1, "black")
    hits_label = LABEL_FONT.render(f"Hits: {targets_pressed}", 1, "black")
    lives_label = LABEL_FONT.render(f"Lives: {LIVES - misses}", 1, "black")

    win.blit(timer_label, (5, 5))
    win.blit(speed_label, (200, 5))
    win.blit(hits_label, (450, 5))
    win.blit(lives_label, (650, 5))

def end_screen(win, elapsed_time, targets_pressed, clicks):
    win.fill(BG_COLOR)
    time_label = LABEL_FONT.render(f"Time: {format_time(elapsed_time)}", 1, "white")
    speed = round(targets_pressed / elapsed_time, 1) 
    speed_label = LABEL_FONT.render(f"Speed: {speed} t/s", 1, "white")
    hits_label = LABEL_FONT.render(f"Hits: {targets_pressed}", 1, "white")
    accuracy = round(targets_pressed / clicks * 100, 1) if clicks > 0 else 0
    accuracy_label = LABEL_FONT.render(f"Accuracy: {accuracy}%", 1, "white")

    win.blit(time_label, (get_middle(time_label), 100))
    win.blit(speed_label, (get_middle(speed_label), 200))
    win.blit(hits_label, (get_middle(hits_label), 300))
    win.blit(accuracy_label, (get_middle(accuracy_label), 400))

    # Define button areas
    play_again_button = pygame.Rect(WIDTH / 2 - 150, 500, 150, 50)
    quit_button = pygame.Rect(WIDTH / 2 + 30, 500, 110, 50)

    # Draw buttons
    pygame.draw.rect(win, (144, 238, 144), play_again_button)
    pygame.draw.rect(win, (255, 127, 127), quit_button)

    play_again_text = BUTTON_FONT.render("Play Again", True, "black")
    quit_text = BUTTON_FONT.render("Quit", True, "black")
    
    win.blit(play_again_text, (play_again_button.x + 10, play_again_button.y + 10))
    win.blit(quit_text, (quit_button.x + 25, quit_button.y + 10))

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if play_again_button.collidepoint(mouse_pos):
                    main()  # Restart the Game
                    return
                elif quit_button.collidepoint(mouse_pos):
                    pygame.quit() # Quit the Game
                    quit()

def get_middle(surface):
    return WIDTH / 2 - surface.get_width() / 2

def welcome_screen(win):
    heading_text = HEADING_FONT.render("AIM TRAINER", True, "white")
    target = Target(WIDTH // 2, HEIGHT // 2)
    instruction_text = BUTTON_FONT.render("Click on the Target to Start", True, "white")

    while True:
        win.fill(BG_COLOR)
        win.blit(heading_text, (get_middle(instruction_text), HEIGHT // 2 - 150))
        target.draw(win)
        win.blit(instruction_text, (get_middle(instruction_text), HEIGHT // 2 + 80))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if target.collide(*mouse_pos):
                    return  # Start the Game

def main():
    welcome_screen(WIN)  # Display Welcome Screen before the Game Starts

    run = True
    clock = pygame.time.Clock()
    targets_pressed = 0
    clicks = 0
    misses = 0
    start_time = time.time()
    countdown = 60

    target = Target(
        random.randint(TARGET_PADDING, WIDTH - TARGET_PADDING),
        random.randint(TARGET_PADDING + TOP_BAR_HEIGHT, HEIGHT - TARGET_PADDING)
    )

    while run:
        clock.tick(60)
        click = False
        mouse_pos = pygame.mouse.get_pos()
        elapsed_time = time.time() - start_time

        # Update the countdown every frame (60 FPS)
        if countdown > 0:
            countdown -= 1 / 60  # Decrease countdown every frame
        else:
            countdown = 0  # Ensure countdown doesn't go negative

        # End the game if the countdown reaches zero
        if countdown <= 0:
            end_screen(WIN, elapsed_time, targets_pressed, clicks)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True
                clicks += 1

        if target and click:
            if target.collide(*mouse_pos):
                targets_pressed += 1
                target = Target(
                    random.randint(TARGET_PADDING, WIDTH - TARGET_PADDING),
                    random.randint(TARGET_PADDING + TOP_BAR_HEIGHT, HEIGHT - TARGET_PADDING)
                )
            else:
                misses += 1

        if misses >= LIVES:
            end_screen(WIN, elapsed_time, targets_pressed, clicks)

        draw(WIN, target)
        draw_top_bar(WIN, countdown, targets_pressed, misses, elapsed_time)
        pygame.display.update()
    
    pygame.quit()

if __name__ == "__main__":
    main()
