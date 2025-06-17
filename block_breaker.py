import pygame
import sys

# 初期化
pygame.init()

# 画面サイズ
WIDTH, HEIGHT = 600, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("ブロック崩し")

# 色
WHITE = (255, 255, 255)
BLUE = (0, 102, 204)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# パドル設定
PADDLE_WIDTH = 120
PADDLE_HEIGHT = 15
paddle = pygame.Rect(WIDTH // 2 - PADDLE_WIDTH // 2, HEIGHT - 50, PADDLE_WIDTH, PADDLE_HEIGHT)
paddle_speed = 10

# ボール設定
BALL_RADIUS = 10
ball = pygame.Rect(WIDTH // 2 - BALL_RADIUS, HEIGHT // 2, BALL_RADIUS * 2, BALL_RADIUS * 2)
ball_speed = [5, -5]

# ブロック設定
BLOCK_COLS = 8
BLOCK_ROWS = 6
BLOCK_WIDTH = WIDTH // BLOCK_COLS
BLOCK_HEIGHT = 30
blocks = []
for y in range(BLOCK_ROWS):
    for x in range(BLOCK_COLS):
        block = pygame.Rect(x * BLOCK_WIDTH, y * BLOCK_HEIGHT + 50, BLOCK_WIDTH - 2, BLOCK_HEIGHT - 2)
        blocks.append(block)

font = pygame.font.SysFont(None, 60)
game_over = False
win = False

clock = pygame.time.Clock()

while True:
    screen.fill(BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if not game_over:
        # パドル操作
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and paddle.left > 0:
            paddle.left -= paddle_speed
        if keys[pygame.K_RIGHT] and paddle.right < WIDTH:
            paddle.right += paddle_speed

        # ボール移動
        ball.x += ball_speed[0]
        ball.y += ball_speed[1]

        # 壁反射
        if ball.left <= 0 or ball.right >= WIDTH:
            ball_speed[0] = -ball_speed[0]
        if ball.top <= 0:
            ball_speed[1] = -ball_speed[1]

        # パドル反射
        if ball.colliderect(paddle):
            ball_speed[1] = -abs(ball_speed[1])

        # ブロック衝突
        hit_index = ball.collidelist(blocks)
        if hit_index != -1:
            hit_block = blocks.pop(hit_index)
            ball_speed[1] = -ball_speed[1]
        
        # ゲームオーバー判定
        if ball.top > HEIGHT:
            game_over = True
            win = False

        # クリア判定
        if not blocks:
            game_over = True
            win = True

    # 描画
    pygame.draw.rect(screen, BLUE, paddle)
    pygame.draw.ellipse(screen, RED, ball)
    for block in blocks:
        pygame.draw.rect(screen, GREEN, block)
    
    if game_over:
        if win:
            msg = font.render('CLEAR!', True, WHITE)
        else:
            msg = font.render('GAME OVER', True, WHITE)
        screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2 - msg.get_height() // 2))

    pygame.display.flip()
    clock.tick(60)