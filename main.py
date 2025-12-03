import turtle
import random
import time
import json
import os

"""
Tic Tac Toe
-----------
A complete graphical implementation of Tic Tac Toe featuring:
- Persistent Data: Statistics are saved to a local JSON file.
- Game Modes: Single Player (AI) and Two Player (PvP).
- Custom UI Engine: Button handling, rounded rectangles, and modal dialogs.
- Animations: Smooth winning line drawing and state transitions.
"""

# --- Configuration & Constants ---

# Display Settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
GRID_SIZE = 500
CELL_SIZE = GRID_SIZE / 3
OFFSET = 60
DATA_FILE = "leaderboard.json"

# Color Palette
C_BG = "#2C3E50"          # Background
C_GRID = "#34495E"        # Grid Lines
C_ACCENT = "#1ABC9C"      # UI Highlights
C_X = "#E74C3C"           # Player X
C_O = "#F1C40F"           # Player O
C_TEXT = "#ECF0F1"        # Primary Text
C_SHADOW = "#1a252f"      # UI Shadows
C_BUTTON = "#2980B9"      # Interactive Buttons
C_WIN_LINE = "#2ECC71"    # Winning Animation

# --- Global Application State ---

board = [""] * 9
turn = "X"
game_active = False
game_mode = "2"  # '1' = PvAI, '2' = PvP
active_buttons = []

# Statistics Data Structure
stats = {
    "pvp": {"x_wins": 0, "o_wins": 0, "draws": 0},
    "ai": {"player_wins": 0, "ai_wins": 0, "draws": 0}
}

# Drawing Controllers
ui_pen = turtle.Turtle()     # Static UI elements (Grid, Text)
game_pen = turtle.Turtle()   # Dynamic Game elements (X, O)
anim_pen = turtle.Turtle()   # Top-layer Animations
popup_pen = turtle.Turtle()  # Modal Overlays


# --- Persistence Layer ---

def load_stats():
    """Attempts to load statistics from the local file system."""
    global stats
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                stats = json.load(f)
        except (IOError, json.JSONDecodeError):
            print("Warning: Could not load stats. Starting fresh.")
    else:
        save_stats()


def save_stats():
    """Persists current statistics to the local file system."""
    try:
        with open(DATA_FILE, "w") as f:
            json.dump(stats, f, indent=4)
    except IOError:
        print("Warning: Could not save stats.")


# --- Graphics Engine ---

def setup_turtle():
    """
    Initializes the application window and rendering pens.
    Disables automatic tracer for manual render control.
    """
    window = turtle.Screen()
    window.title("Tic Tac Toe")
    window.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
    window.bgcolor(C_BG)
    window.tracer(0)

    # Initialize pens with identical defaults
    for p in [ui_pen, game_pen, anim_pen, popup_pen]:
        p.hideturtle()
        p.penup()
        p.speed(0)
        p.width(5)

    return window


def draw_rounded_rect(pen, x, y, w, h, radius, color, shadow=True):
    """
    Renders a rectangle with rounded corners.
    Optionally draws an offset shadow layer for depth.
    """
    pen.penup()

    # Render shadow layer
    if shadow:
        pen.color(C_SHADOW)
        pen.goto(x + 5, y - 5)
        _draw_rect_path(pen, w, h, radius)

    # Render main layer
    pen.penup()
    pen.color(color)
    pen.goto(x, y)
    _draw_rect_path(pen, w, h, radius)


def _draw_rect_path(pen, w, h, radius):
    """
    Internal helper to trace the path of a rounded rectangle.
    Uses circular arcs for corners.
    """
    pen.pendown()
    pen.begin_fill()
    pen.forward(w / 2 - radius)
    pen.circle(-radius, 90)
    pen.forward(h - 2 * radius)
    pen.circle(-radius, 90)
    pen.forward(w - 2 * radius)
    pen.circle(-radius, 90)
    pen.forward(h - 2 * radius)
    pen.circle(-radius, 90)
    pen.forward(w / 2 - radius)
    pen.end_fill()
    pen.penup()


def draw_button(pen, x, y, w, h, text, action, font_size=14):
    """
    Renders a button and registers its collision box for event handling.
    """
    active_buttons.append({
        'x_min': x - w / 2,
        'x_max': x + w / 2,
        'y_min': y - h / 2,
        'y_max': y + h / 2,
        'action': action
    })

    draw_rounded_rect(pen, x, y + h / 2, w, h, 10, C_BUTTON)

    pen.color(C_TEXT)
    # Adjust y-position slightly to account for font baseline
    pen.goto(x, y - (font_size * 0.7))
    pen.write(text, align="center", font=("Verdana", font_size, "bold"))


def animate_win_line(start_idx, end_idx):
    """
    Draws the winning line frame-by-frame for a smooth visual effect.
    Uses manual event loop iteration to prevent UI freezing.
    """
    start_x, start_y = get_cell_center(start_idx)
    end_x, end_y = get_cell_center(end_idx)

    anim_pen.clear()
    anim_pen.color(C_WIN_LINE)
    anim_pen.pensize(20)
    anim_pen.penup()
    anim_pen.goto(start_x, start_y)
    anim_pen.pendown()

    steps = 40
    dx = (end_x - start_x) / steps
    dy = (end_y - start_y) / steps

    for _ in range(steps):
        current_x, current_y = anim_pen.pos()
        anim_pen.goto(current_x + dx, current_y + dy)
        screen.update()
        time.sleep(0.015)


# --- Interface & Screens ---

def show_start_screen():
    """Renders the Main Menu interface."""
    global game_active, active_buttons
    game_active = False
    active_buttons = []

    ui_pen.clear()
    game_pen.clear()
    popup_pen.clear()
    anim_pen.clear()

    # Main Header
    ui_pen.color(C_TEXT)
    ui_pen.goto(0, 150)
    ui_pen.write("TIC TAC TOE", align="center", font=("Verdana", 50, "bold"))

    # Navigation
    draw_button(ui_pen, 0, 30, 260, 60, "1 PLAYER (AI)", lambda: start_game('1'))
    draw_button(ui_pen, 0, -50, 260, 60, "2 PLAYERS", lambda: start_game('2'))
    draw_button(ui_pen, 0, -130, 260, 60, "LEADERBOARD", show_leaderboard)
    draw_button(ui_pen, 0, -210, 260, 60, "EXIT", screen.bye)

    screen.update()


def show_leaderboard():
    """Renders the persistent statistics screen."""
    global active_buttons
    active_buttons = []

    ui_pen.clear()
    game_pen.clear()
    popup_pen.clear()
    anim_pen.clear()

    ui_pen.color(C_TEXT)
    ui_pen.goto(0, 300)
    ui_pen.write("LIFETIME STATS", align="center", font=("Verdana", 35, "bold"))

    # PvP Card (Centered Left)
    draw_rounded_rect(ui_pen, -200, 150, 350, 300, 15, C_GRID)
    ui_pen.color(C_TEXT)
    ui_pen.goto(-200, 90)
    ui_pen.write("2 PLAYERS", align="center", font=("Verdana", 20, "bold"))
    ui_pen.goto(-200, 60)
    ui_pen.write("________________", align="center", font=("Verdana", 12, "normal"))

    pvp = stats["pvp"]
    ui_pen.goto(-200, 20)
    ui_pen.write(f"Player X Wins:  {pvp['x_wins']}", align="center", font=("Verdana", 14, "normal"))
    ui_pen.goto(-200, -20)
    ui_pen.write(f"Player O Wins:  {pvp['o_wins']}", align="center", font=("Verdana", 14, "normal"))
    ui_pen.goto(-200, -60)
    ui_pen.write(f"Draws:  {pvp['draws']}", align="center", font=("Verdana", 14, "normal"))

    # AI Card (Centered Right)
    draw_rounded_rect(ui_pen, 200, 150, 350, 300, 15, C_GRID)
    ui_pen.color(C_TEXT)
    ui_pen.goto(200, 90)
    ui_pen.write("VS AI", align="center", font=("Verdana", 20, "bold"))
    ui_pen.goto(200, 60)
    ui_pen.write("________________", align="center", font=("Verdana", 12, "normal"))

    ai = stats["ai"]
    ui_pen.goto(200, 20)
    ui_pen.write(f"Human Wins:  {ai['player_wins']}", align="center", font=("Verdana", 14, "normal"))
    ui_pen.goto(200, -20)
    ui_pen.write(f"AI Wins:  {ai['ai_wins']}", align="center", font=("Verdana", 14, "normal"))
    ui_pen.goto(200, -60)
    ui_pen.write(f"Draws:  {ai['draws']}", align="center", font=("Verdana", 14, "normal"))

    draw_button(ui_pen, 0, -250, 200, 60, "BACK", show_start_screen)

    screen.update()


def start_game(mode):
    """Initializes the game session with the selected mode."""
    global game_mode
    game_mode = mode
    reset_game()


def draw_scoreboard():
    """Renders the in-game status banner."""
    ui_pen.clear()
    draw_rounded_rect(ui_pen, 0, 360, 600, 80, 20, C_GRID)

    ui_pen.color(C_TEXT)
    ui_pen.goto(0, 305)

    if game_mode == '1':
        s = stats['ai']
        text = f"VS AI   |   YOU: {s['player_wins']}   |   AI: {s['ai_wins']}"
    else:
        s = stats['pvp']
        text = f"2 PLAYER   |   X: {s['x_wins']}   |   O: {s['o_wins']}"

    ui_pen.write(text, align="center", font=("Verdana", 20, "bold"))


def draw_grid():
    """Renders the main 3x3 playing grid."""
    ui_pen.pensize(10)
    ui_pen.color(C_GRID)

    half_grid = GRID_SIZE / 2
    step = GRID_SIZE / 3

    lines = [
        (-half_grid + step, half_grid, -half_grid + step, -half_grid),
        (-half_grid + 2 * step, half_grid, -half_grid + 2 * step, -half_grid),
        (-half_grid, half_grid - step, half_grid, half_grid - step),
        (-half_grid, half_grid - 2 * step, half_grid, half_grid - 2 * step)
    ]

    for x1, y1, x2, y2 in lines:
        ui_pen.penup()
        ui_pen.goto(x1, y1)
        ui_pen.pendown()
        ui_pen.goto(x2, y2)
        ui_pen.penup()

    screen.update()


def draw_x(x, y):
    """Renders the X symbol with a shadow layer."""
    game_pen.pensize(12)
    game_pen.color(C_SHADOW)
    _draw_x_lines(x + 4, y - 4)
    game_pen.color(C_X)
    _draw_x_lines(x, y)
    screen.update()


def _draw_x_lines(x, y):
    game_pen.penup()
    game_pen.goto(x - OFFSET, y + OFFSET)
    game_pen.pendown()
    game_pen.goto(x + OFFSET, y - OFFSET)
    game_pen.penup()
    game_pen.goto(x - OFFSET, y - OFFSET)
    game_pen.pendown()
    game_pen.goto(x + OFFSET, y + OFFSET)
    game_pen.penup()


def draw_o(x, y):
    """Renders the O symbol with a shadow layer."""
    game_pen.pensize(12)
    game_pen.color(C_SHADOW)
    game_pen.penup()
    game_pen.goto(x + 4, y - OFFSET - 4)
    game_pen.pendown()
    game_pen.circle(OFFSET)
    game_pen.color(C_O)
    game_pen.penup()
    game_pen.goto(x, y - OFFSET)
    game_pen.pendown()
    game_pen.circle(OFFSET)
    game_pen.penup()
    screen.update()


def show_game_over_modal(message, color):
    """
    Renders the Game Over dialog card.
    Note: Does not blur the background to maintain grid visibility.
    """
    global game_active
    game_active = False
    popup_pen.clear()

    # Result Card
    draw_rounded_rect(popup_pen, 0, 150, 400, 300, 20, color)
    draw_rounded_rect(popup_pen, 0, 50, 360, 180, 10, C_BG, shadow=False)

    popup_pen.color(C_TEXT)
    popup_pen.goto(0, 80)
    popup_pen.write(message, align="center", font=("Verdana", 28, "bold"))

    draw_button(popup_pen, 0, -30, 160, 50, "PLAY AGAIN", reset_game)
    draw_button(popup_pen, 0, -100, 160, 50, "MAIN MENU", show_start_screen)

    screen.update()


# --- Game Logic ---

def get_grid_index(x, y):
    """
    Maps screen coordinates to the 0-8 board index.
    Returns None if click is outside grid bounds.
    """
    half = GRID_SIZE / 2
    if not (-half < x < half and -half < y < half): return None
    norm_x = x + half
    norm_y = half - y
    col = int(norm_x // (GRID_SIZE / 3))
    row = int(norm_y // (GRID_SIZE / 3))
    return (row * 3) + col


def get_cell_center(index):
    """Calculates the center (x, y) coordinates for a given grid index."""
    row = index // 3
    col = index % 3
    step = GRID_SIZE / 3
    half = GRID_SIZE / 2
    return -half + (col * step) + (step / 2), half - (row * step) - (step / 2)


def check_winner_details():
    """Checks board state and returns winning details (mark, start_index, end_index)."""
    wins = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]
    for a, b, c in wins:
        if board[a] and board[a] == board[b] == board[c]:
            return board[a], a, c
    return None


def reset_game():
    """Resets all game state and redraws the playing board."""
    global board, turn, game_active, active_buttons
    board = [""] * 9
    turn = "X"
    game_active = True
    active_buttons = []

    game_pen.clear()
    popup_pen.clear()
    anim_pen.clear()
    ui_pen.clear()

    draw_scoreboard()
    draw_grid()
    screen.update()


def handle_game_end(winner_data):
    """
    Orchestrates the end-of-game sequence:
    1. Animate winning line.
    2. Wait for visual confirmation.
    3. Update statistics.
    4. Show result modal.
    """

    if winner_data:
        winner, start, end = winner_data

        # Execute visual confirmation
        animate_win_line(start, end)
        screen.update()
        time.sleep(1)

        # Record Statistic
        if game_mode == '1':  # PvAI
            if winner == "X":
                stats['ai']['player_wins'] += 1
                msg = "YOU WON!"
                color = C_ACCENT
            else:
                stats['ai']['ai_wins'] += 1
                msg = "AI WINS!"
                color = C_O
        else:  # PvP
            if winner == "X":
                stats['pvp']['x_wins'] += 1
                msg = "PLAYER X WINS!"
                color = C_X
            else:
                stats['pvp']['o_wins'] += 1
                msg = "PLAYER O WINS!"
                color = C_O
    else:
        # Handle Draw
        time.sleep(1)
        msg = "IT'S A DRAW!"
        color = "#95a5a6"
        if game_mode == '1':
            stats['ai']['draws'] += 1
        else:
            stats['pvp']['draws'] += 1

    save_stats()
    draw_scoreboard()
    show_game_over_modal(msg, color)


def ai_move():
    """
    AI Logic Engine:
    Prioritizes Winning > Blocking > Center > Random Available.
    """
    if not game_active: return
    opts = [i for i, x in enumerate(board) if x == ""]
    if not opts: return

    move = None

    # 1. Check for winning moves or blocking moves
    for player in ["O", "X"]:
        for i in opts:
            board[i] = player
            if check_winner_details(): move = i
            board[i] = ""
            if move: break
        if move: break

    # 2. Fallback to center or random
    if not move: move = 4 if 4 in opts else random.choice(opts)

    board[move] = "O"
    cx, cy = get_cell_center(move)
    draw_o(cx, cy)

    win_data = check_winner_details()
    if win_data:
        handle_game_end(win_data)
    elif "" not in board:
        handle_game_end(None)
    else:
        global turn
        turn = "X"


def on_click(x, y):
    """
    Primary event handler for mouse clicks.
    Delegates to button handler or game grid based on coordinates.
    """
    global turn

    # Priority: Check UI Buttons first
    for btn in active_buttons:
        if btn['x_min'] < x < btn['x_max'] and btn['y_min'] < y < btn['y_max']:
            btn['action']()
            return

    if not game_active: return

    # Secondary: Check Game Grid
    idx = get_grid_index(x, y)
    if idx is not None and board[idx] == "":
        board[idx] = turn
        cx, cy = get_cell_center(idx)

        if turn == "X":
            draw_x(cx, cy)
        else:
            draw_o(cx, cy)

        win_data = check_winner_details()
        if win_data:
            handle_game_end(win_data)
        elif "" not in board:
            handle_game_end(None)
        else:
            if turn == "X":
                turn = "O"
                if game_mode == '1': screen.ontimer(ai_move, 500)
            else:
                turn = "X"


if __name__ == "__main__":
    screen = setup_turtle()
    load_stats()
    show_start_screen()
    screen.onclick(on_click)
    screen.listen()
    turtle.mainloop()
