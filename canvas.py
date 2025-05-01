import pygame
import sys

# Initialize
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Graphics Editor")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), BLACK]
current_color = BLACK

# Tools
TOOLS = ["line", "rect", "circle", "brush"]
current_tool = "line"
fill_shape = False  # Toggle for filled shapes

# Variables
drawing = False
start_pos = None
canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill(WHITE)
last_pos = None  # For brush

# UI Rects
tool_buttons = [pygame.Rect(10 + i*70, 10, 60, 30) for i in range(len(TOOLS))]
color_buttons = [pygame.Rect(10 + i*40, 50, 30, 30) for i in range(len(colors))]
clear_button = pygame.Rect(WIDTH - 100, 10, 90, 30)

font = pygame.font.SysFont(None, 24)

def draw_ui():
    # Tool buttons
    for i, tool in enumerate(TOOLS):
        pygame.draw.rect(screen, (200, 200, 200), tool_buttons[i])
        label = font.render(tool, True, BLACK)
        screen.blit(label, (tool_buttons[i].x + 5, tool_buttons[i].y + 5))
    
    # Color buttons
    for i, color in enumerate(colors):
        pygame.draw.rect(screen, color, color_buttons[i])
    
    # Clear button
    pygame.draw.rect(screen, (255, 100, 100), clear_button)
    screen.blit(font.render("Clear", True, BLACK), (clear_button.x + 15, clear_button.y + 5))

    # Fill indicator
    fill_text = "Fill: ON" if fill_shape else "Fill: OFF"
    fill_label = font.render(fill_text, True, BLACK)
    screen.blit(fill_label, (WIDTH - 200, 15))

# Main loop
while True:
    screen.fill(WHITE)
    screen.blit(canvas, (0, 0))
    draw_ui()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                fill_shape = not fill_shape  # Toggle fill

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos

            # Tool buttons
            for i, btn in enumerate(tool_buttons):
                if btn.collidepoint(mx, my):
                    current_tool = TOOLS[i]

            # Color buttons
            for i, btn in enumerate(color_buttons):
                if btn.collidepoint(mx, my):
                    current_color = colors[i]

            # Clear
            if clear_button.collidepoint(mx, my):
                canvas.fill(WHITE)

            # Start drawing
            if my > 90:
                start_pos = event.pos
                last_pos = start_pos
                drawing = True

        elif event.type == pygame.MOUSEBUTTONUP and drawing:
            end_pos = event.pos
            if current_tool == "line":
                pygame.draw.line(canvas, current_color, start_pos, end_pos, 2)
            elif current_tool == "rect":
                x, y = start_pos
                w, h = end_pos[0] - x, end_pos[1] - y
                if fill_shape:
                    pygame.draw.rect(canvas, current_color, (x, y, w, h))
                else:
                    pygame.draw.rect(canvas, current_color, (x, y, w, h), 2)
            elif current_tool == "circle":
                x, y = start_pos
                radius = int(((end_pos[0] - x) ** 2 + (end_pos[1] - y) ** 2) ** 0.5)
                if fill_shape:
                    pygame.draw.circle(canvas, current_color, start_pos, radius)
                else:
                    pygame.draw.circle(canvas, current_color, start_pos, radius, 2)
            drawing = False

        elif event.type == pygame.MOUSEMOTION and drawing:
            if current_tool == "brush":
                pygame.draw.line(canvas, current_color, last_pos, event.pos, 2)
                last_pos = event.pos

    pygame.display.flip()
