import pygame
import sys
from game import game

# --------------------------------------------------
# BASIC CONFIG
# --------------------------------------------------
WIDTH, HEIGHT = 1400, 800
FPS = 60

BG_COLOR = (245, 225, 200)
TEXT_COLOR = (60, 40, 20)
PIT_COLOR = (235, 235, 235)
AI_PIT_COLOR = (200, 180, 150)
HIGHLIGHT_COLOR = (255, 210, 120)

PIT_RADIUS = 45

# --------------------------------------------------
# PIT POSITIONS — FIXED
# --------------------------------------------------
START_X = 260
GAP_X   = 130

TOP_Y    = 320      # AI row
BOTTOM_Y = 480      # Player row

PIT_POSITIONS = {
    0: (START_X + 0 * GAP_X, BOTTOM_Y),
    1: (START_X + 1 * GAP_X, BOTTOM_Y),
    2: (START_X + 2 * GAP_X, BOTTOM_Y),
    3: (START_X + 3 * GAP_X, BOTTOM_Y),
    4: (START_X + 4 * GAP_X, BOTTOM_Y),
    5: (START_X + 5 * GAP_X, BOTTOM_Y),
    6: (START_X + 6 * GAP_X, BOTTOM_Y),

    7: (START_X + 0 * GAP_X, TOP_Y),
    8: (START_X + 1 * GAP_X, TOP_Y),
    9: (START_X + 2 * GAP_X, TOP_Y),
    10: (START_X + 3 * GAP_X, TOP_Y),
    11: (START_X + 4 * GAP_X, TOP_Y),
    12: (START_X + 5 * GAP_X, TOP_Y),
    13: (START_X + 6 * GAP_X, TOP_Y),
}

# --------------------------------------------------
# INIT
# --------------------------------------------------
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pallanguzhi – AI vs You")
clock = pygame.time.Clock()

TITLE_FONT  = pygame.font.SysFont("Verdana", 54, True)
LABEL_FONT  = pygame.font.SysFont("Verdana", 32, True)
PIT_FONT    = pygame.font.SysFont("Verdana", 28, True)
SMALL_FONT  = pygame.font.SysFont("Verdana", 22)

g = game(14, 5)

AI_MODES = {
    "Naive": 1,
    "Greedy": 2,
    "MinMax": 3,
    "AlphaBeta": 4,
    "Reinforcement Learning": 5
}

# backend key
ai_mode_name = "Greedy"
# UI display text
ai_mode_name_display = "Greedy"

game_over = False
winner_text = ""

# —— animation state (UI only) ——
animating = False
anim_board = None


# --------------------------------------------------
# GAME LOGIC
# --------------------------------------------------
def apply_human_move(pit):
    global game_over, winner_text

    if pit not in g.current_game_board.getCurrentChoices(g.current_player):
        return

    animate_sowing(pit)
    score = g.current_game_board.move(pit, False, g.current_score)
    g.updateScore(score)
    g.changePlayerTurn()

    if not g.checkGameStatus():
        finish_game()
        return

    ai_move()

    if not g.checkGameStatus():
        finish_game()


def ai_move():
    mode = AI_MODES[ai_mode_name]

    if mode == 1:
        g.naiveAgent()
    elif mode == 2:
        g.greedyAgent()
    elif mode == 3:
        g.minMaxAgent(2)
    elif mode == 4:
        g.AlphaBetaPlay(2)
    elif mode == 5:
        g.rlagent(g.current_game_board.board)


def finish_game():
    global game_over, winner_text
    g.current_game_board.getAllPiecesElements(g.current_score)
    game_over = True

    p0, p1 = g.current_score
    if p0 > p1:
        winner_text = "Congrats! Player 1 (You) Won"
    elif p1 > p0:
        winner_text = "! AI Agent Won !"
    else:
        winner_text = "Draw!"


def reset_game():
    global g, game_over, winner_text, animating, anim_board
    g = game(14, 5)
    game_over = False
    winner_text = ""
    animating = False
    anim_board = None


def pit_clicked(pos):
    mx, my = pos
    for idx, (x, y) in PIT_POSITIONS.items():
        if (mx - x)**2 + (my - y)**2 <= PIT_RADIUS**2:
            return idx
    return None


# --------------------------------------------------
# SIMPLE VISUAL SOWING ANIMATION (UI ONLY)
# --------------------------------------------------
def animate_sowing(start_pit):
    global animating, anim_board

    board = g.current_game_board.board
    stones = board[start_pit]
    if stones <= 0:
        return

    anim_board = list(board)
    anim_board[start_pit] = 0

    idx = start_pit
    animating = True

    for _ in range(stones):
        idx = (idx + 1) % len(anim_board)
        anim_board[idx] += 1

        draw()
        pygame.display.update()
        pygame.time.delay(200)

    animating = False
    anim_board = None


# --------------------------------------------------
# UI HELPER
# --------------------------------------------------
def draw_center(text, font, x, y, color=TEXT_COLOR):
    surf = font.render(text, True, color)
    rect = surf.get_rect(center=(x, y))
    screen.blit(surf, rect)


# --------------------------------------------------
# RESET BUTTON RECT
# --------------------------------------------------
RESET_RECT = pygame.Rect(0, 0, 120, 30)


# --------------------------------------------------
# RENDER
# --------------------------------------------------
def draw():
    screen.fill(BG_COLOR)

    draw_center("Pallanghuzi", TITLE_FONT, WIDTH//2, 60)
    draw_center("Player 2 (AI Agent)", LABEL_FONT, WIDTH//2, 240)
    draw_center("Player 1 (You)", LABEL_FONT, WIDTH//2, 560)

    # ==== TRAY BOXES ====
    tray_color = (160, 110, 60)
    shadow_color = (120, 80, 40)

    TRAY_WIDTH = 960
    TRAY_HEIGHT = 90
    TRAY_RADIUS = 38

    AI_TRAY_Y = TOP_Y - TRAY_HEIGHT//2
    PLAYER_TRAY_Y = BOTTOM_Y - TRAY_HEIGHT//2

    pygame.draw.rect(screen, shadow_color, (160, AI_TRAY_Y+4, TRAY_WIDTH, TRAY_HEIGHT), border_radius=TRAY_RADIUS)
    pygame.draw.rect(screen, tray_color,  (165, AI_TRAY_Y, TRAY_WIDTH-10, TRAY_HEIGHT-6), border_radius=TRAY_RADIUS)

    pygame.draw.rect(screen, shadow_color, (160, PLAYER_TRAY_Y+4, TRAY_WIDTH, TRAY_HEIGHT), border_radius=TRAY_RADIUS)
    pygame.draw.rect(screen, tray_color,  (165, PLAYER_TRAY_Y, TRAY_WIDTH-10, TRAY_HEIGHT-6), border_radius=TRAY_RADIUS)

    # ==== SCORE BOX ====
    SCORE_X = WIDTH - 245
    SCORE_Y = 280
    SCORE_W = 200
    SCORE_H = 270

    score_color = (245, 215, 175)

    score_rect = pygame.Rect(SCORE_X, SCORE_Y, SCORE_W, SCORE_H)
    pygame.draw.rect(screen, score_color, score_rect, border_radius=25)
    pygame.draw.rect(screen, (80, 50, 30), score_rect, 4, border_radius=25)

    padX = SCORE_X + 20
    padY = SCORE_Y + 20

    draw_center("Score", SMALL_FONT, score_rect.centerx, padY + 5)
    padY += 40

    pygame.draw.line(screen, TEXT_COLOR, (padX, padY), (SCORE_X + SCORE_W - 20, padY), 2)
    padY += 25

    p0, p1 = g.current_score
    screen.blit(SMALL_FONT.render(f"You: {p0}", True, TEXT_COLOR), (padX, padY))
    padY += 30
    screen.blit(SMALL_FONT.render(f"AI : {p1}", True, TEXT_COLOR), (padX, padY))
    padY += 35

    pygame.draw.line(screen, TEXT_COLOR, (padX, padY), (SCORE_X + SCORE_W - 20, padY), 2)
    padY += 22

    # === AI MODE LABEL ===
    screen.blit(SMALL_FONT.render("AI Mode:", True, TEXT_COLOR), (padX, padY))
    padY += 30

    # 🔥 RENDER UI MULTILINE (display text)
    for i, line in enumerate(ai_mode_name_display.split("\n")):
        surf = SMALL_FONT.render(line, True, TEXT_COLOR)
        screen.blit(surf, (padX, padY + i * (surf.get_height() + 3)))

    # ==== RESET TEXT ====
    RESET_TEXT_X = SCORE_X + 10
    RESET_TEXT_Y = SCORE_Y - 150

    screen.blit(SMALL_FONT.render("[R] Reset", True, TEXT_COLOR), (RESET_TEXT_X, RESET_TEXT_Y))
    screen.blit(SMALL_FONT.render("[1–5] Change AI", True, TEXT_COLOR), (SCORE_X + 10, SCORE_Y - 120))

    RESET_RECT.x = RESET_TEXT_X - 5
    RESET_RECT.y = RESET_TEXT_Y - 5
    RESET_RECT.width = 120
    RESET_RECT.height = 30

    # ==== PITS ====
    board_state = anim_board if animating and anim_board is not None else g.current_game_board.board
    valid_moves = g.current_game_board.getCurrentChoices(0)

    for idx, (x, y) in PIT_POSITIONS.items():
        if game_over:
            color = PIT_COLOR
        elif g.current_player == 0 and idx in valid_moves and idx < 7:
            color = HIGHLIGHT_COLOR
        else:
            color = PIT_COLOR if idx < 7 else AI_PIT_COLOR

        pygame.draw.circle(screen, color, (x, y), PIT_RADIUS)
        pygame.draw.circle(screen, (100,60,40), (x, y), PIT_RADIUS, 3)

        t = PIT_FONT.render(str(board_state[idx]), True, TEXT_COLOR)
        screen.blit(t, t.get_rect(center=(x, y)))

    if game_over:
        draw_center(winner_text, LABEL_FONT, WIDTH//2, HEIGHT - 60)


# --------------------------------------------------
# MAIN LOOP
# --------------------------------------------------
def main():
    global ai_mode_name, ai_mode_name_display, animating

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                if e.key == pygame.K_r:
                    reset_game()

                if e.key == pygame.K_1:
                    ai_mode_name = "Naive"
                    ai_mode_name_display = "Naive"
                if e.key == pygame.K_2:
                    ai_mode_name = "Greedy"
                    ai_mode_name_display = "Greedy"
                if e.key == pygame.K_3:
                    ai_mode_name = "MinMax"
                    ai_mode_name_display = "MinMax"
                if e.key == pygame.K_4:
                    ai_mode_name = "AlphaBeta"
                    ai_mode_name_display = "AlphaBeta"
                if e.key == pygame.K_5:
                    ai_mode_name = "Reinforcement Learning"
                    ai_mode_name_display = "Reinforcement\nLearning"

            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                if RESET_RECT.collidepoint(e.pos):
                    reset_game()
                    continue

                if not game_over and not animating and g.current_player == 0:
                    pit = pit_clicked(e.pos)
                    if pit is not None and pit < 7:
                        apply_human_move(pit)

        draw()
        pygame.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
