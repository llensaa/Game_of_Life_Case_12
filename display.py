import pygame
import os
import math
import ru_local as ru

_alive_color = (255, 255, 255)
_dead_color = (0, 0, 0)
_grid_color = (40, 40, 40)
_text_color = (0, 255, 0)

_font_small = None
_font_medium = None
_font_large = None

RES_PATH = r"Case_12/resources"
IMG_PATH = os.path.join(RES_PATH, "images")
SND_PATH = os.path.join(RES_PATH, "sounds")

SCREEN_MAIN_MENU = 0
SCREEN_SHAPE_SELECT = 1
SCREEN_COLOR_SELECT = 2
SCREEN_GAME = 3
SCREEN_PRESET_SELECT = 4

SHAPE_SQUARE = 0
SHAPE_HEXAGON = 1

SHAPE_NAMES = {
    SHAPE_SQUARE: ru.shapes["SQUARE"],
    SHAPE_HEXAGON: ru.shapes["HEXAGON"]
}

COLOR_SCHEMES = [
    (ru.colors["CLASSIC"], (255, 255, 255), (0, 0, 0), (40, 40, 40)),
    (ru.colors["NEON"], (0, 255, 0), (0, 0, 0), (0, 50, 0)),
    (ru.colors["FIRE"], (255, 100, 0), (30, 0, 0), (80, 20, 0)),
    (ru.colors["SEA"], (0, 150, 255), (0, 0, 50), (0, 30, 80)),
    (ru.colors["MYSTIC"], (200, 0, 255), (30, 0, 30), (60, 0, 60))
]


def create_buttons(names, w, start=200):
    """
    Creates a list of button dictionaries for UI screens.

    Each button contains:
    - rectangle (position and size)
    - text label
    - hover state

    :param names: list of button labels
    :param w: screen width (used for centering)
    :param start: starting Y position for the first button
    :return: list of button dictionaries
    """
    buttons = []
    for i, n in enumerate(names):
        rect = pygame.Rect(w // 2 - 100, start + i * 70, 200, 50)
        buttons.append({
            "rect": rect,
            "text": n,
            "hover": False
        })
    return buttons


def draw_button(screen, btn):
    """
    Draws a single button on the screen.

    The button changes color when hovered.

    :param screen: pygame surface to draw on
    :param btn: button dictionary
    :return: None
    """
    color = (150, 150, 150) if btn["hover"] else (100, 100, 100)
    pygame.draw.rect(screen, color, btn["rect"])
    pygame.draw.rect(screen, (255, 255, 255), btn["rect"], 2)

    txt = _font_medium.render(btn["text"], True, (255, 255, 255))
    screen.blit(txt, txt.get_rect(center=btn["rect"].center))


def handle_button(btn, e):
    """
    Handles mouse interaction with a button.

    Updates hover state and detects clicks.

    :param btn: button dictionary
    :param e: pygame event
    :return: True if button was clicked, otherwise False
    """
    if e.type == pygame.MOUSEMOTION:
        btn["hover"] = btn["rect"].collidepoint(e.pos)

    if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
        return btn["rect"].collidepoint(e.pos)

    return False


def init_display(rows, cols, cell=20):
    """
    Initializes the pygame display and fonts.

    Screen size depends on grid dimensions.

    :param rows: number of grid rows
    :param cols: number of grid columns
    :param cell: size of each cell in pixels
    :return: (screen, clock, width, height)
    """
    global _font_small, _font_medium, _font_large
    pygame.init()
    pygame.font.init()
    pygame.mixer.init()

    _font_small = pygame.font.Font(None, 24)
    _font_medium = pygame.font.Font(None, 36)
    _font_large = pygame.font.Font(None, 48)

    w = cols * cell if rows else 800
    h = rows * cell + 60 if rows else 600

    screen = pygame.display.set_mode((w, h))
    clock = pygame.time.Clock()
    return screen, clock, w, h


def load_background(screen):
    """
    Loads and scales the menu background image.

    If the image is not found, returns None.

    :param screen: pygame surface
    :return: background image or None
    """
    try:
        p = os.path.join(IMG_PATH, "menu_bg.jpg")
        if os.path.exists(p):
            img = pygame.image.load(p)
            return pygame.transform.scale(img, screen.get_size())
    except:
        pass
    return None


def load_music():
    """
    Loads and starts background music.

    Music is played in a loop if the file exists.

    :return: None
    """
    try:
        p = os.path.join(SND_PATH, "background_music.mp3")
        if os.path.exists(p):
            pygame.mixer.music.load(p)
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.play(-1)
    except:
        pass


def handle_color_scheme(a, d, g):
    """
    Applies a color scheme to the grid.

    Updates global color variables.

    :param a: color for alive cells
    :param d: color for dead cells
    :param g: grid line color
    :return: None
    """
    global _alive_color, _dead_color, _grid_color
    _alive_color, _dead_color, _grid_color = a, d, g


def draw_hex(screen, x, y, size, color):
    """
    Draws a hexagonal cell.

    :param screen: pygame surface
    :param x: center X coordinate
    :param y: center Y coordinate
    :param size: radius of the hexagon
    :param color: fill color
    :return: None
    """
    pts = [(x + size * math.cos(math.pi / 3 * i), y + size * math.sin(math.pi / 3 * i)) for i in range(6)]
    pygame.draw.polygon(screen, color, pts)


def draw_grid(screen, grid, shape):
    """
    Draws the entire grid on the screen.

    Supports square and hexagonal cells.

    :param screen: pygame surface
    :param grid: 2D grid of cells
    :param shape: shape type (square or hex)
    :return: None
    """
    rows, cols = len(grid), len(grid[0])
    w, _ = screen.get_size()
    cell = w // cols

    for r in range(rows):
        for c in range(cols):
            color = _alive_color if grid[r][c] else _dead_color
            x, y = c * cell, r * cell
            if shape == SHAPE_SQUARE:
                pygame.draw.rect(screen, color, (x, y, cell, cell))
            else:
                draw_hex(screen, x + cell // 2, y + cell // 2, cell // 2, color)


def draw_ui(screen, gen, speed, run):
    """
    Draws UI panel with game information and controls.

    :param screen: pygame surface
    :param gen: current generation number
    :param speed: simulation speed
    :param run: whether simulation is running
    :return: None
    """
    w, h = screen.get_size()
    pygame.draw.rect(screen, (20, 20, 20), (0, h - 80, w, 80))

    screen.blit(_font_medium.render(f"Gen:{gen}", True, _text_color), (10, h - 70))
    screen.blit(_font_medium.render(f"{speed:.2f}", True, _text_color), (10, h - 40))
    screen.blit(_font_medium.render(ru.ui["RUN"] if run else ru.ui["PAUSE"], True, (0, 255, 0)), (w - 150, h - 70))

    controls = ru.ui["CONTROLS"]
    txt = _font_small.render(controls, True, (180, 180, 180))
    screen.blit(txt, (w // 2 - txt.get_width() // 2, h - 25))
    